offset = 2  #How far the data is from the start of the file
storedBlocks = [None] * 3

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
print(int.from_bytes(storedBlocks[0][16:24].replace(b" ", b""), byteorder = 'big'))
print("------------------------------------")
print(storedBlocks[1])
print("------------------------------------")
print(storedBlocks[2])
