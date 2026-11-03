package com.example.app.data

import com.example.app.protocol.Frame

data class DeviceKeymap(val revision: Int, val mode: Int, val notes: List<Int>) {
    val modeLabel: String get() = when(mode) {
        0 -> "低八度 · C3–B3"
        1 -> "正常 · C4–B4"
        2 -> "高八度 · C5–B5"
        else -> "自定义键位"
    }
}

/** Commit only a complete, revision-matched begin/items/end snapshot. */
class DeviceKeymapDecoder {
    private var revision = -1
    private var mode = -1
    private val notes = arrayOfNulls<Int>(7)
    fun reset() { revision=-1; mode=-1; notes.fill(null) }
    fun accept(f: Frame): DeviceKeymap? {
        when(f.cmd.toInt() and 255) {
            0x87 -> {
                reset()
                if(f.a1 in 0..3 && f.a2==7) { revision=f.a0; mode=f.a1 }
            }
            0x88 -> {
                if(revision<0 || f.a0!=revision) return null
                if(f.a1 !in 0..6 || f.a2 !in 21..108) { reset(); return null }
                if(notes[f.a1]!=null && notes[f.a1]!=f.a2) { reset(); return null }
                notes[f.a1]=f.a2
            }
            0x89 -> {
                if(revision<0 || f.a0!=revision) return null
                val candidate=if(f.a1==mode && f.a2==7 && notes.all { it!=null })
                    DeviceKeymap(revision,mode,notes.map { it!! }) else null
                reset()
                if(candidate!=null && candidate.mode in 0..2) {
                    val root=48+12*candidate.mode
                    if(candidate.notes!=listOf(0,2,4,5,7,9,11).map { root+it }) return null
                }
                return candidate
            }
        }
        return null
    }
}
