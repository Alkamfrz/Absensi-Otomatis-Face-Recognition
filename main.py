import capture
import delete
import presence
import recognize

import tkinter as tk
from tkinter import *

def gui_main():
    root = tk.Tk()
    root.title("Aplikasi Absensi")
    root.resizable(False, False)
    label = tk.Label(root, text="Pilih menu yang akan dijalankan", font=("Arial", 10), anchor="w", justify="center")
    label.grid(row=0, column=2, padx=5, pady=5, columnspan=2, sticky="we", ipadx=5, ipady=5)
    button1 = tk.Button(root, text="Tambah Data", font=("Arial", 10), command=capture.gui_capture)
    button1.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="ew", ipadx=5, ipady=5)
    button2 = tk.Button(root, text="Hapus Data", font=("Arial", 10), command=delete.gui_hapus)
    button2.grid(row=1, column=3, padx=5, pady=5, columnspan=2, sticky="ew", ipadx=5, ipady=5)
    button3 = tk.Button(root, text="Presensi", font=("Arial", 10), command=presence.gui_absen)
    button3.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky="ew", ipadx=5, ipady=5)
    button4 = tk.Button(root, text="Rekognisi", font=("Arial", 10), command=recognize.recognition)
    button4.grid(row=2, column=3, padx=5, pady=5, columnspan=2, sticky="ew", ipadx=5, ipady=5)
    button1.config(command=lambda: [root.destroy(), capture.gui_capture()])
    button2.config(command=lambda: [root.destroy(), delete.gui_hapus()])
    button3.config(command=lambda: [root.destroy(), presence.gui_absen()])
    button4.config(command=lambda: [root.destroy(), recognize.recognition()])
    root.mainloop()
if __name__ == "__main__":
    gui_main()