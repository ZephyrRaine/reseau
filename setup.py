from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("client.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':'threading,socket,sys,tkinter'
    },

}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)