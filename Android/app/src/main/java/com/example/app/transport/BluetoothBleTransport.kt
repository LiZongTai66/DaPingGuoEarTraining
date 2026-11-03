@file:Suppress("MissingPermission", "DEPRECATION")
package com.example.app.transport

import android.bluetooth.*
import android.content.Context
import android.os.Build
import java.io.IOException
import java.util.UUID
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/** Nordic UART Service: app writes RX, device notifies TX. All waits run off the UI thread. */
class BluetoothBleTransport(private val context: Context, private val device: BluetoothDevice) : Transport {
    override val name get() = runCatching { device.name ?: device.address }.getOrDefault(device.address)
    override var onRaw: ((ByteArray) -> Unit)? = null
    override var onClosed: ((String) -> Unit)? = null
    @Volatile private var closed = false
    @Volatile private var ready = false
    @Volatile private var error: String? = null
    @Volatile private var gatt: BluetoothGatt? = null
    @Volatile private var rx: BluetoothGattCharacteristic? = null
    private val readyLatch = CountDownLatch(1)
    private val writeLock = Any()
    @Volatile private var writeLatch: CountDownLatch? = null
    @Volatile private var writeStatus = -1

    private fun fail(message: String) {
        if (closed) return
        error = message
        ready = false
        readyLatch.countDown()
        writeLatch?.countDown()
        onClosed?.invoke(message)
    }
    private val callback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(g: BluetoothGatt, status: Int, newState: Int) {
            if (closed) { g.close(); return }
            if (status != BluetoothGatt.GATT_SUCCESS || newState == BluetoothProfile.STATE_DISCONNECTED) {
                fail("BLE 连接断开（$status）")
            } else if (newState == BluetoothProfile.STATE_CONNECTED) {
                if (!g.discoverServices()) fail("无法发现 BLE 服务")
            }
        }
        override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
            if (closed) return
            val service = g.getService(SERVICE_UUID)
            val input = service?.getCharacteristic(RX_UUID)
            val output = service?.getCharacteristic(TX_UUID)
            if (status != BluetoothGatt.GATT_SUCCESS || input == null || output == null) {
                fail("设备未提供大苹果 BLE 服务，请先烧录配套 ESP32 固件"); return
            }
            if (input.properties and BluetoothGattCharacteristic.PROPERTY_WRITE == 0 ||
                output.properties and BluetoothGattCharacteristic.PROPERTY_NOTIFY == 0) {
                fail("BLE 特征属性不匹配"); return
            }
            rx = input
            val descriptor = output.getDescriptor(CCCD_UUID)
            if (descriptor == null || !g.setCharacteristicNotification(output, true)) {
                fail("无法启用设备回传"); return
            }
            val ok = if (Build.VERSION.SDK_INT >= 33) {
                g.writeDescriptor(descriptor, BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE) == BluetoothStatusCodes.SUCCESS
            } else {
                descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                g.writeDescriptor(descriptor)
            }
            if (!ok) fail("提交 BLE 通知订阅失败")
        }
        override fun onDescriptorWrite(g: BluetoothGatt, descriptor: BluetoothGattDescriptor, status: Int) {
            if (closed || descriptor.uuid != CCCD_UUID) return
            if (status == BluetoothGatt.GATT_SUCCESS) { ready = true; readyLatch.countDown() }
            else fail("订阅设备回传失败（$status）")
        }
        override fun onCharacteristicWrite(g: BluetoothGatt, c: BluetoothGattCharacteristic, status: Int) {
            if (c.uuid == RX_UUID) { writeStatus = status; writeLatch?.countDown() }
        }
        override fun onCharacteristicChanged(g: BluetoothGatt, c: BluetoothGattCharacteristic, value: ByteArray) {
            if (!closed && c.uuid == TX_UUID) onRaw?.invoke(value.copyOf())
        }
        override fun onCharacteristicChanged(g: BluetoothGatt, c: BluetoothGattCharacteristic) {
            if (Build.VERSION.SDK_INT < 33 && !closed && c.uuid == TX_UUID) onRaw?.invoke(c.value.copyOf())
        }
    }
    override fun connect() {
        try {
            gatt = device.connectGatt(context.applicationContext, false, callback, BluetoothDevice.TRANSPORT_LE)
            if (!readyLatch.await(18, TimeUnit.SECONDS)) throw IOException("BLE 连接超时，请检查开发板供电及距离")
            if (closed || !ready || error != null) throw IOException(error ?: "连接已取消")
        } catch (e: Exception) { close(); throw IOException(e.message ?: "BLE 连接失败", e) }
    }
    override fun write(data: ByteArray) = synchronized(writeLock) {
        val g = gatt ?: throw IOException("BLE 未连接")
        val c = rx ?: throw IOException("BLE 服务未就绪")
        if (closed || !ready) throw IOException(error ?: "BLE 未连接")
        // Default MTU 23 permits 20 bytes. Six-byte frames fit without MTU negotiation.
        for (chunk in data.toList().chunked(20)) {
            val latch = CountDownLatch(1)
            writeLatch = latch; writeStatus = -1
            val bytes = chunk.toByteArray()
            val ok = if (Build.VERSION.SDK_INT >= 33) {
                g.writeCharacteristic(c, bytes, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT) == BluetoothStatusCodes.SUCCESS
            } else {
                c.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT; c.value = bytes
                g.writeCharacteristic(c)
            }
            if (!ok || !latch.await(5, TimeUnit.SECONDS) || writeStatus != BluetoothGatt.GATT_SUCCESS || closed) {
                close(); throw IOException("BLE 发送失败或超时，请重新连接")
            }
            writeLatch = null
        }
    }
    override fun close() {
        closed = true; ready = false
        readyLatch.countDown(); writeLatch?.countDown()
        val g = gatt; gatt = null; rx = null
        runCatching { g?.disconnect() }; runCatching { g?.close() }
    }
    companion object {
        val SERVICE_UUID: UUID = UUID.fromString("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
        val RX_UUID: UUID = UUID.fromString("6e400002-b5a3-f393-e0a9-e50e24dcca9e")
        val TX_UUID: UUID = UUID.fromString("6e400003-b5a3-f393-e0a9-e50e24dcca9e")
        val CCCD_UUID: UUID = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
    }
}
