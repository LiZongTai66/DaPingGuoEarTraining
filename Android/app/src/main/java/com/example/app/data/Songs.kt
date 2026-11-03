package com.example.app.data

import com.example.app.protocol.Protocol

/** 曲谱事件（与 FPGA SONG_DATA 参数一一对应） */
data class SongEvent(
    val dt5ms: Int,      // 距上一事件的时间增量，单位 5ms（0..255）
    val note: Int,       // MIDI 音符号；0 = 仅用于长间隔拆包的静音占位
    val on: Boolean,     // true=按下 false=抬起
    val velocity: Int    // 0..127
) {
    fun toFrame() = Protocol.songData(dt5ms, note, on, velocity)
}

/** 记谱单元：noteName 如 C4 / D#4 / Eb4；R = 休止 */
data class NoteToken(
    val noteName: String, val beats: Float, val velocity: Int = 100,
    val startBeat: Double? = null, val part: String? = null
)

data class Song(
    val id: String, val title: String, val bpm: Int, val tokens: List<NoteToken>,
    val beatMs: Int = 0, val stepGapMs: Int = 0
)

/** 把事件列表转成 SONG_DATA 帧；Δt 超过 255（1275ms）时拆成多个静音占位事件 */
fun splitEvents(events: List<SongEvent>): List<SongEvent> {
    val out = ArrayList<SongEvent>(events.size + 8)
    for (e in events) {
        var dt = e.dt5ms.coerceAtLeast(0)
        while (dt > 255) {
            out.add(SongEvent(255, 0, false, 0))
            dt -= 255
        }
        out.add(SongEvent(dt, e.note, e.on, e.velocity))
    }
    return out
}

/** 把事件列表转成 SONG_DATA 帧 */
fun encodeFrames(events: List<SongEvent>): List<ByteArray> =
    splitEvents(events).map { it.toFrame() }

/** MIDI 音符号 → 显示名，如 60 → "C4"，61 → "C#4" */
fun noteDisplayName(note: Int): String {
    val names = arrayOf("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
    val oct = note / 12 - 1
    return names[note % 12] + oct
}

private val SEMITONE = mapOf(
    "C" to 0, "D" to 2, "E" to 4, "F" to 5,
    "G" to 7, "A" to 9, "B" to 11
)

/** C4=60，支持 # 与 b；R 表示休止（返回 null） */
fun midiNote(name: String): Int? {
    if (name == "R") return null
    val m = Regex("^([A-G])(#|b)?(-?\\d)$").matchEntire(name) ?: return null
    val (letter, acc, octStr) = m.destructured
    val oct = octStr.toInt()
    var semi = SEMITONE.getValue(letter)
    when (acc) {
        "#" -> semi += 1
        "b" -> semi -= 1
    }
    return (oct + 1) * 12 + semi
}

/** Resolved score positions are shared by playback and the visual score preview. */
data class NoteSpan(val index: Int, val token: NoteToken, val startMs: Double, val endMs: Double)

fun noteSpans(song: Song): List<NoteSpan> {
    val beatMs = if (song.beatMs > 0) song.beatMs.toDouble() else 60000.0 / song.bpm
    val timed = song.tokens.any { it.startBeat != null }
    require(!timed || song.tokens.all { it.startBeat != null }) { "同一首曲谱的音符必须全部填写 startBeat，或全部省略" }
    require(!timed || song.stepGapMs == 0) { "多声部曲谱请省略 stepGapMs，使用 startBeat 指定起音" }
    var cursor = 0.0
    return song.tokens.mapIndexed { i, token ->
        val start = token.startBeat?.times(beatMs) ?: cursor
        val end = start + token.beats.toDouble() * beatMs
        cursor = end + song.stepGapMs
        NoteSpan(i, token, start, end)
    }
}

fun songDurationMs(song: Song): Double =
    (noteSpans(song).maxOfOrNull { it.endMs } ?: 0.0) + song.stepGapMs

/** Absolute score times -> existing UART events. Off precedes on at the same 5ms tick. */
fun compose(song: Song): List<SongEvent> {
    data class TimedEvent(val tick: Int, val note: Int, val on: Boolean, val velocity: Int)
    val spans = noteSpans(song)
    val absolute = ArrayList<TimedEvent>()
    for (span in spans) {
        val note = midiNote(span.token.noteName) ?: continue
        absolute.add(TimedEvent(Math.round(span.startMs / 5).toInt(), note, true, span.token.velocity))
        absolute.add(TimedEvent(Math.round(span.endMs / 5).toInt(), note, false, 0))
    }
    absolute.sortWith(compareBy<TimedEvent> { it.tick }.thenBy { if (it.on) 1 else 0 })
    val active = mutableSetOf<Int>()
    val events = ArrayList<SongEvent>()
    var lastTick = 0
    for (e in absolute) {
        if (e.on) {
            require(active.add(e.note)) { "同音 ${noteDisplayName(e.note)} 的时值重叠，请先合并或缩短音符" }
            require(active.size <= 7) { "当前设备最多支持 7 个蓝牙音符同时发声" }
        } else active.remove(e.note)
        events.add(SongEvent(e.tick - lastTick, e.note, e.on, e.velocity))
        lastTick = e.tick
    }
    // Include trailing rests; quantize cumulative absolute times, never each delta.
    val finalTick = Math.round(((spans.maxOfOrNull { it.endMs } ?: 0.0) + song.stepGapMs) / 5).toInt()
    if (finalTick > lastTick) events.add(SongEvent(finalTick - lastTick, 0, false, 0))
    return events
}

object SongLibrary { val songs: List<Song> = GowinDemoSongs.songs }
