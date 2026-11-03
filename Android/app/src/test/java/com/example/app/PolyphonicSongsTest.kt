package com.example.app

import com.example.app.data.*
import com.example.app.protocol.Frame
import org.json.JSONArray
import org.junit.Assert.*
import org.junit.Test

class PolyphonicSongsTest {
    private fun parse(notes: String, extra: String = ""): Song = OnlineSongs.parse(
        """{"title":"双声部","bpm":120,$extra"notes":[$notes]}"""
    ).single()

    @Test fun accompanimentStartsTogetherWhileMelodyIsHeld() {
        val song = parse("""
            {"note":"C5","beats":2,"startBeat":0,"velocity":100,"part":"主旋律"},
            {"note":"C3","beats":0.5,"startBeat":0,"velocity":60,"part":"伴奏"},
            {"note":"G3","beats":0.5,"startBeat":0.5,"velocity":55,"part":"伴奏"}
        """)
        val events = compose(song)
        assertEquals(listOf(0,0,50,0,50,100), events.map { it.dt5ms })
        assertEquals(listOf(72,48,48,55,55,72), events.map { it.note })
        assertEquals(listOf(true,true,false,true,false,false), events.map { it.on })
        assertEquals(1000.0, songDurationMs(song), 0.00001)
    }

    @Test fun unsortedNotesAreScheduledByAbsoluteTime() {
        val song = parse("""
            {"note":"G4","beats":1,"startBeat":2},
            {"note":"C4","beats":1,"startBeat":0}
        """)
        assertEquals(listOf(0,100,100,100), compose(song).map { it.dt5ms })
        assertEquals(listOf(60,60,67,67), compose(song).map { it.note })
        assertEquals(1500.0, songDurationMs(song), 0.00001)
    }

    @Test fun sameTickReattackSendsOffBeforeOn() {
        val song = parse("""
            {"note":"C4","beats":1,"startBeat":1},
            {"note":"C4","beats":1,"startBeat":0}
        """)
        val events = compose(song)
        assertEquals(listOf(0,100,0,100), events.map { it.dt5ms })
        assertFalse(events[1].on); assertTrue(events[2].on)
    }

    @Test fun timedRestsRetainFinalDurationAndLeadingSilence() {
        val song = parse("""
            {"note":"C4","beats":1,"startBeat":1},
            {"note":"R","beats":2,"startBeat":2}
        """)
        assertEquals(listOf(100,100,200), compose(song).map { it.dt5ms })
        assertEquals(0, compose(song).last().note)
    }

    @Test fun downloadedSongPersistsBothStavesWithoutFlattening() {
        val song = parse("""
            {"note":"Eb5","beats":0.75,"startBeat":0.5,"velocity":100,"part":"主旋律"},
            {"note":"C3","beats":0.46875,"startBeat":0,"velocity":55,"part":"伴奏"}
        """)
        val restored = OnlineSongs.parse(OnlineSongs.encode(listOf(song))).single()
        assertEquals(song, restored)
        assertEquals(compose(song), compose(restored))
    }

    @Test fun rejectsAmbiguousTimingAndLegacyGapWithAbsoluteStarts() {
        val partial = """{"note":"C4","beats":1,"startBeat":0},{"note":"G4","beats":1}"""
        assertTrue(runCatching { parse(partial) }.isFailure)
        assertTrue(runCatching { parse("""{"note":"C4","beats":1,"startBeat":0}""", "\"stepGapMs\":1,") }.isFailure)
    }

    @Test fun rejectsSamePitchOverlapsInsteadOfSilencingAnotherStaff() {
        assertTrue(runCatching { parse("""
            {"note":"C4","beats":2,"startBeat":0},
            {"note":"C4","beats":1,"startBeat":1}
        """) }.isFailure)
    }

    @Test fun enforcesActualSevenVoiceGatewayCapacity() {
        val chord = listOf("C3","D3","E3","F3","G3","A3","B3","C4").map {
            """{"note":"$it","beats":1,"startBeat":0}"""
        }
        assertEquals(14, compose(parse(chord.take(7).joinToString(","))).size)
        assertTrue(runCatching { parse(chord.joinToString(",")) }.isFailure)
    }

    @Test fun validatesAbsolutePositionsAndLabels() {
        listOf("-1", "32000", "\"bad\"", "null").forEach { start ->
            assertTrue(runCatching { parse("""{"note":"C4","beats":1,"startBeat":$start}""") }.isFailure)
        }
        assertTrue(runCatching { parse("""{"note":"C4","beats":1,"startBeat":0,"part":""}""") }.isFailure)
    }

    @Test fun entireStarlightScoreMatchesIndependentWireReference() {
        val loader = javaClass.classLoader!!
        val songs = OnlineSongs.parse(loader.getResourceAsStream("starlight-poly.json")!!.bufferedReader().readText())
        val expected = JSONArray(loader.getResourceAsStream("starlight-poly-events.json")!!.bufferedReader().readText())
        assertEquals(2, songs.size)
        songs.forEachIndexed { index, song ->
            assertEquals(456, song.tokens.size)
            assertEquals(195, song.tokens.count { it.part == "主旋律" })
            assertEquals(261, song.tokens.count { it.part == "伴奏" })
            val events = splitEvents(compose(song))
            assertEquals(914, events.size)
            assertEquals(127620L, events.sumOf { it.dt5ms.toLong() } * 5)
            val reference = expected.getJSONArray(index)
            events.forEachIndexed { j, e ->
                val r = reference.getJSONArray(j)
                assertEquals("song $index event $j", listOf(r.getInt(0),r.getInt(1),r.getInt(2),r.getInt(3)),
                    listOf(e.dt5ms,e.note,if(e.on) 1 else 0,e.velocity))
                // Exercise the exact existing six-byte protocol path, including zero-delta chords.
                val frame = Frame.from(e.toFrame())
                assertEquals(e.dt5ms, frame.a0); assertEquals(e.note, frame.a1)
                assertEquals((if(e.on) 128 else 0) or e.velocity, frame.a2)
            }
            assertEquals(song, OnlineSongs.parse(OnlineSongs.encode(listOf(song))).single())
        }
        songs[0].tokens.zip(songs[1].tokens).forEach { (a,b) ->
            assertEquals(midiNote(a.noteName)!!-12, midiNote(b.noteName))
            assertEquals(a.startBeat,b.startBeat); assertEquals(a.beats,b.beats)
        }
    }
}
