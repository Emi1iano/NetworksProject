import os

def allSongNames(root):
    names = []
    root = os.path.abspath(root)
    
    for dirpath, dirs, _ in os.walk(root):
        for dir in dirs:
            names.append(dir)
            #print(dirpath + " " + dir)
    names.sort
    return names
    