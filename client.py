from socket import *

import os
import time
import shutil
import pickle
import dir

serverName = '127.0.0.1'
serverPort = 3232
clientSocket = socket(AF_INET, SOCK_DGRAM)

songFolderPath = "F:\\Code\\Networks\\Song 1"
ClientSongs = dir.allSongNames(songFolderPath)

message = pickle.dumps("")
clientSocket.sendto(message, (serverName, serverPort))
ServerSongs, serverAddress = clientSocket.recvfrom(8096)
ServerSongs = pickle.loads(ServerSongs)
SongsClientDoesntHave = []

def printClientSongNames():
    count = 1
    for Song in ClientSongs:
        print(str(count) + ": " + Song)
        count += 1

def findDifferingSongs():
    for Song in ServerSongs:
        if Song not in ClientSongs:
            SongsClientDoesntHave.append(Song)

def printSongsClientDoesntHave():
    print("You dont have these songs:")
    count = 1
    for Song in SongsClientDoesntHave:
        print(str(count) + ": " + Song)
        count += 1
    return count

findDifferingSongs()
while True:
    if len(SongsClientDoesntHave) == 0:
        print("You have all their songs")
        break
    NumberOfServerSongs = printSongsClientDoesntHave()
    print("Enter the index of the song you want to download: ") 
    index = 0
    while True:
        try:
            index = int(input(''))
            break
        except ValueError:
            if len(SongsClientDoesntHave) == 0:
                print("Invalid Input. No differing songs from server: ")
            elif len(SongsClientDoesntHave) == 1:
                print("Invalid Input. You only have 1 option: ")
            else:
                print("Invalid Input. Pick from " + str(0)  + "-" + str((len(SongsClientDoesntHave) - 1)))
            continue

    message = pickle.dumps(SongsClientDoesntHave[index-1])
    clientSocket.sendto(message, (serverName, serverPort))

    SongName = SongsClientDoesntHave[index-1]

    received_data = b""
    while True:
        data, serverAddress = clientSocket.recvfrom(32768)
        if not data:
            break
        if data == b"EOF":
            print(SongName + " downloaded")
            SongsClientDoesntHave.remove(SongName)
            break
        received_data += data


    SongRequestZip = SongName + "idk.zip"
    with open(SongRequestZip, 'wb') as f:
        f.write(received_data)
        f.close()
        
    os.mkdir(os.path.join(songFolderPath, SongName))
    shutil.unpack_archive(SongRequestZip, os.path.join(songFolderPath, SongName), 'zip')

    time.sleep(1)    
    os.remove(SongRequestZip)