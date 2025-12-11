import os
import sys

offset = 2  #How far the data is from the start of the file
storedBlocks = [bytearray(b'\x00' * 512), bytearray(b'\x00' * 512), bytearray(b'\x00' * 512)]   #Initialize our 3 memory spots
magicNumber = int.from_bytes("4348PRJ3".encode('ascii'), byteorder = 'big', signed=False)   #The integer value of the magic number
keyCount = 0    #Unused, can be used to track the total number of entries in the tree

#Get a field from a block in memory
#Inputs: ID of the block in memory, index of the desired field in that block
#Outputs: The specified field as an integer
def get_field(workingBlockID, index):
    index = index * 8   #Convert index to location in block
    if index > 512 or index < 0:    #Should not be possible to trigger
        print("ERROR: invalid field index")
        sys.exit()

    return int.from_bytes(storedBlocks[workingBlockID][index: index + 8], byteorder = 'big', signed=False)

#Get a field from a block in memory
#Inputs: ID of the block in memory, index of the desired field in that block, value to set the field to
#Outputs: The specified field of the specified block in memory is changed to value
#NOTE: This method works on the block in memory, it does not change the block in the file
def set_field(workingBlockID, index, value):
    if isinstance(value, str):  #Value can be either a string or an int, both are converted to bytes
        value = value.encode('ascii')
    elif isinstance(value, int):
        value = int.to_bytes(value, 8, byteorder='big', signed=False)

    index = index * 8
    if index > 512 or index < 0:
        print("ERROR: invalid field index")
        sys.exit()

    k = 0
    for i in range(index, index + 8):   #Store the byte value on the block in memory
        storedBlocks[workingBlockID][i] = value[k]
        k += 1

#Retrieve a block from the file
#Inputs: File to read from, index of the block on file, index of location in memory to put block
#Outputs: The specified block is copied from the file to memory
def get_block(workingFile, blockNumber, memoryDest):
    if workingFile.mode != "rb":    #Check if the file is in the correct mode
        print("ERROR: incorrect file mode in get_block")
        sys.exit()

    workingFile.seek(blockNumber * 512 + offset)    #Retrieve the specific block we want
    storedBlocks[memoryDest] = bytearray(workingFile.read(512))
    if storedBlocks[memoryDest] == b'': #Special case for if we are reading past the end of the file
        storedBlocks[memoryDest] = bytearray(b'\x00' * 512)

#Print a block from memory in a more human readable form
#Inputs: Index of block in memory to print
#Outputs: The block of memory is printed to console
#NOTE: Does not have a special format for the headder, fields will be correct but mislabled
def print_block(memoryDest):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Block ID: {get_field(memoryDest, 0)}")
    print(f"Block Parent ID: {get_field(memoryDest, 1)}")
    print(f"Block Size: {get_field(memoryDest, 2)}")
    global keyCount
    keyCount = keyCount + get_field(memoryDest, 2) #Can be used with print_file to get the total number of keys on the table + total number of blocks
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
    print(f"{get_field(memoryDest, 3 + 19 + 19 + 19)}")

#Stores the specified block from memory to the specified location on file
#Inputs: Name of file to store the data on, index of block location in file, index of block location in memory
#Outputs: The specified block is from memory is stored on file at the specified location
def set_block(filename, blockNumber, memNumber):
    workingFile = open(filename, "r+b")

    workingFile.seek(blockNumber * 512 + offset)

    workingFile.write(storedBlocks[memNumber])  #Only writes the block specified

    workingFile.close()

#Creates a file that can store B-trees using the name specified
#Inputs: Name of file to create
#Outputs: A file is created with a B-tree header using the specified name, unless a file of that name already exists
def create_file(filename):
    if os.path.exists(filename):
        print("ERROR: file already exists")
        sys.exit()

    set_field(0, 0, "4348PRJ3") #Initiailize the header fields
    set_field(0, 1, 0)
    set_field(0, 2, 0)

    workingFile = open(filename, "wb")  #Creates the file, has a different mode than set_block

    workingFile.seek(0 * 512 + offset)

    workingFile.write(storedBlocks[0])

    workingFile.close()

