package com.example.app.synth

import com.example.app.protocol.*
import com.example.app.data.DeviceKeymap
import com.example.app.data.DeviceKeymapDecoder
import com.example.app.transport.Transport
import kotlinx.coroutines.*
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import java.io.IOException
import java.util.concurrent.atomic.AtomicInteger

enum class ConnState { DISCONNECTED, CONNECTING, CONNECTED }
class ProtocolException(val code: Int) : IOException("设备返回错误码 0x%02X".format(code))

class SynthClient(private val scope: CoroutineScope) {
    private val _state = MutableStateFlow(ConnState.DISCONNECTED)
    val state = _state.asStateFlow()
    private val _deviceName = MutableStateFlow("")
    val deviceName = _deviceName.asStateFlow()
    private val _notice = MutableStateFlow<String?>(null)
    val notice = _notice.asStateFlow()
    fun clearNotice() { _notice.value = null }
    var onEarEvent: ((Frame) -> Unit)? = null
    private var undoReply: CompletableDeferred<Frame>? = null
    private var undoSession = -1
    var onGameEvent: ((Frame) -> Unit)? = null
    var onLinkLost: (() -> Unit)? = null
    var onDeviceEvent: ((Frame) -> Unit)? = null
    var onVoiceState: ((Int) -> Unit)? = null
    var onKeymapState: ((DeviceKeymap) -> Unit)? = null
    private val keymapDecoder = DeviceKeymapDecoder()
    var onPlaybackStopped: (() -> Unit)? = null
    @Volatile private var transport: Transport? = null
    private val decoder = FrameDecoder()
    private val incoming = Channel<Pair<Int, Frame>>(1024)
    private val outgoing = Channel<Pair<Int, ByteArray>>(512)
    private val configMutex = Mutex()
    private val wireMutex = Mutex()
    private val session = AtomicInteger(0)
    private var ack: CompletableDeferred<Frame>? = null
    private var ackCommand: Byte? = null
    private var ready: CompletableDeferred<Int>? = null
    private var pong: CompletableDeferred<Int>? = null
    private var pongSequence = 0
    private var heartbeat: Job? = null
    private var connecting: Job? = null

