package com.example.app.ui.game

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.data.*
import com.example.app.synth.ConnState
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

internal val Cyan=Color(0xFF5CE1E6)
internal val Green=Color(0xFF7AE2B1)
internal val Purple=Color(0xFFB9A3FF)
internal val Coral=Color(0xFFFF9AAB)
internal val Muted=Color(0xFFADBBD2)
internal fun dateText(time: Long) = SimpleDateFormat("MM-dd HH:mm",Locale.CHINA).format(Date(time))
internal fun valueText(value: Double, metric: TrendMetric) =
    if(metric==TrendMetric.ACCURACY) "%.1f%%".format(value) else "%.0f %s".format(value,metric.unit)

@Composable
fun GameStatsScreen(vm: AppViewModel, onBack: () -> Unit) {
    val round by vm.gameRound.collectAsState()
    val history by vm.gameHistory.collectAsState()
    val connection by vm.connState.collectAsState()
    val label by vm.practiceLabel.collectAsState()
    var help by remember { mutableStateOf(false) }
    var editLabel by remember { mutableStateOf(false) }
    var example by remember { mutableStateOf(false) }
    var filter by remember { mutableStateOf<String?>(null) }
    var filterMenu by remember { mutableStateOf(false) }
    var limit by remember { mutableIntStateOf(10) }
    var metric by remember { mutableStateOf(TrendMetric.ACCURACY) }
    val exampleReports=remember { dashboardExamples() }
    LaunchedEffect(round.running) {
        if(round.running) { if(example) filter=null;example=false }
    }
    val source=if(example) exampleReports else history
    val labels=source.map { it.label }.distinct()
    val reports=remember(source,filter,limit) { validPracticeReports(source,filter,limit) }
    val visibleHistory=source.filter { filter==null || it.label==filter }
    val latest=reports.lastOrNull()
    AppScreen("练习分析",vm,onBack,actions={
        IconButton(onClick={help=true}) { Icon(Icons.Filled.Info,contentDescription="统计说明",tint=Muted) }
    }) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal=18.dp,vertical=14.dp),
            verticalArrangement=Arrangement.spacedBy(18.dp)) {
            Column {
                Text("PRACTICE INSIGHTS",color=Cyan,fontSize=11.sp,letterSpacing=2.sp)
                Text("每一次练习，都看得见",color=Color.White,fontSize=23.sp,fontWeight=FontWeight.Bold,modifier=Modifier.padding(top=6.dp))
            }
            Surface(shape=RoundedCornerShape(14.dp),color=if(example) Purple.copy(alpha=.12f) else Color.White.copy(alpha=.05f)) {
                Row(Modifier.fillMaxWidth().padding(12.dp),verticalAlignment=Alignment.CenterVertically) {
                    Box(Modifier.size(7.dp).background(if(example) Purple else if(connection==ConnState.CONNECTED) Green else Muted,RoundedCornerShape(7.dp)))
                    Spacer(Modifier.width(9.dp))
                    Text(if(example) "示例数据 · 不会存入练习记录" else if(connection==ConnState.CONNECTED) "蓝牙已连接 · ${if(round.running) "正在接收判定" else "在 TJC 开始即可记录"}" else "连接蓝牙后，在 TJC 开始游戏",color=if(example) Purple else Muted,fontSize=12.sp,modifier=Modifier.weight(1f))
                    if(example) TextButton(onClick={example=false;filter=null}) { Text("返回",color=Purple) }
                }
            }
            if(!example) {
                Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("练习标签",color=Muted,fontSize=11.sp)
                        Text(label.ifEmpty { "未分类" },color=Color.White,fontWeight=FontWeight.SemiBold)
                    }
                    TextButton(onClick={editLabel=true},enabled=!round.running) { Text(if(label.isEmpty()) "设置曲目 / 难度" else "更改",color=if(round.running) Muted else Cyan) }
                }
            }
            if(round.running && !example) DashboardPanel {
                SectionHeading("正在演奏", "LIVE",Green)
                Text("${round.combo}",fontSize=46.sp,fontWeight=FontWeight.Bold,color=Green)
                Text("当前连击 · 已判定 ${round.events.size} 个目标",color=Muted,fontSize=13.sp)
                val r=round.report()
                Text("Perfect ${r.perfect}   Good ${r.good}   漏按 ${r.misses}   错按 ${r.bad}",color=Color.White,fontSize=13.sp)
            }
            if(!example && round.started && !round.running && !round.report().complete) {
                Surface(color=Coral.copy(alpha=.10f),shape=RoundedCornerShape(14.dp)) {
                    Text("本局${round.status}，记录未计入趋势。重新开始一局即可继续。",color=Coral,fontSize=12.sp,modifier=Modifier.padding(14.dp))
                }
            }
            Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp),verticalAlignment=Alignment.CenterVertically) {
                listOf(5,10,20).forEach { n -> FilterChip(selected=limit==n,onClick={limit=n},label={Text("近 $n 局",fontSize=11.sp)}) }
                Spacer(Modifier.weight(1f))
                Box(Modifier.widthIn(max=112.dp)) {
                    TextButton(onClick={filterMenu=true}) { Text(if(filter==null) "全部标签 ▾" else "${filter!!.ifEmpty { "未分类" }} ▾",maxLines=1,color=Cyan,fontSize=11.sp) }
                    DropdownMenu(expanded=filterMenu,onDismissRequest={filterMenu=false}) {
                        DropdownMenuItem(text={Text("全部标签")},onClick={filter=null;filterMenu=false})
                        labels.forEach { l -> DropdownMenuItem(text={Text(l.ifEmpty { "未分类" })},onClick={filter=l;filterMenu=false}) }
                    }
                }
            }
            Row(horizontalArrangement=Arrangement.spacedBy(10.dp)) {
                MetricTile("平均命中率",if(reports.isEmpty()) "—" else "%.1f%%".format(reports.map { TrendMetric.ACCURACY.value(it)!! }.average()),"${reports.size} 局完整记录",Cyan,Modifier.weight(1f))
                MetricTile("最佳连击",reports.maxOfOrNull { it.maxCombo }?.toString() ?: "—","连续命中的目标数",Purple,Modifier.weight(1f))
            }
            DashboardPanel {
                SectionHeading("成长趋势","TREND",Cyan)
                Row(horizontalArrangement=Arrangement.spacedBy(6.dp)) {
                    TrendMetric.entries.forEach { m -> FilterChip(selected=metric==m,onClick={metric=m},label={Text(m.title,fontSize=12.sp)}) }
                }
                TrendChart(reports,metric)
                Text(if(metric.lowerIsBetter) "平均绝对偏差，越低越稳定；没有命中数据的局不绘制。" else "仅统计完整结束的练习；点击圆点查看该局数据。",fontSize=11.sp,color=Muted)
                if(filter==null && labels.size>1) Text("比较进步时，建议筛选同一曲目 / 难度标签。",fontSize=11.sp,color=Purple)
                if(reports.isEmpty() && !example) TextButton(onClick={example=true;filter=null}) { Text("查看图表示例 →",color=Cyan) }
            }
            DashboardPanel {
                SectionHeading("判定分布","DISTRIBUTION",Purple)
                DistributionChart(reports.takeLast(10))
                Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) {
                    LegendDot("Perfect",Cyan);LegendDot("Good",Green);LegendDot("漏按",Coral);LegendDot("错按",Purple)
                }
                Text("每根柱代表一局，各色高度为该类判定比例。显示最近至多 10 局。",color=Muted,fontSize=11.sp)
            }
            if(latest!=null) DashboardPanel {
                SectionHeading("最近一局 · 分段表现","FOCUS",Green)
                Text("${latest.label.ifEmpty { "未分类" }}  ·  ${dateText(latest.time)}",color=Muted,fontSize=12.sp)
                SectionBars(latest)
                Surface(color=Green.copy(alpha=.08f),shape=RoundedCornerShape(12.dp)) {
                    Text(latest.advice,color=Green,fontSize=13.sp,modifier=Modifier.padding(13.dp))
                }
            }
            Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) {
                Text("练习记录",color=Color.White,fontSize=18.sp,fontWeight=FontWeight.Bold)
                Text("${visibleHistory.size} / 20 局",color=Muted,fontSize=12.sp)
            }
            if(visibleHistory.isEmpty()) DashboardPanel {
                Text("你的练习轨迹，从第一局开始",color=Color.White,fontWeight=FontWeight.SemiBold)
                Text("完成游戏后自动保存，折线图和柱状图会随记录更新。",color=Muted,fontSize=13.sp)
            }
            visibleHistory.forEachIndexed { i,r -> HistoryCard(r,i) }
            Text("分段按目标音符序号均分。节奏偏差相对 FPGA 判定中心，单位 ms。",color=Muted.copy(alpha=.75f),fontSize=11.sp)
            Spacer(Modifier.height(8.dp))
        }
    }
    if(help) AlertDialog(onDismissRequest={help=false},title={Text("怎样读懂练习数据")},text={
        Column(Modifier.verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {
            Text("先连接蓝牙，再从 TJC 开始游戏。完整结束的局才进入趋势图，断连或中途退出的记录仍保留。")
            Text("可在开局前设置曲目和难度标签，同一标签下比较更有意义。旧记录会显示为未分类。")
            Text("节奏趋势使用平均绝对偏差，越低越好。单局详情中的有符号偏差：负数偏早，正数偏晚，约 2 ms 量化。")
            Text("前、中、后段按音符序号划分，不是实际小节。最多保存最近 20 局；示例数据不保存、不参与真实成绩。")
        }
    },confirmButton={TextButton(onClick={help=false}){Text("知道了")}})
    if(editLabel) {
        var draft by remember { mutableStateOf(label) }
        AlertDialog(onDismissRequest={editLabel=false},title={Text("设置练习标签")},text={
            Column(verticalArrangement=Arrangement.spacedBy(10.dp)) {
                Text("例如“两只老虎 · 普通”。开局时自动附到本局记录。")
                OutlinedTextField(value=draft,onValueChange={draft=it.take(30)},singleLine=true,label={Text("曲目 / 难度")})
            }
        },confirmButton={TextButton(onClick={vm.setPracticeLabel(draft);editLabel=false}){Text("保存")}},dismissButton={TextButton(onClick={editLabel=false}){Text("取消")}})
    }
}

