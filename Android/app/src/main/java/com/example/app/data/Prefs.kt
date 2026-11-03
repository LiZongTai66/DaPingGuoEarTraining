package com.example.app.data

import android.content.Context

/** 轻量持久化：自定义打击垫键位、上次使用的音色/音量 */
class Prefs(context: Context) {
    private val sp = context.getSharedPreferences("gw2a_synth", Context.MODE_PRIVATE)

    /** 10 个自定义打击垫 → MIDI 音符，默认 C4..E5 */
    fun loadKeymap(): IntArray {
        val def = IntArray(PAD_COUNT) { 60 + it }
        val raw = sp.getString(KEY_KEYMAP, null) ?: return def
        val parts = raw.split(",").mapNotNull { it.toIntOrNull() }
        return if (parts.size == PAD_COUNT && parts.all { it in 21..108 }) parts.toIntArray() else def
    }

    fun saveKeymap(notes: IntArray) {
        sp.edit().putString(KEY_KEYMAP, notes.joinToString(",")).apply()
    }

    fun loadPhysicalKeymap(): IntArray {
        val defaults = intArrayOf(60, 62, 64, 65, 67, 69, 71)
        val values = sp.getString("physical_keymap", "")!!.split(",").mapNotNull { it.toIntOrNull() }
        return if (values.size == 7 && values.all { it in 21..108 }) values.toIntArray() else defaults
    }
    fun savePhysicalKeymap(notes: IntArray) { sp.edit().putString("physical_keymap", notes.joinToString(",")).apply() }

    var voice: Int
        get() = sp.getInt(KEY_VOICE, 0)
        set(v) = sp.edit().putInt(KEY_VOICE, v.coerceIn(0, 3)).apply()

    var volume: Int
        get() = sp.getInt(KEY_VOLUME, 80)
        set(v) = sp.edit().putInt(KEY_VOLUME, v.coerceIn(0, 100)).apply()

    companion object {
        const val PAD_COUNT = 10
        private const val KEY_KEYMAP = "keymap"
        private const val KEY_VOICE = "voice"
        private const val KEY_VOLUME = "volume"
    }
}
