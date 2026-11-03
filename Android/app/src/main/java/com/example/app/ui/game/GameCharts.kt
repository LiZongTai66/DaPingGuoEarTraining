package com.example.app.ui.game

import android.graphics.Paint
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.data.*
import kotlin.math.abs
import kotlin.math.ceil
import kotlin.math.max
import kotlin.math.min

private fun DrawScope.chartText(text: String,x: Float,y: Float,color: Color=Muted,center: Boolean=false) {
    val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply {
        this.color=color.toArgb();textSize=10.sp.toPx()
        textAlign=if(center) Paint.Align.CENTER else Paint.Align.LEFT
    }
    drawContext.canvas.nativeCanvas.drawText(text,x,y,paint)
}

private fun ceilingFor(metric: TrendMetric, maxValue: Double): Float {
    if(metric==TrendMetric.ACCURACY) return 100f
    val step=when { maxValue<=5 -> 1.0;maxValue<=20 -> 5.0;maxValue<=100 -> 20.0;else -> ceil(maxValue/5/10)*10 }
    return max(step,ceil(maxValue/step)*step).toFloat()
}

@Composable
internal fun TrendChart(reports: List<GameReport>,metric: TrendMetric) {
    val entries=remember(reports,metric) { trendEntries(reports,metric) }
    var selected by remember(entries) { mutableIntStateOf((entries.size-1).coerceAtLeast(0)) }
    val highlight=entries.getOrNull(selected)
    val tint=when(metric) { TrendMetric.ACCURACY -> Cyan;TrendMetric.COMBO -> Purple;TrendMetric.TIMING -> Green }
    val ceiling=ceilingFor(metric,entries.maxOfOrNull { it.value } ?: 0.0)
    val description=if(entries.isEmpty()) "暂无${metric.title}数据" else "${metric.title}折线图，${entries.size}次记录。最新${valueText(entries.last().value,metric)}"
    Box(Modifier.fillMaxWidth().height(206.dp)) {
        Canvas(Modifier.fillMaxSize().semantics { contentDescription=description }.pointerInput(entries) {
            detectTapGestures { tap ->
                if(entries.isNotEmpty()) {
                    val left=42.dp.toPx();val width=(size.width-left-28.dp.toPx()).coerceAtLeast(1f)
                    fun x(e: TrendEntry)=left+width*if(reports.size<=1) .5f else (e.number-1).toFloat()/(reports.size-1)
                    selected=entries.indices.minByOrNull { abs(x(entries[it])-tap.x) } ?: 0
                }
            }
        }) {
            val left=42.dp.toPx();val top=18.dp.toPx();val bottom=size.height-30.dp.toPx()
            val width=(size.width-left-28.dp.toPx()).coerceAtLeast(1f);val height=(bottom-top).coerceAtLeast(1f)
            for(i in 0..4) {
                val y=bottom-height*i/4
                drawLine(Color.White.copy(alpha=.07f),Offset(left,y),Offset(left+width,y),1.dp.toPx())
                chartText("${(ceiling*i/4).toInt()}",0f,y+4.dp.toPx())
            }
            chartText(if(metric==TrendMetric.ACCURACY) "%" else metric.unit,0f,top-6.dp.toPx())
            if(entries.isNotEmpty()) {
                fun x(e: TrendEntry)=left+width*if(reports.size<=1) .5f else (e.number-1).toFloat()/(reports.size-1)
                fun y(e: TrendEntry)=bottom-height*(e.value/ceiling).toFloat().coerceIn(0f,1f)
                val path=Path();val area=Path()
                entries.forEachIndexed { i,e ->
                    if(i==0) { path.moveTo(x(e),y(e));area.moveTo(x(e),bottom);area.lineTo(x(e),y(e)) }
                    else { path.lineTo(x(e),y(e));area.lineTo(x(e),y(e)) }
                }
                area.lineTo(x(entries.last()),bottom);area.close()
                drawPath(area,Brush.verticalGradient(listOf(tint.copy(alpha=.22f),tint.copy(alpha=.01f)),top,bottom))
                drawPath(path,tint.copy(alpha=.13f),style=Stroke(8.dp.toPx(),cap=StrokeCap.Round,join=StrokeJoin.Round))
                drawPath(path,tint,style=Stroke(2.5.dp.toPx(),cap=StrokeCap.Round,join=StrokeJoin.Round))
                entries.forEachIndexed { i,e ->
                    if(i==selected) drawLine(tint.copy(alpha=.25f),Offset(x(e),top),Offset(x(e),bottom),1.dp.toPx(),pathEffect=PathEffect.dashPathEffect(floatArrayOf(5.dp.toPx(),4.dp.toPx())))
                    drawCircle(Color(0xFF1B2942),if(i==selected) 6.dp.toPx() else 4.dp.toPx(),Offset(x(e),y(e)))
                    drawCircle(tint,if(i==selected) 3.5.dp.toPx() else 2.dp.toPx(),Offset(x(e),y(e)))
                }
            }
            if(reports.isNotEmpty()) {
                chartText("第 1 局",if(reports.size==1) left+width*.5f else left,bottom+22.dp.toPx(),center=true)
                if(reports.size>1) chartText("第 ${reports.size} 局",left+width,bottom+22.dp.toPx(),center=true)
            }
        }
        if(entries.isEmpty()) Text(if(reports.isEmpty()) "暂无完整记录" else "暂无命中节奏数据",color=Muted,fontSize=13.sp,modifier=Modifier.align(Alignment.Center))
    }
    if(highlight!=null) {
        Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
            TextButton(enabled=selected>0,onClick={selected--},contentPadding=PaddingValues(0.dp),modifier=Modifier.width(40.dp)) { Text("‹",color=if(selected>0) tint else Muted.copy(alpha=.3f),fontSize=24.sp) }
            Column(Modifier.weight(1f),horizontalAlignment=Alignment.CenterHorizontally) {
                Text("第 ${highlight.number} 局 · ${valueText(highlight.value,metric)}",color=tint,fontSize=16.sp)
                Text(dateText(highlight.report.time),color=Muted,fontSize=10.sp)
            }
            TextButton(enabled=selected<entries.lastIndex,onClick={selected++},contentPadding=PaddingValues(0.dp),modifier=Modifier.width(40.dp)) { Text("›",color=if(selected<entries.lastIndex) tint else Muted.copy(alpha=.3f),fontSize=24.sp) }
        }
    }
}

