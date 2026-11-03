package com.example.app

import com.example.app.data.*
import com.example.app.protocol.*
import com.example.app.synth.*
import com.example.app.transport.Transport
import kotlinx.coroutines.*
import org.junit.Assert.*
import org.junit.Test

class UpgradeTest {
    @Test fun decoder_recoversWhenLostByteSwallowsNextHeader() {
        val good = Protocol.ping(42)
        val damaged = Protocol.noteOn(60, 100).dropLast(1).toByteArray()
        val output = FrameDecoder().feed(damaged + good)
        assertEquals(1, output.size); assertArrayEquals(good, output.single())
    }
    @Test fun keymapAndTelemetry_roundTrip() {
        val map = Frame.from(Protocol.setKeymap(6, 71))
        assertEquals(Cmd.SET_KEYMAP, map.cmd); assertEquals(6, map.a0); assertEquals(71, map.a1)
        val event = Protocol.buildFrame(Cmd.DEVICE_EVENT, 25, 60, 0xE4)
        assertTrue(Protocol.isValid(event)); assertEquals(25, Frame.from(event).a0)
    }
    @Test fun longRests_keepExactTime() {
        val events = splitEvents(listOf(SongEvent(1000, 60, true, 90)))
        assertEquals(1000, events.sumOf { it.dt5ms })
        assertTrue(events.all { it.dt5ms in 0..255 }); assertEquals(60, events.last().note)
    }
    @Test fun onlineSongs_validateAndPersistRoundTrip() {
        val text = """{"title":"测试","bpm":120,"notes":[{"note":"C4","beats":1},{"note":"R","beats":2},{"note":"G4","beats":0.5,"velocity":80}]}"""
        val songs = OnlineSongs.parse(text)
        assertEquals(60, midiNote(songs.single().tokens.first().noteName))
        assertEquals(songs, OnlineSongs.parse(OnlineSongs.encode(songs)))
        assertEquals(4, compose(songs.single()).size)
    }
    @Test fun onlineSongs_rejectInvalidNotesAndOversizedInput() {
        listOf(
            """{"title":"x","bpm":0,"notes":[{"note":"C4","beats":1}]}""",
            """{"title":"x","bpm":120,"notes":[{"note":"H4","beats":1}]}""",
            """{"title":"x","bpm":120,"notes":[{"note":"C4","beats":-1}]}""",
            """{"title":"x","bpm":120,"notes":[{"note":"R","beats":1}]}""",
            " ".repeat(OnlineSongs.MAX_BYTES + 1)
        ).forEach { input -> assertTrue(runCatching { OnlineSongs.parse(input) }.isFailure) }
    }
    @Test fun boundedInput_rejectsOversizedStream() {
        assertEquals(4, byteArrayOf(1,2,3,4).inputStream().readBytesLimited(4).size)
        assertTrue(runCatching { byteArrayOf(1,2,3,4,5).inputStream().readBytesLimited(4) }.isFailure)
    }
    private class Loopback : Transport {
        override val name = "test"
        override var onRaw: ((ByteArray) -> Unit)? = null
        @Volatile var closed = false
        var telemetry = false
        override fun connect() { Thread.sleep(30) }
        override fun close() { closed = true }
        override fun write(data: ByteArray) {
            if (closed) error("closed")
            val f = Frame.from(data)
            val reply = when (f.cmd) {
                Cmd.PING -> Protocol.buildFrame(Cmd.PONG, f.a0, f.a1, f.a2)
                Cmd.SET_KEYMAP -> Protocol.buildFrame(Cmd.ACK, f.cmd.toInt() and 255, f.a0, f.a1)
                Cmd.SONG_END -> Protocol.buildFrame(Cmd.SONG_READY, f.a0, f.a1, f.a2)
                Cmd.SONG_DATA -> return
                else -> Protocol.buildFrame(Cmd.ACK, f.cmd.toInt() and 255)
            }
            onRaw?.invoke(reply)
            if (telemetry) onRaw?.invoke(Protocol.buildFrame(Cmd.DEVICE_EVENT, 0, 60, 0xE4))
        }
    }
    @Test fun client_handshakeDownloadMappingAndTelemetry() = runBlocking {
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
        val client = SynthClient(scope); val t = Loopback()
        val got = CompletableDeferred<Frame>(); client.onDeviceEvent = { got.complete(it) }
        try {
            client.connect { t }
            withTimeout(3000) { while (client.state.value != ConnState.CONNECTED) delay(10) }
            client.setKeymap(3, 65)
            assertTrue(client.downloadSong(listOf(Protocol.songData(0, 60, true))))
            t.telemetry = true; client.setVolume(80)
            assertEquals(60, withTimeout(2000) { got.await() }.a1)
            client.disconnect(); assertTrue(t.closed); assertEquals(ConnState.DISCONNECTED, client.state.value)
        } finally { scope.cancel() }
    }
}
