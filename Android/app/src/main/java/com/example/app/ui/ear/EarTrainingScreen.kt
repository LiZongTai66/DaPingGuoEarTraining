package com.example.app.ui.ear

import androidx.compose.animation.core.*
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Headphones
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.app.data.*
import com.example.app.synth.ConnState
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen
import com.example.app.ui.game.*

@Composable
fun EarTrainingScreen(vm:AppViewModel,onBack:()->Unit) {
    val round by vm.earRound.collectAsState()
    val history by vm.earHistory.collectAsState()
    val connection by vm.connState.collectAsState()
    val pending by vm.earUndoPending.collectAsState()
    var help by remember { mutableStateOf(false) }
    val result=round.result()
    AppScreen("听音记忆",vm,onBack,actions={TextButton(onClick={help=true}) { Text("玩法",color=Cyan) }}) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(18.dp),verticalArrangement=Arrangement.spacedBy(18.dp)) {
            Column {
                Text("LISTEN · REMEMBER · PLAY",color=Cyan,fontSize=11.sp,letterSpacing=2.sp)
                Text("把听见的旋律，弹回来",fontSize=25.sp,fontWeight=FontWeight.Bold,color=Color.White,modifier=Modifier.padding(top=7.dp))
                Text("7 个随机音符 · 可重复 · Do～Si",color=Muted,fontSize=12.sp,modifier=Modifier.padding(top=6.dp))
            }
            Surface(shape=RoundedCornerShape(26.dp),color=Color(0xFF20344C),border=BorderStroke(1.dp,Cyan.copy(alpha=.15f))) {
                Column(Modifier.fillMaxWidth().background(Brush.verticalGradient(listOf(Cyan.copy(alpha=.06f),Purple.copy(alpha=.08f)))).padding(20.dp),horizontalAlignment=Alignment.CenterHorizontally,verticalArrangement=Arrangement.spacedBy(14.dp)) {
                    ListeningOrb(round.phase==EarPhase.LISTENING)
                    Text(when(round.phase) {
                        EarPhase.IDLE->"听一段，记一段"
                        EarPhase.PREPARING->"正在准备旋律"
                        EarPhase.LISTENING->"请仔细听 · 第 ${round.listens} 遍"
                        EarPhase.INPUT->if(round.answer.size==7) "准备揭晓了吗？" else "轮到你演奏"
                        EarPhase.SUBMITTING->"正在校验答案"
                        EarPhase.COMPLETE->"这一轮，你答对 ${result?.correct} / 7"
                        EarPhase.ERROR->"这一轮暂未完成"
                        EarPhase.CANCELLED->"休息一下，再试一次"
                    },color=Color.White,fontSize=22.sp,fontWeight=FontWeight.Bold)
                    Text(round.message,color=Muted,fontSize=12.sp)
                    if(round.phase==EarPhase.INPUT || round.phase==EarPhase.SUBMITTING) {
                        LinearProgressIndicator(progress={round.answer.size/7f},modifier=Modifier.fillMaxWidth(),color=Cyan,trackColor=Color.White.copy(alpha=.08f))
                    }
                    if(!round.active) Button(onClick=vm::startEarTraining,enabled=connection==ConnState.CONNECTED,modifier=Modifier.fillMaxWidth().height(52.dp),shape=RoundedCornerShape(15.dp)) {
                        Text(if(round.phase==EarPhase.COMPLETE) "开始下一题" else "开始训练",fontWeight=FontWeight.Bold)
                    }
                    if(connection!=ConnState.CONNECTED) Text("先到首页连接真实 ESP32 开发板",color=Coral,fontSize=12.sp)
                    if(round.active) TextButton(onClick=vm::cancelEarTraining) { Text("结束本轮",color=Muted) }
                }
            }
            if(round.phase in listOf(EarPhase.INPUT,EarPhase.SUBMITTING,EarPhase.COMPLETE)) DashboardPanel {
                Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) {
                    Text("你的输入",fontWeight=FontWeight.SemiBold,color=Color.White)
                    Text("${round.answer.size} / 7",color=Cyan,fontSize=12.sp)
                }
                NoteStrip(round.answer,if(result!=null) round.target else null)
                if(round.phase==EarPhase.INPUT) {
                    Row(horizontalArrangement=Arrangement.spacedBy(9.dp)) {
                        OutlinedButton(onClick=vm::undoEarNote,enabled=round.answer.isNotEmpty(),modifier=Modifier.weight(1f)) { Text(if(pending==0) "↶ 撤回上一个" else "撤回中 ($pending)") }
                        OutlinedButton(onClick=vm::replayEarTraining,enabled=pending==0,modifier=Modifier.weight(1f)) { Text("再听一遍") }
                    }
                    Text("点一次撤回一个；重听会清空当前输入。",color=Muted,fontSize=11.sp)
                    Button(onClick=vm::submitEarTraining,enabled=round.answer.size==7 && pending==0,modifier=Modifier.fillMaxWidth().height(48.dp),shape=RoundedCornerShape(14.dp)) { Text("提交校验 · 揭晓旋律",fontWeight=FontWeight.Bold) }
                }
            }
            if(result!=null) DashboardPanel {
                Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("本轮正确率",color=Muted,fontSize=12.sp)
                        Text("${result.accuracy}%",color=Green,fontSize=42.sp,fontWeight=FontWeight.Bold)
                    }
                    Text("听了 ${result.listens} 遍\n答对 ${result.correct} 个",color=Muted,fontSize=13.sp)
                }
                Text("标准旋律",color=Color.White,fontSize=13.sp)
                NoteStrip(result.target.map { it },null)
                Text(if(result.correct==7) "完整复现！下一题会是一组新的随机旋律。" else "对比上方输入与标准旋律，找出记错的位置再练一轮。",color=Green,fontSize=12.sp)
            }
            Row(horizontalArrangement=Arrangement.spacedBy(10.dp)) {
                SmallMetric("训练记录",history.size.toString(),"最近保存 30 轮",Modifier.weight(1f))
                SmallMetric("平均正确率",if(history.isEmpty()) "—" else "${history.map { it.correct*100.0/7 }.average().toInt()}%","只统计已提交的轮次",Modifier.weight(1f))
            }
            DashboardPanel {
                Text("听音成长曲线",color=Color.White,fontSize=17.sp,fontWeight=FontWeight.SemiBold)
                TrendChart(history.take(20).asReversed().map { it.chartReport() },TrendMetric.ACCURACY)
                Text("最近 20 轮，由早到晚。重听次数保存在每轮详情中。",color=Muted,fontSize=11.sp)
            }
            Text("记忆档案",color=Color.White,fontSize=18.sp,fontWeight=FontWeight.Bold)
            if(history.isEmpty()) Text("完成第一轮后，这里会保存题目、输入与重听次数。",color=Muted,fontSize=12.sp)
            history.forEachIndexed { i,r ->
                var expanded by remember(r.time,i) { mutableStateOf(false) }
                DashboardPanel {
                    Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(dateText(r.time),color=Color.White,fontWeight=FontWeight.SemiBold)
                            Text("${r.correct}/7 答对 · 听了 ${r.listens} 遍",color=Muted,fontSize=12.sp)
                        }
                        TextButton(onClick={expanded=!expanded}) { Text("${r.accuracy}% ${if(expanded) "∧" else "∨"}",color=Cyan) }
                    }
                    if(expanded) {
                        Text("你的输入",color=Muted,fontSize=11.sp);NoteStrip(r.answer.map { it },r.target)
                        Text("标准旋律",color=Muted,fontSize=11.sp);NoteStrip(r.target.map { it },null)
                    }
                }
            }
            Text("开局会将七个实体压传恢复为 Do、Re、Mi、Fa、Sol、La、Si。请松开再按，同一个音可以重复输入。",color=Muted,fontSize=11.sp)
        }
    }
    if(help) AlertDialog(onDismissRequest={help=false},title={Text("听音记忆 · 玩法")},text={
        Column(Modifier.verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(10.dp)) {
            Text("1. 点击开始，App随机生成7个Do～Si音符，允许重复。板子会先播放一遍，播放时按键不计入答案。")
            Text("2. 提示作答后，松开琴键，再依次按压。App实时显示自己的输入，但暂不显示标准答案。")
            Text("3. 点一次撤回一个音；也可以再听一遍，同题重听会清空当前输入。")
            Text("4. 输入7个后点击提交，逐位校验。顺序相同才算答对，不考核速度或节奏。")
            Text("每轮最多等待60秒输入。只保存成功提交的轮次，记录保存在手机本机。开局会恢复实体键位为Do～Si，结束后保持这个映射。")
        }
    },confirmButton={TextButton(onClick={help=false}){Text("开始体验")}})
}

