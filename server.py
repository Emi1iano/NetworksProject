from socket import *


import os
import time
import shutil
import pickle
import dir

serverPort = 4343
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

songFolderPath = "F:\\Code\\Networks\\Song 1"#"F:\\Games\\Clone Hero\\songsdsa"
ServerSongs = dir.allSongNames(songFolderPath)

def printServerSongNames():
    count = 1
    for Song in ServerSongs:
        print(str(count) + ": " + Song)
        count += 1

print("The server is ready to receive...")
while True:
    message, clientAddress = serverSocket.recvfrom(1024)
    print("Sent " + str(len(ServerSongs)) + " songs")
    serverSocket.sendto(pickle.dumps(ServerSongs), clientAddress)

    SongRequest, clientAddress = serverSocket.recvfrom(1024)
    SongRequest = pickle.loads(SongRequest)
    
    root = os.path.abspath(songFolderPath)
    
    for dirpath, dirs, _ in os.walk(root):
        for dir in dirs:
            if SongRequest == dir:
                shutil.make_archive(SongRequest, 'zip', os.path.join(dirpath, dir))
                break
                
    print("Requested the song " + SongRequest)
    with open(SongRequest + ".zip", 'rb') as f:
        while True:
            bytes_read = f.read(32768)
            if not bytes_read:
                break
            serverSocket.sendto(bytes_read, clientAddress)
            time.sleep(.01)
            #print(f"Sent {len(bytes_read)} bytes.")
            
        time.sleep(.01)
        serverSocket.sendto(b"EOF", clientAddress)
        print("File sent successfully.")
    
    time.sleep(1)    
    os.remove(SongRequest + ".zip")