import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Absensi Face Recognition",
    version = "0.1",
    description = "Membuat absensi dengan face recognition",
    executables = [Executable("main.py", base=base)]
)