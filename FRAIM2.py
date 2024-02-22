from fer import FER
import cv2
import music21 as mus
import random
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

whole = mus.duration.Duration(4)
half = mus.duration.Duration(2)
halfTriplet = mus.duration.Duration(3)
quarter = mus.duration.Duration(1)
eighth = mus.duration.Duration(1/2)
triplet = mus.duration.Duration(1/3)
major = mus.interval.Interval('M3')
minor = mus.interval.Interval('m3')
fifth = mus.interval.Interval('P5')
minSev = mus.interval.Interval("m7")
notes = [mus.note.Note('c2'), mus.note.Note('d-2'), mus.note.Note('d2'), mus.note.Note('e-2'), mus.note.Note('e2'), 
        mus.note.Note('f2'), mus.note.Note('g-2'), mus.note.Note('g2'), mus.note.Note('a-2'), mus.note.Note('a2'),  
        mus.note.Note('b-2'), mus.note.Note('b2'),mus.note.Note('c3'), mus.note.Note('d-3'), mus.note.Note('d3'), mus.note.Note('e-3'), mus.note.Note('e3'), 
        mus.note.Note('f3'), mus.note.Note('g-3'), mus.note.Note('g3'), mus.note.Note('a-3'), mus.note.Note('a3'),  
        mus.note.Note('b-3'), mus.note.Note('b3'), mus.note.Note('c4'), mus.note.Note('d-4'), mus.note.Note('d4'), 
        mus.note.Note('e-4'), mus.note.Note('e4'), mus.note.Note('f4'), mus.note.Note('g-4'), mus.note.Note('g4'), 
        mus.note.Note('a-4'), mus.note.Note('a4'), mus.note.Note('b-4'), mus.note.Note('b4')]
progression = []
happyArray = [["I", "vi", "IV", "V"], ["i", "VI", "III", "VII"], ["I", "IV", "V", "V7"],
            ["I", "III", "IV", "IV"], ["I", "IV", "vi", "V"], ["I", "II7", "IV", "I"],
            ["IV", "I", "V", "vii7"], ["I", "FLAT VII", "IV", "I"],
            ["I", "vi", "III", "V"], ["ii", "iii", "I", "IV"],["IV", "FLAT VII7", "IV", "I"]]
sadArray = [["vi", "IV", "I", "V"], ["vi", "iii", "V", "IV"], ["I", "iii", "IV", "V"], 
            ["I", "vi", "ii", "V"], ["i", "i7", "IV7", "VI"], ["i", "VII", "IV", "IV"],
            ["i", "VII", "VI", "V7"], ["i", "VI", "v", "v"], ["iii", "ii", "I", "I"],
            ["i", "V7", "VII", "IV"], ["I", "V", "vi", "IV"],
            ["I", "v", "v", "ii"], ["ii7", "V7", "I7", "vi7"], ["IV", "V", "I", "vi7"], 
            ["IV", "V", "iii", "vi"], ["i", "IV", "vi", "III"]]
romanNumeralsMajTonic = {"I7": 0, "i": 0, "I": 0, "II7": 2, "ii": 2, "ii7": 2, "iii": 4, "III": 4, "IV": 5, "V7": 7, "V": 7, "v": 7, "vi/3": 0, "vi": 9, "vi7": 9, "FLAT VII7": 10, "FLAT VII": 10, "viio": 11, "vii7": 11}
romanNumeralsMinTonic = {"I7": 0, "I": 0, "i": 0, "i7": 0, "ii": 2, "ii7": 2, "iio": 2, "iii": 3, "III": 3, "IV7": 5, "IV": 5, "iv": 5, "V7": 7, "V": 7, "v": 7, "vi": 8, "VI": 8, "FLAT` VII7": 9, "FLAT VII": 9, "VII": 10}

# cd C:\Users\siddh\OneDrive\Documents\cosmos\FRAIM\testimages

root = Tk()
root.title('FRAIM')
root.geometry('620x480+50+50')
root['background']= '#cc1d3d'
root.resizable(False, False)
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, padding = 20, justify= "center", text="Hi, we are MIND GOBLIN Software and welcome to FRAIM! \nPress the button to open your webcam and press space to generate music based on your facial expression. \nThe software will be able to tell if you are happy, sad, angry, or surprised.").grid(column=0, row=1)
ttk.Button(frm, text="Continue", command=root.destroy,width=50,padding=30).grid(column=0,row=2)
img = ImageTk.PhotoImage(Image.open("LOGO.png"))
ttk.Label(frm, image = img).grid(column=0,row=0,pady=20)
root.mainloop()

