package com.example.app.ui.record

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.app.data.Recording
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen

@Composable
fun RecordScreen(vm: AppViewModel, onBack: () -> Unit) {
    val recording by vm.isRecording.collectAsState()
    val device by vm.deviceRecording.collectAsState()
    val count by vm.recordedEventCount.collectAsState()
    val busy by vm.busy.collectAsState()
    val playing by vm.playingTitle.collectAsState()
    var recordings by remember { mutableStateOf(vm.loadRecordings()) }
    var pendingExport by remember { mutableStateOf<Recording?>(null) }
    var pendingDelete by remember { mutableStateOf<Recording?>(null) }
    val export = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/json")) { uri ->
        val rec = pendingExport
        if (uri != null && rec != null) vm.exportRecording(rec, uri)
        pendingExport = null
    }
    LaunchedEffect(recording) { recordings = vm.loadRecordings() }
    AppScreen("演奏录音", vm, onBack) { pad ->
        LazyColumn(Modifier.fillMaxSize().padding(pad).padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(vertical = 16.dp)) {
            item {
                Text("记录音符、力度与时间，可导出事件文件或下发到设备重放。本版不录制 WAV / MP3 声音。", color = Color(0xFFB8C0D0))
                Spacer(Modifier.height(8.dp))
                if (!recording) {
                    Button(onClick = { vm.startDeviceRecording() }, enabled = !busy) { Text("开始接收实体琴演奏") }
                    Text("连接设备后开始录制，再弹实体琴；需 FPGA 上报演奏事件。", color = Color(0xFFB8C0D0))
                } else {
                    Text("${if (device) "实体琴回传" else "手机演奏"}录制中 · $count 个事件", color = Color(0xFFFCA5A5))
                    Button(onClick = { vm.stopRecordingAndNotify(); recordings = vm.loadRecordings() }) { Text("停止并保存") }
                    if (device && count == 0) Text("等待设备事件。一直为 0 时请检查 FPGA 上报固件和独立串口。", color = Color(0xFFB8C0D0))
                }
                if (playing != null) OutlinedButton(onClick = { vm.stopPlayback() }, enabled = !busy) { Text("停止回放：$playing") }
            }
            if (recordings.isEmpty()) item { Text("还没有演奏记录。也可以在演奏台录制手机按键。", color = Color(0xFFB8C0D0)) }
            items(recordings, key = { "${it.name}-${it.createdAt}" }) { rec ->
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(14.dp)) {
                        Text(rec.name)
                        Text("${rec.events.size} 个事件 · ${rec.events.sumOf { it.dt5ms.toLong() } * 5 / 1000.0} 秒")
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Button(onClick = { vm.playRecording(rec) }, enabled = !busy && !recording) { Text("下发回放") }
                            OutlinedButton(onClick = { pendingExport = rec; export.launch("dapingguo-${rec.createdAt}.json") }) { Text("导出") }
                            TextButton(onClick = { pendingDelete = rec }) { Text("删除") }
                        }
                    }
                }
            }
        }
    }
    pendingDelete?.let { rec ->
        AlertDialog(onDismissRequest = { pendingDelete = null }, title = { Text("删除这条演奏记录？") }, text = { Text(rec.name) },
            confirmButton = { TextButton(onClick = { vm.deleteRecording(rec); recordings = vm.loadRecordings(); pendingDelete = null }) { Text("删除") } },
            dismissButton = { TextButton(onClick = { pendingDelete = null }) { Text("取消") } })
    }
}
