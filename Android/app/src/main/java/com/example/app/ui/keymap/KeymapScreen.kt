@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.example.app.ui.keymap

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.data.noteDisplayName
import com.example.app.protocol.Protocol
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen

@Composable
fun KeymapScreen(vm: AppViewModel, onBack: () -> Unit) {
    val keymap by vm.keymap.collectAsState()
    val physical by vm.physicalKeymap.collectAsState()
    val status by vm.keymapStatus.collectAsState()
    val device by vm.deviceKeymap.collectAsState()
    val busy by vm.busy.collectAsState()
    var editingPhysical by remember { mutableStateOf<Int?>(null) }
    var editingIndex by remember { mutableStateOf<Int?>(null) }

    AppScreen(title = "键位自定义", vm = vm, onBack = onBack) { pad ->
        LazyColumn(
            Modifier.fillMaxSize().padding(pad).padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(vertical = 16.dp)
        ) {
            item {
                Text(
                    "设置实体琴的 7 个按键，再点下发。需配套 FPGA 固件支持；下方手机打击垫单独设置。",
                    color = Color(0xFFB8C0D0), fontSize = 12.sp
                )
            }
            item {
                Card(Modifier.fillMaxWidth(), colors=CardDefaults.cardColors(containerColor=Color(0xFF18394B))) {
                    Column(Modifier.padding(16.dp), verticalArrangement=Arrangement.spacedBy(8.dp)) {
                        Text("板上实际实体键位",color=Color(0xFF48CAE4),fontWeight=FontWeight.Bold)
                        val actual=device
                        Text(actual?.modeLabel ?: "等待设备回传 · 请连接新版 FPGA",color=Color.White)
                        if(actual!=null) {
                            Text(actual.notes.mapIndexed { i,n -> "${i+1}: ${noteDisplayName(n)}" }.joinToString("   "),color=Color.White)
                        }
                        Text("调低 / 调高：低八度 ↔ 正常 ↔ 高八度。按实体八度键会恢复对应八度的 Do～Si；听音训练恢复正常八度。",fontSize=12.sp,color=Color(0xFFB8C0D0))
                    }
                }
            }
            item { Text("手机编辑区 · 下发后生效",color=Color.White,fontWeight=FontWeight.Bold) }
            itemsIndexed(physical.toList()) { index, note ->
                Card(Modifier.fillMaxWidth()) {
                    Row(Modifier.fillMaxWidth().padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text("实体键 ${index + 1} · ${listOf("Do", "Re", "Mi", "Fa", "Sol", "La", "Si")[index]}", modifier = Modifier.weight(1f))
                        Text(noteDisplayName(note))
                        TextButton(onClick = { editingPhysical = index }, enabled = !busy) { Text("修改") }
                    }
                }
            }
            item {
                Button(onClick = { vm.sendPhysicalKeymap() }, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text(if (busy) "下发中…" else "下发 7 键映射到设备") }
                Text(status, color = Color(0xFFB8C0D0), modifier = Modifier.padding(vertical = 8.dp))
                Text("手机打击垫（仅保存在 App）", color = Color.White)
            }
            itemsIndexed(keymap.toList()) { index, note ->
                Card(
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0x26FFFFFF)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 14.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("P${index + 1}", color = Color(0xFF48CAE4), fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        Spacer(Modifier.weight(1f))
                        Text(noteDisplayName(note), color = Color.White, fontSize = 16.sp)
                        Spacer(Modifier.width(12.dp))
                        TextButton(onClick = { editingIndex = index }) { Text("修改") }
                    }
                }
            }
        }
    }

    editingPhysical?.let { idx ->
        NotePickerDialog(physical[idx], { editingPhysical = null }) { note ->
            vm.setPhysicalNote(idx, note); editingPhysical = null
        }
    }
    editingIndex?.let { idx ->
        NotePickerDialog(
            current = keymap[idx],
            onDismiss = { editingIndex = null },
            onPick = { note ->
                vm.setPadNote(idx, note)
                editingIndex = null
            }
        )
    }
}

@Composable
private fun NotePickerDialog(current: Int, onDismiss: () -> Unit, onPick: (Int) -> Unit) {
    val notes = remember { (Protocol.NOTE_MIN..Protocol.NOTE_MAX).toList() }
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = Color(0xFF1B2238)) {
        Text(
            "选择音符（当前 ${noteDisplayName(current)}）",
            color = Color.White, fontSize = 15.sp, fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(start = 20.dp, bottom = 8.dp)
        )
        LazyColumn(
            modifier = Modifier.fillMaxWidth().heightIn(max = 460.dp).padding(horizontal = 12.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            itemsIndexed(notes) { _, note ->
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = if (note == current) Color(0xFF0E7490) else Color(0x1AFFFFFF),
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onPick(note) }
                ) {
                    Text(
                        noteDisplayName(note) + if (note == 60) "  （中央 C）" else "",
                        color = Color.White, fontSize = 15.sp,
                        modifier = Modifier
                            .padding(horizontal = 16.dp, vertical = 12.dp)
                    )
                }
            }
        }
    }
}
