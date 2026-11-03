package com.example.app.ui.home

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bluetooth
import androidx.compose.material.icons.filled.LibraryMusic
import androidx.compose.material.icons.filled.Piano
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material.icons.filled.FiberManualRecord
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.synth.ConnState
import com.example.app.ui.AppViewModel
import com.example.app.ui.Routes

private data class Feature(val title: String, val desc: String, val icon: ImageVector, val route: String)

@Composable
fun HomeScreen(vm: AppViewModel, onOpen: (String) -> Unit, onPiano: () -> Unit) {
    val conn by vm.connState.collectAsState()
    val devName by vm.deviceName.collectAsState()

    val features = listOf(
        Feature("听音记忆训练", "听旋律、复现、撤回修改与成长记录", Icons.Filled.Piano, Routes.EAR),
        Feature("音游练习分析", "实时成绩、节奏偏差与分段建议", Icons.Filled.LibraryMusic, Routes.GAME),
        Feature("蓝牙连接", "连接 ESP32-S3 BLE / 模拟设备", Icons.Filled.Bluetooth, Routes.CONNECT),
        Feature("在线曲谱", "HTTPS 下载曲谱并下发设备", Icons.Filled.LibraryMusic, Routes.SONGS),
        Feature("键位自定义", "设置 7 个实体琴键的音符", Icons.Filled.Tune, Routes.KEYMAP),
        Feature("演奏录音", "接收实体琴音符事件并保存", Icons.Filled.FiberManualRecord, Routes.RECORD)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(listOf(Color(0xFF1a1a2e), Color(0xFF16213e), Color(0xFF0f3460)))
            )
            .systemBarsPadding()
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {
        Spacer(Modifier.height(32.dp))
        Text("大苹果", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color.White)
        Text("你的随身电子琴助手 · ESP32-S3", fontSize = 14.sp, color = Color(0xFFBBBBBB), modifier = Modifier.padding(top = 4.dp))

        Spacer(Modifier.height(16.dp))
        ConnectionChip(conn = conn, deviceName = devName, onClick = { onOpen(Routes.CONNECT) })

        Spacer(Modifier.height(24.dp))
        features.forEach { f ->
            FeatureCard(f.title, f.desc, f.icon) { onOpen(f.route) }
        }

        Spacer(Modifier.height(16.dp))
        Button(
            onClick = onPiano,
            modifier = Modifier.fillMaxWidth().height(56.dp),
            shape = RoundedCornerShape(16.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF00B4D8))
        ) {
            Icon(Icons.Filled.Piano, contentDescription = null, tint = Color(0xFF001219))
            Spacer(Modifier.width(10.dp))
            Text("进入演奏台", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF001219))
        }
        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun ConnectionChip(conn: ConnState, deviceName: String, onClick: () -> Unit) {
    val (dot, text) = when (conn) {
        ConnState.CONNECTED -> Color(0xFF4ADE80) to ("已连接 · $deviceName")
        ConnState.CONNECTING -> Color(0xFFFACC15) to "连接中…"
        ConnState.DISCONNECTED -> Color(0xFFF87171) to "未连接（点击连接）"
    }
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = Color(0x22FFFFFF),
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick)
    ) {
        Row(
            Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(Modifier.size(10.dp).background(dot, RoundedCornerShape(5.dp)))
            Spacer(Modifier.width(10.dp))
            Text(text, color = Color.White, fontSize = 14.sp, modifier = Modifier.weight(1f))
            Text("›", color = Color(0xAAFFFFFF), fontSize = 20.sp)
        }
    }
}

@Composable
private fun FeatureCard(title: String, desc: String, icon: ImageVector, onClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp).clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0x33FFFFFF)),
        elevation = CardDefaults.cardElevation(0.dp)
    ) {
        Row(
            Modifier.fillMaxWidth().padding(18.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = Color(0xFF48CAE4), modifier = Modifier.size(26.dp))
            Spacer(Modifier.width(16.dp))
            Column(Modifier.weight(1f)) {
                Text(title, fontSize = 18.sp, fontWeight = FontWeight.SemiBold, color = Color.White)
                Text(desc, fontSize = 13.sp, color = Color(0xCCFFFFFF), modifier = Modifier.padding(top = 3.dp))
            }
            Text("▶", fontSize = 16.sp, color = Color(0x88FFFFFF))
        }
    }
}
