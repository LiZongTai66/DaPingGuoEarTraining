package com.example.app

import com.example.app.data.*
import com.example.app.protocol.Frame
import com.example.app.protocol.FrameDecoder
import org.junit.Assert.*
import org.junit.Test
import kotlin.random.Random

class EarTrainingTest {
    @Test fun actualFpgaUartCaptureMatchesAppAcrossFragmentsUndoAndReplay() {
        val bytes=javaClass.getResource("/ear-uart.hex")!!.readText().trim().split(Regex("\\s+")).map { it.toInt(16).toByte() }.toByteArray()
        val decoder=FrameDecoder();var round=EarRound(123,EarPhase.PREPARING,target,time=100)
        var pos=0;var chunk=1
        while(pos<bytes.size) {
            val end=minOf(bytes.size,pos+chunk)
            decoder.feed(bytes.copyOfRange(pos,end)).forEach { raw ->
                val f=Frame.from(raw)
                if((f.cmd.toInt() and 255)==0x81 && f.a0==0x46) round=round.copy(phase=EarPhase.SUBMITTING)
                round=round.accept(f)
            }
            pos=end;chunk=if(chunk==19) 1 else chunk+1
        }
        val result=round.result()!!
        assertEquals(target,result.answer);assertEquals(100,result.accuracy);assertEquals(2,result.listens)
    }
    private fun f(cmd:Int,value:Int,sid:Int=123)=Frame(cmd.toByte(),sid shr 8,sid and 255,value)
    private val target=listOf(0,0,2,4,6,5,1)
    private fun initial()=EarRound(123,EarPhase.PREPARING,target,time=100).accept(f(0xB0,1)).accept(f(0xB0,2))
    @Test fun randomNotesAllowDuplicatesAndCoverAllSeven() {
        val random=Random(1);val phrases=List(100){randomPhrase(random)}
        assertTrue(phrases.all { it.size==7 && it.all { n->n in 0..6 } })
        assertEquals((0..6).toSet(),phrases.flatten().toSet())
        assertTrue(phrases.any { it.zipWithNext().any { pair->pair.first==pair.second } })
    }
    @Test fun inputsShownImmediatelyAndUndoRemovesExactlyOneEach() {
        var r=initial()
        for(i in 0..3)r=r.accept(f(0xB1,(i shl 3) or target[i]))
        assertEquals(target.take(4),r.answer)
        r=r.accept(f(0xB5,3));r=r.accept(f(0xB5,2))
        assertEquals(target.take(2),r.answer)
        r=r.accept(f(0xB1,(2 shl 3) or 6));assertEquals(listOf(0,0,6),r.answer)
    }
    @Test fun replayClearsInputsAndCountsListensWithoutDuplicateIncrement() {
        val r=initial().accept(f(0xB1,0)).copy(phase=EarPhase.PREPARING)
            .accept(f(0xB0,1)).accept(f(0xB0,1))
        assertTrue(r.answer.isEmpty());assertEquals(2,r.listens)
        assertEquals(EarPhase.LISTENING,r.phase)
    }
    @Test fun targetNotRevealedUntilCompleteSnapshotAndExplicitSubmit() {
        var r=initial()
        for(i in 0..6)r=r.accept(f(0xB1,(i shl 3) or target[i]))
        assertNull(r.result());assertEquals(EarPhase.INPUT,r.phase)
        r=r.copy(phase=EarPhase.SUBMITTING)
        for(i in 0..6)r=r.accept(f(0xB6,(i shl 3) or target[i]))
        r=r.accept(f(0xB2,7));val result=r.result()!!
        assertEquals(7,result.correct);assertEquals(100,result.accuracy)
        assertEquals(result,EarResult.parse(result.json()))
    }
    @Test fun missingRealtimeInputRecoveredByFinalSnapshot() {
        var r=initial().accept(f(0xB1,(2 shl 3) or 2))
        assertEquals(listOf(null,null,2),r.answer)
        r=r.copy(phase=EarPhase.SUBMITTING)
        for(i in 0..6)r=r.accept(f(0xB6,(i shl 3) or target[i]))
        assertEquals(100,r.accept(f(0xB2,7)).result()!!.accuracy)
    }
    @Test fun staleSessionsAndIncompleteSnapshotsNeverBecomeScores() {
        assertEquals(initial(),initial().accept(f(0xB1,0,999)))
        assertEquals(EarPhase.ERROR,initial().copy(phase=EarPhase.SUBMITTING).accept(f(0xB2,7)).phase)
        assertNull(initial().accept(f(0xB0,5)).result())
    }
    @Test fun gradeUsesPositionNotNoteSetAndStoresListenCount() {
        val result=EarResult(1,target,target.reversed(),3)
        assertEquals(target.indices.count { target[it]==target.reversed()[it] },result.correct)
        assertEquals(3,EarResult.parse(result.json()).listens)
    }
}
