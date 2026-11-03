package com.example.app

import com.example.app.data.*
import org.junit.Assert.*
import org.junit.Test

class GowinSongsTest {
    private fun sourceSteps(song: Int): List<Pair<Int, Int>> {
        val source = javaClass.classLoader!!.getResourceAsStream("gowin-song-step.txt")!!.bufferedReader().readText()
        val body = Regex("2'd$song: begin\\s*case \\(index\\)(.*?)endcase", RegexOption.DOT_MATCHES_ALL).find(source)!!.groupValues[1]
        return Regex("(\\d+): song_step = \\{4'd(\\d+),3'd(\\d+)\\}").findAll(body).map {
            it.groupValues[2].toInt() to it.groupValues[3].toInt()
        }.toList()
    }
    @Test fun titlesAndFourteenNotes_matchCurrentBoard() {
        assertEquals(listOf("小星星", "两只老虎", "欢乐颂"), SongLibrary.songs.map { it.title })
        val notes = listOf("C4", "D4", "E4", "F4", "G4", "A4", "B4", "R")
        SongLibrary.songs.forEachIndexed { i, song ->
            val steps = sourceSteps(i)
            assertEquals(14, steps.size)
            assertEquals(steps.map { notes[it.second] }, song.tokens.map { it.noteName })
            assertEquals(steps.map { it.first.toFloat() }, song.tokens.map { it.beats })
            assertTrue(song.tokens.all { it.velocity == 110 })
        }
    }
    @Test fun onsets_matchBoardStateMachineWithinProtocolResolution() {
        SongLibrary.songs.forEachIndexed { i, song ->
            var timeMs = 0L
            val expected = sourceSteps(i).map { (duration, _) -> timeMs.also { timeMs += duration * 350 + 1 } }
            var ticks = 0
            val got = compose(song).mapNotNull { e -> ticks += e.dt5ms; if (e.on) ticks * 5L else null }
            assertEquals(14, got.size)
            got.zip(expected).forEach { (a, b) -> assertTrue("$a vs $b", kotlin.math.abs(a - b) <= 2) }
            assertEquals(5614L, timeMs)
            assertEquals(5615L, compose(song).sumOf { it.dt5ms.toLong() } * 5)
        }
    }
    @Test fun exactTiming_survivesJsonRoundTrip() {
        val loaded = OnlineSongs.parse(OnlineSongs.encode(SongLibrary.songs))
        SongLibrary.songs.zip(loaded).forEach { (a, b) ->
            assertEquals(a.tokens, b.tokens); assertEquals(compose(a), compose(b))
        }
    }
    @Test fun fractionalTempo_doesNotAccumulatePerNoteRounding() {
        val song = Song("t", "t", 137, List(200) { NoteToken("C4", 1f) })
        assertEquals(Math.round(200 * 60000.0 / 137 / 5), compose(song).sumOf { it.dt5ms.toLong() })
    }
    @Test fun trailingRests_arePreserved() {
        val song = Song("t", "t", 120, listOf(NoteToken("C4", 1f), NoteToken("R", 2f)))
        assertEquals(1500L, compose(song).sumOf { it.dt5ms.toLong() } * 5)
    }
}
