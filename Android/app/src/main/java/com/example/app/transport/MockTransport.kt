package com.example.app.transport

import android.os.HandlerThread
import android.os.Handler
import com.example.app.protocol.Cmd
import com.example.app.protocol.Frame
import com.example.app.protocol.Protocol
import java.io.IOException

/**
 * 模拟 FPGA 设备：无硬件时即可完整调试 App 全部功能。
 * 行为严格模拟 FPGA 固件：
 *  - NOTE_ON / NOTE_OFF / SONG_DATA：无应答（实时路径）
 *  - 其余配置类命令：回 ACK
 *  - PING → PONG（回显序列号）
 *  - SONG_END → 先 ACK 再回 SONG_READY(实际接收事件数)
 *  - 未知命令 → ERR(0x02)
 * 回复加 15ms 延迟，模拟真实无线/串口往返。
 */
class MockTransport : Transport {
    override val name: String = "模拟设备（无需硬件）"

    private val thread = HandlerThread("mock-fpga").apply { start() }
    private val handler = Handler(thread.looper)
    @Volatile private var closed = false
    private var songCount = 0

    override var onRaw: ((ByteArray) -> Unit)? = null

    override fun connect() {
        closed = false
        songCount = 0
        // 模拟连接耗时
        Thread.sleep(200)
        if (closed) throw IOException("已关闭")
    }

    override fun write(data: ByteArray) {
        if (closed) throw IOException("模拟设备未连接")
        if (!Protocol.isValid(data)) {
            handler.postDelayed({ emit(Protocol.buildFrame(Cmd.ERR, Err.BAD_CHECKSUM)) }, 15)
            return
        }
        val f = Frame.from(data)
        when (f.cmd) {
            Cmd.NOTE_ON, Cmd.NOTE_OFF, Cmd.SONG_DATA -> {
                if (f.cmd == Cmd.SONG_DATA) songCount++
                // 实时事件：无应答
            }
            Cmd.SET_KEYMAP -> handler.postDelayed({ emit(Protocol.buildFrame(Cmd.ACK, f.cmd.toInt() and 255, f.a0, f.a1)) }, 15)
            Cmd.PING -> handler.postDelayed({
                emit(Protocol.buildFrame(Cmd.PONG, f.a0, f.a1, f.a2))
            }, 15)
            Cmd.SONG_START -> {
                songCount = 0
                ackLater(f.cmd)
            }
            Cmd.SONG_END -> {
                val n = songCount
                ackLater(f.cmd)
                handler.postDelayed({ emit(Protocol.buildFrame(Cmd.SONG_READY, (n shr 16) and 0xFF, (n shr 8) and 0xFF, n and 0xFF)) }, 30)
            }
            Cmd.SET_VOICE -> handler.postDelayed({ emit(Protocol.buildFrame(Cmd.ACK, f.cmd.toInt() and 255, f.a0, 0)); emit(Protocol.buildFrame(Cmd.VOICE_STATE,f.a0,1,0)) },15)
            Cmd.ALL_OFF, Cmd.SET_VOLUME, Cmd.SET_TEMPO,
            Cmd.PLAY, Cmd.STOP -> ackLater(f.cmd)
            else -> handler.postDelayed({ emit(Protocol.buildFrame(Cmd.ERR, Err.UNKNOWN)) }, 15)
        }
    }

    private fun ackLater(cmd: Byte) {
        handler.postDelayed({ emit(Protocol.buildFrame(Cmd.ACK, cmd.toInt() and 0xFF)) }, 15)
    }

    private fun emit(raw: ByteArray) {
        if (!closed) onRaw?.invoke(raw)
    }

    override fun close() {
        closed = true
        thread.quitSafely()
    }

    private object Err {
        const val BAD_CHECKSUM = 0x01
        const val UNKNOWN = 0x02
    }
}
