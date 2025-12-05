import sys

offset = 2  #How far the data is from the start of the file
storedBlocks = [None] * 3

def get_field(workingBlock, index):
    index = index * 8
    if index > 512 or index < 0:
        print("ERROR: invalid field index")
        sys.exit()

    return int.from_bytes(workingBlock[index: index + 8].replace(b" ", b""), byteorder = 'big')

def get_block(workingFile, blockNumber, memoryDest):
    workingFile.seek(blockNumber * 512 + offset)

    storedBlocks[memoryDest] = workingFile.read(512)

def print_file(filename):
    workingFile = open(filename, "rb")

    get_block(workingFile, 0, 0)
    get_block(workingFile, 1, 1)
    get_block(workingFile, 2, 2)

    workingFile.close()

print_file("test.idx")

print(storedBlocks[0])
print("------------------------------------")
print(get_field(storedBlocks[0], 2))
print("------------------------------------")
print(storedBlocks[1])
print("------------------------------------")
print(storedBlocks[2])
