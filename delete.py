import json
from logging import root
import tkinter as tk
import pickle
import shutil
import main

from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno


def hapus_data(nim):
    with open("mahasiswa.json", "r") as f:
        data = json.load(f)
    for i in data["mahasiswa"]:
        if i["nim"] == nim:
            nama = i["nama"]
            break
    shutil.rmtree("dataset/" + nama)
    data = pickle.loads(open("encodings.pickle", "rb").read())
    data["encodings"].pop(data["names"].index(nama))
    data["names"].remove(nama)
    f = open("encodings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()
    data = []
    with open("mahasiswa.json", "r") as f:
        data = json.load(f)
    for i in data["mahasiswa"]:
        if i["nim"] == nim:
            data["mahasiswa"].remove(i)
            break
    with open("mahasiswa.json", "w") as f:
        json.dump(data, f)
    messagebox.showinfo("Informasi", "Data berhasil dihapus")

def gui_hapus():
    root = tk.Tk()
    root.title("Hapus Data")
    root.resizable(False, False)
    nim = StringVar()
    label = tk.Label(root, text="Masukkan NIM yang akan dihapus",
                     font=("Arial", 10), anchor="w", justify="center")
    label.grid(row=0, column=1, padx=5, pady=5)
    entry = tk.Entry(root, textvariable=nim, width=30,
                     justify="center", border=2, relief="groove")
    entry.grid(row=1, column=1, padx=17, pady=5)
    entry.insert(0, "Masukkan NIM")
    entry.config(fg="grey", font="Arial 10 italic")
    entry.focus_set()

    def focus_in(event):
        if entry.get() == "Masukkan NIM":
            entry.delete(0, "end")
            entry.config(fg="black", font="Arial 10")

    def focus_out(event):
        if entry.get() == "":
            entry.insert(0, "Masukkan NIM")
            entry.config(fg="grey", font="Arial 10 italic")

    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)

    def hapus():
        if nim.get() == "":
            messagebox.showerror("Error", "NIM tidak boleh kosong")
        else:
            with open("mahasiswa.json", "r") as f:
                data = json.load(f)
            for i in data["mahasiswa"]:
                if i["nim"] == nim.get():
                    if askyesno("Konfirmasi", "Apakah anda yakin ingin menghapus data " + i["nama"] + " (" + i["nim"] + ")?"):
                        hapus_data(nim.get())
                        root.destroy()
                        main.gui_main()
                    break
            else:
                messagebox.showerror("Error", "NIM tidak ditemukan")

    def batal():
        root.destroy()
        main.gui_main()
    button = tk.Button(root, text="Hapus", command=hapus, width=10, height=1, font="normal 10", relief="flat", bg="#ff0000", fg="white", activebackground="#ff0000",
                       activeforeground="white", cursor="hand2", highlightthickness=0, padx=5, pady=5, overrelief="flat", bd=0, highlightbackground="#ff0000", highlightcolor="#ff0000")
    button.grid(row=2, column=0, padx=5, pady=5, sticky="w", columnspan=2)
    button = tk.Button(root, text="Batal", command=batal, width=10, height=1, font="normal 10", relief="flat", bg="#0000ff", fg="white", activebackground="#0000ff",
                       activeforeground="white", cursor="hand2", highlightthickness=0, padx=5, pady=5, overrelief="flat", bd=0, highlightbackground="#0000ff", highlightcolor="#0000ff")
    button.grid(row=2, column=0, padx=5, pady=5, sticky="e", columnspan=2)
    root.bind("<Return>", lambda event: hapus())
    root.bind("<Escape>", lambda event: batal())
    root.protocol("WM_DELETE_WINDOW", batal)
    root.mainloop()


if __name__ == "__main__":
    gui_hapus()
    main.gui_main()