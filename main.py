storedBlocks = [None] * 3

def get_block(workingFile, blockNumber, memoryDest):
    workingFile.seek(blockNumber * 512)
    storedBlocks[memoryDest] = workingFile.read(512)

def print_file(filename):
    workingFile = open(filename, "rb")

    get_block(workingFile, 0, 0)

    workingFile.close()

print_file("test.idx")
