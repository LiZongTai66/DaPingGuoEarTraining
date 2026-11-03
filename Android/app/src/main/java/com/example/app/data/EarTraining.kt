package com.example.app.data

import com.example.app.protocol.Frame
import org.json.JSONArray
import org.json.JSONObject
import kotlin.random.Random

val solfege = listOf("Do", "Re", "Mi", "Fa", "Sol", "La", "Si")
fun randomPhrase(random: Random = Random.Default): List<Int> = List(7) { random.nextInt(7) }
enum class EarPhase { IDLE, PREPARING, LISTENING, INPUT, SUBMITTING, COMPLETE, CANCELLED, ERROR }
data class EarResult(val time:Long,val target:List<Int>,val answer:List<Int>,val listens:Int) {
    init { require(target.size==7 && answer.size==7 && (target+answer).all { it in 0..6 } && listens>=1) }
    val correct:Int get()=target.zip(answer).count { it.first==it.second }
    val accuracy:Int get()=(correct*100.0/7).toInt()
    fun json()=JSONObject().put("time",time).put("target",JSONArray(target)).put("answer",JSONArray(answer)).put("listens",listens)
    fun chartReport()=GameReport(time,7,correct,0,7-correct,0,0,null,null,true,"已完成",emptyList(),"听音记忆")
    companion object { fun parse(o:JSONObject):EarResult {
        fun notes(key:String)=o.getJSONArray(key).let { a -> (0 until a.length()).map { a.getInt(it) } }
        return EarResult(o.getLong("time"),notes("target"),notes("answer"),o.getInt("listens"))
    } }
}
data class EarRound(
    val session:Int=0,val phase:EarPhase=EarPhase.IDLE,val target:List<Int> = emptyList(),
    val answer:List<Int?> = emptyList(),val snapshot:List<Int?> = List(7) { null },
    val listens:Int=0,val time:Long=0,val message:String="准备好，听一段属于你的旋律"
) {
    val active:Boolean get()=phase in listOf(EarPhase.PREPARING,EarPhase.LISTENING,EarPhase.INPUT,EarPhase.SUBMITTING)
    fun accept(f:Frame):EarRound {
        val c=f.cmd.toInt() and 255
        if(((f.a0 shl 8) or f.a1)!=session || !active) return this
        if(c==0xB0) return when(f.a2) {
            0 -> copy(message="正在下发题目，键位已恢复 Do～Si")
            1 -> copy(phase=EarPhase.LISTENING,answer=emptyList(),snapshot=List(7){null},
                listens=listens+if(phase==EarPhase.LISTENING) 0 else 1,message="请听完 7 个音，随后开始作答")
            2 -> copy(phase=EarPhase.INPUT,message="轮到你了：松开琴键后，按顺序输入")
            4 -> copy(phase=EarPhase.CANCELLED,message="本轮已取消，可以重新开始")
            5 -> copy(phase=EarPhase.ERROR,message="等待超时，请重新开始")
            else -> copy(phase=EarPhase.ERROR,message="题目未准备完成，请重新开始")
        }
        if(c==0xB1 && phase==EarPhase.INPUT) {
            val index=(f.a2 shr 3) and 7;val note=f.a2 and 7
            if(f.a2>63 || index>6 || note>6) return copy(phase=EarPhase.ERROR,message="输入数据异常，请重新开始")
            val next=answer.toMutableList();while(next.size<=index)next.add(null);next[index]=note
            return copy(answer=next,message=if(next.size==7) "已输入 7 个音，可撤回修改或提交校验" else "已输入 ${next.size} / 7，可继续或撤回")
        }
        if(c==0xB5 && phase==EarPhase.INPUT && f.a2 in 0..7) {
            val next=answer.take(f.a2).toMutableList();while(next.size<f.a2)next.add(null)
            return copy(answer=next,message="已回退，剩余 ${next.size} / 7 个音")
        }
        if(c==0xB4) return copy(message="请一次按一个键，输入满 7 个后点提交；按住不会重复计数")
        if(c==0xB6 && phase==EarPhase.SUBMITTING) {
            val i=(f.a2 shr 3) and 7;val n=f.a2 and 7
            if(f.a2>63 || i>6 || n>6) return copy(phase=EarPhase.ERROR,message="回传校验失败，请重试")
            return copy(snapshot=snapshot.toMutableList().also { it[i]=n })
        }
        if(c==0xB2 && phase==EarPhase.SUBMITTING) {
            return if(f.a2==7 && snapshot.all { it!=null } && target.size==7 && listens>0)
                copy(phase=EarPhase.COMPLETE,answer=snapshot,message="答案已揭晓")
            else copy(phase=EarPhase.ERROR,message="回传不完整，本轮不计入成绩")
        }
        return this
    }
    fun result():EarResult? = if(phase==EarPhase.COMPLETE) EarResult(time,target,answer.filterNotNull(),listens) else null
}
