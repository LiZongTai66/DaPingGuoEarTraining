package com.example.app.ui

import android.app.Application
import android.bluetooth.BluetoothDevice
import android.os.SystemClock
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.app.data.*
import com.example.app.protocol.*
import com.example.app.synth.*
import com.example.app.transport.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import java.io.File

class AppViewModel(app: Application) : AndroidViewModel(app) {
    private val gamePrefs = app.getSharedPreferences("game_stats", 0)
    private val _practiceLabel = MutableStateFlow(gamePrefs.getString("practice_label", "") ?: "")
    val practiceLabel = _practiceLabel.asStateFlow()
    fun setPracticeLabel(label: String) {
        if (_gameRound.value.running) return
        _practiceLabel.value = label.trim().take(30)
        gamePrefs.edit().putString("practice_label",_practiceLabel.value).apply()
    }
    private val _gameRound = MutableStateFlow(GameRound())
    val gameRound = _gameRound.asStateFlow()
    private val _gameHistory = MutableStateFlow<List<GameReport>>(runCatching {
        val a=org.json.JSONArray(gamePrefs.getString("history", "[]"))
        (0 until minOf(a.length(),20)).map { GameReport.fromJson(a.getJSONObject(it)) }
    }.getOrDefault(emptyList()))
    val gameHistory = _gameHistory.asStateFlow()
    private fun saveGame(round: GameRound) {
        if(!round.started) return
        val report=round.report()
        _gameHistory.value=(listOf(report)+_gameHistory.value).take(20)
        val a=org.json.JSONArray();_gameHistory.value.forEach { a.put(it.json()) }
        gamePrefs.edit().putString("history",a.toString()).apply()
    }
    private fun endGameLink() {
        if(_gameRound.value.running) {
            _gameRound.value=_gameRound.value.interrupted();saveGame(_gameRound.value)
        }
    }
    private val earPrefs = app.getSharedPreferences("ear_training",0)
    private val _earRound = MutableStateFlow(EarRound())
    val earRound = _earRound.asStateFlow()
    private val _earHistory = MutableStateFlow<List<EarResult>>(runCatching {
        val a=org.json.JSONArray(earPrefs.getString("history","[]"))
        (0 until minOf(a.length(),30)).map { EarResult.parse(a.getJSONObject(it)) }
    }.getOrDefault(emptyList()))
    val earHistory = _earHistory.asStateFlow()
    private val _earUndoPending = MutableStateFlow(0)
    val earUndoPending = _earUndoPending.asStateFlow()
    private val earUndoQueue=kotlinx.coroutines.channels.Channel<Pair<Int,Int>>(32)
    private var undoNonce=0
    private var earSerial=earPrefs.getInt("serial",0)
    private var earJob: Job?=null
    private fun earInterrupted() {
        if(_earRound.value.active) { earJob?.cancel();_earRound.value=_earRound.value.copy(phase=EarPhase.ERROR,message="连接中断，本轮未保存，请重新开始") }
    }
    fun startEarTraining() {
        if(_earRound.value.active || _busy.value) return
        if(connState.value!=ConnState.CONNECTED) { _localError.value="请先连接真实开发板";return }
        if(_recording.value) { _localError.value="请先停止录音";return }
        if(_volume.value==0) { _localError.value="请先把演奏音量调大";return }
        earSerial=(earSerial+1) and 65535;earPrefs.edit().putInt("serial",earSerial).apply()
        val sid=earSerial;val notes=randomPhrase();undoNonce=0
        _earRound.value=EarRound(sid,EarPhase.PREPARING,notes,time=System.currentTimeMillis(),message="正在准备 7 个随机音符…")
        earJob=viewModelScope.launch {
            try {
                client.stop();client.allOffAck();client.setVolume(_volume.value);client.setVoice(_voice.value)
                client.earCommand(0x40,sid,7)
                val defaults=intArrayOf(60,62,64,65,67,69,71)
                _physicalKeymap.value=defaults;physicalDraftDirty=false;prefs.savePhysicalKeymap(defaults);_keymapStatus.value="听音训练已恢复 Do～Si"
                notes.forEachIndexed { i,n -> client.earCommand(0x41,sid,(i shl 3) or n) }
                client.earCommand(0x42,sid)
            } catch(e:Exception) {
                if(e is CancellationException) throw e
                _earRound.value=_earRound.value.copy(phase=EarPhase.ERROR,message="启动失败，请更新配套 FPGA / ESP32 后重试：${e.message}")
                runCatching { client.allOffAck() }
            }
        }
    }
    fun replayEarTraining() {
        val r=_earRound.value
        if(r.phase!=EarPhase.INPUT || _earUndoPending.value!=0) return
        _earRound.value=r.copy(phase=EarPhase.PREPARING,message="重新播放，会清空本次输入…")
        action { try { client.earCommand(0x44,r.session) } catch(e:Exception) { earInterrupted();throw e } }
    }
    fun undoEarNote() {
        val r=_earRound.value
        if(r.phase!=EarPhase.INPUT || r.answer.isEmpty()) return
        undoNonce=(undoNonce+1) and 255
        if(earUndoQueue.trySend(r.session to undoNonce).isSuccess) _earUndoPending.value++
    }
    fun submitEarTraining() {
        val r=_earRound.value
        if(r.phase!=EarPhase.INPUT || r.answer.size!=7 || _earUndoPending.value!=0) return
        _earRound.value=r.copy(phase=EarPhase.SUBMITTING,snapshot=List(7){null},message="正在接收 FPGA 最终答案…")
        action { try { client.earCommand(0x46,r.session) } catch(e:Exception) { earInterrupted();throw e } }
    }
    fun cancelEarTraining() {
        val r=_earRound.value;if(!r.active) return
        earJob?.cancel();_earRound.value=r.copy(phase=EarPhase.CANCELLED,message="本轮已取消，不计入记录")
        action { client.earCommand(0x43,r.session);client.allOffAck() }
    }
    private val prefs = Prefs(app)
    private val recordingStore = RecordingStore(app)
    private val client = SynthClient(viewModelScope)
    val connState = client.state
    val deviceName = client.deviceName
    val notice = client.notice
    fun clearNotice() = client.clearNotice()
    private val _localError = MutableStateFlow<String?>(null)
    val localError = _localError.asStateFlow()
    fun clearLocalError() { _localError.value = null }
    private val _voice = MutableStateFlow(prefs.voice.coerceIn(0, 1))
    val voice = _voice.asStateFlow()
    private val _voiceSwitching = MutableStateFlow(false)
    val voiceSwitching = _voiceSwitching.asStateFlow()
    private val _voiceStatus = MutableStateFlow("等待设备音色同步")
    val voiceStatus = _voiceStatus.asStateFlow()
    private val _volume = MutableStateFlow(prefs.volume)
    val volume = _volume.asStateFlow()
    val voiceNames = listOf("钢琴", "吉他")
    private fun action(block: suspend () -> Unit) {
        viewModelScope.launch {
            try { block() } catch (e: Exception) {
                if (e is CancellationException) throw e
                _localError.value = e.message ?: "操作失败"
            }
        }
    }
    fun setVoice(v: Int) {
        if(_earRound.value.active || v !in 0..1 || _voiceSwitching.value) return
        if(connState.value != ConnState.CONNECTED) {
            _voice.value=v;prefs.voice=v;_voiceStatus.value="未连接设备，尚未切换板载音色";return
        }
        _voiceSwitching.value=true;_voiceStatus.value="正在切换板载音色…"
        action {
            try {
                client.setVoice(v)
                _voice.value=v;prefs.voice=v;_voiceStatus.value="设备已确认，新按下的音符使用此音色"
            } catch(e: Exception) {
                _voiceStatus.value="切换未完成，请检查连接后重试";throw e
            } finally { _voiceSwitching.value=false }
        }
    }
    private var volumeJob: Job? = null
    fun setVolume(v: Int) {
        _volume.value = v; prefs.volume = v
        volumeJob?.cancel()
        volumeJob = viewModelScope.launch { delay(250); if (connState.value == ConnState.CONNECTED) {
            try { client.setVolume(v) } catch (e: Exception) { if (e is CancellationException) throw e; _localError.value = e.message }
        } }
    }
    fun connectMock() = client.connect { MockTransport() }
    fun connectBluetooth(device: BluetoothDevice) = client.connect { BluetoothBleTransport(getApplication(), device) }
    fun disconnect() = client.disconnect()
    private val _busy = MutableStateFlow(false)
    val busy = _busy.asStateFlow()
    private val _playingTitle = MutableStateFlow<String?>(null)
    val playingTitle = _playingTitle.asStateFlow()
    private var playbackTimer: Job? = null
    fun noteOn(note: Int) {
        if (_earRound.value.active || _busy.value || connState.value != ConnState.CONNECTED) return
        if (_recording.value && !_deviceRecording.value) recordPhoneEvent(note, true)
        client.noteOn(note, 100)
    }
    fun noteOff(note: Int) {
        if (_recording.value && !_deviceRecording.value) recordPhoneEvent(note, false)
        if (!_busy.value && connState.value == ConnState.CONNECTED) client.noteOff(note)
    }
    fun allOff() { if (connState.value == ConnState.CONNECTED) client.allOff() }
    fun downloadAndPlay(title: String, events: List<SongEvent>) {
        if(_earRound.value.active) { _localError.value="请先结束听音训练";return }
        if (_busy.value) return
        if (connState.value != ConnState.CONNECTED) { _localError.value = "请先连接设备"; return }
        if (_recording.value) { _localError.value = "请先停止录制，再回放"; return }
        _busy.value = true
        action {
            try {
                val frames = encodeFrames(events)
                if (client.downloadSong(frames)) {
                    client.play(); _playingTitle.value = title
                    playbackTimer?.cancel()
                    playbackTimer = viewModelScope.launch {
                        delay(events.sumOf { it.dt5ms.toLong() } * 5 + 300)
                        _playingTitle.value = null
                    }
                }
            } finally { _busy.value = false }
        }
    }
    fun playSong(song: Song) = downloadAndPlay(song.title, compose(song))
    fun stopPlayback() {
        if (_busy.value) { _localError.value = "正在传输曲谱，请等待完成或断开连接"; return }
        action { client.stop(); client.allOffAck(); playbackTimer?.cancel(); _playingTitle.value = null }
    }
    private val songsFile = File(app.filesDir, "online_songs.json")
    private val _downloadedSongs = MutableStateFlow<List<Song>>(emptyList())
    val downloadedSongs = _downloadedSongs.asStateFlow()
    val featuredSongs: List<Song> = OnlineSongs.parse(
        app.assets.open("starlight-poly.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
    )
    private val _fetching = MutableStateFlow(false)
    val fetching = _fetching.asStateFlow()
    init {
        client.onEarEvent = { f ->
            val old=_earRound.value;val next=old.accept(f);_earRound.value=next
            if(old.phase!=EarPhase.COMPLETE && next.phase==EarPhase.COMPLETE) {
                next.result()?.let { report ->
                    _earHistory.value=(listOf(report)+_earHistory.value).take(30)
                    val a=org.json.JSONArray();_earHistory.value.forEach { a.put(it.json()) }
                    earPrefs.edit().putString("history",a.toString()).apply()
                }
            }
        }
        viewModelScope.launch {
            _earRound.map { it.session to it.phase }.distinctUntilChanged().collectLatest { (sid,phase) ->
                val waitMs=when(phase) {
                    EarPhase.PREPARING -> 20000L
                    EarPhase.LISTENING -> 12000L
                    EarPhase.INPUT -> 65000L
                    EarPhase.SUBMITTING -> 8000L
                    else -> 0L
                }
                if(waitMs>0) {
                    delay(waitMs)
                    if(_earRound.value.session==sid && _earRound.value.phase==phase) {
                        earJob?.cancel()
                        _earRound.value=_earRound.value.copy(phase=EarPhase.ERROR,message="等待设备回应超时，请检查连接后重新开始")
                        viewModelScope.launch { runCatching { client.allOffAck() } }
                    }
                }
            }
        }
        viewModelScope.launch {
            for((sid,nonce) in earUndoQueue) {
                try { if(_earRound.value.session==sid && _earRound.value.phase==EarPhase.INPUT) client.earUndo(sid,nonce) }
                catch(e:Exception) { if(e is CancellationException) throw e;if(_earRound.value.session==sid) earInterrupted() }
                finally { _earUndoPending.value=(_earUndoPending.value-1).coerceAtLeast(0) }
            }
        }
        client.onKeymapState = { actual ->
            _deviceKeymap.value=actual
            if(!physicalDraftDirty && !physicalSending) {
                _physicalKeymap.value=actual.notes.toIntArray()
                prefs.savePhysicalKeymap(_physicalKeymap.value)
                _keymapStatus.value="已同步板上实际键位 · ${actual.modeLabel}"
            } else if(!physicalSending) {
                _keymapStatus.value="板上键位已更新；手机修改尚未下发"
            }
        }
        client.onVoiceState = { v ->
            _voice.value=v;prefs.voice=v;_voiceStatus.value="已同步板载音色 · 新按键生效"
        }
        client.onGameEvent = { f ->
            val old=_gameRound.value
            if((f.cmd.toInt() and 255)==0xA0 && old.running) saveGame(old.interrupted())
            val received=old.accept(f,System.currentTimeMillis())
            val next=if((f.cmd.toInt() and 255)==0xA0) received.copy(label=_practiceLabel.value) else received
            _gameRound.value=next
            if(old.running && !next.running) saveGame(next)
        }
        client.onLinkLost = { endGameLink();earInterrupted() }
        action {
            _downloadedSongs.value = withContext(Dispatchers.IO) {
                runCatching { if (songsFile.exists()) OnlineSongs.parse(songsFile.readText()) else emptyList() }.getOrDefault(emptyList())
            }
        }
        client.onDeviceEvent = { f ->
            if (_recording.value && _deviceRecording.value &&
                (f.a1 == 0 || f.a1 in Protocol.NOTE_MIN..Protocol.NOTE_MAX)) {
                lastDeviceArrivalMs = SystemClock.uptimeMillis()
                appendEvent(SongEvent(f.a0, f.a1, f.a2 and 128 != 0, f.a2 and 127))
            }
        }
        client.onPlaybackStopped = { playbackTimer?.cancel(); _playingTitle.value = null }
        viewModelScope.launch {
            yield()
            connState.collect { state ->
                if (state == ConnState.DISCONNECTED) {
                    _voiceStatus.value="未连接设备，尚未同步音色"
                    _keymapStatus.value = "未连接设备，尚未同步实际键位"
                    _deviceKeymap.value=null
                    if (_recording.value) stopRecordingAndNotify()
                }
            }
        }
    }
    fun fetchSongs(address: String) {
        if (_fetching.value) return
        _fetching.value = true
        action {
            try { saveImported(withContext(Dispatchers.IO) { OnlineSongs.download(address) }) }
            finally { _fetching.value = false }
        }
    }
    fun importSongs(uri: android.net.Uri) {
        if (_fetching.value) return
        _fetching.value = true
        action {
            try {
                val songs = withContext(Dispatchers.IO) {
                    val text = getApplication<Application>().contentResolver.openInputStream(uri)?.use { it.readBytesLimited(OnlineSongs.MAX_BYTES).toString(Charsets.UTF_8) }
                        ?: error("无法读取文件")
                    OnlineSongs.parse(text)
                }
                saveImported(songs)
            } finally { _fetching.value = false }
        }
    }
    private suspend fun saveImported(songs: List<Song>) {
        val merged = (_downloadedSongs.value + songs).associateBy { it.id }.values.toList()
        require(merged.size <= 100) { "最多保存 100 首导入曲谱" }
        val json = OnlineSongs.encode(merged)
        require(json.toByteArray().size <= OnlineSongs.MAX_BYTES) { "曲谱库已满" }
        withContext(Dispatchers.IO) {
            val tmp = File(songsFile.path + ".tmp"); tmp.writeText(json)
            check(tmp.renameTo(songsFile)) { "保存曲谱失败" }
        }
        _downloadedSongs.value = merged; _localError.value = "已保存 ${songs.size} 首曲谱，可离线查看和下发"
    }
    private val _keymap = MutableStateFlow(prefs.loadKeymap())
    val keymap = _keymap.asStateFlow()
    fun setPadNote(index: Int, note: Int) {
        val next = _keymap.value.copyOf(); next[index] = note; _keymap.value = next; prefs.saveKeymap(next)
    }
    private var physicalDraftDirty=false
    private var physicalSending=false
    private val _deviceKeymap=MutableStateFlow<DeviceKeymap?>(null)
    val deviceKeymap=_deviceKeymap.asStateFlow()
    private val _physicalKeymap = MutableStateFlow(prefs.loadPhysicalKeymap())
    val physicalKeymap = _physicalKeymap.asStateFlow()
    private val _keymapStatus = MutableStateFlow("尚未下发到设备")
    val keymapStatus = _keymapStatus.asStateFlow()
    fun setPhysicalNote(index: Int, note: Int) {
        physicalDraftDirty=true
        val next = _physicalKeymap.value.copyOf(); next[index] = note
        _physicalKeymap.value = next; prefs.savePhysicalKeymap(next); _keymapStatus.value = "已保存到手机，待下发"
    }
    fun sendPhysicalKeymap() {
        if(_earRound.value.active) { _localError.value="训练中固定使用 Do～Si 键位";return }
        if (_busy.value) return
        if (connState.value != ConnState.CONNECTED) { _localError.value = "请先连接设备"; return }
        val snapshot = _physicalKeymap.value.copyOf()
        _busy.value = true; physicalSending=true; _keymapStatus.value = "正在下发…"
        action {
            try {
                snapshot.forEachIndexed { i, note -> client.setKeymap(i, note) }
                if(snapshot.contentEquals(_physicalKeymap.value)) physicalDraftDirty=false
                _keymapStatus.value = if (snapshot.contentEquals(_physicalKeymap.value)) "7 个实体琴键已获设备确认" else "下发期间有修改，请再次下发"
            } catch (e: Exception) { _keymapStatus.value = "下发未完成，请重试整组键位"; throw e }
            finally { physicalSending=false; _busy.value = false }
        }
    }
    private val _recording = MutableStateFlow(false)
    val isRecording = _recording.asStateFlow()
    private val _deviceRecording = MutableStateFlow(false)
    val deviceRecording = _deviceRecording.asStateFlow()
    private val _recCount = MutableStateFlow(0)
    val recordedEventCount = _recCount.asStateFlow()
    private val rawEvents = ArrayList<SongEvent>()
    private val activeNotes = mutableSetOf<Int>()
    private var startMs = 0L
    private var lastTick = 0L
    private var lastDeviceArrivalMs = 0L
    fun startRecording() = beginRecording(false)
    fun startDeviceRecording() = beginRecording(true)
    private fun beginRecording(device: Boolean) {
        if (_earRound.value.active) { _localError.value="请先结束听音训练";return }
        if (_recording.value || _busy.value) return
        if (connState.value != ConnState.CONNECTED) { _localError.value = "请先连接设备"; return }
        if (_playingTitle.value != null) { _localError.value = "请先停止曲谱回放"; return }
        rawEvents.clear(); activeNotes.clear(); _recCount.value = 0
        startMs = SystemClock.uptimeMillis(); lastTick = 0; lastDeviceArrivalMs = startMs
        _deviceRecording.value = device; _recording.value = true
    }
    private fun recordPhoneEvent(note: Int, on: Boolean) {
        val tick = (SystemClock.uptimeMillis() - startMs) / 5
        appendEvent(SongEvent((tick - lastTick).coerceAtMost(Int.MAX_VALUE.toLong()).toInt(), note, on, if (on) 100 else 0)); lastTick = tick
    }
    private fun appendEvent(event: SongEvent) {
        if (rawEvents.size >= 15000) { stopRecordingAndNotify(); _localError.value = "录制已达容量上限，已自动保存"; return }
        if (event.note != 0) { if (event.on) activeNotes.add(event.note) else activeNotes.remove(event.note) }
        rawEvents.add(event); _recCount.value = rawEvents.size
    }
    fun stopRecording(): Boolean {
        if (!_recording.value) return false
        _recording.value = false
        if (rawEvents.none { it.on }) { rawEvents.clear(); _recCount.value = 0; return false }
        val tail = if (_deviceRecording.value) ((SystemClock.uptimeMillis() - lastDeviceArrivalMs) / 5).coerceAtLeast(0).toInt() else (((SystemClock.uptimeMillis() - startMs) / 5) - lastTick).coerceAtLeast(0).toInt()
        activeNotes.toList().forEachIndexed { i, n -> rawEvents.add(SongEvent(if (i == 0) tail else 0, n, false, 0)) }
        val normalized = splitEvents(rawEvents).toMutableList()
        if (normalized.size > SynthClient.SONG_MAX_EVENTS) { rawEvents.clear(); _localError.value = "录制时间间隔超出容量，未保存"; return false }
        normalized[0] = normalized[0].copy(dt5ms = 0)
        val prefix = if (_deviceRecording.value) "实体琴" else "手机演奏"
        recordingStore.add(Recording(prefix + " " + android.text.format.DateFormat.format("MM-dd HH:mm:ss", System.currentTimeMillis()), System.currentTimeMillis(), normalized))
        rawEvents.clear(); activeNotes.clear(); _recCount.value = 0; return true
    }
    fun stopRecordingAndNotify() {
        _localError.value = if (stopRecording()) "演奏事件已保存，可在录音页导出或下发回放" else "未收到有效音符，没有保存录音"
    }
    fun loadRecordings() = recordingStore.load()
    fun deleteRecording(rec: Recording) = recordingStore.delete(rec.name, rec.createdAt)
    fun playRecording(rec: Recording) = downloadAndPlay(rec.name, rec.events)
    fun exportRecording(rec: Recording, uri: android.net.Uri) = action {
        withContext(Dispatchers.IO) {
            val json = org.json.JSONObject().put("format", "dapingguo-events-v1").put("title", rec.name)
                .put("events", org.json.JSONArray().apply { rec.events.forEach { put(org.json.JSONObject().put("dt5ms", it.dt5ms).put("note", it.note).put("on", it.on).put("velocity", it.velocity)) } })
            getApplication<Application>().contentResolver.openOutputStream(uri)?.use { it.write(json.toString(2).toByteArray(Charsets.UTF_8)) } ?: error("无法写入文件")
        }
        _localError.value = "演奏记录已导出"
    }
    override fun onCleared() { client.disconnect(silent = true); super.onCleared() }
}
