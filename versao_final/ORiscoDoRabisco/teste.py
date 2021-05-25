from sys import platform
print(platform)
if platform == "win32":
    print(__file__.rsplit("\\",1)[0] + " <== caminho do arquivo")
else:
    print(__file__.rsplit("/",1)[0] + " <== caminho do arquivo")