package com.example.app.protocol

// GW2A 音乐合成器串口协议 v1.0（与 docs/PROTOCOL.md 逐字节对齐）
// 帧：AA CMD ARG0 ARG1 ARG2 CHK，CHK = ~(CMD+ARG0+ARG1+ARG2) & 0xFF

object Cmd {
    // App → FPGA
    const val NOTE_ON: Byte    = 0x01
    const val NOTE_OFF: Byte   = 0x02
    const val ALL_OFF: Byte    = 0x03
    const val SET_VOICE: Byte  = 0x04
    const val SET_VOLUME: Byte = 0x05
    const val SET_TEMPO: Byte  = 0x06
    const val SONG_START: Byte = 0x10
    const val SONG_DATA: Byte  = 0x11
    const val SONG_END: Byte   = 0x12
    const val PLAY: Byte       = 0x13
    const val STOP: Byte       = 0x14
    const val PING: Byte       = 0x20

    const val SET_KEYMAP: Byte = 0x30

    // FPGA → App
    const val ACK: Byte        = 0x81.toByte()
    const val ERR: Byte        = 0x82.toByte()
    const val PONG: Byte       = 0x83.toByte()
    const val SONG_READY: Byte = 0x84.toByte()
    const val DEVICE_EVENT: Byte = 0x90.toByte()
    const val STATE: Byte      = 0x85.toByte()
    const val VOICE_STATE: Byte = 0x86.toByte()
}

object ErrCode {
    const val BAD_CHECKSUM = 0x01
    const val UNKNOWN_CMD  = 0x02
    const val SONG_FULL    = 0x03
}

object Protocol {
    const val HEAD: Byte = 0xAA.toByte()
    const val FRAME_LEN  = 6

    const val NOTE_MIN = 21
    const val NOTE_MAX = 108

    fun checksum(cmd: Int, a0: Int, a1: Int, a2: Int): Int =
        (cmd + a0 + a1 + a2).inv() and 0xFF

    /** 组装一帧，参数均为 0..255 */
    fun buildFrame(cmd: Byte, a0: Int = 0, a1: Int = 0, a2: Int = 0): ByteArray {
        val c = cmd.toInt() and 0xFF
        return byteArrayOf(
            HEAD, cmd,
            (a0 and 0xFF).toByte(),
            (a1 and 0xFF).toByte(),
            (a2 and 0xFF).toByte(),
            checksum(c, a0, a1, a2).toByte()
        )
    }

    // ---- 高层命令构造（参数语义见 PROTOCOL.md 第 3、5 节） ----

    fun noteOn(note: Int, velocity: Int = 100) =
        buildFrame(Cmd.NOTE_ON, note, velocity, 0)

    fun noteOff(note: Int) =
        buildFrame(Cmd.NOTE_OFF, note, 0, 0)

    fun setKeymap(index: Int, note: Int) = buildFrame(Cmd.SET_KEYMAP, index, note)

    fun allOff() = buildFrame(Cmd.ALL_OFF)

    fun setVoice(voice: Int) = buildFrame(Cmd.SET_VOICE, voice)

    fun setVolume(volume0_100: Int) = buildFrame(Cmd.SET_VOLUME, volume0_100)

    fun setTempo(bpm: Int) = buildFrame(Cmd.SET_TEMPO, (bpm shr 8) and 0xFF, bpm and 0xFF)

    fun songStart(count: Int) = buildFrame(Cmd.SONG_START, (count shr 16) and 0xFF, (count shr 8) and 0xFF, count and 0xFF)

    /**
     * 曲谱事件：dt5ms=距上一事件的时间增量(5ms 单位, 0..255)；note=MIDI 音符号；
     * on=true 按下 / false 抬起；velocity=力度 0..127
     */
    fun songData(dt5ms: Int, note: Int, on: Boolean, velocity: Int = 100) =
        buildFrame(
            Cmd.SONG_DATA,
            dt5ms and 0xFF,
            note and 0xFF,
            (if (on) 0x80 else 0x00) or (velocity and 0x7F)
        )

    fun songEnd(count: Int) = buildFrame(Cmd.SONG_END, (count shr 16) and 0xFF, (count shr 8) and 0xFF, count and 0xFF)

    fun play() = buildFrame(Cmd.PLAY)
    fun stop() = buildFrame(Cmd.STOP)
    fun ping(seq: Int) = buildFrame(Cmd.PING, (seq shr 16) and 0xFF, (seq shr 8) and 0xFF, seq and 0xFF)

    /** 校验一帧是否合法（长度、帧头、校验和） */
    fun isValid(frame: ByteArray): Boolean {
        if (frame.size != FRAME_LEN || frame[0] != HEAD) return false
        val sum = (1..4).sumOf { frame[it].toInt() and 0xFF }
        return (sum.inv() and 0xFF) == (frame[5].toInt() and 0xFF)
    }
}

/** 一帧解析后的结构化结果 */
data class Frame(val cmd: Byte, val a0: Int, val a1: Int, val a2: Int) {
    val arg24: Int get() = (a0 shl 16) or (a1 shl 8) or a2

    companion object {
        fun from(raw: ByteArray): Frame {
            require(raw.size == Protocol.FRAME_LEN)
            return Frame(
                raw[1],
                raw[2].toInt() and 0xFF,
                raw[3].toInt() and 0xFF,
                raw[4].toInt() and 0xFF
            )
        }
    }
}

/**
 * 字节流帧重组器：搜帧头 0xAA → 收 5 字节 → 校验。
 * 校验失败丢弃整帧并从下一字节重新搜头，偶发误码只损失一帧。
 */
class FrameDecoder {
    private val buf = ArrayList<Byte>(16)

    /** 喂入任意长度的原始字节，返回本次新拼出的所有合法帧 */
    @Synchronized
    fun feed(bytes: ByteArray): List<ByteArray> {
        val out = ArrayList<ByteArray>()
        for (b in bytes) {
            buf.add(b)
            while (buf.isNotEmpty() && buf[0] != Protocol.HEAD) buf.removeAt(0)
            while (buf.size >= Protocol.FRAME_LEN) {
                val frame = buf.take(Protocol.FRAME_LEN).toByteArray()
                if (Protocol.isValid(frame)) {
                    out.add(frame)
                    repeat(Protocol.FRAME_LEN) { buf.removeAt(0) }
                } else buf.removeAt(0)
                while (buf.isNotEmpty() && buf[0] != Protocol.HEAD) buf.removeAt(0)
            }
        }
        return out
    }

    @Synchronized
    fun reset() = buf.clear()
}
