import keyboard
import threading

isPlaying = False
storedIndex = 0
conversionCases = {'!': '1', '@': '2', '£': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0'}

key_delete = 'delete'
key_shift = 'shift'
key_end = 'end'
key_home = 'home'

def onDelPress(event):
    global isPlaying
    isPlaying = not isPlaying

    if isPlaying:
        print("Playing...")
        playNextNote()
    else:
        print("Stopping...")

    return True

def isShifted(charIn):
    asciiValue = ord(charIn)
    if 65 <= asciiValue <= 90:
        return True
    if charIn in "!@#$%^&*()_+{}|:\"<>?":
        return True
    return False

def pressLetter(strLetter):
    if isShifted(strLetter):
        strLetter = conversionCases.get(strLetter, strLetter)
        keyboard.release(strLetter.lower())
        keyboard.press(key_shift)
        keyboard.press(strLetter.lower())
        keyboard.release(key_shift)
    else:
        keyboard.release(strLetter)
        keyboard.press(strLetter)

def releaseLetter(strLetter):
    if isShifted(strLetter):
        strLetter = conversionCases.get(strLetter, strLetter)
        keyboard.release(strLetter.lower())
    else:
        keyboard.release(strLetter)

def processFile():
    try:
        with open("song.txt", "r") as macro_file:
            lines = macro_file.read().split("\n")
            if len(lines) < 2:
                raise ValueError("Invalid file format")

            tOffsetSet = False
            tOffset = 0
            playback_speed = float(lines[0].split("=")[1])
            print(f"Playback speed is set to {playback_speed:.2f}")
            tempo = 60 / float(lines[1].split("=")[1])

            processedNotes = [[float(l[0]), l[1]] for l in (line.split() for line in lines[1:]) if len(l) >= 2]

            if not tOffsetSet:
                tOffset = processedNotes[0][0]
                print("Start time offset =", tOffset)
                tOffsetSet = True

        return [tempo, tOffset, processedNotes]
    except FileNotFoundError:
        print("Error: File not found")
        return None
    except (ValueError, IndexError):
        print("Error: Invalid file format")
        return None

def parseInfo():
    tempo = infoTuple[0]
    notes = infoTuple[2][1:]

    for i in range(len(notes) - 1):
        note = notes[i]
        nextNote = notes[i + 1]
        if "tempo" in note[1]:
            tempo = 60 / float(note[1].split("=")[1])
            notes.pop(i)
            note = notes[i]
            if i < len(notes) - 1:
                nextNote = notes[i + 1]
        else:
            note[0] = (nextNote[0] - note[0]) * tempo

    notes[-1][0] = 1.00

    return notes

def playNextNote():
    global isPlaying
    global storedIndex

    notes = infoTuple[2]
    if isPlaying and storedIndex < len(infoTuple[2]):
        noteInfo= notes[storedIndex]
        delay = max(noteInfo[0], 0)

        if noteInfo[1][0] == "~":
            for n in noteInfo[1][1:]:
                releaseLetter(n)
        else:
            for n in noteInfo[1]:
                pressLetter(n)
        if "~" not in noteInfo[1]:
            print("%10.2f %15s" % (delay, noteInfo[1]))
        storedIndex += 1
        if delay == 0:
            playNextNote()
        else:
            threading.Timer(delay / playback_speed, playNextNote).start()
    elif storedIndex > len(infoTuple[2]) - 1:
        isPlaying = False
        storedIndex = 0

def rewind(KeyboardEvent):
    global storedIndex
    if storedIndex - 10 < 0:
        storedIndex = 0
    else:
        storedIndex -= 10
    print("Rewound to %.2f" % storedIndex)

def skip(KeyboardEvent):
    global storedIndex
    if storedIndex + 10 > len(infoTuple[2]):
        isPlaying = False
        storedIndex = 0
    else:
        storedIndex += 10
    print("Skipped to %.2f" % storedIndex)

def main():
    global isPlaying
    global infoTuple
    global playback_speed

    infoTuple = processFile()

    if infoTuple is None:
        return

    infoTuple[2] = parseInfo()

    keyboard.on_press_key(key_delete, onDelPress)
    keyboard.on_press_key(key_home, rewind)
    keyboard.on_press_key(key_end, skip)

    print()
    print("Controls")
    print("-" * 20)
    print("Press DELETE to play/pause")
    print("Press HOME to rewind")
    print("Press END to advance")
    while True:
        input("Press Ctrl+C or close window to exit\n\n")

if __name__ == "__main__":
    main()
