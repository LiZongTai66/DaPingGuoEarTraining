package com.example.app.data

import com.example.app.protocol.Frame
import org.json.JSONArray
import org.json.JSONObject

data class GameHit(val index: Int, val judgement: Int, val offsetMs: Int?)
data class GameSection(val name: String, val total: Int, val hits: Int, val misses: Int, val bad: Int) {
    val errorRate: Double get() = if (total == 0) 0.0 else (misses + bad).toDouble() / total
}
data class GameReport(
    val time: Long, val total: Int, val perfect: Int, val good: Int, val misses: Int, val bad: Int,
    val maxCombo: Int, val meanOffset: Double?, val meanAbsOffset: Double?,
    val complete: Boolean, val status: String, val sections: List<GameSection>, val label: String = ""
) {
    val accuracy: Int get() = if (total == 0) 0 else (100.0 * (perfect + good) / total).toInt()
    val advice: String get() {
        if (!complete) return "记录不完整，请先连接 App，再从 TJC 重新开始一局；本次不生成整曲练习建议。"
        if (total < 6) return "本局目标音符较少，建议完成更长的一局后再分析薄弱段落。"
        val worst = sections.filter { it.total > 0 }.maxByOrNull { it.errorRate }!!
        val segment = if (worst.errorRate == 0.0) "本局没有漏按或错按，可以尝试提高节奏稳定性。"
        else "${worst.name}漏按及错按率最高（${(worst.errorRate * 100).toInt()}%），建议重点练习这一段。"
        val timing = when {
            meanOffset == null -> ""
            meanOffset > 30 -> " 命中按键整体偏晚，可适当提前准备。"
            meanOffset < -30 -> " 命中按键整体偏早，可跟稳节拍再按下。"
            else -> ""
        }
        return segment + timing
    }
    fun json(): JSONObject = JSONObject().put("time",time).put("total",total).put("perfect",perfect)
        .put("good",good).put("misses",misses).put("bad",bad).put("maxCombo",maxCombo)
        .put("meanOffset",meanOffset ?: JSONObject.NULL).put("meanAbsOffset",meanAbsOffset ?: JSONObject.NULL)
        .put("complete",complete).put("status",status).put("label",label).put("sections",JSONArray().also { a ->
            sections.forEach { a.put(JSONObject().put("name",it.name).put("total",it.total)
                .put("hits",it.hits).put("misses",it.misses).put("bad",it.bad)) }
        })
    companion object {
        fun fromJson(o: JSONObject): GameReport {
            val a=o.getJSONArray("sections")
            return GameReport(o.getLong("time"),o.getInt("total"),o.getInt("perfect"),o.getInt("good"),
                o.getInt("misses"),o.getInt("bad"),o.getInt("maxCombo"),
                if(o.isNull("meanOffset")) null else o.getDouble("meanOffset"),
                if(o.isNull("meanAbsOffset")) null else o.getDouble("meanAbsOffset"),
                o.getBoolean("complete"),o.getString("status"),(0 until a.length()).map { i ->
                    val x=a.getJSONObject(i);GameSection(x.getString("name"),x.getInt("total"),x.getInt("hits"),x.getInt("misses"),x.getInt("bad"))
                },o.optString("label", ""))
        }
    }
}

/** Timing is relative to FPGA judgement center, NOT Bluetooth arrival time. */
data class GameRound(
    val session: Int=0, val running: Boolean=false, val started: Boolean=false,
    val events: List<GameHit> = emptyList(), val valid: Boolean=true,
    val targets: Int=0, val status: String="等待 TJC 开始游戏", val time: Long=0, val label: String=""
) {
    val combo: Int get() = events.asReversed().takeWhile { it.judgement <= 2 }.size
    fun report(): GameReport {
        val total=maxOf(targets,events.maxOfOrNull { it.index } ?: 0)
        val ordered=events.sortedBy { it.index }
        var streak=0;var maximum=0;var previous=0
        ordered.forEach { e ->
            if(e.index!=previous+1) streak=0
            streak=if(e.judgement<=2) streak+1 else 0
            maximum=maxOf(maximum,streak);previous=e.index
        }
        val offsets=events.filter { it.judgement<=2 }.mapNotNull { it.offsetMs }
        val sections=listOf("前段","中段","后段").mapIndexed { section,name ->
            val start=total*section/3+1;val end=total*(section+1)/3
            val es=events.filter { it.index in start..end }
            GameSection(name,maxOf(0,end-start+1),es.count { it.judgement<=2 },es.count { it.judgement==3 },es.count { it.judgement==4 })
        }
        return GameReport(time,total,events.count { it.judgement==1 },events.count { it.judgement==2 },
            events.count { it.judgement==3 },events.count { it.judgement==4 },maximum,
            offsets.takeIf { it.isNotEmpty() }?.average(),offsets.takeIf { it.isNotEmpty() }?.map { kotlin.math.abs(it) }?.average(),
            started && !running && valid && status=="已完成" && total==events.size,
            status,sections,label)
    }
    fun accept(f: Frame, now: Long): GameRound {
        val c=f.cmd.toInt() and 255;val index=(f.a0 shl 8) or f.a1
        if(c==0xA0) return GameRound(index,true,true,valid=f.a2==1,status="游戏进行中",time=now)
        if(c==0xAF) return copy(valid=false,status=if(running) "游戏进行中（数据缺失）" else status)
        if(c in 0xA1..0xA4) {
            if(!running || !started) return copy(valid=false,status="未收到开局，请从 TJC 重新开始")
            if(index==events.lastOrNull()?.index) return copy(valid=false)
            val sequential=index==(events.lastOrNull()?.index ?: 0)+1
            val timingOk=if(c==0xA3) f.a2==255 else f.a2 in 0..149
            if(index==0 || events.size>=10000 || index<=(events.lastOrNull()?.index ?: 0)) return copy(valid=false)
            val hit=GameHit(index,c-0xA0,if(c in 0xA1..0xA2 && timingOk) f.a2*2-150 else null)
            return copy(events=events+hit,targets=index,valid=valid && sequential && timingOk)
        }
        if(c==0xA5 && running) return copy(running=false,targets=index,
            valid=valid && index==events.size,status=if(f.a2==0) "已完成" else "已退出")
        return this
    }
    fun interrupted() = if(running) copy(running=false,valid=false,status="连接中断") else this
}
