from os import path
from subprocess import check_call
for p in (
path.expandvars("%LOCALAPPDATA%\Programs"),
path.expandvars("%ProgramFiles(x86)%"),
path.expandvars("%ProgramFiles%")):
    if path.exists(f"{p}\Inno Setup 6\iscc.exe"):
        check_call([f"{p}\Inno Setup 6\iscc.exe","setup.iss"])
        break
