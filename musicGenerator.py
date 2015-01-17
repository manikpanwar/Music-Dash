# file which generates random music using markov chains and some machine 
# learning to generate completely new music on it's own
# all music training and generation is done in midi format

import midi

class MusicGenerator(object):
    @staticmethod
    def make2dList(rows = 0, cols = 0, value = 0):
        ls = list()
        for row in xrange(rows):
            ls += [[value]*cols]
        return ls

    def parseMIDIFile(self, path): 
        # returns array of pitch, velocity and ticks in a midi file
        pattern = midi.read_midifile(path)
        pitches, velocities, ticks = ([] , [], [])
        # print pattern
        for musicEvent in pattern[1]:
            if type(musicEvent) == midi.NoteOnEvent:
                # note starts
                # print musicEvent
                pitches.append((musicEvent.pitch, "on"))
                velocities.append((musicEvent.velocity, "on"))
                ticks.append((musicEvent.tick, "on"))
            elif type(musicEvent) == midi.NoteOffEvent:
                # note ended
                # print musicEvent
                pitches.append((musicEvent.pitch, "off"))
                velocities.append((musicEvent.velocity, "off"))
                ticks.append((musicEvent.tick, "off"))
            elif type(musicEvent) == midi.ProgramChangeEvent:
                # print "Midi %d"%musicEvent.data[0]
                pass
            elif type(musicEvent) == midi.EndOfTrackEvent : 
                # track has ended
                print "finished"
        return pitches, velocities, ticks

    def trainMIDIFile(self, path):
        pitches, velocities, ticks = self.parseMIDIFile(path)
        self.trainPitchesFromMIDIFile(pitches)

    def trainPitchesFromMIDIFile(self, pitches):
        pass

    def __init__(self):
        self.pitchMatrix = MusicGenerator.make2dList(128, 128) 
        # there are total 128 possible notes

        # self.velocityMatrix = MusicGenerator.make2dList()
        # self.ticks = MusicGenerator.make2dList()

m = MusicGenerator()
m.trainMIDIFile("happy_birthday.mid")



