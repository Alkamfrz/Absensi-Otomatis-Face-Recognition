import cv2
import os
import json
import tkinter as tk
import training
import main

from tkinter import *
from tkinter import messagebox


def gui_capture():
    make_dir()
    make_json()
    with open("mahasiswa.json", "r") as f:
        data = json.load(f)
    popup = tk.Tk()
    popup.wm_title("Tambah Data")
    popup.resizable(False, False)
    label = tk.Label(popup, text="Nama", width=5, anchor="w",
                     relief="groove", borderwidth=1)
    label.grid(row=0, column=0, padx=5, pady=5)
    label2 = tk.Label(popup, text="NIM", width=5, anchor="w",
                      relief="groove", borderwidth=1)
    label2.grid(row=1, column=0, padx=5, pady=5)
    nama = tk.Entry(popup, justify="center", width=25, relief="solid")
    nama.grid(row=0, column=1, padx=5, pady=5)
    nim = tk.Entry(popup, justify="center", width=25, relief="solid")
    nim.grid(row=1, column=1, padx=5, pady=5)
    nama.insert(0, "Masukkan nama")
    nim.insert(0, "Masukkan NIM")
    nama.config(fg="grey", font="italic 10")
    nim.config(fg="grey", font="italic 10")

    def enter(event):
        if nama.get() == "Masukkan nama" or nim.get() == "Masukkan nim":
            messagebox.showerror("Error", "Nama dan NIM tidak boleh kosong")
        elif nama.get() == "" or nim.get() == "":
            messagebox.showerror("Error", "Nama dan NIM tidak boleh kosong")
        elif nim.get().isdigit() == False:
            messagebox.showerror("Error", "NIM harus berupa angka")
        elif nim.get() in [i["nim"] for i in data["mahasiswa"]]:
            messagebox.showerror("Error", "NIM sudah terdaftar")
        else:
            tambah(nama.get(), nim.get())
            capture(nama.get(), nim.get())
            popup.destroy()
            main.gui_main()

    def on_entry_click(event):
        if event.widget.get() == "Masukkan nama" or event.widget.get() == "Masukkan NIM":
            event.widget.delete(0, "end")
            event.widget.config(fg="black", font="normal 10")

    def on_focusout(event):
        if event.widget.get() == "":
            event.widget.insert(
                0, "Masukkan nama" if event.widget == nama else "Masukkan NIM")
            event.widget.config(fg="grey", font="italic 10")

    nama.bind('<FocusIn>', on_entry_click)
    nama.bind('<FocusOut>', on_focusout)
    nim.bind('<FocusIn>', on_entry_click)
    nim.bind('<FocusOut>', on_focusout)

    def ok():
        if nama.get() == "Masukkan nama" or nim.get() == "Masukkan nim":
            messagebox.showerror("Error", "Nama dan nim tidak boleh kosong")
        elif nama.get() == "" or nim.get() == "":
            messagebox.showerror("Error", "Nama dan nim tidak boleh kosong")
        elif nim.get().isdigit() == False:
            messagebox.showerror("Error", "NIM harus berupa angka")
        elif nim.get() in [i["nim"] for i in data["mahasiswa"]]:
            messagebox.showerror("Error", "NIM sudah terdaftar")
        else:
            tambah(nama.get(), nim.get())
            capture(nama.get(), nim.get())
            popup.destroy()
            main.gui_main()

    def cancel():
        popup.destroy()
        main.gui_main()
    
    def batal():
        popup.destroy()
        main.gui_main()

    ok = tk.Button(popup, text="Simpan", command=ok, width=10, height=1, font="normal 10", relief="flat", bg="#00b894", fg="white", activebackground="#00b894",
                   activeforeground="white", cursor="hand2", bd=0, highlightthickness=0, padx=5, pady=5, overrelief="flat", highlightbackground="#00b894", highlightcolor="#00b894")
    ok.grid(row=2, column=0, padx=5, pady=5, sticky="e", columnspan=2)
    cancel = tk.Button(popup, text="Batal", command=cancel, width=10, height=1, font="normal 10", relief="flat", bg="#d63031", fg="white", activebackground="#d63031",
                       activeforeground="white", cursor="hand2", bd=0, highlightthickness=0, padx=5, pady=5, overrelief="flat", highlightbackground="#d63031", highlightcolor="#d63031")
    cancel.grid(row=2, column=0, padx=5, pady=5, sticky="w", columnspan=2)
    popup.bind('<Return>', enter)
    popup.bind('<Escape>', lambda e: main.gui_main())
    popup.protocol("WM_DELETE_WINDOW", batal)
    popup.mainloop()

def capture(nama, nim):
    messagebox.showinfo(
        "Info", "Mohon menghadap ke kamera dan menunggu proses pengambilan gambar selesai")
    if not os.path.exists("dataset/{}".format(nama)):
        os.makedirs("dataset/{}".format(nama))
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    sampleNum = 0
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            cv2.imwrite("dataset/{}/{}.jpg".format(nama,
                        sampleNum), gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.waitKey(100)
        cv2.imshow("Capturing", img)
        cv2.waitKey(1)
        if sampleNum > 0:
            break
    cam.release()
    cv2.destroyAllWindows()
    training.training()

def make_json():
    if not os.path.exists("mahasiswa.json"):
        with open("mahasiswa.json", "w") as f:
            json.dump({"mahasiswa": []}, f)


def tambah(nama, nim):
    with open("mahasiswa.json", "r") as f:
        data = json.load(f)
    data["mahasiswa"].append({"nama": nama, "nim": nim})
    with open("mahasiswa.json", "w") as f:
        json.dump(data, f, indent=4)


def make_dir():
    if not os.path.exists("dataset"):
        os.makedirs("dataset")


if __name__ == "__main__":
    gui_capture()
    main.gui_main()