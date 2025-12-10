import os
from re import L
import sys

offset = 2  #How far the data is from the start of the file
storedBlocks = [bytearray(b'\x00' * 512), bytearray(b'\x00' * 512), bytearray(b'\x00' * 512)]
magicNumber = int.from_bytes("4348PRJ3".encode('ascii'), byteorder = 'big', signed=False)


def get_field(workingBlockID, index):
    index = index * 8
    if index > 512 or index < 0:
        print("ERROR: invalid field index")
        sys.exit()

    return int.from_bytes(storedBlocks[workingBlockID][index: index + 8].replace(b" ", b""), byteorder = 'big', signed=False)

def set_field(workingBlockID, index, value):
    if isinstance(value, str):
        value = value.encode('ascii')
    elif isinstance(value, int):
        value = int.to_bytes(value, 8, byteorder='big', signed=False)

    index = index * 8
    if index > 512 or index < 0:
        print("ERROR: invalid field index")
        sys.exit()

    k = 0
    for i in range(index, index + 8):
        storedBlocks[workingBlockID][i] = value[k]
        k += 1

def get_block(workingFile, blockNumber, memoryDest):
    if workingFile.mode != "rb":
        print("ERROR: incorrect file mode in get_block")
        sys.exit()

    workingFile.seek(blockNumber * 512 + offset)

    storedBlocks[memoryDest] = workingFile.read(512)

def print_block(memoryDest):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Block ID: {get_field(memoryDest, 0)}")
    print(f"Block Parent ID: {get_field(memoryDest, 1)}")
    print(f"Block Size: {get_field(memoryDest, 2)}")
    print("Block Keys:\t", end = '')
    for i in range(0, 18):
        print(f"{get_field(memoryDest, 3 + i)}", end = ',')
    print(f"{get_field(memoryDest, 3 + 18)}")
    print("Block Values:\t", end = '')
    for i in range(0, 18):
        print(f"{get_field(memoryDest, 3 + 19 + i)}", end = ',')
    print(f"{get_field(memoryDest, 3 + 20 + i)}")
    print("Block Pointers:\t", end = '')
    for i in range(0, 19):
        print(f"{get_field(memoryDest, 3 + 19 + 19 + i)}", end = ',')
    print(f"{get_field(memoryDest, 3 + 19 + 19)}")

def set_block(filename, blockNumber):
    workingFile = open(filename, "wb")

    workingFile.seek(blockNumber * 512 + offset)

    workingFile.write(storedBlocks[blockNumber])

    workingFile.close()

def create_file(filename):
    if os.path.exists(filename):
        print("ERROR: file already exists")
        sys.exit()

    set_field(0, 0, "4348PRJ3")
    set_field(0, 1, 0)
    set_field(0, 2, 1)

    set_block(filename, 0)

def search_file(filename, val):
    try:
        workingFile = open(filename, "rb")
    except FileNotFoundError:
        print("ERROR: file not found")
        sys.exit()

    get_block(workingFile, 0, 0)
    nextBlock = get_field(0, 1)
    print_block(0)

    while True:
        nextBlock = nextBlock = 1
        get_block(workingFile, nextBlock, 0)
        blockSize = get_field(0, 2)

        if get_field(0, 2) == 0:
            break

        if val < get_field(0, 3):
            nextBlock = get_field(0, 3 + 19 + 19)
            continue

        if val > get_field(0, 2 + blockSize):
            nextBlock = get_field(0, 3 + 19 + 19 + blockSize)
            continue

        for i in range(0, blockSize):
            workingKey = get_field(0, i + 3)
            if workingKey == val:
                print(f"{get_field(0, i + 3)},{get_field(0, i + 19 + 3)}")
                return
            
            if i < blockSize:
                if val > workingKey and val < get_field(0, i + 1 + 3):
                    nextBlock = get_field(0, 3 + 19 + 19 + i + 1)
                    break

    print(f"ERROR: unable to find index {val} in file {filename}")

def print_file(filename):
    try:
        workingFile = open(filename, "rb")
    except FileNotFoundError:
        print("ERROR: file not found")
        sys.exit()

    get_block(workingFile, 0, 0)
    if(get_field(0, 0) != magicNumber):
        print("ERROR: improper file format")
        workingFile.close()
        sys.exit()

    totalBlocks = get_field(0, 2)
    for i in range(1, totalBlocks):
        get_block(workingFile, i, 0)
        numKeys = get_field(0, 2)
        for k in range(1, numKeys + 1):
            print(f"{get_field(0, k + 2)},{get_field(0, k + 19 + 2)}")

    workingFile.close()

def extract_file(sourceFileName, destFileName):
    try:
        sourceFile = open(sourceFileName, "rb")
    except FileNotFoundError:
        print("ERROR: file not found")
        sys.exit()

    get_block(sourceFile, 0, 0)
    if(get_field(0, 0) != magicNumber):
        print("ERROR: improper source file format")
        sourceFile.close()
        sys.exit()

    if os.path.exists(destFileName):
        print("ERROR: destination file already exists")
        sys.exit()

    destFile = open(destFileName, "w")

    totalBlocks = get_field(0, 2)
    for i in range(1, totalBlocks):
        get_block(sourceFile, i, 0)
        numKeys = get_field(0, 2)
        for k in range(1, numKeys + 1):
            destFile.write(f"{get_field(0, k + 2)},{get_field(0, k + 19 + 2)}\n")

    sourceFile.close()
    destFile.close()

if len(sys.argv) < 2:
    print("Error: no arguments given")
    sys.exit()

task = sys.argv[1]
if task == "create":
    if len(sys.argv) < 3:
        print("ERROR: missing file name")
    else:
        create_file(sys.argv[2])
if task == "search":
    if len(sys.argv) < 3:
        print("ERROR: no file given")
    elif len(sys.argv) < 4:
        print("ERROR: no index given")
    elif not sys.argv[3].isdigit():
        print("ERROR: index must be unsigned integer")
    else:
        if int(sys.argv[3]) < 0:
            print("ERROR: index must be unsigned integer")
        search_file(sys.argv[2], int(sys.argv[3]))
elif task == "print":
    if len(sys.argv) > 2:
        print_file(sys.argv[2])
    else:
        print("ERROR: no file given")
elif task == "extract":
    if len(sys.argv) < 3:
        print("ERROR: missing source file")
    elif len(sys.argv) < 4:
        print("ERROR: missing destination file")
    else:
        extract_file(sys.argv[2], sys.argv[3])
else:
    print("ERROR: incrorrect command")
