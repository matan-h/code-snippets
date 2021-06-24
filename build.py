import os
import subprocess
import sys
import time
import logging
import platform

platform = platform.system()
sys.excepthook = lambda *args: logging.exception("Uncaught exception", exc_info=args)


def error(msg, *args, exc_info=True, **kwargs):
    """logging.exception(error) and then exit"""
    if exc_info and not (sys.exc_info()):
        exc_info = False
    logging.exception(msg, *args, exc_info, **kwargs)
    quit(1)


############

file = 'main.py'
if platform == "Windows":
    exe_file = 'snippets.exe'
else:
    exe_file = "snippets.bin"
add = lambda s, l: list(map(lambda x: s + x, l))


def run(*args):
    command = ' '.join(args)
    return os.system(command)


def compile_exe(debug=False):
    plugins = ['multiprocessing', 'tk-inter', 'pylint-warnings']

    options = [
        # one file,standalone:
        'onefile',
        'windows-onefile-tempdir',
        'standalone' if not debug else None,
        # without console
        'windows-disable-console' if not debug else None,
        # Removes the build directory after producing
        'remove-output',
        'windows-icon-from-ico=icon.ico',
        'linux-onefile-icon=icon.ico'
        # todo:set icon with --windows-icon-from-ico and --linux-onefile-icon)
    ]
    options = list(filter(None, options))

    plugins = add('--plugin-enable=', plugins)
    options = add('--', options)

    # plugins = list(map(lambda x: '--plugin-enable=' + x, plugins))
    return run(
        "python -m nuitka",
        *options,
        *plugins,
        "-o " + exe_file,
        file,
    )


def valid():
    if compile_exe(debug=True) != 0:
        error("error in debug compiling")
    p = subprocess.Popen(exe_file)
    time.sleep(4)
    if p.poll() is not None:
        if p.returncode != 0:
            error(f"error when run snippets.exe - {p.returncode}")
    p.kill()
    print("done debug")


if __name__ == '__main__':
    a = sys.argv[1:]
    if a:
        if a[0].lower().strip() == "debug":
            valid()

    if compile_exe() != 0:
        error('error in normal compiling')

    print("done")
