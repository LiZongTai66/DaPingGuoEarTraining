package com.example.app.data

import android.content.Context
import java.io.File

/** 一条演奏录音（与曲谱同一套事件编码，可直接下载到 FPGA 回放） */
data class Recording(
    val name: String,
    val createdAt: Long,
    val events: List<SongEvent>
)

/**
 * 录音存储：应用私有目录下单个文本文件，每行一条录音：
 * 名称|时间戳|事件hex（每事件 3 字节：dt note flags）
 */
class RecordingStore(context: Context) {
    private val file = File(context.filesDir, "recordings.txt")

    fun load(): List<Recording> {
        if (!file.exists()) return emptyList()
        return file.readLines().mapNotNull { line ->
            val parts = line.split("|")
            if (parts.size != 3) return@mapNotNull null
            val name = parts[0]
            val ts = parts[1].toLongOrNull() ?: return@mapNotNull null
            val hex = parts[2]
            if (hex.length % 6 != 0) return@mapNotNull null
            val events = runCatching { hex.chunked(6).map { chunk ->
                val dt = chunk.substring(0, 2).toInt(16)
                val note = chunk.substring(2, 4).toInt(16)
                val flags = chunk.substring(4, 6).toInt(16)
                SongEvent(dt, note, (flags and 0x80) != 0, flags and 0x7F)
            }
            }.getOrNull() ?: return@mapNotNull null
            if (events.size > 16000 || events.any { it.note != 0 && it.note !in 21..108 }) return@mapNotNull null
            Recording(name, ts, events)
        }.sortedByDescending { it.createdAt }
    }

    fun add(rec: Recording) {
        val lines = file.takeIf { it.exists() }?.readLines()?.toMutableList() ?: mutableListOf()
        lines.add(encode(rec))
        file.writeText(lines.joinToString("\n"))
    }

    fun delete(name: String, createdAt: Long) {
        if (!file.exists()) return
        val kept = file.readLines().filterNot {
            it.startsWith(name.replace("|", " ") + "|" + createdAt + "|")
        }
        file.writeText(kept.joinToString("\n"))
    }

    private fun encode(rec: Recording): String {
        val hex = rec.events.joinToString("") { e ->
            val flags = (if (e.on) 0x80 else 0) or (e.velocity and 0x7F)
            "%02X%02X%02X".format(e.dt5ms and 0xFF, e.note and 0xFF, flags)
        }
        return "${rec.name.replace("|", " ")}|${rec.createdAt}|$hex"
    }
}
