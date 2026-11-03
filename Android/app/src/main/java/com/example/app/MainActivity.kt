package com.example.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.app.ui.AppViewModel
import com.example.app.ui.Routes
import com.example.app.ui.connect.ConnectScreen
import com.example.app.ui.home.HomeScreen
import com.example.app.ui.keymap.KeymapScreen
import com.example.app.ui.piano.PianoScreen
import com.example.app.ui.record.RecordScreen
import com.example.app.ui.songs.SongsScreen
import com.example.app.ui.theme.GW2A_Synth_Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            GW2A_Synth_Theme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    // 在 Activity 级创建，所有页面共享同一个 ViewModel（含连接状态）
                    val vm: AppViewModel = viewModel()
                    val nav = rememberNavController()

                    NavHost(navController = nav, startDestination = Routes.HOME) {
                        composable(Routes.HOME) {
                            HomeScreen(
                                vm = vm,
                                onOpen = { route -> nav.navigate(route) },
                                onPiano = { nav.navigate(Routes.PIANO) }
                            )
                        }
                        composable(Routes.CONNECT) { ConnectScreen(vm = vm, onBack = { nav.popBackStack() }) }
                        composable(Routes.PIANO) { PianoScreen(vm = vm, onBack = { nav.popBackStack() }) }
                        composable(Routes.SONGS) { SongsScreen(vm = vm, onBack = { nav.popBackStack() }) }
                        composable(Routes.KEYMAP) { KeymapScreen(vm = vm, onBack = { nav.popBackStack() }) }
                        composable(Routes.EAR) { com.example.app.ui.ear.EarTrainingScreen(vm=vm,onBack={ nav.popBackStack() }) }
                        composable(Routes.GAME) { com.example.app.ui.game.GameStatsScreen(vm=vm,onBack={ nav.popBackStack() }) }
                        composable(Routes.RECORD) { RecordScreen(vm = vm, onBack = { nav.popBackStack() }) }
                    }
                }
            }
        }
    }
}