@Composable
internal fun DistributionChart(allReports: List<GameReport>) {
    val reports=allReports.takeLast(10)
    val base=allReports.size-reports.size
    var selected by remember(reports) { mutableIntStateOf((reports.size-1).coerceAtLeast(0)) }
    val desc=if(reports.isEmpty()) "暂无判定分布" else "最近${reports.size}局判定分布柱状图，各柱总高度为百分之百"
    Box(Modifier.fillMaxWidth().height(174.dp)) {
        Canvas(Modifier.fillMaxSize().semantics { contentDescription=desc }.pointerInput(reports) {
            detectTapGestures { p ->
                if(reports.isNotEmpty()) {
                    val left=34.dp.toPx();val width=(size.width-left-8.dp.toPx()).coerceAtLeast(1f)
                    selected=((p.x-left)/width*reports.size).toInt().coerceIn(0,reports.lastIndex)
                }
            }
        }) {
            val left=34.dp.toPx();val top=10.dp.toPx();val bottom=size.height-28.dp.toPx()
            val width=(size.width-left-8.dp.toPx()).coerceAtLeast(1f);val height=(bottom-top).coerceAtLeast(1f)
            listOf(0,50,100).forEach { percent ->
                val y=bottom-height*percent/100
                drawLine(Color.White.copy(alpha=.07f),Offset(left,y),Offset(left+width,y),1.dp.toPx())
                chartText("$percent",0f,y+4.dp.toPx())
            }
            if(reports.isNotEmpty()) {
                val step=width/reports.size;val bar=min(25.dp.toPx(),step*.62f)
                reports.forEachIndexed { i,r ->
                    val x=left+step*(i+.5f);var y=bottom
                    val counts=listOf(r.perfect,r.good,r.misses,r.bad)
                    counts.forEachIndexed { n,count ->
                        val h=height*count/r.total.coerceAtLeast(1)
                        y-=h
                        if(h>0) drawRect(listOf(Cyan,Green,Coral,Purple)[n].copy(alpha=if(i==selected) 1f else .6f),Offset(x-bar/2,y),Size(bar,h))
                    }
                    if(i==selected) drawLine(Color.White.copy(alpha=.7f),Offset(x-bar/2-2.dp.toPx(),bottom+4.dp.toPx()),Offset(x+bar/2+2.dp.toPx(),bottom+4.dp.toPx()),2.dp.toPx(),cap=StrokeCap.Round)
                    chartText("${base+i+1}",x,bottom+22.dp.toPx(),center=true)
                }
            }
        }
        if(reports.isEmpty()) Text("练习结束后生成判定柱状图",color=Muted,fontSize=12.sp,modifier=Modifier.align(Alignment.Center))
    }
    reports.getOrNull(selected)?.let { r ->
        Text("第 ${base+selected+1} 局 · Perfect ${r.perfect} / Good ${r.good} / 漏按 ${r.misses} / 错按 ${r.bad}",color=Muted,fontSize=11.sp)
    }
}
