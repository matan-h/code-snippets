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
    ext = ".bin"

exe_file = os.path.join("dist", "snippets") + ext


def run(*args):
    args = " ".join(args)
    subprocess.check_call(args, shell=True)


def compile_exe(debug=False):
    run(
        "pyinstaller",
        "--onefile",
        "--windowed" if not debug else '',
        "--icon icon.ico",
        "--name snippets",
        "--add-data icon.ico",
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
            valid()

    compile_exe()

    if os.path.exists(exe_file):
        print("exe_file:", exe_file)
    else:
        print("exe_file not found...", "here is dir:", os.listdir())
        if os.path.exists("dist"):
            print("dir of dist:", os.listdir("dist"))

    print("done")
