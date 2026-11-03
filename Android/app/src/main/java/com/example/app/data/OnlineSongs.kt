package com.example.app.data

import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.net.URL
import javax.net.ssl.HttpsURLConnection

/** Downloads a documented, bounded JSON song file. No server or account is required. */
object OnlineSongs {
    const val MAX_BYTES = 512 * 1024
    fun download(address: String): List<Song> {
        var url = URL(address.trim())
        repeat(5) {
            require(url.protocol == "https" && url.userInfo == null) { "请使用不含账号密码的 HTTPS 曲谱链接" }
            val c = url.openConnection() as HttpsURLConnection
            c.connectTimeout = 15000; c.readTimeout = 15000; c.instanceFollowRedirects = false
            c.setRequestProperty("Accept", "application/json")
            try {
                val status = c.responseCode
                if (status in 300..399) {
                    url = URL(url, c.getHeaderField("Location") ?: throw IOException("重定向地址为空"))
                } else {
                    if (status != 200) throw IOException("曲谱服务器返回 HTTP $status")
                    val bytes = c.inputStream.use { it.readBytesLimited(MAX_BYTES) }
                    return parse(bytes.toString(Charsets.UTF_8))
                }
            } finally { c.disconnect() }
        }
        throw IOException("曲谱链接重定向次数过多")
    }
    fun parse(text: String): List<Song> {
        require(text.toByteArray(Charsets.UTF_8).size <= MAX_BYTES) { "曲谱文件不能超过 512 KB" }
        val root = JSONObject(text)
        val array = root.optJSONArray("songs") ?: JSONArray().put(root)
        require(array.length() in 1..100) { "每个文件需包含 1～100 首曲谱" }
        return (0 until array.length()).map { i ->
            val obj = array.getJSONObject(i)
            val title = obj.getString("title").trim()
            require(title.length in 1..60) { "曲名需为 1～60 个字符" }
            val bpm = obj.getInt("bpm"); require(bpm in 20..300) { "BPM 需为 20～300" }
            val beatMs = obj.optInt("beatMs", 0)
            require(beatMs == 0 || beatMs in 200..3000) { "beatMs 需为 200～3000，或省略" }
            val gapMs = obj.optInt("stepGapMs", 0)
            require(gapMs in 0..10) { "stepGapMs 需为 0～10" }
            val notes = obj.getJSONArray("notes")
            require(notes.length() in 1..4000) { "每首曲谱需包含 1～4000 个音符" }
            val tokens = (0 until notes.length()).map { j ->
                val n = notes.getJSONObject(j)
                val name = n.getString("note").trim()
                require(name == "R" || midiNote(name) in 21..108) { "无效音符：$name" }
                val beats = n.getDouble("beats")
                require(beats.isFinite() && beats in 0.03125..32.0) { "音符时值需为 0.03125～32 拍" }
                val velocity = n.optInt("velocity", 100); require(velocity in 1..127) { "力度需为 1～127" }
                val start = if (n.has("startBeat")) n.getDouble("startBeat") else null
                require(start == null || (start.isFinite() && start in 0.0..32000.0 && start + beats <= 32000.0)) { "startBeat 和音符结束位置需为 0～32000 拍" }
                val part = if (n.has("part")) n.getString("part").trim() else null
                require(part == null || part.length in 1..24) { "声部名称需为 1～24 个字符" }
                NoteToken(name, beats.toFloat(), velocity, start, part)
            }
            val song = Song("online_${title.hashCode()}_${bpm}", title, bpm, tokens, beatMs, gapMs)
            val events = compose(song)
            require(events.any { it.on } && splitEvents(events).size in 1..16000) { "曲谱事件数需为 1～16000，不能只有休止符" }
            song
        }
    }
    fun encode(songs: List<Song>): String = JSONObject().put("songs", JSONArray().apply {
        songs.forEach { song -> put(JSONObject().put("title", song.title).put("bpm", song.bpm).put("beatMs", song.beatMs).put("stepGapMs", song.stepGapMs).put("notes", JSONArray().apply {
            song.tokens.forEach {
                val note = JSONObject().put("note", it.noteName).put("beats", it.beats.toDouble()).put("velocity", it.velocity)
                it.startBeat?.let { start -> note.put("startBeat", start) }
                it.part?.let { part -> note.put("part", part) }
                put(note)
            }
        })) }
    }).toString()
}
fun java.io.InputStream.readBytesLimited(limit: Int): ByteArray {
    val out = java.io.ByteArrayOutputStream()
    val buffer = ByteArray(8192)
    while (true) {
        val n = read(buffer); if (n < 0) break
        require(out.size() + n <= limit) { "文件过大，最多允许 ${limit / 1024} KB" }
        out.write(buffer, 0, n)
    }
    return out.toByteArray()
}
