package com.example.app.data

/** Extracted from fourth/src/ads1115_pressure_test.v song_step, demo_last_index=13.
 * Nominal beat=350ms; the current state machine adds one idle millisecond per step.
 * This is song data only; screen commands B1/B2/B3 are not sent on the App BLE channel.
 */
object GowinDemoSongs {
    val songs = listOf(
        Song("twinkle", "小星星", 171, listOf(NoteToken("C4", 1f, 110), NoteToken("C4", 1f, 110), NoteToken("G4", 1f, 110), NoteToken("G4", 1f, 110), NoteToken("A4", 1f, 110), NoteToken("A4", 1f, 110), NoteToken("G4", 2f, 110), NoteToken("F4", 1f, 110), NoteToken("F4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("D4", 1f, 110), NoteToken("D4", 1f, 110), NoteToken("C4", 2f, 110)), beatMs = 350, stepGapMs = 1),
        Song("two_tigers", "两只老虎", 171, listOf(NoteToken("C4", 1f, 110), NoteToken("D4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("C4", 1f, 110), NoteToken("C4", 1f, 110), NoteToken("D4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("C4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("F4", 1f, 110), NoteToken("G4", 2f, 110), NoteToken("E4", 1f, 110), NoteToken("F4", 1f, 110), NoteToken("G4", 2f, 110)), beatMs = 350, stepGapMs = 1),
        Song("ode_to_joy", "欢乐颂", 171, listOf(NoteToken("E4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("F4", 1f, 110), NoteToken("G4", 1f, 110), NoteToken("G4", 1f, 110), NoteToken("F4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("D4", 1f, 110), NoteToken("C4", 1f, 110), NoteToken("C4", 1f, 110), NoteToken("D4", 1f, 110), NoteToken("E4", 1f, 110), NoteToken("E4", 2f, 110), NoteToken("D4", 2f, 110)), beatMs = 350, stepGapMs = 1)
    )
}
