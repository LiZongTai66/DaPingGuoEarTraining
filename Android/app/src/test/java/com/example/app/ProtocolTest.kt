package com.example.app

import com.example.app.protocol.Cmd
import com.example.app.protocol.Frame
import com.example.app.protocol.FrameDecoder
import com.example.app.protocol.Protocol
import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

// 以 PROTOCOL.md 第 6 节示例帧为对拍基准，输出必须逐字节一致
class ProtocolTest {

    private fun h(s: String) =
        s.trim().split(" ").map { it.toInt(16).toByte() }.toByteArray()

    @Test
    fun exampleFrames_matchSpec() {
        assertArrayEquals(h("AA 01 3C 64 00 5E"), Protocol.noteOn(60, 100))
        assertArrayEquals(h("AA 01 45 64 00 55"), Protocol.noteOn(69, 100))
        assertArrayEquals(h("AA 02 3C 00 00 C1"), Protocol.noteOff(60))
        assertArrayEquals(h("AA 04 01 00 00 FA"), Protocol.setVoice(1))
        assertArrayEquals(h("AA 05 50 00 00 AA"), Protocol.setVolume(80))
        assertArrayEquals(h("AA 06 00 78 00 81"), Protocol.setTempo(120))
        assertArrayEquals(h("AA 03 00 00 00 FC"), Protocol.allOff())
        assertArrayEquals(h("AA 10 00 00 64 8B"), Protocol.songStart(100))
        assertArrayEquals(h("AA 11 04 3C E4 CA"), Protocol.songData(4, 60, true, 100))
        assertArrayEquals(h("AA 12 00 00 64 89"), Protocol.songEnd(100))
        assertArrayEquals(h("AA 13 00 00 00 EC"), Protocol.play())
        assertArrayEquals(h("AA 20 00 00 01 DE"), Protocol.ping(1))
    }

    @Test
    fun parse_ackAndPong() {
        val ack = Frame.from(h("AA 81 01 00 00 7D"))
        assertEquals(Cmd.ACK, ack.cmd)
        assertEquals(0x01, ack.a0)

        val pong = Frame.from(h("AA 83 00 00 01 7B"))
        assertEquals(Cmd.PONG, pong.cmd)
        assertEquals(1, pong.arg24)

        val err = Frame.from(h("AA 82 01 00 00 7C"))
        assertEquals(Cmd.ERR, err.cmd)
        assertEquals(0x01, err.a0)
    }

    @Test
    fun checksum_validAndInvalid() {
        assertTrue(Protocol.isValid(h("AA 01 3C 64 00 5E")))
        // 故意损坏校验字节
        assertFalse(Protocol.isValid(h("AA 01 3C 64 00 5F")))
        // 损坏数据字节
        assertFalse(Protocol.isValid(h("AA 01 3D 64 00 5E")))
    }

    @Test
    fun decoder_concatenatedFrames() {
        val dec = FrameDecoder()
        val stream = h("AA 20 00 00 01 DE AA 83 00 00 01 7B")
        val frames = dec.feed(stream)
        assertEquals(2, frames.size)
        assertArrayEquals(h("AA 20 00 00 01 DE"), frames[0])
        assertArrayEquals(h("AA 83 00 00 01 7B"), frames[1])
    }

    @Test
    fun decoder_splitAcrossFeeds() {
        val dec = FrameDecoder()
        assertEquals(0, dec.feed(h("AA 01 3C")).size)
        val frames = dec.feed(h("64 00 5E"))
        assertEquals(1, frames.size)
        assertArrayEquals(h("AA 01 3C 64 00 5E"), frames[0])
    }

    @Test
    fun decoder_resyncAfterCorruptFrame() {
        val dec = FrameDecoder()
        // 一帧坏数据(校验错) + 一帧合法 PING：坏帧丢弃后能重新同步
        val frames = dec.feed(h("AA 01 3C 64 00 00 AA 20 00 00 01 DE"))
        assertEquals(1, frames.size)
        assertArrayEquals(h("AA 20 00 00 01 DE"), frames[0])
    }

    @Test
    fun decoder_ignoresNoiseBeforeHead() {
        val dec = FrameDecoder()
        val frames = dec.feed(h("00 FF 12 34 AA 03 00 00 00 FC"))
        assertEquals(1, frames.size)
        assertEquals(Cmd.ALL_OFF, Frame.from(frames[0]).cmd)
    }
}
