from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("dmextender_main.py", base=base)]

packages = ["idna", "sys"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "<applic>",
    options = options,
    version = "0.1",
    description = '',
    executables = executables
)