#Inserts the specified key/value pair into the given file
#Inputs: Name of the file in insert into, key and value to insert
#Output: The specified key/value pair is inserted into the file
def insert_into(filename, key, val):
    try:
        workingFile = open(filename, "rb")
    except FileNotFoundError:
        print("ERROR: file not found")
        sys.exit()

    get_block(workingFile, 0, 0)    #Check file format
    if(get_field(0, 0) != magicNumber):
        print("ERROR: improper file format")
        workingFile.close()
        sys.exit()

    nextBlock = get_field(0, 1) #Special case if this is the first key of the tree
    if nextBlock == 0 and get_field(0, 2) == 0:
        set_field(0, 2, 1)
        set_block(filename, 0, 0)

    while True: #Searches for the leaf to insert into
        get_block(workingFile, nextBlock + 1, 0)
        blockSize = get_field(0, 2)

        if get_field(0, 3 + 19 + 19) == get_field(0, 3 + 19 + 19 + 1):  #Checks if we are at a leaf since no 2 non-zero pointers can be the same
            break

        if key <= get_field(0, 3):  #Cases for if we are the leftmost or rightmost node
            nextBlock = get_field(0, 3 + 19 + 19)
            continue

        if key >= get_field(0, 2 + blockSize):
            nextBlock = get_field(0, 3 + 19 + 19 + blockSize)
            continue

        for i in range(0, blockSize):   #Traverses down the tree using an inner pointer
            workingKey = get_field(0, i + 3)
            
            if i < blockSize:
                if key >= workingKey and key <= get_field(0, i + 1 + 3):
                    nextBlock = get_field(0, 3 + 19 + 19 + i + 1)
                    break
    if blockSize < 19:  #Case for if we don't need to split
        set_field(0, 2, get_field(0, 2) + 1)
        for i in reversed(range(0, blockSize + 1)): #Insert the key/value into the correct location
            if get_field(0, 2 + i) > key and 2 + i != 2:
                set_field(0, 3 + i, get_field(0, 3 + i - 1))
                set_field(0, 3 + 19 + i, get_field(0, 3 + 19 + i - 1))
            else:
                set_field(0, 3 + i, key)
                set_field(0, 3 + 19 + i, val)
                break

        workingFile.close()
        set_block(filename, nextBlock + 1, 0)   #Save our insertion to the file
        
    else:
        workingFile.close()
        split_node(filename, key, val)  #Case for if we do need to split

#Splits a node as a result of insertion
#Inputs: Name of file to insert into, key/value pair that caused the split, boolean for if this split will increase tree depth, pointer related to the key
#It is assumed that the node to split is in memory location 0
#Outputs: The node is split and the middle key gets promoted
def split_node(filename, key, value, newRoot = False, pointer = 0):
    file = open(filename, "rb")
    get_block(file, 0, 2)
    newID = get_field(2, 2) #Update the header's next block ID
    set_field(2, 2, newID + 1)
    set_block(filename, 0, 2)
    storedBlocks[1] = bytearray(b'\x00' * 512)  #Reset memory location 1 to hold a new node

    set_field(1, 0, newID)
    set_field(1, 1, get_field(0, 1))
    set_field(1, 2, 10)
    set_field(0, 2, 9)  #Set up the new node, and set the sizes for both nodes

    midVal = get_field(0, 2 + 10)
    if key >= midVal:   #Seperate cases for if the new key is in the left or right child, this one if it is in the right node
        k = 0   #Tracks if we already inserted the key
        for i in range(1, 11):
            if get_field(0, 22 - i) > key or k == 1:    #Move key/value/pointers from the left node to the right node
                set_field(1, 13 - i, get_field(0, 3 + 19 - i + k))
                set_field(0, 3 + 19 - i + k, 0)
                set_field(1, 13 + 19 - i, get_field(0, 3 + 19 + 19 - i + k))
                set_field(0, 3 + 19 + 19 - i + k, 0)
                set_field(1, 13 + 19 + 20 - i, get_field(0, 3 + 19 + 19 + 20 - i + k))
                set_field(0, 3 + 19 + 19 + 20 - i + k, 0)
            else:
                set_field(1, 13 - i, key)   #Insert the key/value/pointer
                set_field(1, 13 + 19 - i, value)
                set_field(1, 13 + 19 + 20 - i, pointer)
                k = 1
        set_field(1, 13 + 19 + 20 - 11, get_field(0, 3 + 19 + 19 + 20 - 11 + k))
        set_field(0, 3 + 19 + 19 + 20 - 11 + k, 0)
    else:   #Same thing but for if the key falls on the left node
        for i in range(1, 11):  #Move left to right
            set_field(1, 13 - i, get_field(0, 3 + 19 - i))
            set_field(0, 3 + 19 - i, 0)
            set_field(1, 13 + 19 - i, get_field(0, 3 + 19 + 19 - i))
            set_field(0, 3 + 19 + 19 - i, 0)
            set_field(1, 13 + 19 + 20 - i, get_field(0, 3 + 19 + 19 + 20 - i))
            set_field(0, 3 + 19 + 19 + 20 - i, 0)
        set_field(1, 13 + 19 + 20 - 11, get_field(0, 3 + 19 + 19 + 20 - 11))
        set_field(0, 3 + 19 + 19 + 20 - 11, 0)

        for i in reversed(range(0, 10)):    #Insert key into correct spot
            if get_field(0, 2 + i) > key and i != 0:
                set_field(0, 3 + i, get_field(0, 3 + i - 1))
                set_field(0, 3 + 19 + i, get_field(0, 3 + 19 + i - 1))
                set_field(0, 3 + 19 + 19 + i, get_field(0, 3 + 19 + 19 + i - 1))
            else:
                set_field(0, 3 + i, key)
                set_field(0, 3 + 19 + i, value)
                set_field(0, 3 + 19 + 19 + i, pointer)
                break

    midKey = get_field(0, 2 + 10)   #Find the key/value pair we will promote, it's pointer remains here
    midVal = get_field(0, 2 + 19 + 10)

    set_field(0, 12, 0) 
    set_field(0, 2 + 19 + 10, 0)

    if get_field(0, 4 + 19 + 19) != 0:  #Update the parent id of the right node's children if applicable
        for i in range(0, 11):
            thisID = get_field(1, 0)
            get_block(file, get_field(1, 3 + 19 + 19 + i) + 1, 2)
            set_field(2, 1, thisID)
            set_block(filename, get_field(1, 3 + 19 + 19 + i) + 1, 2)
        get_block(file, 0, 2)   #Need the header in memory location 2 for future methods

    set_block(filename, get_field(0, 0) + 1, 0) #Store our changes on file
    set_block(filename, get_field(1, 0) + 1, 1)

    file.close()
    expandingDepth = get_field(2, 1) == 0   #Special case for if this is our first time promoting
    promote_key(filename, midKey, midVal, expandingDepth or newRoot)    #Promote the middle value

