package com.example.app.ui.piano

import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.StopCircle
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.data.noteDisplayName
import com.example.app.synth.ConnState
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen
import kotlin.math.roundToInt

@Composable
fun PianoScreen(vm: AppViewModel, onBack: () -> Unit) {
    val conn by vm.connState.collectAsState()
    val voice by vm.voice.collectAsState()
    val voiceSwitching by vm.voiceSwitching.collectAsState()
    val voiceStatus by vm.voiceStatus.collectAsState()
    val volume by vm.volume.collectAsState()
    val keymap by vm.keymap.collectAsState()
    val recording by vm.isRecording.collectAsState()
    val recCount by vm.recordedEventCount.collectAsState()
    val busy by vm.busy.collectAsState()
    val playing by vm.playingTitle.collectAsState()

    val pressed = remember { mutableStateListOf<Int>() }
    DisposableEffect(Unit) { onDispose { if (conn == ConnState.CONNECTED) vm.allOff() } }
    fun down(note: Int) { if (!pressed.contains(note)) pressed.add(note); vm.noteOn(note) }
    fun up(note: Int) { pressed.remove(note); vm.noteOff(note) }

    AppScreen(
        title = "演奏台",
        vm = vm,
        onBack = onBack,
        actions = {
            TextButton(onClick = { vm.allOff(); pressed.clear() }) {
                Text("全部静音", color = Color(0xFFF87171))
            }
        }
    ) { pad ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(pad)
                .padding(horizontal = 14.dp)
        ) {
            if (conn != ConnState.CONNECTED) {
                WarningBar("未连接设备：可先到「蓝牙连接」页连接模拟设备")
                Spacer(Modifier.height(8.dp))
            }

            // 音色
            Text("音色", color = Color(0xFFB8C0D0), fontSize = 13.sp)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                vm.voiceNames.forEachIndexed { i, name ->
                    FilterChip(
                        selected = voice == i,
                        enabled = !voiceSwitching,
                        onClick = { vm.setVoice(i) },
                        label = { Text(name) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = Color(0xFF00B4D8),
                            selectedLabelColor = Color(0xFF001219)
                        )
                    )
                }
            }

            Text(voiceStatus,color=Color(0xFF80CBC4),fontSize=11.sp)

            // 音量
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("音量", color = Color(0xFFB8C0D0), fontSize = 13.sp, modifier = Modifier.width(40.dp))
                Slider(
                    value = volume.toFloat(),
                    onValueChange = { vm.setVolume(it.roundToInt()) },
                    valueRange = 0f..100f,
                    modifier = Modifier.weight(1f)
                )
                Text("$volume", color = Color.White, fontSize = 13.sp, modifier = Modifier.width(34.dp))
            }

            // 录音条
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 4.dp)) {
                Button(
                    onClick = { if (recording) vm.stopRecordingAndNotify() else vm.startRecording() },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (recording) Color(0xFFB91C1C) else Color(0xFF00B4D8)
                    ),
                    modifier = Modifier.height(40.dp)
                ) {
                    Text(
                        if (recording) "■ 停止录音（$recCount）" else "● 开始录音",
                        color = if (recording) Color.White else Color(0xFF001219),
                        fontWeight = FontWeight.Bold
                    )
                }
                if (recording) {
                    Spacer(Modifier.width(10.dp))
                    Text("录制中：音符事件（非音频）", color = Color(0xFFFCA5A5), fontSize = 12.sp)
                }
            }

            // 自定义打击垫（2×5）
            Text("自定义打击垫（在「键位自定义」中改键）", color = Color(0xFFB8C0D0), fontSize = 12.sp)
            Spacer(Modifier.height(6.dp))
            for (row in 0 until 2) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 8.dp)) {
                    for (col in 0 until 5) {
                        val idx = row * 5 + col
                        val note = keymap[idx]
                        Pad(
                            label = "P${idx + 1}\n${noteDisplayName(note)}",
                            active = pressed.contains(note),
                            modifier = Modifier.weight(1f),
                            onDown = { down(note) },
                            onUp = { up(note) }
                        )
                    }
                }
            }

            Spacer(Modifier.height(4.dp))

            // 回放状态
            if (playing != null || busy) {
                Surface(shape = RoundedCornerShape(10.dp), color = Color(0x2200B4D8), modifier = Modifier.fillMaxWidth()) {
                    Row(
                        Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            if (busy) "正在下载曲谱到 FPGA…" else "正在回放：$playing",
                            color = Color.White, fontSize = 13.sp, modifier = Modifier.weight(1f)
                        )
                        if (playing != null) {
                            IconButton(onClick = { vm.stopPlayback() }) {
                                Icon(Icons.Filled.StopCircle, "停止", tint = Color(0xFFF87171))
                            }
                        }
                    }
                }
                Spacer(Modifier.height(6.dp))
            }

            // 钢琴键盘（C4..B5，横向滚动，多指）
            Text("钢琴键盘（C4 – B5）", color = Color(0xFFB8C0D0), fontSize = 12.sp)
            Spacer(Modifier.height(4.dp))
            PianoKeyboard(
                startNote = 60,
                octaves = 2,
                pressed = pressed,
                onDown = ::down,
                onUp = ::up,
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@Composable
private fun WarningBar(text: String) {
    Surface(shape = RoundedCornerShape(8.dp), color = Color(0x33FACC15), modifier = Modifier.fillMaxWidth()) {
        Text(text, color = Color(0xFFFDE68A), fontSize = 12.sp, modifier = Modifier.padding(10.dp))
    }
}

@Composable
private fun Pad(
    label: String,
    active: Boolean,
    modifier: Modifier = Modifier,
    onDown: () -> Unit,
    onUp: () -> Unit
) {
    Box(
        modifier
            .height(64.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(if (active) Color(0xFF00B4D8) else Color(0x33FFFFFF))
            .pressNote(onDown, onUp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            label,
            color = if (active) Color(0xFF001219) else Color.White,
            fontSize = 13.sp,
            fontWeight = FontWeight.SemiBold
        )
    }
}

/** 按下/抬起手势：多指独立，每个触点触发一次音符开关 */
@Composable
private fun Modifier.pressNote(onDown: () -> Unit, onUp: () -> Unit): Modifier {
    val latestDown by rememberUpdatedState(onDown)
    val latestUp by rememberUpdatedState(onUp)
    return this.pointerInput(Unit) {
        awaitEachGesture {
            val down = awaitFirstDown(requireUnconsumed = false)
            val pointerId = down.id
            latestDown()
            try {
                while (true) {
                    val change = awaitPointerEvent().changes.firstOrNull { it.id == pointerId } ?: break
                    if (!change.pressed) break
                }
            } finally { latestUp() }
        }
    }

}

@Composable
private fun PianoKeyboard(
    startNote: Int,         // 必须是 C
    octaves: Int,
    pressed: List<Int>,
    onDown: (Int) -> Unit,
    onUp: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    val whiteCount = octaves * 7
    val whiteWidth = 54.dp
    val blackWidth = 34.dp
    val whiteOffsets = intArrayOf(0, 2, 4, 5, 7, 9, 11)
    // 每个八度里黑键位于“第几号白键之后”（白键下标：C0 D1 E2 F3 G4 A5 B6）
    val blackAfter = intArrayOf(0, 1, 3, 4, 5)
    val blackSemi = intArrayOf(1, 3, 6, 8, 10)

    Box(
        modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
    ) {
        Box(
            Modifier
                .width(whiteWidth * whiteCount)
                .fillMaxHeight()
                .clip(RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp))
                .background(Color(0xFF0E1424))
        ) {
            // 白键
            Row(Modifier.fillMaxSize()) {
                for (i in 0 until whiteCount) {
                    val oct = i / 7
                    val note = startNote + oct * 12 + whiteOffsets[i % 7]
                    Box(
                        Modifier
                            .width(whiteWidth)
                            .fillMaxHeight()
                            .padding(1.dp)
                            .clip(RoundedCornerShape(bottomStart = 6.dp, bottomEnd = 6.dp))
                            .background(if (pressed.contains(note)) Color(0xFF7DD3FC) else Color(0xFFF1F5F9))
                            .pressNote({ onDown(note) }, { onUp(note) }),
                        contentAlignment = Alignment.BottomCenter
                    ) {
                        Text(
                            noteDisplayName(note),
                            color = Color(0xFF64748B),
                            fontSize = 9.sp,
                            modifier = Modifier.padding(bottom = 6.dp)
                        )
                    }
                }
            }
            // 黑键（绝对定位在相邻白键接缝处）
            for (i in 0 until whiteCount) {
                val oct = i / 7
                val posInOct = i % 7
                if (posInOct in blackAfter) {
                    val k = blackAfter.indexOf(posInOct)
                    val note = startNote + oct * 12 + blackSemi[k]
                    val left = whiteWidth * (i + 1) - blackWidth / 2
                    Box(
                        Modifier
                            .offset { IntOffset(left.roundToPx(), 0) }
                            .width(blackWidth)
                            .fillMaxHeight(0.62f)
                            .clip(RoundedCornerShape(bottomStart = 6.dp, bottomEnd = 6.dp))
                            .background(if (pressed.contains(note)) Color(0xFF0EA5E9) else Color(0xFF111827))
                            .pressNote({ onDown(note) }, { onUp(note) })
                    )
                }
            }
        }
    }
}
