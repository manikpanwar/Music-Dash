# file which generates random music using markov chains and some machine 
# learning to generate completely new music on it's own
# all music training and generation is done in midi format

import midi, random, os, pygame
import pygame.midi, pygame.mixer
from time import sleep

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
        try:
            pattern = midi.read_midifile(path)
        except:
            print "Error in %s"%path
            return
        # print pattern
        pitches, velocities, ticks = ([] , [], [])
        try:
            p = pattern[1]
        except:
            p = pattern
        # print p
        for musicEvent in p:
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
        a = self.parseMIDIFile(path)
        if a:
            pitches, velocities, ticks = a
            self.trainPitchesFromMIDIFile(pitches)
        else:
            print "weird data set"

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
            # if lastNote in noteProbablityList:
            #     # @TODO: Naively biased for now to keep next note away different note
            #     noteProbablityList.pop(noteProbablityList.index(lastNote))
            nextNote = random.choice(noteProbablityList)
            #  or (nextNote == lastNote and nextNote == noteProbablityList[-2]
            # work on repetitions
            while (self.pitchMatrix[nextNote] == [] or (nextNote == lastNote and 
                (len(noteProbablityList)>=2 and nextNote == noteProbablityList[-2]))):
                nextNote = random.choice(noteProbablityList)
            # print generatedMusicNotes, noteProbablityList, nextNote
            generatedMusicNotes.append(nextNote)
            lastNote = nextNote
        # print generatedMusicNotes
        return generatedMusicNotes

    def createMIDIFromNotesList(self, notes, nameOfGeneratedFile = "example.mid",
                                tickVal = 200):
        pattern = midi.Pattern()
        # Instantiate a MIDI Track (contains a list of MIDI events)
        track = midi.Track()
        # Append the track to the pattern
        pattern.append(track)
        # Instantiate a MIDI note on event, append it to the track
        for note in notes:
            on = midi.NoteOnEvent(tick=0, velocity=70, pitch=note)
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
        if not os.path.isdir(path):
            if (path.endswith("mid") or path.endswith("midi") or 
                            path.endswith("MID") or path.endswith("MIDI")):
                # print os.path.basename(path)
                self.trainMIDIFileFromPath(path)
        else:
            for filename in os.listdir(path):
                self.train(path + os.sep + filename)
        # at this point could save matrix to text file
        # so don't have to train all the time
        
    def playNoteOneAtATime(self, note, velocity = 127, tickVal = 1000):
        pattern = midi.Pattern()
        # Instantiate a MIDI Track (contains a list of MIDI events)
        track = midi.Track()
        # Append the track to the pattern
        pattern.append(track)
        # Instantiate a MIDI note on event, append it to the track
        on = midi.NoteOnEvent(tick=0, velocity=70, pitch=note)
        track.append(on)
        # Instantiate a MIDI note off event, append it to the track
        off = midi.NoteOffEvent(tick=tickVal, pitch=note)
        track.append(off)
        # Add the end of track event, append it to the track
        eot = midi.EndOfTrackEvent(tick=1)
        track.append(eot)
        # Save the pattern to disk
        midi.write_midifile("generatedMidiFiles/%s"%"temp.mid", pattern)
        pygame.init()
        pygame.mixer.music.load("generatedMidiFiles/%s"%"temp.mid")
        pygame.mixer.music.play()


# m = MusicGenerator()
# m.trainMIDIFile("trainingMidiFiles/Beatles1HB.mid")
# m.trainMIDIFileFromPath("trainingMidiFiles/happy_birthday.mid")

# m.train("/Users/manikpanwar/Desktop/Manik/Git/Music-Dash/trainingMidiFiles/MozartCMajor")
# m.createMIDIFromNotesList(m.generateMusic(200), "mozartC1.mid")

# m.playNoteOneAtATime(64)



