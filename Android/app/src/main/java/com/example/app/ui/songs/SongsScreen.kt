package com.example.app.ui.songs

import android.os.SystemClock
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.data.*
import com.example.app.synth.ConnState
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen
import kotlinx.coroutines.delay

private fun scoreNote(token: NoteToken): String {
    val n = midiNote(token.noteName)
    val index = listOf(60, 62, 64, 65, 67, 69, 71).indexOf(n)
    val label = if (token.noteName == "R") "0" else if (index >= 0) "${index + 1}" else token.noteName
    return label + if (token.beats == 2f) "—" else if (token.beats != 1f) "(${token.beats}拍)" else ""
}

@Composable
fun SongsScreen(vm: AppViewModel, onBack: () -> Unit) {
    val busy by vm.busy.collectAsState()
    val playing by vm.playingTitle.collectAsState()
    val downloaded by vm.downloadedSongs.collectAsState()
    val fetching by vm.fetching.collectAsState()
    val conn by vm.connState.collectAsState()
    var address by rememberSaveable { mutableStateOf("") }
    var showImport by rememberSaveable { mutableStateOf(false) }
    var detail by remember { mutableStateOf<Song?>(null) }
    val importFile = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri -> if (uri != null) vm.importSongs(uri) }
    AppScreen("在线曲谱", vm, onBack) { pad ->
        LazyColumn(Modifier.fillMaxSize().padding(pad).padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(vertical = 16.dp)) {
            item {
                Text("主旋律与伴奏", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                Text("《星光下的梦想》按简谱编配，包含主旋律和低音伴奏。建议先选钢琴音色试听。", color = Color(0xFFB8C0D0), modifier = Modifier.padding(top = 6.dp))
                Text("连接 ESP32 后下发到琴上演奏；手机简谱预览无声。", color = Color(0xFFB8C0D0), fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
            }
            items(vm.featuredSongs, key = { "featured_${it.id}" }) { song ->
                SongRow(song, "主旋律 + 伴奏 · ${song.bpm} BPM", busy, playing == song.title, conn == ConnState.CONNECTED,
                    { detail = song }, { vm.playSong(song) }, { vm.stopPlayback() })
            }
            item {
                HorizontalDivider()
                Text("基础示范片段", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                Text("Do–Si = C4、D4、E4、F4、G4、A4、B4。每首14个音、16拍，1拍350毫秒；此处保留旧版练习片段。", color = Color(0xFFB8C0D0), fontSize = 12.sp)
            }
            items(SongLibrary.songs, key = { it.id }) { song ->
                SongRow(song, "单声部练习 · 350毫秒/拍", busy, playing == song.title, conn == ConnState.CONNECTED,
                    { detail = song }, { vm.playSong(song) }, { vm.stopPlayback() })
            }
            item {
                HorizontalDivider()
                TextButton(onClick = { showImport = !showImport }) { Text(if (showImport) "收起在线下载 / 文件导入" else "在线下载 / 文件导入") }
            }
            if (showImport) item {
                Text("支持旧版单声部 JSON，也支持带 startBeat 的主旋律与伴奏曲谱。下载后可离线下发。", color = Color(0xFFB8C0D0), fontSize = 12.sp)
                OutlinedTextField(address, { address = it }, label = { Text("HTTPS 曲谱 JSON 链接") }, singleLine = true, modifier = Modifier.fillMaxWidth())
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { vm.fetchSongs(address) }, enabled = !fetching && address.isNotBlank()) { Text(if (fetching) "获取中…" else "在线下载") }
                    OutlinedButton(onClick = { importFile.launch(arrayOf("application/json", "text/plain", "application/octet-stream")) }, enabled = !fetching) { Text("导入文件") }
                }
                Text("不能直接填写网页、MP3 或 MIDI 链接。", color = Color(0xFFB8C0D0), fontSize = 12.sp)
            }
            if (downloaded.isNotEmpty()) {
                item { Text("已下载 / 导入（不属于板上固定曲目）", color = Color.White) }
                items(downloaded, key = { "downloaded_${it.id}" }) { song ->
                    SongRow(song, if (song.beatMs > 0) "${song.beatMs}毫秒/拍" else "${song.bpm} BPM", busy,
                        playing == song.title, conn == ConnState.CONNECTED,
                        { detail = song }, { vm.playSong(song) }, { vm.stopPlayback() })
                }
            }
        }
    }
    detail?.let { song -> ScoreDialog(song) { detail = null } }
}