@Composable
internal fun DashboardPanel(content: @Composable ColumnScope.() -> Unit) {
    Surface(modifier=Modifier.fillMaxWidth(),shape=RoundedCornerShape(22.dp),color=Color(0xFF1B2942),border=BorderStroke(1.dp,Color.White.copy(alpha=.06f))) {
        Column(Modifier.padding(18.dp),verticalArrangement=Arrangement.spacedBy(12.dp),content=content)
    }
}

@Composable
private fun SectionHeading(title: String, caption: String, tint: Color) {
    Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically,horizontalArrangement=Arrangement.SpaceBetween) {
        Text(title,color=Color.White,fontSize=16.sp,fontWeight=FontWeight.SemiBold,modifier=Modifier.weight(1f))
        Text(caption,color=tint,fontSize=9.sp,letterSpacing=1.sp)
    }
}

@Composable
private fun MetricTile(title: String,value: String,subtitle: String,tint: Color,modifier: Modifier) {
    Surface(modifier=modifier,shape=RoundedCornerShape(20.dp),color=tint.copy(alpha=.09f),border=BorderStroke(1.dp,tint.copy(alpha=.12f))) {
        Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(6.dp)) {
            Text(title,color=Muted,fontSize=12.sp)
            Text(value,color=tint,fontSize=30.sp,fontWeight=FontWeight.Bold)
            Text(subtitle,color=Muted,fontSize=10.sp)
        }
    }
}

