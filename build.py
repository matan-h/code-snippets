import os
import subprocess
import platform
import sys
import time

platform = platform.system()

file = "main.py"

if platform == "Windows":
    ext = '.exe'
elif platform == "Darwin":
    ext = ".app"
else:
    ext = ""

exe_file = os.path.join("dist", "snippets") + ext


def run(*args):
    args = " ".join(args)
    return subprocess.check_call(args, shell=True)


def compile_exe(debug=False, my_computer: bool = False):
    d = ";" if os.name == "nt" else ":"  # ; for windows, : in linux
    tk_arg = ''
    if my_computer:  # in my computer - I need to add tk to the exe
        from tkinter import Tcl
        tk_path: str = Tcl().eval("info library").split("\n")[0].strip()
        tk_arg = "--add-data " + tk_path + d + os.path.join("tcl", os.path.basename(tk_path))

    return run(
        "pyinstaller",
        "--onefile",
        "--windowed" if not debug else '',
        "--icon icon.ico",
        "--name snippets",
        "--add-data icon.ico" + d + ".",
        tk_arg,
        "main.py"
    )


def valid(my_computer: bool = False):
    compile_exe(debug=True, my_computer=my_computer)
    p = subprocess.Popen(exe_file)
    time.sleep(5)
    if p.poll() is not None:
        if p.returncode != 0:
            raise Exception(f"error when run snippets.exe - {p.returncode}")
    subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=p.pid))
    print("done debug")


if __name__ == '__main__':
    a = sys.argv[1:]
    if a:
        if a[0].lower().strip() == "debug":
            print("start debug")
            valid(bool(a[1:]))

    compile_exe()

    if os.path.exists(exe_file):
        print("exe_file:", exe_file)
        if os.path.isdir(exe_file):
            print("exe_file is dir ")
            print("listdir:", os.listdir(exe_file))

    else:
        print("exe file not found...", "here is dir:", os.listdir())

    if os.path.exists("dist"):
        print("dir of dist:", os.listdir("dist"))

    print("done")