#Promotes the selected key/value pair in the specified file
#Inputs: The name of the file, the key/value of the node to promote, a boolean for if we are increasing the depth of the tree with this promotion
def promote_key(filename, key, value, expandingDepth):
    file = open(filename, "rb")

    if expandingDepth:  #If we are increasing depth
        get_block(file, 0, 2)
        set_field(2, 1, get_field(2, 2))
        ID = get_field(2, 2)    #Update the parent pointers of the left and right node
        set_field(0, 1, ID)
        set_field(1, 1, ID)
        set_block(filename, get_field(0, 0) + 1, 0)
        set_block(filename, get_field(1, 0) + 1, 1)
        set_field(2, 2, ID + 1) #Update the header
        set_block(filename, 0, 2)
        storedBlocks[2] = bytearray(b'\x00' * 512)  #Create the new root

        set_field(2, 0, ID) #Set up and fill the new root
        set_field(2, 2, 1)
        set_field(2, 3, key)
        set_field(2, 3 + 19, value)
        set_field(2, 3 + 19 + 19, get_field(0, 0))
        set_field(2, 3 + 19 + 19 + 1, get_field(1, 0))
        file.close()
        set_block(filename, ID + 1, 2)
    else:   #If we are not increasing depth
        get_block(file, get_field(0, 1) + 1, 2)
        parSize = get_field(2, 2)   #Check how many keys are in the parent we are promoting into
        if parSize < 19:    #If the parent has space, we can insert into it
            set_field(2, 2, get_field(2, 2) + 1)
            for i in reversed(range(0, parSize + 1)):
                if get_field(2, 2 + i) > key:
                    set_field(2, 3 + i, get_field(2, 3 + i - 1))
                    set_field(2, 3 + 19 + i, get_field(2, 3 + 19 + i - 1))
                    set_field(2, 3 + 19 + 20 + i, get_field(2, 3 + 19 + 20 + i - 1))
                else:
                    set_field(2, 3 + i, key)
                    set_field(2, 3 + 19 + i, value)
                    set_field(2, 3 + 19 + 20 + i, get_field(1, 0))
                    break
            file.close()
            set_block(filename, get_field(0, 1) + 1, 2)
        else:   #If th parent does not have space, we will have to split it
            parID = get_field(2, 1)
            get_block(file, get_field(2, 0) + 1, 0) #Set up our memory to work with split_node
            get_block(file, 0, 2)
            ID = get_field(2, 2)
            file.close()
            if parID == 0:  #If the parent who is full is the root, we need to increase the depth of the tree
                split_node(filename, key, value, True, ID - 1)
            else:
                split_node(filename, key, value, False, ID - 1)