    init {
        scope.launch {
            for ((id, f) in incoming) if (id == session.get()) dispatch(f)
        }
        scope.launch {
            for ((id, bytes) in outgoing) if (id == session.get()) {
                try { send(bytes) } catch (e: Exception) {
                    if (e is CancellationException) throw e
                    _notice.value = "发送失败：${e.message}"; disconnect()
                }
            }
        }
    }
    private suspend fun send(bytes: ByteArray) = wireMutex.withLock {
        val t = transport ?: throw IOException("未连接设备")
        withContext(Dispatchers.IO) { t.write(bytes) }
    }
    fun connect(factory: () -> Transport) {
        if (_state.value != ConnState.DISCONNECTED) return
        val id = session.incrementAndGet()
        _state.value = ConnState.CONNECTING
        decoder.reset()
        connecting = scope.launch {
            var candidate: Transport? = null
            try {
                val t = factory(); candidate = t; transport = t
                t.onRaw = { raw ->
                    if (id == session.get()) decoder.feed(raw).forEach {
                        if (!incoming.trySend(id to Frame.from(it)).isSuccess) {
                            scope.launch { if (id == session.get()) { _notice.value = "设备回传过快，请重新连接"; disconnect() } }
                        }
                    }
                }
                t.onClosed = { reason -> scope.launch {
                    if (id == session.get()) { _notice.value = reason; disconnect() }
                } }
                withContext(Dispatchers.IO) { t.connect() }
                if (id != session.get()) { t.close(); return@launch }
                if (!ping()) throw IOException("BLE 已连接，但设备协议无应答；请检查 ESP32 固件和 FPGA 独立串口")
                _deviceName.value = t.name
                _state.value = ConnState.CONNECTED
                heartbeat = scope.launch {
                    var missed = 0
                    while (isActive) {
                        delay(3000)
                        if (ping()) missed = 0 else missed++
                        if (missed >= 3) { _notice.value = "设备心跳丢失，请重新连接"; disconnect(); break }
                    }
                }
            } catch (e: Exception) {
                candidate?.close()
                if (e is CancellationException) throw e
                if (id == session.get()) { _notice.value = "连接失败：${e.message}"; disconnect() }
            }
        }
    }
    fun disconnect(silent: Boolean = false) {
        keymapDecoder.reset()
        undoReply?.completeExceptionally(IOException("连接已断开"));undoReply=null
        onLinkLost?.invoke()
        session.incrementAndGet()
        heartbeat?.cancel(); heartbeat = null
        connecting?.cancel(); connecting = null
        val t = transport; transport = null
        t?.onRaw = null; t?.onClosed = null; t?.close()
        ack?.completeExceptionally(IOException("连接已断开")); ack = null
        ready?.completeExceptionally(IOException("连接已断开")); ready = null
        pong?.complete(-1); pong = null
        decoder.reset()
        _state.value = ConnState.DISCONNECTED
        _deviceName.value = ""
        onPlaybackStopped?.invoke()
    }
    private fun queue(bytes: ByteArray) {
        if (_state.value != ConnState.CONNECTED) { _notice.value = "请先连接设备"; return }
        if (!outgoing.trySend(session.get() to bytes).isSuccess) {
            _notice.value = "发送队列已满，连接已关闭"; disconnect()
        }
    }
    fun noteOn(note: Int, velocity: Int = 100) = queue(Protocol.noteOn(note, velocity))
    fun noteOff(note: Int) = queue(Protocol.noteOff(note))
    fun allOff() = queue(Protocol.allOff())
    suspend fun earCommand(cmd:Int,session:Int,value:Int=0) = requestAck(Protocol.buildFrame(cmd.toByte(),session shr 8,session and 255,value),cmd.toByte())
    suspend fun earUndo(session:Int,nonce:Int) {
        val d=CompletableDeferred<Frame>();undoSession=session;undoReply=d
        try { earCommand(0x45,session,nonce);withTimeout(2500) { d.await() } }
        finally { if(undoReply===d) undoReply=null }
    }
    suspend fun setVoice(v: Int) = requestAck(Protocol.setVoice(v), Cmd.SET_VOICE)
    suspend fun setVolume(v: Int) = requestAck(Protocol.setVolume(v), Cmd.SET_VOLUME)
    suspend fun setTempo(v: Int) = requestAck(Protocol.setTempo(v), Cmd.SET_TEMPO)
    suspend fun setKeymap(index: Int, note: Int) = requestAck(Protocol.setKeymap(index, note), Cmd.SET_KEYMAP)
    suspend fun play() = requestAck(Protocol.play(), Cmd.PLAY)
    suspend fun stop() = requestAck(Protocol.stop(), Cmd.STOP)
    suspend fun allOffAck() = requestAck(Protocol.allOff(), Cmd.ALL_OFF)
    private suspend fun requestAck(bytes: ByteArray, cmd: Byte) = configMutex.withLock {
        repeat(3) {
            val d = CompletableDeferred<Frame>(); ackCommand = cmd; ack = d
            try {
                send(bytes)
                val reply = withTimeoutOrNull(2000) { d.await() }
                if (reply != null) {
                    if (cmd == Cmd.SET_KEYMAP && (reply.a1 != (bytes[2].toInt() and 255) || reply.a2 != (bytes[3].toInt() and 255))) {
                        throw IOException("键位确认与发送内容不一致")
                    }
                    if (cmd == Cmd.SET_VOICE && reply.a1 != (bytes[2].toInt() and 255)) {
                        throw IOException("音色确认与发送内容不一致")
                    }
                    return@withLock
                }
            } finally { if (ack === d) { ack = null; ackCommand = null } }
        }
        throw IOException("设备未确认命令 0x%02X".format(cmd.toInt() and 255))
    }
    suspend fun downloadSong(frames: List<ByteArray>): Boolean {
        if (frames.size !in 1..SONG_MAX_EVENTS) { _notice.value = "曲谱需为 1～$SONG_MAX_EVENTS 个事件"; return false }
        return try {
            requestAck(Protocol.songStart(frames.size), Cmd.SONG_START)
            for (f in frames) { currentCoroutineContext().ensureActive(); send(f) }
            val d = CompletableDeferred<Int>(); ready = d
            try {
                send(Protocol.songEnd(frames.size))
                val received = withTimeoutOrNull(5000) { d.await() }
                if (received != frames.size) throw IOException("曲谱接收数量不符或等待超时：$received / ${frames.size}")
                true
            } finally { ready = null }
        } catch (e: Exception) {
            if (e is CancellationException) throw e
            _notice.value = "曲谱传输失败：${e.message}"; false
        }
    }
    private suspend fun ping(): Boolean {
        val seq = (++pongSequence) and 0xFFFFFF
        val d = CompletableDeferred<Int>(); pong = d
        return try { send(Protocol.ping(seq)); withTimeoutOrNull(2000) { d.await() } == seq }
        catch (e: Exception) { if (e is CancellationException) throw e; false }
        finally { if (pong === d) pong = null }
    }
    private fun dispatch(f: Frame) {
        if((f.cmd.toInt() and 255) in 0x87..0x89) {
            keymapDecoder.accept(f)?.let { onKeymapState?.invoke(it) }; return
        }
        if((f.cmd.toInt() and 255) in 0xB0..0xB6) {
            onEarEvent?.invoke(f)
            if((f.cmd.toInt() and 255)==0xB5 && ((f.a0 shl 8) or f.a1)==undoSession) undoReply?.complete(f)
            return
        }
        if ((f.cmd.toInt() and 255) in 0xA0..0xA5 || (f.cmd.toInt() and 255)==0xAF) {
            onGameEvent?.invoke(f); return
        }
        if(f.cmd==Cmd.ERR && f.a0==8) onLinkLost?.invoke()
        when (f.cmd) {
            Cmd.VOICE_STATE -> if (f.a0 in 0..1 && f.a1 == 1) onVoiceState?.invoke(f.a0)
            Cmd.ACK -> if (f.a0 == ((ackCommand?.toInt() ?: -1) and 255)) ack?.complete(f)
            Cmd.PONG -> if (f.arg24 == (pongSequence and 0xFFFFFF)) pong?.complete(f.arg24)
            Cmd.SONG_READY -> ready?.complete(f.arg24)
            Cmd.DEVICE_EVENT -> onDeviceEvent?.invoke(f)
            Cmd.STATE -> if (f.a0 and 1 == 0) onPlaybackStopped?.invoke()
            Cmd.ERR -> {
                val e = ProtocolException(f.a0)
                _notice.value = if (f.a0 == 2) "设备不支持该功能，请更新配套固件" else e.message
                ack?.completeExceptionally(e); ready?.completeExceptionally(e)
            }
        }
    }
    companion object { const val SONG_MAX_EVENTS = 16000 }
}
