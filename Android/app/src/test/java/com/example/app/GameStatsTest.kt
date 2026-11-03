package com.example.app

import com.example.app.data.*
import com.example.app.protocol.Frame
import com.example.app.protocol.FrameDecoder
import org.junit.Assert.*
import org.junit.Test

class GameStatsTest {
    @Test fun fpgaUartCaptureDecodedAcrossBleFragments() {
        val text=javaClass.getResource("/game-uart.hex")!!.readText()
        val bytes=text.trim().split(Regex("\\s+")).map { it.toInt(16).toByte() }.toByteArray()
        val decoder=FrameDecoder();var round=GameRound();val reports=mutableListOf<GameReport>()
        var position=0;var size=1
        while(position<bytes.size) {
            val end=minOf(bytes.size,position+size)
            decoder.feed(bytes.copyOfRange(position,end)).forEach { raw ->
                val f=Frame.from(raw)
                if((f.cmd.toInt() and 255) in 0xA0..0xA5) {
                    val old=round;round=round.accept(f,123)
                    if(old.running && !round.running) reports+=round.report()
                }
            }
            position=end;size=if(size==19) 1 else size+1
        }
        assertEquals(3,reports.size)
        assertTrue(reports[0].complete);assertEquals(6,reports[0].total)
        assertEquals(3,reports[0].misses);assertEquals(1,reports[0].bad)
        assertTrue(reports[1].complete);assertEquals(70,reports[1].maxCombo)
        assertEquals(100,reports[1].accuracy);assertFalse(reports[2].complete)
        assertEquals("已退出",reports[2].status)
    }
    private fun frame(c:Int,index:Int,v:Int)=Frame(c.toByte(),index shr 8,index and 255,v)
    private fun start()=GameRound().accept(frame(0xA0,1,1),123)
    @Test fun middleMissesAndUncappedCombo() {
        var r=start()
        for(i in 1..240) r=r.accept(frame(if(i in 81..160) 0xA3 else 0xA1,i,if(i in 81..160) 255 else 75),0)
        r=r.accept(frame(0xA5,240,0),0)
        val report=r.report()
        assertTrue(report.complete);assertEquals(80,report.maxCombo);assertEquals(80,report.misses)
        assertEquals(0.0,report.meanOffset!!,0.01);assertTrue(report.advice.contains("中段"))
        assertEquals(listOf(80,80,80),report.sections.map { it.total })
        assertEquals(report,GameReport.fromJson(report.json()))
    }
    @Test fun noteLossCannotBecomeMissOrValidAdvice() {
        var r=start().accept(frame(0xA1,1,75),0).accept(frame(0xA2,3,100),0)
        r=r.accept(frame(0xA5,3,0),0)
        assertFalse(r.report().complete);assertEquals(0,r.report().misses)
        assertTrue(r.report().advice.contains("记录不完整"))
    }
    @Test fun droppedFinalEventDetectedByEndCount() {
        val r=start().accept(frame(0xA1,1,75),0).accept(frame(0xA5,2,0),0)
        assertFalse(r.report().complete)
    }
    @Test fun disconnectAbortOverflowAndMissingStart() {
        assertFalse(start().interrupted().report().complete)
        assertFalse(start().accept(frame(0xA5,0,1),0).report().complete)
        assertFalse(start().accept(frame(0xAF,0,1),0).accept(frame(0xA5,0,0),0).report().complete)
        assertFalse(GameRound().accept(frame(0xA1,1,75),0).started)
    }
    @Test fun offsetsAndBadSeparateFromMiss() {
        val r=start().accept(frame(0xA2,1,0),0).accept(frame(0xA1,2,100),0)
            .accept(frame(0xA4,3,75),0).accept(frame(0xA3,4,255),0).accept(frame(0xA5,4,0),0)
        val report=r.report()
        assertTrue(report.complete);assertEquals(-50.0,report.meanOffset!!,0.01)
        assertEquals(100.0,report.meanAbsOffset!!,0.01);assertEquals(1,report.bad);assertEquals(1,report.misses)
        assertEquals(2,report.maxCombo)
    }
    @Test fun invalidTimingDuplicateAndProtocolVersion() {
        assertFalse(start().accept(frame(0xA1,1,255),0).valid)
        val r=start().accept(frame(0xA1,1,75),0).accept(frame(0xA1,1,75),0)
        assertFalse(r.valid);assertEquals(1,r.events.size)
        assertFalse(GameRound().accept(frame(0xA0,1,2),0).valid)
    }
}