#Searches the specified file for the given key
#Input: The file to search, the key to find
#Output: The key/value pair for the given key is printed to console, or an error if it is not found
def search_file(filename, val):
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

    nextBlock = get_field(0, 1) #Similar search algotithm as insert

    while True:
        get_block(workingFile, nextBlock + 1, 0)
        blockSize = get_field(0, 2)
        if get_field(0, 2) == 0:
            break

        if val < get_field(0, 3):
            nextBlock = get_field(0, 3 + 19 + 19)
            if nextBlock == get_field(0, 0):    #Check if we are at node 0 to prevent a loop
                break
            continue

        if val > get_field(0, 2 + blockSize):
            nextBlock = get_field(0, 3 + 19 + 19 + blockSize)
            if nextBlock == get_field(0, 0):
                break
            continue

        for i in range(0, blockSize):
            workingKey = get_field(0, i + 3)
            if workingKey == val:   #Case for if we find the key
                print(f"{get_field(0, i + 3)},{get_field(0, i + 19 + 3)}")
                workingFile.close()
                return
            
            if i < blockSize:
                if val > workingKey and val < get_field(0, i + 1 + 3):
                    nextBlock = get_field(0, 3 + 19 + 19 + i + 1)
                    break
        if nextBlock == get_field(0, 0):
            break

    print(f"ERROR: unable to find index {val} in file {filename}")
    workingFile.close()

#Loads the given csv file into the given B-tree file
#Input: The file names for the index and csv files, in that order. The csv file is comma seperated with 2 columns, and rows are sperated by new lines
#Output: All entries from the csv file are interted one by one into the index file
def load_file(indexFileName, csvFileName):
    try:
        workingcsvFile = open(csvFileName, "r")
    except FileNotFoundError:
        print("ERROR: csv file not found")
        sys.exit()

    text = workingcsvFile.read()

    keys, vals = [], [] #Parsing the csv file
    for line in text.split('\n'):
        column_list = line.split(',')
        keys.append(column_list[0])
        vals.append(column_list[1])

    for i in range(0, len(keys)):   #Inserting the parsed values
        insert_into(indexFileName, int(keys[i]), int(vals[i]))

#Prints all key/value pairs of the given B-tree file
#Input: The name of the file to read from
#Output: All key/value pairs are printed to the console
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

    totalBlocks = get_field(0, 2)   #Get the total number of blocks from the header
    for i in range(1, totalBlocks + 1):
        get_block(workingFile, i, 0)    #Iterate through all the blocks linearly
        numKeys = get_field(0, 2)
        for k in range(1, numKeys + 1):
            print(f"{get_field(0, k + 2)},{get_field(0, k + 19 + 2)}")

    workingFile.close()

#Writes all key/value pairs of the given B-tree file to the given destination file
#Input: The name of the file to read from, and the name of the file to write to
#Destination file is created, it must not already exist
#Output: All key/value pairs are written to the destination file
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

    totalBlocks = get_field(0, 2)   #Same algorithm as read_file
    for i in range(1, totalBlocks + 1):
        get_block(sourceFile, i, 0)
        numKeys = get_field(0, 2)
        for k in range(1, numKeys + 1):
            destFile.write(f"{get_field(0, k + 2)},{get_field(0, k + 19 + 2)}\n")

    sourceFile.close()
    destFile.close()

if len(sys.argv) < 2:   #input handling
    print("Error: no arguments given")
    sys.exit()

task = sys.argv[1]
if task == "create":    #Check all possible commands, and all condtions that could cause them to fail
    if len(sys.argv) < 3:
        print("ERROR: missing file name")
    else:
        create_file(sys.argv[2])
elif task == "insert":
    if len(sys.argv) < 3:
        print("ERROR: no file given")
    elif len(sys.argv) < 4:
        print("ERROR: no key given")
    elif not sys.argv[3].isdigit():
        print("ERROR: key must be unsigned integer")
    elif len(sys.argv) < 5:
        print("ERROR: no value given")
    elif not sys.argv[4].isdigit():
        print("ERROR: value must be unsigned integer")
    else:
        if int(sys.argv[3]) < 0:
            print("ERROR: key must be unsigned integer")
        elif int(sys.argv[4]) < 0:
            print("ERROR: value must be unsigned integer")
        else:
            insert_into(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))    #Convert command line arguments to integers as needed
elif task == "search":
    if len(sys.argv) < 3:
        print("ERROR: no file given")
    elif len(sys.argv) < 4:
        print("ERROR: no key given")
    elif not sys.argv[3].isdigit():
        print("ERROR: key must be unsigned integer")
    else:
        if int(sys.argv[3]) < 0:
            print("ERROR: index must be unsigned integer")
        else:
            search_file(sys.argv[2], int(sys.argv[3]))
elif task == "load":
    if len(sys.argv) < 3:
        print("ERROR: no index file given")
    elif len(sys.argv) < 4:
        print("ERROR: no csv file given")
    else:
        load_file(sys.argv[2], sys.argv[3])
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

#print(keyCount) #Used to count the total number of keys on the B-tree