@Composable
private fun LegendDot(label: String,tint: Color) {
    Row(verticalAlignment=Alignment.CenterVertically) {
        Box(Modifier.size(6.dp).background(tint,RoundedCornerShape(2.dp)));Spacer(Modifier.width(4.dp))
        Text(label,color=Muted,fontSize=10.sp)
    }
}

@Composable
private fun SectionBars(r: GameReport) {
    r.sections.forEach { section ->
        val rate=if(section.total==0) 0f else section.hits.toFloat()/section.total
        Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
            Text(section.name,color=Muted,fontSize=12.sp,modifier=Modifier.width(40.dp))
            Box(Modifier.weight(1f).height(9.dp).background(Color.White.copy(alpha=.06f),RoundedCornerShape(8.dp))) {
                if(rate>0) Box(Modifier.fillMaxWidth(rate.coerceIn(0f,1f)).fillMaxHeight().background(if(rate<.7f) Coral else Cyan,RoundedCornerShape(8.dp)))
            }
            Text("${(rate*100).toInt()}%",color=Color.White,fontSize=12.sp,modifier=Modifier.width(42.dp).padding(start=8.dp))
        }
    }
}

@Composable
private fun HistoryCard(r: GameReport,index: Int) {
    var expanded by remember(r.time,index) { mutableStateOf(false) }
    Surface(modifier=Modifier.fillMaxWidth().clickable { expanded=!expanded },shape=RoundedCornerShape(18.dp),color=Color.White.copy(alpha=.045f)) {
        Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment=Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text(r.label.ifEmpty { "未分类练习" },color=Color.White,fontWeight=FontWeight.SemiBold)
                    Text("${dateText(r.time)} · ${if(r.complete) "完整记录" else r.status+" · 未计入趋势"}",color=Muted,fontSize=11.sp,modifier=Modifier.padding(top=4.dp))
                }
                Column(horizontalAlignment=Alignment.End) {
                    Text("${r.accuracy}%",color=if(r.complete) Cyan else Muted,fontSize=23.sp,fontWeight=FontWeight.Bold)
                    Text(if(expanded) "收起 ∧" else "详情 ∨",color=Muted,fontSize=10.sp)
                }
            }
            if(expanded) {
                HorizontalDivider(color=Color.White.copy(alpha=.06f))
                Text("最高连击 ${r.maxCombo}  ·  得分 ${r.perfect*100+r.good*60}  ·  目标 ${r.total}",color=Color.White,fontSize=12.sp)
                Text("Perfect ${r.perfect}   Good ${r.good}   漏按 ${r.misses}   错按 ${r.bad}",color=Muted,fontSize=12.sp)
                Text("平均偏差 ${r.meanOffset?.let { "%+.0f ms".format(it) } ?: "—"}  /  绝对偏差 ${r.meanAbsOffset?.let { "%.0f ms".format(it) } ?: "—"}",color=Muted,fontSize=12.sp)
                SectionBars(r)
                Text(r.advice,color=if(r.complete) Green else Coral,fontSize=12.sp)
            }
        }
    }
}