@Composable
private fun SongRow(song: Song, subtitle: String, busy: Boolean, playing: Boolean, connected: Boolean,
    onDetail: () -> Unit, onPlay: () -> Unit, onStop: () -> Unit) {
    val duration = remember(song) { compose(song).sumOf { it.dt5ms.toLong() } * 5 }
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(7.dp)) {
            Text(song.title, fontWeight = FontWeight.Bold, fontSize = 19.sp)
            Text("$subtitle · ${song.tokens.size}个记谱单元 · 单遍约${duration / 1000.0}秒", fontSize = 12.sp)
            if (song.tokens.any { it.startBeat != null }) {
                Text("${song.tokens.mapNotNull { it.part }.distinct().joinToString(" + ").ifBlank { "多声部" }} · 同时演奏", color = Color(0xFF7DD3FC))
            } else {
                Text(song.tokens.take(28).joinToString("  ") { scoreNote(it) } + if (song.tokens.size > 28) " …" else "", color = Color(0xFF7DD3FC))
            }
            if (playing) Text("设备单遍回放中…", color = Color(0xFF4ADE80))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = onDetail) { Text("简谱 / 节拍预览") }
                if (playing) OutlinedButton(onClick = onStop, enabled = !busy) { Text("停止") }
                else OutlinedButton(onClick = onPlay, enabled = connected && !busy) { Text(if (busy) "下发中…" else "下发单遍") }
            }
            if (!connected) Text("查看简谱无需连接；下发需先连接设备。", fontSize = 11.sp)
        }
    }
}

@Composable
private fun ScoreDialog(song: Song, onDismiss: () -> Unit) {
    var running by remember(song.id) { mutableStateOf(false) }
    var activeIndices by remember(song.id) { mutableStateOf(emptySet<Int>()) }
    var loop by rememberSaveable(song.id) { mutableStateOf(true) }
    val spans = remember(song) { noteSpans(song).sortedBy { it.startMs } }
    val period = remember(song) { songDurationMs(song) }
    LaunchedEffect(running, loop) {
        if (!running) return@LaunchedEffect
        val start = SystemClock.uptimeMillis()
        while (running) {
            val elapsed = (SystemClock.uptimeMillis() - start).toDouble()
            if (!loop && elapsed >= period) { running = false; activeIndices = emptySet(); break }
            val position = elapsed % period
            activeIndices = spans.filter { position >= it.startMs && position < it.endMs }.map { it.index }.toSet()
            delay(16)
        }
    }
    AlertDialog(onDismissRequest = onDismiss, title = { Text(song.title + " · 简谱") }, text = {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("无声节拍预览，只显示进度，不驱动手机或 FPGA 发声。", fontSize = 12.sp)
            Text(if (song.beatMs > 0) "1拍${song.beatMs}毫秒；2拍${song.beatMs * 2}毫秒" else "速度 ${song.bpm} BPM")
            if (song.stepGapMs > 0) Text("按当前 FPGA 状态机计入每音${song.stepGapMs}毫秒切换时间。", fontSize = 11.sp)
            if (activeIndices.isNotEmpty()) Text(activeIndices.joinToString(" · ") {
                val token = song.tokens[it]
                "${token.part ?: "音符"} ${token.noteName}"
            }, color = Color(0xFF7DD3FC))
            Row {
                Checkbox(checked = loop, onCheckedChange = { loop = it })
                Text("循环预览", modifier = Modifier.padding(top = 12.dp))
            }
            LazyColumn(Modifier.fillMaxWidth().heightIn(max = 260.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                items(spans, key = { it.index }) { span ->
                    val token = span.token
                    Surface(color = if (span.index in activeIndices) Color(0xFF0E7490) else Color(0x221E90FF), modifier = Modifier.fillMaxWidth()) {
                        val position = token.startBeat?.let { "第${it + 1}拍 · " } ?: ""
                        Text("${token.part?.plus(" · ") ?: ""}$position${scoreNote(token)} · 力度${token.velocity}", modifier = Modifier.padding(8.dp))
                    }
                }
            }
        }
    }, confirmButton = {
        TextButton(onClick = { running = !running; if (!running) activeIndices = emptySet() }) { Text(if (running) "停止预览" else "开始预览") }
    }, dismissButton = { TextButton(onClick = onDismiss) { Text("关闭") } })
}
