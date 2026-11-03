package com.example.app.data

enum class TrendMetric(val title: String, val unit: String, val lowerIsBetter: Boolean = false) {
    ACCURACY("命中率", "%"), COMBO("最高连击", "次"), TIMING("节奏偏差", "ms", true);
    fun value(r: GameReport): Double? = when(this) {
        ACCURACY -> 100.0 * (r.perfect + r.good) / r.total.coerceAtLeast(1)
        COMBO -> r.maxCombo.toDouble()
        TIMING -> r.meanAbsOffset?.takeIf { it.isFinite() && it >= 0 }
    }
}

data class TrendEntry(val report: GameReport, val number: Int, val value: Double)

/** The input is newest-first as stored by AppViewModel. Missing timing never becomes zero. */
fun validPracticeReports(history: List<GameReport>, label: String?, limit: Int): List<GameReport> =
    history.filter { it.complete && it.total > 0 && (label == null || it.label == label) }
        .sortedByDescending { it.time }.take(limit.coerceIn(1,20)).asReversed()

fun trendEntries(reports: List<GameReport>, metric: TrendMetric): List<TrendEntry> =
    reports.mapIndexedNotNull { index, report -> metric.value(report)?.let { TrendEntry(report,index+1,it) } }

/** UI-only fixtures; never sent to FPGA or written to history. */
fun dashboardExamples(): List<GameReport> {
    val examples=listOf(64,71,69,78,83,81,89,94)
    val epoch=1760000000000L
    return examples.mapIndexed { i,hits ->
        val perfect=hits*(65+i*3)/100
        val frontHits=hits/3+2;val middleHits=hits/3-3;val lastHits=hits-frontHits-middleHits
        val sections=listOf(33 to frontHits,33 to middleHits,34 to lastHits).mapIndexed { n,(total,hit) ->
            val errors=total-hit
            GameSection(listOf("前段","中段","后段")[n],total,hit,errors*2/3,errors-errors*2/3)
        }
        GameReport(epoch+i*240000L,100,perfect,hits-perfect,sections.sumOf { it.misses },sections.sumOf { it.bad },12+i*5,
            45.0-i*5,95.0-i*9,true,"已完成",sections,"示例练习")
    }.asReversed()
}
