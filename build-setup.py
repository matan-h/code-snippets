from os import path, system

for p in (
path.expandvars("%LOCALAPPDATA%\Programs"),
path.expandvars("%ProgramFiles(x86)%"),
path.expandvars("%ProgramFiles%")):
    if path.exists(f"{p}\Inno Setup 6\iscc.exe"):
        system(f"{p}\Inno Setup 6\iscc.exe setup.iss")
        break
