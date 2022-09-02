# mod2asylum.py
# meant for creation of new Asylum Music Format files
# so that one could add new music to the Crusader games
# creator based on OpenMPT's loader code and comparing AMFs in a hex editor
# by RocketeerEatingEggs

import sys
import math

ModPeriodTable = [
    0,    12928,12192,11520,10848,10240, 9664, 9120, 8608, 8128, 7680, 7248,
     3424, 3232, 3048, 2880, 2712, 2560, 2416, 2280, 2152, 2032, 1920, 1812, # octave 1
     1712, 1616, 1524, 1440, 1356, 1280, 1208, 1140, 1076, 1016,  960,  906, # octave 2
      856,  808,  762,  720,  678,  640,  604,  570,  538,  508,  480,  453, # octave 3, amiga
      428,  404,  381,  360,  339,  320,  302,  285,  269,  254,  240,  226, # octave 4, amiga
      214,  202,  190,  180,  170,  160,  151,  143,  135,  127,  120,  113, # octave 5, amiga
      107,  101,   95,   90,   85,   80,   75,   71,   67,   63,   60,   56, # octave 6
       53,   50,   47,   45,   42,   40,   37,   35,   33,   31,   30,   28, # octave 7
       26,   25,   23,   22,   21,   20,   18,   17,   16,   15,   15,   14, # octave 8
    0
    ]

ModChannelsTable = [
    "1CHN","2CHN","3CHN","M.K.","5CHN","6CHN","7CHN","8CHN"
    ]

def compareMagic(magic):
    for i in range(8):
        if magic == ModChannelsTable[i]:
            return i + 1
    return 0

def periodToNote(lower, upper):
    newPeriod = (upper << 8) + lower
    for i in range(len(ModPeriodTable)):
        if (ModPeriodTable[i] > newPeriod) and (ModPeriodTable[i+1] < newPeriod):
            return i
        if ModPeriodTable[i] == newPeriod:
            return i
    return 0

# repurposed from mod2ptm, hence why some of the globals are the same
with open(sys.argv[2], "wb+") as PTMfile:
    with open(sys.argv[1], "rb") as MODfile:
        MODfile.seek(1080)
        numChannels = compareMagic(str(MODfile.read(4), encoding="utf-8"))
        if numChannels != 8:
            print("Not an 8 channel MOD")
        else:
            PTMfile.write(b"ASYLUM Music Format V1.0")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00")
            MODfile.seek(950)
            numOrders = int.from_bytes(MODfile.read(1), byteorder="big")
            restartPosition = MODfile.read(1)
            numPatterns = 0
            for i in range(numOrders):
                patternNumber = int.from_bytes(MODfile.read(1), byteorder="big")
                if patternNumber > numPatterns:
                    numPatterns = patternNumber
            numPatterns = numPatterns + 1
            PTMfile.write((6).to_bytes(1, byteorder="little"))
            PTMfile.write((125).to_bytes(1, byteorder="little"))
            PTMfile.write((31).to_bytes(1, byteorder="little"))
            PTMfile.write(numPatterns.to_bytes(1, byteorder="little"))
            PTMfile.write(numOrders.to_bytes(1, byteorder="little"))
            PTMfile.write(restartPosition)
            MODfile.seek(952)
            PTMfile.write(MODfile.read(128))
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            MODfile.seek(20)
            smpLengths = []
            for i in range(31):
                smpName = MODfile.read(22)
                PTMfile.write(smpName)
                smpLength = int.from_bytes(MODfile.read(2), byteorder="big") * 2
                smpLengths.append(smpLength)
                smpLengthBytes = smpLength.to_bytes(2, byteorder="little")
                smpFinetune = MODfile.read(1)
                PTMfile.write(smpFinetune)
                smpVolume = MODfile.read(1)
                PTMfile.write(smpVolume)
                PTMfile.write(b"\x00")
                smpRepStart = int.from_bytes(MODfile.read(2), byteorder="big") * 2
                smpRepLength = int.from_bytes(MODfile.read(2), byteorder="big") * 2
                smpRepStartBytes = smpRepStart.to_bytes(2, byteorder="little")
                PTMfile.write(smpLengthBytes)
                PTMfile.write(b"\x00\x00")
                PTMfile.write(smpRepStartBytes)
                PTMfile.write(b"\x00\x00")
                smpRepLengthBytes = smpRepLength.to_bytes(2, byteorder="little")
                PTMfile.write(smpRepLengthBytes)
                PTMfile.write(b"\x00\x00")
            for i in range(33):
                PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                PTMfile.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                PTMfile.write(b"\x00\x00\x00\x00\x00")
            MODfile.seek(1084)
            for patternNumber in range(numPatterns):
                for rowNumber in range(64):
                    for channelNumber in range(numChannels):
                        eventPart1 = int.from_bytes(MODfile.read(1), byteorder="little")
                        lowerPeriod = int.from_bytes(MODfile.read(1), byteorder="little")
                        eventPart3 = int.from_bytes(MODfile.read(1), byteorder="little")
                        effectParam = int.from_bytes(MODfile.read(1), byteorder="little")
                        upperPeriod = eventPart1 & 15
                        note = periodToNote(lowerPeriod, upperPeriod)
                        instrument = (((eventPart1 & 240) << 4) | (eventPart3 & 240)) >> 4
                        effectNumber = eventPart3 & 15
                        PTMfile.write(note.to_bytes(1, byteorder="big"))
                        PTMfile.write(instrument.to_bytes(1, byteorder="big"))
                        PTMfile.write(effectNumber.to_bytes(1, byteorder="big"))
                        PTMfile.write(effectParam.to_bytes(1, byteorder="big"))
            for i in range(31):
                smpl = MODfile.read(smpLengths[i])
                PTMfile.write(smpl)
