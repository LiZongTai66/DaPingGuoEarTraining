@file:Suppress("MissingPermission")
package com.example.app.ui.connect

import android.Manifest
import android.bluetooth.*
import android.bluetooth.le.*
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.*
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import com.example.app.synth.ConnState
import com.example.app.transport.BluetoothBleTransport
import com.example.app.ui.AppViewModel
import com.example.app.ui.common.AppScreen

@Composable
fun ConnectScreen(vm: AppViewModel, onBack: () -> Unit) {
    val context = LocalContext.current
    val conn by vm.connState.collectAsState()
    val name by vm.deviceName.collectAsState()
    val devices = remember { mutableStateMapOf<String, BluetoothDevice>() }
    var scanning by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf("开发板烧录配套 BLE 固件后，点扫描；无需在系统设置中配对。") }
    val adapter = remember { (context.getSystemService(Context.BLUETOOTH_SERVICE) as? BluetoothManager)?.adapter }
    val handler = remember { Handler(Looper.getMainLooper()) }
    val permissions = remember { if (Build.VERSION.SDK_INT >= 31) arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT) else arrayOf(Manifest.permission.ACCESS_FINE_LOCATION) }
    val callback = remember {
        object : ScanCallback() {
            override fun onScanResult(type: Int, result: ScanResult) {
                handler.post { devices[result.device.address] = result.device }
            }
            override fun onScanFailed(code: Int) {
                handler.post { scanning = false; message = "扫描失败（$code），请稍后重试" }
            }
        }
    }
    fun stopScan() {
        runCatching { adapter?.bluetoothLeScanner?.stopScan(callback) }
        scanning = false; handler.removeCallbacksAndMessages(null)
    }
    fun startScan() {
        if (adapter == null) { message = "手机不支持蓝牙"; return }
        if (!adapter.isEnabled) { message = "请先开启手机蓝牙，然后再次扫描"; return }
        stopScan(); devices.clear()
        try {
            val filter = ScanFilter.Builder().setServiceUuid(ParcelUuid(BluetoothBleTransport.SERVICE_UUID)).build()
            adapter.bluetoothLeScanner.startScan(listOf(filter), ScanSettings.Builder().setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY).build(), callback)
            scanning = true; message = "正在查找大苹果 ESP32-S3…"
            handler.postDelayed({ stopScan(); message = if (devices.isEmpty()) "未找到设备：请确认固件已烧录、开发板已供电且没有被其他手机连接。" else "选择下方设备连接" }, 10000)
        } catch (e: Exception) { stopScan(); message = "无法扫描：${e.message}" }
    }
    val permissionLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { result ->
        if (permissions.all { result[it] == true || ContextCompat.checkSelfPermission(context, it) == PackageManager.PERMISSION_GRANTED }) startScan()
        else message = "请在应用权限中允许附近设备权限；安卓 11 及更早系统还需位置权限并开启定位。"
    }
    val enableLauncher = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { }
    val lifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event -> if (event == Lifecycle.Event.ON_STOP) stopScan() }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer); stopScan() }
    }
    AppScreen("连接设备 · BLE", vm, onBack) { pad ->
        LazyColumn(Modifier.fillMaxSize().padding(pad).padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), contentPadding = PaddingValues(vertical = 16.dp)) {
            item { Text(message, color = Color(0xFFB8C0D0)) }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = {
                        if (scanning) stopScan()
                        else if (permissions.any { ContextCompat.checkSelfPermission(context, it) != PackageManager.PERMISSION_GRANTED }) permissionLauncher.launch(permissions)
                        else startScan()
                    }, enabled = conn != ConnState.CONNECTING) { Text(if (scanning) "停止扫描" else "扫描开发板") }
                    OutlinedButton(onClick = { runCatching { enableLauncher.launch(Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)) }.onFailure { message = "请在手机设置中开启蓝牙" } }) { Text("开启蓝牙") }
                }
            }
            items(devices.values.toList(), key = { it.address }) { d ->
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(16.dp)) {
                        Text(runCatching { d.name }.getOrNull() ?: "大苹果 BLE 设备")
                        Text(d.address)
                        Button(onClick = { stopScan(); vm.connectBluetooth(d) }, enabled = conn == ConnState.DISCONNECTED) { Text("连接") }
                    }
                }
            }
            if (conn != ConnState.DISCONNECTED) item {
                Text(if (conn == ConnState.CONNECTING) "正在连接并检查设备协议…" else "已连接：$name", color = Color.White)
                OutlinedButton(onClick = { vm.disconnect() }) { Text(if (conn == ConnState.CONNECTING) "取消连接" else "断开连接") }
            }
            item {
                HorizontalDivider()
                Text("没有硬件时可体验界面与数据流程。模拟设备不会驱动真实琴，也不会播放声音。", color = Color(0xFFB8C0D0), modifier = Modifier.padding(vertical = 8.dp))
                OutlinedButton(onClick = { stopScan(); vm.connectMock() }, enabled = conn == ConnState.DISCONNECTED) { Text("连接模拟设备") }
            }
        }
    }
}
