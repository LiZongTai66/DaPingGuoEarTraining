package com.example.app

import com.example.app.data.*
import org.junit.Assert.*
import org.junit.Test

class GameTrendsTest {
    private fun report(t:Long,label:String="A",complete:Boolean=true,offset:Double?=10.0)=
        GameReport(t,100,70,10,12,8,25,-5.0,offset,complete,"已完成",emptyList(),label)
    @Test fun filtersBeforeLimitAndReturnsChronologicalOrder() {
        val history=listOf(report(7,"B"),report(6),report(5,complete=false),report(4),report(3,"B"),report(2),report(1))
        assertEquals(listOf(2L,4L,6L),validPracticeReports(history,"A",3).map { it.time })
        assertEquals(listOf(4L,6L,7L),validPracticeReports(history,null,3).map { it.time })
    }
    @Test fun zeroTargetsAndInterruptedRoundsNotIncluded() {
        val history=listOf(report(3).copy(total=0),report(2,complete=false),report(1))
        assertEquals(listOf(1L),validPracticeReports(history,null,20).map { it.time })
        assertEquals(emptyList<GameReport>(),validPracticeReports(history,"missing",5))
    }
    @Test fun missingTimingIsNotZeroAndSessionNumbersAreRetained() {
        val entries=trendEntries(listOf(report(1),report(2,offset=null),report(3,offset=0.0)),TrendMetric.TIMING)
        assertEquals(listOf(1,3),entries.map { it.number })
        assertEquals(listOf(10.0,0.0),entries.map { it.value })
        assertEquals(80.0,TrendMetric.ACCURACY.value(report(1))!!,0.01)
        assertEquals(25.0,TrendMetric.COMBO.value(report(1))!!,0.01)
    }
    @Test fun oldHistoryWithoutLabelLoadsAndNewLabelRoundTrips() {
        val old=report(1).json();old.remove("label")
        assertEquals("",GameReport.fromJson(old).label)
        val current=report(2,"两只老虎 · 普通")
        assertEquals(current,GameReport.fromJson(current.json()))
    }
    @Test fun examplesAreConsistentAndSeparateFromStorage() {
        val examples=dashboardExamples()
        assertEquals(8,examples.size)
        examples.forEach { r ->
            assertEquals(100,r.perfect+r.good+r.misses+r.bad)
            assertEquals(r.total,r.sections.sumOf { it.total })
            assertEquals(r.misses,r.sections.sumOf { it.misses })
            assertEquals(r.bad,r.sections.sumOf { it.bad })
            assertEquals("示例练习",r.label)
        }
    }
}
