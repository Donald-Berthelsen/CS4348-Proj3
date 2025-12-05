import os
import sys

offset = 2  #How far the data is from the start of the file
storedBlocks = [None] * 3
magicNumber = int.from_bytes("4348PRJ3".encode('ascii'), byteorder = 'big', signed=False)


def get_field(workingBlockID, index):
    index = index * 8
    if index > 512 or index < 0:
        print("ERROR: invalid field index")
        sys.exit()

    return int.from_bytes(storedBlocks[workingBlockID][index: index + 8].replace(b" ", b""), byteorder = 'big', signed=False)

def get_block(workingFile, blockNumber, memoryDest):
    workingFile.seek(blockNumber * 512 + offset)

    storedBlocks[memoryDest] = workingFile.read(512)

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
if task == "print":
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