cam = cv2.VideoCapture(0)
cv2.namedWindow("FRAIM")

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("FRAIM", frame)
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame.png"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))

        #emotion detector
        emotion_detector = FER(mtcnn=True)
        test_img = cv2.imread("opencv_frame.png")
        analysis = emotion_detector.detect_emotions(test_img)
        dominant_emotion, emotion_score = emotion_detector.top_emotion(test_img)
        print(dominant_emotion)
        
        # music 21
        s = mus.stream.Score()
        stream1 = mus.stream.Part()

        if dominant_emotion == "sad" or dominant_emotion == "neutral":
            a = random.randint(0,15)
            progression = sadArray[a]
        else:
            a = random.randint(0,10)
            progression = happyArray[a]

        if dominant_emotion == "sad" or dominant_emotion == "neutral" or dominant_emotion == "happy":
            print (progression)
            pos1 = random.randint(11,23)
            if progression[0].isupper() or progression[0] == "ii7" or progression[0] == "iii" or progression[0] == "vi":
                for i in range(4):
                    if i == 0:
                        x1 = notes[pos1]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([x1, major.transposeNote(x1), fifth.transposeNote(x1)], duration = whole)
                            else:
                                chord = mus.chord.Chord([x1, major.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = whole)
                        elif progression[i].islower():
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([x1, minor.transposeNote(x1), fifth.transposeNote(x1)], duration = whole)
                            else:
                                chord = mus.chord.Chord([x1, minor.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = whole)
                    if i == 1:
                        x2 = notes[pos1 + (romanNumeralsMajTonic[progression[1]] - romanNumeralsMajTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([x2, major.transposeNote(x2), fifth.transposeNote(x2)], duration = whole)
                            else:
                                chord2 = mus.chord.Chord([x2, major.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = whole)
                        elif progression[i].islower():
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([x2, minor.transposeNote(x2), fifth.transposeNote(x2)], duration = whole)
                            else:
                                chord2 = mus.chord.Chord([x2, minor.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = whole)
                    if i == 2:
                        x3 = notes[pos1 + (romanNumeralsMajTonic[progression[2]] - romanNumeralsMajTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([x3, major.transposeNote(x3), fifth.transposeNote(x3)], duration = whole)
                            else:
                                chord3 = mus.chord.Chord([x3, major.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = whole)
                        elif progression[i].islower():
                            chord3 = mus.chord.Chord([x3, minor.transposeNote(x3), fifth.transposeNote(x3)], duration = whole)
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([x3, minor.transposeNote(x3), fifth.transposeNote(x3)], duration = whole)
                            else:
                                chord3 = mus.chord.Chord([x3, minor.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = whole)
                    if i == 3:
                        x4 = notes[pos1 + (romanNumeralsMajTonic[progression[3]] - romanNumeralsMajTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([x4, major.transposeNote(x4), fifth.transposeNote(x4)], duration = whole)
                            else:
                                chord4 = mus.chord.Chord([x4, major.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = whole)
                        elif progression[i].islower():
                            chord4 = mus.chord.Chord([x4, minor.transposeNote(x4), fifth.transposeNote(x4)], duration = whole)
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([x4, minor.transposeNote(x4), fifth.transposeNote(x4)], duration = whole)
                            else:
                                chord4 = mus.chord.Chord([x4, minor.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = whole)
            elif progression[0].islower():
                for i in range(4):
                    if i == 0:
                        x1 = notes[pos1]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([x1, major.transposeNote(x1), fifth.transposeNote(x1)], duration = whole)
                            else:
                                chord = mus.chord.Chord([x1, major.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = whole)
                        elif progression[i].islower():
                            chord = mus.chord.Chord([x1, minor.transposeNote(x1), fifth.transposeNote(x1)], duration = whole)
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([x1, minor.transposeNote(x1), fifth.transposeNote(x1)], duration = whole)
                            else:
                                chord = mus.chord.Chord([x1, minor.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = whole)
                    if i == 1:
                        x2 = notes[pos1 + (romanNumeralsMinTonic[progression[1]] - romanNumeralsMinTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([x2, major.transposeNote(x2), fifth.transposeNote(x2)], duration = whole)
                            else:
                                chord2 = mus.chord.Chord([x2, major.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = whole)
                        elif progression[i].islower():
                            chord2 = mus.chord.Chord([x2, minor.transposeNote(x2), fifth.transposeNote(x2)], duration = whole)
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([x2, minor.transposeNote(x2), fifth.transposeNote(x2)], duration = whole)
                            else:
                                chord2 = mus.chord.Chord([x2, minor.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = whole)
                    if i == 2:
                        x3 = notes[pos1 + (romanNumeralsMinTonic[progression[2]] - romanNumeralsMinTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([x3, major.transposeNote(x3), fifth.transposeNote(x3)], duration = whole)
                            else:
                                chord3 = mus.chord.Chord([x3, major.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = whole)
                        elif progression[i].islower():
                            chord3 = mus.chord.Chord([x3, minor.transposeNote(x3), fifth.transposeNote(x3)], duration = whole)
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([x3, minor.transposeNote(x3), fifth.transposeNote(x3)], duration = whole)
                            else:
                                chord3 = mus.chord.Chord([x3, minor.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = whole)
                    if i == 3:
                        x4 = notes[pos1 + (romanNumeralsMinTonic[progression[3]] - romanNumeralsMinTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([x4, major.transposeNote(x4), fifth.transposeNote(x4)], duration = whole)
                            else:
                                chord4 = mus.chord.Chord([x4, major.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = whole)
                        elif progression[i].islower():
                            chord4 = mus.chord.Chord([x4, minor.transposeNote(x4), fifth.transposeNote(x4)], duration = whole)
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([x4, minor.transposeNote(x4), fifth.transposeNote(x4)], duration = whole)
                            else:
                                chord4 = mus.chord.Chord([x4, minor.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = whole)
            
            stream1.append(chord)
            stream1.append(chord2)
            stream1.append(chord3)
            stream1.append(chord4)

        if dominant_emotion == "angry":
            for i in range(0,4):
                x = notes[random.randint(0,7)]
                chord = mus.chord.Chord([x, major.transposeNote(x), fifth.transposeNote(x)], duration = quarter)
                stream1.repeatAppend(chord, 4)

        if dominant_emotion == "surprise":       
            print (progression)
            pos1 = random.randint(11,23)
            if progression[0].isupper():
                for i in range(4):
                    if i == 0:
                        x1 = notes[pos1]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([major.transposeNote(x1), fifth.transposeNote(x1)], duration = halfTriplet)
                            else:
                                chord = mus.chord.Chord([major.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = halfTriplet)
                        elif progression[i].islower():
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([minor.transposeNote(x1), fifth.transposeNote(x1)], duration = halfTriplet)
                            else:
                                chord = mus.chord.Chord([minor.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = halfTriplet)
                    if i == 1:
                        x2 = notes[pos1 + (romanNumeralsMajTonic[progression[1]] - romanNumeralsMajTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([major.transposeNote(x2), fifth.transposeNote(x2)], duration = halfTriplet)
                            else:
                                chord2 = mus.chord.Chord([major.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = halfTriplet)
                        elif progression[i].islower():
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([minor.transposeNote(x2), fifth.transposeNote(x2)], duration = halfTriplet)
                            else:
                                chord2 = mus.chord.Chord([minor.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = halfTriplet)
                    if i == 2:
                        x3 = notes[pos1 + (romanNumeralsMajTonic[progression[2]] - romanNumeralsMajTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([major.transposeNote(x3), fifth.transposeNote(x3)], duration = halfTriplet)
                            else:
                                chord3 = mus.chord.Chord([major.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = halfTriplet)
                        elif progression[i].islower():
                            chord3 = mus.chord.Chord([minor.transposeNote(x3), fifth.transposeNote(x3)], duration = halfTriplet)
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([minor.transposeNote(x3), fifth.transposeNote(x3)], duration = halfTriplet)
                            else:
                                chord3 = mus.chord.Chord([minor.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = halfTriplet)
                    if i == 3:
                        x4 = notes[pos1 + (romanNumeralsMajTonic[progression[3]] - romanNumeralsMajTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([major.transposeNote(x4), fifth.transposeNote(x4)], duration = halfTriplet)
                            else:
                                chord4 = mus.chord.Chord([major.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = halfTriplet)
                        elif progression[i].islower():
                            chord4 = mus.chord.Chord([minor.transposeNote(x4), fifth.transposeNote(x4)], duration = halfTriplet)
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([minor.transposeNote(x4), fifth.transposeNote(x4)], duration = halfTriplet)
                            else:
                                chord4 = mus.chord.Chord([minor.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = halfTriplet)
            elif progression[0].islower():
                for i in range(4):
                    if i == 0:
                        x1 = notes[pos1]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([major.transposeNote(x1), fifth.transposeNote(x1)], duration = halfTriplet)
                            else:
                                chord = mus.chord.Chord([major.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = halfTriplet)
                        elif progression[i].islower():
                            chord = mus.chord.Chord([minor.transposeNote(x1), fifth.transposeNote(x1)], duration = halfTriplet)
                            if progression[i].find("7") == -1:
                                chord = mus.chord.Chord([minor.transposeNote(x1), fifth.transposeNote(x1)], duration = halfTriplet)
                            else:
                                chord = mus.chord.Chord([minor.transposeNote(x1), fifth.transposeNote(x1), minSev.transposeNote(x1)], duration = halfTriplet)
                    if i == 1:
                        x2 = notes[pos1 + (romanNumeralsMinTonic[progression[1]] - romanNumeralsMinTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([major.transposeNote(x2), fifth.transposeNote(x2)], duration = halfTriplet)
                            else:
                                chord2 = mus.chord.Chord([major.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = halfTriplet)
                        elif progression[i].islower():
                            chord2 = mus.chord.Chord([minor.transposeNote(x2), fifth.transposeNote(x2)], duration = halfTriplet)
                            if progression[i].find("7") == -1:
                                chord2 = mus.chord.Chord([minor.transposeNote(x2), fifth.transposeNote(x2)], duration = halfTriplet)
                            else:
                                chord2 = mus.chord.Chord([minor.transposeNote(x2), fifth.transposeNote(x2), minSev.transposeNote(x2)], duration = halfTriplet)
                    if i == 2:
                        x3 = notes[pos1 + (romanNumeralsMinTonic[progression[2]] - romanNumeralsMinTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([major.transposeNote(x3), fifth.transposeNote(x3)], duration = halfTriplet)
                            else:
                                chord3 = mus.chord.Chord([major.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = halfTriplet)
                        elif progression[i].islower():
                            chord3 = mus.chord.Chord([minor.transposeNote(x3), fifth.transposeNote(x3)], duration = halfTriplet)
                            if progression[i].find("7") == -1:
                                chord3 = mus.chord.Chord([minor.transposeNote(x3), fifth.transposeNote(x3)], duration = halfTriplet)
                            else:
                                chord3 = mus.chord.Chord([minor.transposeNote(x3), fifth.transposeNote(x3), minSev.transposeNote(x3)], duration = halfTriplet)
                    if i == 3:
                        x4 = notes[pos1 + (romanNumeralsMinTonic[progression[3]] - romanNumeralsMinTonic[progression[0]])]
                        if progression[i].isupper():
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([major.transposeNote(x4), fifth.transposeNote(x4)], duration = halfTriplet)
                            else:
                                chord4 = mus.chord.Chord([major.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = halfTriplet)
                        elif progression[i].islower():
                            chord4 = mus.chord.Chord([minor.transposeNote(x4), fifth.transposeNote(x4)], duration = halfTriplet)
                            if progression[i].find("7") == -1:
                                chord4 = mus.chord.Chord([minor.transposeNote(x4), fifth.transposeNote(x4)], duration = halfTriplet)
                            else:
                                chord4 = mus.chord.Chord([minor.transposeNote(x4), fifth.transposeNote(x4), minSev.transposeNote(x4)], duration = halfTriplet)  
         
            stream1.append(chord)
            stream1.append(chord2)
            stream1.append(chord3)
            stream1.append(chord4)

            x = notes[pos1 + 8]
            chord = mus.chord.Chord([x, minor.transposeNote(x), fifth.transposeNote(x)], duration = triplet)
            stream1.repeatAppend(chord, 12)   

        s.append(stream1)  
        if dominant_emotion == "sad" or dominant_emotion == "neutral":      
            hiHatNote = mus.note.Note(42, quarterLength=1)
            snareNote = mus.note.Note(38, quarterLength=3)
            snareNote2 = mus.note.Note(38, quarterLength=1)
            snareNote3 = mus.note.Note(38, quarterLength=2)
            bassNote = mus.note.Note(35, quarterLength=1)
            bassNote2 = mus.note.Note(35, quarterLength=3)
            bassNote3 = mus.note.Note(35, quarterLength=1/2)
            quarterRest = mus.note.Rest()
            hiHat = mus.instrument.HiHatCymbal()
            snareDrum = mus.instrument.BassDrum()
            bassDrum = mus.instrument.BassDrum()
            hiHatPart = mus.stream.Part()
            snareDrumPart = mus.stream.Part()
            bassDrumPart = mus.stream.Part()
            hiHatPart.insert(hiHat)
            snareDrumPart.insert(snareDrum)
            bassDrumPart.insert(bassDrum)
            hiHatPart.repeatAppend(hiHatNote, 16)
            for i in range(0,4):
                if random.randint(1,2) == 1:
                    snareDrumPart.repeatAppend(snareNote,1)
                    snareDrumPart.repeatAppend(snareNote2,1)
                else:
                    snareDrumPart.repeatAppend(snareNote3,1)
                    snareDrumPart.repeatAppend(snareNote2,2)
            for i in range(0,4):
                if random.randint(1,2) == 1:
                    bassDrumPart.repeatAppend(bassNote,1)
                    bassDrumPart.repeatAppend(bassNote2,1)
                else:
                    bassDrumPart.repeatAppend(quarterRest,1)
                    bassDrumPart.repeatAppend(bassNote3,2)
                    bassDrumPart.repeatAppend(quarterRest,1)
                    bassDrumPart.repeatAppend(bassNote3,2)
            s.insert(0, hiHatPart)
            s.insert(0, snareDrumPart)
            s.insert(0, bassDrumPart)

        if dominant_emotion == "happy":
            hiHatNote = mus.note.Note(42, quarterLength=1)
            hiHatNote2 = mus.note.Note(42, quarterLength=2/3)
            hiHatNote3 = mus.note.Note(42, quarterLength=1/3)
            hiHatNote4 = mus.note.Note(42, quarterLength=1/2)
            snareNote = mus.note.Note(38, quarterLength=3/2)
            snareNote2 = mus.note.Note(38, quarterLength=1)
            bassNote = mus.note.Note(35, quarterLength=1/2)
            bassNote2 = mus.note.Note(35, quarterLength=2)
            quarterRest = mus.note.Rest()
            hiHat = mus.instrument.HiHatCymbal()
            snareDrum = mus.instrument.BassDrum()
            bassDrum = mus.instrument.BassDrum()
            hiHatPart = mus.stream.Part()
            snareDrumPart = mus.stream.Part()
            bassDrumPart = mus.stream.Part()
            hiHatPart.insert(hiHat)
            snareDrumPart.insert(snareDrum)
            bassDrumPart.insert(bassDrum)
            for i in range(0,4):
                snareDrumPart.repeatAppend(snareNote,2)
                snareDrumPart.repeatAppend(snareNote2,1)
            if random.randint(1,2) == 1:
                for i in range(0,4):
                    hiHatPart.repeatAppend(hiHatNote,3)
                    hiHatPart.repeatAppend(hiHatNote2,1)
                    hiHatPart.repeatAppend(hiHatNote3,1)
            else:
                hiHatPart.repeatAppend(hiHatNote4,32)
            for i in range(0,4):
                if random.randint(1,2) == 1:
                    bassDrumPart.repeatAppend(bassNote2,2)
                else:
                    bassDrumPart.repeatAppend(bassNote,2)
                    bassDrumPart.repeatAppend(quarterRest,1)
                    bassDrumPart.repeatAppend(bassNote,2)
                    bassDrumPart.repeatAppend(quarterRest,1)
            s.insert(0, hiHatPart)
            s.insert(0, snareDrumPart)
            s.insert(0, bassDrumPart)

        if dominant_emotion == "angry":
            hiHatNote = mus.note.Note(42, quarterLength=1/2)
            snareNote = mus.note.Note(38, quarterLength=1/2)
            bassNote = mus.note.Note(35, quarterLength=1/2)
            eightRest = mus.note.Rest(quarterLength=1/2)
            hiHat = mus.instrument.HiHatCymbal()
            snareDrum = mus.instrument.BassDrum()
            bassDrum = mus.instrument.BassDrum()
            hiHatPart = mus.stream.Part()
            snareDrumPart = mus.stream.Part()
            bassDrumPart = mus.stream.Part()
            hiHatPart.insert(hiHat)
            snareDrumPart.insert(snareDrum)
            bassDrumPart.insert(bassDrum)
            hiHatPart.repeatAppend(hiHatNote,32)
            for i in range(0,16):
                snareDrumPart.repeatAppend(snareNote,1)
                bassDrumPart.repeatAppend(bassNote,1)
                bassDrumPart.repeatAppend(eightRest,1)
                snareDrumPart.repeatAppend(eightRest,1)
            s.insert(0, hiHatPart)
            s.insert(0, snareDrumPart)
            s.insert(0, bassDrumPart)

        s.show()

cam.release()
cv2.destroyAllWindows()

#0 I - vi - IV - V (Example: C-Am-F-G)
#1 i - VI - III - VII (Example: Am-F-C-G)
#2 I - IV - V - V7 (Example: G-C-D-D7)
#3 I - III - IV - IV (interlude progression; Example: G-Bb-C)
#4 I - IV - vi - V (Example: C-F-Am-G)
#5 I - II7 - IV - I (Example: C-D7-F-C)
#6 IV - I - IV - V - IV - I - V - viio (Example: F-C-F-G-F-C-F-Bdim.) - Happy
#7 I - flat VII - IV - I (Example: C-Bb-F-C) - Happy
#8 I - vi - V/vi - V (Example: C-Am-E-G) - Happy
#9 I - vi/3 - I - vi/3 - ii - iii(or V) - IV - V (Example: C-Am/C-C-Am/C-Dm-Em(or G)-F-G) - Happy
#10 I - I - I - I - IV - IV - I - I - V - IV - I - I (Example: C-C-C-C-F-F-C-C-G-F-C-C) - Happy
#11 IV - flat VII(or flat VII7) - I - I (Example: F-Bb(or Bb7)-C-C) - Triumphant

#0 vi - IV - I - V (Example: Am-F-C-G)
#1 vi - iii - V - IV (Example: Am-Em-G-F)
#2 I - iii - IV - V (Example: C-Em-F-G)
#3 I - vi - ii(or iii) - V (Example: C-Am-Dm(or Em)-G)
#4 i - i/7 - IV/flat 4 - VI (Example: Am-Am/G-D/F#-F)
#5 i - VII - IV - IV (Example: Bm-A-E-E)
#6 i - VII - VI- V7 (Example: Am-G-F-E7)
#7 i - VI - v -v (Example: Am-F-Em-Em)
#8 iii - ii - I - I (interlude progression; Example: Em-Dm-C-C)
#9 i - V - i - flat VII - flat III - i - V (Example: Am-E7-Am-G-C-G-Am-E7)
#10 I - V - vi - IV (Example: C-G-Am-F) - Sad
#11 I - v - v - ii (Example: C-Gm-Gm-Dm) - Sad
#12 ii7 - V7 - I7 - vi(or IV) (Example: Dm7-G7-CMaj7-Am(or F)) - sad (chord progression of prom dress by mxmtoon)
#13 IV - V - I - vi7 (Example: F-G-C-Am7) - bright with a bit of sad
#14 IV(or ii7) - V - iii - vi (Example: F(or Dm7)-G-Em-Am) - Sadder
#15 IV - V - vi - i (Example: D-E-Fm-Am) - Scared?           

#TO DO

#Code the notes that have a chord over a note
# meaning the note on the bottom is not the start of the actual chord

#Code the melody
# Maybe get an AI to do it

#Code the rest of the emotions
# Do tempo and pitch changes

#Dynamics

#Make the program able to handle more than four chords

#Add in a beat (like drums)

#tkinter for ui