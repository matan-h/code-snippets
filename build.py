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
    subprocess.check_call(args, shell=True)


def compile_exe(debug=False):
    d = ";" if os.name == "nt" else ":"  # ; for windows, : in linux

    run(
        "pyinstaller",
        "--onefile",
        "--windowed" if not debug else '',
        "--icon icon.ico",
        "--name snippets",
        "--add-data icon.ico"+d+".",
        "main.py"
    )


def valid():
    compile_exe(debug=True)
    p = subprocess.Popen(exe_file)
    time.sleep(4)
    if p.poll() is not None:
        if p.returncode != 0:
            raise Exception(f"error when run snippets.exe - {p.returncode}")
    p.kill()
    print("done debug")


if __name__ == '__main__':
    a = sys.argv[1:]
    if a:
        if a[0].lower().strip() == "debug":
            print("start debug")
            valid()

    compile_exe()

    if os.path.exists(exe_file):
        print("exe_file:", exe_file)
        if os.path.isdir(exe_file):
            print("isdir !!!")
            print("listdir:",os.listdir(exe_file))
            ffd = exe_file

            while os.path.isdir(ffd):
                print(f"listdir of :",ffd,":")
                l = os.listdir(ffd)
                if l:
                    ffd = l[0]

    else:
        print("exe_file not found...", "here is dir:", os.listdir())
        if os.path.exists("dist"):
            print("dir of dist:", os.listdir("dist"))

    print("done")
