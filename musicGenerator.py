# file which generates random music using markov chains and some machine 
# learning to generate completely new music on it's own
# all music training and generation is done in midi format

import midi

class MusicGenerator(object):
    @staticmethod
    def make2dHash(rows = 0, cols = 0):
        ls = dict()
        for row in xrange(rows):
            for col in xrange(cols):
                ls[row][col] = dict()
        return ls

    def parseMIDIFile(self, path): 
        # returns array of pitch, velocity and ticks in a midi file
        pattern = midi.read_midifile(path)
        pitch, velocity, ticks = ([] , [], [])
        # print pattern
        for musicEvent in pattern[1]:
            if type(musicEvent) == midi.NoteOnEvent:
                # note starts
                print musicEvent
                ticks.append(musicEvent.tick)
            elif type(musicEvent) == midi.NoteOffEvent:
                # note ended
                print musicEvent
            elif type(musicEvent) == midi.ProgramChangeEvent:
                print "Midi %d"%musicEvent.data[0]
            elif type(musicEvent) == midi.EndOfTrackEvent : 
                # track has ended
                print "finished"
        return pitch, velocity, ticks

    def trainMIDIFile(self, path):
        pitch, velocity, ticks = self.parseMIDIFile(path)
        print pitch, velocity, ticks

    def __init__(self):
        # just gonna work with the pitch matrix right now
        self.pitchMatrix = MusicGenerator.make2dList()
        # self.velocityMatrix = MusicGenerator.make2dList()
        # self.ticks = MusicGenerator.make2dList()

m = MusicGenerator()
m.trainMIDIFile("happy_birthday.mid")



