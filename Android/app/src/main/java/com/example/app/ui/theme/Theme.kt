package com.example.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// 应用固定深色科技风（首页渐变背景）
private val DarkColors = darkColorScheme(
    primary = Color(0xFF00B4D8),
    onPrimary = Color(0xFF001219),
    secondary = Color(0xFF48CAE4),
    background = Color(0xFF101525),
    surface = Color(0xFF1B2238),
    onBackground = Color(0xFFE6EAF2),
    onSurface = Color(0xFFE6EAF2)
)

@Composable
fun GW2A_Synth_Theme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkColors,
        content = content
    )
}
