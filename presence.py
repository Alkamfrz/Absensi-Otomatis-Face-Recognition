import cv2
import os
import face_recognition
import pickle
import json
import datetime
import csv
import main

from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno


def make_dir():
    if not os.path.exists("Data Absensi"):
        os.makedirs("Data Absensi")
    if not os.path.exists("Data Absensi/Check In"):
        os.makedirs("Data Absensi/Check In")
    if not os.path.exists("Data Absensi/Check Out"):
        os.makedirs("Data Absensi/Check Out")

def make_csv_check_in():
    if not os.path.exists("Data Absensi/Check In/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"):
        with open("Data Absensi/Check In/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["No", "NIM", "Nama", "Tanggal", "Waktu"])

def make_csv_check_out():
    if not os.path.exists("Data Absensi/Check Out/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"):
        with open("Data Absensi/Check Out/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["No", "NIM", "Nama", "Tanggal", "Waktu"])

def check_in():
    make_dir()
    make_csv_check_in()
    if not os.path.exists("encodings.pickle"):
        messagebox.showerror("Error", "Data mahasiswa tidak ditemukan")
        return
    messagebox.showinfo("Check-in", "Mohon menghadap ke kamera dan menunggu proses absensi selesai")
    data = pickle.loads(open("encodings.pickle", "rb").read())
    with open("mahasiswa.json", "r") as f:
        data_mahasiswa = json.load(f)
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
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
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if len(names) > 0:
            if names[0] != "Unknown":
                with open("Data Absensi/Check In/{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), "r") as f:
                    reader = csv.reader(f, delimiter=";")
                    for row in reader:
                        if names[0] in row:
                            messagebox.showinfo(
                                "Check-out", "Nama: {}\nNIM: {}\nAnda sudah melakukan check-in hari ini".format(names[0], nims[0]))
                            video_capture.release()
                            cv2.destroyAllWindows()
                            return
                if askyesno("Check-in", "Nama: {}\nNIM: {}\nApakah data tersebut sudah benar?".format(names[0], nims[0])):
                    with open("Data Absensi/Check In/{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), "r") as f:
                        reader = csv.reader(f, delimiter=";")
                        data = list(reader)
                        nomor = len(data)
                    with open("Data Absensi/Check In/{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), "a", newline="") as f:
                        writer = csv.writer(f, delimiter=";")
                        writer.writerow([nomor, nims[0], names[0], datetime.datetime.now().strftime(
                            "%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M")])
                        messagebox.showinfo("Check-in", "Check-in Berhasil")
                        video_capture.release()
                        cv2.destroyAllWindows()
                        return
                else:
                    messagebox.showinfo("Check-in", "Check-in dibatalkan")
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return
            else:
                messagebox.showinfo("Check-in", "Anda belum terdaftar")
                video_capture.release()
                cv2.destroyAllWindows()
                return
    video_capture.release()
    cv2.destroyAllWindows()

def check_out():
    make_dir()
    make_csv_check_out()
    if not os.path.exists("encodings.pickle"):
        messagebox.showerror("Error", "Data mahasiswa tidak ditemukan")
        return
    messagebox.showinfo("Check-out", "Mohon menghadap ke kamera dan menunggu proses absensi selesai")
    data = pickle.loads(open("encodings.pickle", "rb").read())
    with open("mahasiswa.json", "r") as f:
        data_mahasiswa = json.load(f)
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
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
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if len(names) > 0:
            if names[0] != "Unknown":
                with open("Data Absensi/Check Out/{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), "r") as f:
                    reader = csv.reader(f, delimiter=";")
                    for row in reader:
                        if names[0] in row:
                            messagebox.showinfo(
                                "Check-out", "Nama: {}\nNIM: {}\nAnda sudah melakukan check-out hari ini".format(names[0], nims[0]))
                            video_capture.release()
                            cv2.destroyAllWindows()
                            return
                if askyesno("Check Out", "Nama: {}\nNIM: {}\nApakah data tersebut sudah benar?".format(names[0], nims[0])):
                    with open("Data Absensi/Check Out/{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), "r") as f:
                        reader = csv.reader(f, delimiter=";")
                        data = list(reader)
                        nomor = len(data)
                    with open("Data Absensi/Check Out/{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d")), "a", newline="") as f:
                        writer = csv.writer(f, delimiter=";")
                        writer.writerow([nomor, nims[0], names[0], datetime.datetime.now().strftime(
                            "%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M")])
                        messagebox.showinfo("Check-out", "Check-out Berhasil")
                        video_capture.release()
                        cv2.destroyAllWindows()
                        return
                else:
                    messagebox.showinfo("Check-out", "Check-out dibatalkan")
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return
            else:
                messagebox.showinfo("Check-out", "Anda belum terdaftar")
                video_capture.release()
                cv2.destroyAllWindows()
                return
    video_capture.release()
    cv2.destroyAllWindows()

def gui_absen():
    window = Tk()
    window.title("Absensi")
    window.geometry("400x200")
    window.resizable(False, False)
    Label(window, text="REKAM ABSENSI", font=("Arial", 20)).pack()
    btn_check_in = Button(window, text="Check-in", command=check_in)
    btn_check_in.place(x=50, y=50, width=150, height=100)
    btn_check_out = Button(window, text="Check-out", command=check_out)
    btn_check_out.place(x=200, y=50, width=150, height=100)

    def close_window():
        window.destroy()
        main.gui_main()

    window.protocol("WM_DELETE_WINDOW", close_window)
    window.mainloop()
    
if __name__ == "__main__":
    gui_absen()
    main.gui_main()