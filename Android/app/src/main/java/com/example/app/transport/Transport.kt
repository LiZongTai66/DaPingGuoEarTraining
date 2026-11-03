package com.example.app.transport

import java.io.IOException

/** Byte stream transport. Blocking connect/write must run on an IO thread. */
interface Transport {
    val name: String
    @Throws(IOException::class) fun connect()
    @Throws(IOException::class) fun write(data: ByteArray)
    fun close()
    var onRaw: ((ByteArray) -> Unit)?
    var onClosed: ((String) -> Unit)?
        get() = null
        set(value) {}
}
