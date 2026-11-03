package com.example.app

import com.example.app.data.*
import com.example.app.protocol.*
import org.junit.Assert.*
import org.junit.Test

class DeviceKeymapTest {
    private val offsets=listOf(0,2,4,5,7,9,11)
    private fun f(c:Int,a:Int,b:Int,d:Int)=Frame(c.toByte(),a,b,d)
    private fun snapshot(mode:Int,rev:Int=12):List<Frame> = listOf(f(0x87,rev,mode,7)) +
        offsets.mapIndexed { i,n -> f(0x88,rev,i,48+12*mode+n) } + f(0x89,rev,mode,7)
    @Test fun threePresetsCommitOnlyOnEnd() {
        for(mode in 0..2) {
            val d=DeviceKeymapDecoder(); val frames=snapshot(mode)
            frames.dropLast(1).forEach { assertNull(d.accept(it)) }
            val actual=d.accept(frames.last())!!
            assertEquals(mode,actual.mode);assertEquals(offsets.map {48+12*mode+it},actual.notes)
        }
    }
    @Test fun missingOrMixedItemsNeverCommit() {
        val d=DeviceKeymapDecoder(); val frames=snapshot(0)
        frames.filterIndexed { i,_->i!=4 }.forEach { assertNull(d.accept(it)) }
        frames.dropLast(1).forEach {d.accept(it)}
        assertNull(d.accept(f(0x89,99,0,7)))
        assertNotNull(d.accept(frames.last()))
    }
    @Test fun conflictAndInvalidValuesInvalidateSnapshot() {
        val d=DeviceKeymapDecoder();d.accept(f(0x87,1,0,7));d.accept(f(0x88,1,0,48))
        d.accept(f(0x88,1,0,49));assertNull(d.accept(f(0x89,1,0,7)))
        d.accept(f(0x87,1,0,7));d.accept(f(0x88,1,7,60));assertNull(d.accept(f(0x89,1,0,7)))
    }
    @Test fun customAndResetAndRevisionWrap() {
        val d=DeviceKeymapDecoder();d.accept(f(0x87,255,3,7))
        for(i in 0..6)d.accept(f(0x88,255,i,80-i))
        assertEquals(listOf(80,79,78,77,76,75,74),d.accept(f(0x89,255,3,7))!!.notes)
        d.reset();assertNull(d.accept(f(0x89,255,3,7)))
        var result:DeviceKeymap?=null;snapshot(1,0).forEach {d.accept(it)?.let {r->result=r}}
        assertEquals(0,result!!.revision)
    }
    @Test fun wrongPresetNotesAreRejected() {
        val d=DeviceKeymapDecoder();d.accept(f(0x87,1,0,7))
        for(i in 0..6)d.accept(f(0x88,1,i,60+offsets[i]))
        assertNull(d.accept(f(0x89,1,0,7)))
    }
    @Test fun actualFpgaUartStreamSurvivesBleFragmentation() {
        val bytes=javaClass.getResource("/octave-uart.hex")!!.readText().trim().split(Regex("\\s+")).map {it.toInt(16).toByte()}.toByteArray()
        for(chunk in 1..19) {
            val framing=FrameDecoder();val d=DeviceKeymapDecoder();val all=mutableListOf<DeviceKeymap>()
            bytes.toList().chunked(chunk).forEach {part->framing.feed(part.toByteArray()).forEach {raw->d.accept(Frame.from(raw))?.let {all.add(it)}}}
            assertTrue(all.size>=10);assertTrue(all.any {it.mode==0});assertTrue(all.any {it.mode==2});assertTrue(all.any {it.mode==3})
            assertEquals(0,all.last().mode);assertEquals(offsets.map {48+it},all.last().notes)
        }
    }
}
