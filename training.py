import tkinter as tk
import cv2
import os
import face_recognition
import pickle
import main

from tkinter import *
from imutils import paths
from tkinter import messagebox

def training():
    knownNames = []
    knownEncodings = []
    imagePaths = list(paths.list_images("dataset"))
    for (i, imagePath) in enumerate(imagePaths):
        print("[INFO] Memproses data {}/{}".format(i + 1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()
    messagebox.showinfo("Info", "Data mahasiswa berhasil ditambahkan")
    
if __name__ == "__main__":
    training()
    main.gui_main()