@Composable
private fun ListeningOrb(listening:Boolean) {
    val transition=rememberInfiniteTransition(label="listening")
    val scale by transition.animateFloat(1f,1.13f,infiniteRepeatable(tween(950),RepeatMode.Reverse),label="pulse")
    Box(Modifier.size(98.dp),contentAlignment=Alignment.Center) {
        Box(Modifier.size(84.dp).scale(if(listening) scale else 1f).background(Cyan.copy(alpha=.08f),CircleShape))
        Surface(shape=CircleShape,color=Cyan.copy(alpha=.12f),border=BorderStroke(1.dp,Cyan.copy(alpha=.3f))) {
            Icon(Icons.Filled.Headphones,contentDescription=if(listening) "正在播放示范" else "听音训练",tint=Cyan,modifier=Modifier.padding(19.dp).size(28.dp))
        }
    }
}

@Composable
private fun NoteStrip(notes:List<Int?>,target:List<Int>?) {
    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(5.dp)) {
        for(i in 0..6) {
            val n=notes.getOrNull(i);val filled=i<notes.size
            val tint=if(target!=null && n!=null) { if(n==target[i]) Green else Coral } else if(filled) Cyan else Muted
            Surface(modifier=Modifier.weight(1f),shape=RoundedCornerShape(10.dp),color=tint.copy(alpha=if(filled) .13f else .04f),border=BorderStroke(1.dp,tint.copy(alpha=.2f))) {
                Column(Modifier.padding(vertical=11.dp),horizontalAlignment=Alignment.CenterHorizontally) {
                    Text("${i+1}",color=Muted,fontSize=9.sp)
                    Text(n?.let { solfege[it] } ?: if(filled) "?" else "·",color=tint,fontWeight=FontWeight.Bold,fontSize=13.sp)
                    if(target!=null) Text(if(n==target[i]) "✓" else "×",color=tint,fontSize=10.sp)
                }
            }
        }
    }
}

@Composable
private fun SmallMetric(title:String,value:String,detail:String,modifier:Modifier) {
    Surface(modifier=modifier,shape=RoundedCornerShape(18.dp),color=Color(0xFF1B2942)) {
        Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(6.dp)) {
            Text(title,color=Muted,fontSize=12.sp);Text(value,color=Cyan,fontSize=28.sp,fontWeight=FontWeight.Bold)
            Text(detail,color=Muted,fontSize=10.sp)
        }
    }
}
