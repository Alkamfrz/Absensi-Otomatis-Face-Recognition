import imutils
import cv2
import json
import pickle
import face_recognition
import os
import tkinter as tk
import main

from tkinter import *
from tkinter import messagebox

def recognition():
    if not os.path.exists("encodings.pickle"):
        messagebox.showerror("Error", "Data mahasiswa tidak ditemukan")
        main.gui_main()
        return
    data = pickle.loads(open("encodings.pickle", "rb").read())
    with open("mahasiswa.json", "r") as f:
        data_mahasiswa = json.load(f)
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        frame = imutils.resize(frame, width=500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        nims = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                data["encodings"], encoding, tolerance=0.4)
            name = "Unknown"
            nim = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    names.append(name)
                    for i in data_mahasiswa["mahasiswa"]:
                        if i["nama"] == name:
                            nim = i["nim"]
                            nims.append(nim)
            else:
                names.append(name)
                nims.append(nim)
        for ((top, right, bottom, left), name, nim) in zip(boxes, names, nims):
            if name == "Unknown":
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            y = top - 15 if top - 15 > 15 else top + 15
            if name == "Unknown":
                cv2.putText(frame, name, (left, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
            else:
                cv2.putText(frame, name, (left, y-25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
                cv2.putText(frame, nim, (left, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        cv2.imshow("Detektor Wajah", frame)
        if cv2.waitKey(1) == 27:
            break
        if cv2.getWindowProperty("Detektor Wajah", cv2.WND_PROP_VISIBLE) < 1:
            break
    video_capture.release()
    cv2.destroyAllWindows()
    main.gui_main()

if __name__ == "__main__":
    recognition()