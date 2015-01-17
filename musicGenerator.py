# file which generates random music using markov chains and some machine 
# learning to generate completely new music on it's own
# all music training and generation is done in midi format

import midi, random, os


# @TODO Figure out how to deal with velocity, and ticks
# also when to do off
class MusicGenerator(object):
    @staticmethod
    def make2dList(rows = 0, cols = 0, value = 0):
        ls = list()
        for row in xrange(rows):
            ls += [[value]*cols]
        return ls

    @staticmethod
    def maxItemLength(a):
        # from 112 class website
        maxLen = 0
        rows = len(a)
        cols = len(a[0])
        for row in xrange(rows):
            for col in xrange(cols):
                maxLen = max(maxLen, len(str(a[row][col])))
        return maxLen

    @staticmethod
    def print2dList(a):
        # from 112 class website
        if (a == []):
            # So we don't crash accessing a[0]
            print []
            return
        rows = len(a)
        cols = len(a[0])
        fieldWidth = MusicGenerator.maxItemLength(a)
        print "[ ",
        for row in xrange(rows):
            if (row > 0): print "\n  ",
            print "[ ",
            for col in xrange(cols):
                if (col > 0): print ",",
                # The next 2 lines print a[row][col] with the given fieldWidth
                format = "%" + str(fieldWidth) + "s"
                print format % str(a[row][col]),
            print "]",
        print "]"

    def parseMIDIFile(self, path): 
        # returns array of pitch, velocity and ticks in a midi file
        pattern = midi.read_midifile(path)
        # print pattern
        pitches, velocities, ticks = ([] , [], [])
        for musicEvent in pattern[1]:
            if type(musicEvent) == midi.NoteOnEvent:
                # note starts
                # print musicEvent
                pitches.append((musicEvent.pitch))
                velocities.append((musicEvent.velocity))
                ticks.append((musicEvent.tick))
            elif type(musicEvent) == midi.NoteOffEvent:
                # note ended
                # print musicEvent
                pitches.append((musicEvent.pitch))
                velocities.append((musicEvent.velocity))
                ticks.append((musicEvent.tick))
            elif type(musicEvent) == midi.ProgramChangeEvent:
                # print "Midi %d"%musicEvent.data[0]
                pass
            elif type(musicEvent) == midi.EndOfTrackEvent : 
                # track has ended
                pass
                # print "finished"
        return pitches, velocities, ticks

    def trainMIDIFileFromPath(self, path):
        pitches, velocities, ticks = self.parseMIDIFile(path)
        self.trainPitchesFromMIDIFile(pitches)

    def trainPitchesFromMIDIFile(self, pitches):
        if pitches:
            curNote = pitches[0]
            for note in pitches[1:]:
                self.pitchMatrix[curNote].append(note)
                # print curNote, note
                curNote = note


    def __init__(self):
        self.pitchMatrix = MusicGenerator.make2dList(128, 0) 
        # there are total 128 possible notes

        # self.velocityMatrix = MusicGenerator.make2dList()
        # self.ticks = MusicGenerator.make2dList()

    def generateMusic(self, numNotes):
        # returns an array of computer generated notes using markov chains
        l = range(128)
        random.shuffle(l)
        for lastNote in l:
            if self.pitchMatrix[lastNote]:
                break
        generatedMusicNotes = [lastNote]
        # MusicGenerator.print2dList(self.pitchMatrix)
        for index in xrange(numNotes-1): # already added one note
            noteProbablityList = self.pitchMatrix[lastNote]
            if lastNote in noteProbablityList:
                # @TODO: Naively biased for now to keep next note away different note
                noteProbablityList.pop(noteProbablityList.index(lastNote))
            nextNote = random.choice(noteProbablityList)
            while self.pitchMatrix[nextNote] == []:
                nextNote = random.choice(noteProbablityList)
            # print generatedMusicNotes, noteProbablityList, nextNote
            generatedMusicNotes.append(nextNote)
            lastNote = nextNote
        # print generatedMusicNotes
        return generatedMusicNotes

    def createMIDIFromNotesList(self, notes, nameOfGeneratedFile = "example10.mid"):
        pattern = midi.Pattern()
        # Instantiate a MIDI Track (contains a list of MIDI events)
        track = midi.Track()
        # Append the track to the pattern
        pattern.append(track)
        # Instantiate a MIDI note on event, append it to the track
        tickVal = 200
        for note in notes:
            on = midi.NoteOnEvent(tick=0, velocity=50, pitch=note)
            track.append(on)
            # Instantiate a MIDI note off event, append it to the track
            off = midi.NoteOffEvent(tick=tickVal, pitch=note)
            track.append(off)
            tickVal -= 1
        # Add the end of track event, append it to the track
        eot = midi.EndOfTrackEvent(tick=1)
        track.append(eot)
        # Print out the pattern
        # print pattern
        # Save the pattern to disk
        midi.write_midifile("generatedMidiFiles/%s"%nameOfGeneratedFile, pattern)

    def train(self, path):
        for filename in os.listdir(path):
            if filename.endswith("mid") or filename.endswith("midi"):
                self.trainMIDIFileFromPath(path + os.sep + filename)
        


m = MusicGenerator()
# m.trainMIDIFile("trainingMidiFiles/Beatles1HB.mid")
# m.trainMIDIFileFromPath("trainingMidiFiles/happy_birthday.mid")
m.train("/Users/manikpanwar/Desktop/Manik/Git/Music-Dash/trainingMidiFiles/set1")
soundFile = m.createMIDIFromNotesList(m.generateMusic(1000), "bigmidifile.mid")



