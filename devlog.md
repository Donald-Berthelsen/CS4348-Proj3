[12/4/25 8:00 pm]
This project looks somewhat intimidating to me
The stuff related to B-trees is fine, there are plenty of tools to visualize insertion operations for reference
The part that looks tricky is working with blocks of memory
I'm not very experienced in working with raw binary data in a structured way, so I expect that to pose difficulty
I'll be doing the project in Python since Python worked well for project 2
I'll try to have everything in a single main.py file, but I may break things apart if it would be useful

My goal for this first session is to be able to print the provided index file
While I'm at it, I may as well also implement extract since it should be very similar
And in doing that, I would need to be able to read commands
And if I'm reading commands already, it shouldn't be too hard to implement create
I don't know how difficult it will be to implement print, so I don't know if I'll achieve it this session
Part of this session will be exploratory as I figure out how to approach the problem

[8:20 pm]
I'm not too sure where to begin, after opening the file I'm in unknown territory
First I'll need a method that can retrieve blocks of data, I'll have to look up how to do that
Then I'll need to parse the blocks one by one
If I can retrieve blocks, then I can store them as a global variable to force the 3 in the chamber rule
I only care about the first 8 bytes of the first block to verify the magic number
Reading the magic number should be a good test for reading from the file
It looks like I'll only need to read from blocks in 8 byte increments
This means I can have another method to retrieve data at a given location in the block
My next goal will be to read the magic number using these get block and get 8-byt methods

[8:45]
I have made my first attempt at a get_block method
printing the result shows promising results
I can identify the magic number, however it is offset 2? bytes from the start of the file
I don't know the cause for this, perhaps the first 2 bytes are some kind of record keeping by windows or eLearning
I could simply offset my file by 2 bytes to make space for these 2 bytes
If I don't offset, I may not be able to read the index file properly
I'll do the offset for now, and take a note to revisit this issue when testing on the CS machines
As for the other deader fields, they look correct enough

Now the next puzzle to solve is reading the rest of the blocks
I am capable of reading blocks, the question is when to know to stop reading
For this I think I'll look at the next block id field from the header and store it
I'm 80% sure blocks are put in the file in increasing order
It's not like I can open the index file in note pad and check it
So to account for my uncertainty, I'll count how many blocks we read
As opposed to reading the block id of the retrieved block

Upon printing the first block I have encountered another issue where fields are 10 bytes long rather than 8
I can see that the block size is 512 by using the block id field at least
Also the magic number is still 8 bytes long, only the other fields are 10 bytes
At this point I think I'll just make field size and offset as global variables
I'll include some instructions in the readme if I remember for the global variables

Next I'll make get_field method
I won't use get_field on the header block since the magic number has a special offset

I'm having some issues converting byte to int, maybe due to the way I read it
This isn't too unexpected, I'm not very experienced at this
The issue comes from reading spaces between each byte
I'll try first removing whitespace from the read

[9:55 pm]
I have solved the problem after spending too long to realize I can simple use replace
And have realized that the space was used to convey information
\x00<space> is 2 bytes, \x00<no space> is only 1 byte
So the replace has to be when decoding the bytes, not when retrieving them
This means that the field sizes are indeed only 8 bytes, solving that problem
I can now get rid of the field size variable
And I can also treat the magic number as a normal field
Meaning the next goal is get_field

I'll do some basic bounds checking on get_field and end the program if it fails
This should only happen if I make a programming error
I should be able to have get_field return the decoded int, rather than just the bytes
All the fields are ints, and the magic number can be treated as an int as well

[10:10 pm]
Get field works, and with that I have my abstractions done
Finishing print should be a fairly standard process from here
I feel like I'm out of the woods and back into familiar territory

I'll check the magic number first so I don't forget it
Things are going smoothly now that I can easily access arbitrary fields
I also need to check if the file opened properly

[10:40 pm]
I have completed print
There were some rough patches, but it went smoother than expected
Now that I have tools set up, I can start making good progress
I'll take a short break, then work on handling input

[11:10 pm]
Back to work and input handling is done
The main point of interest was learning how to use command line arguments in my IDE
Now I can start implementing other methods, beginning with extract
Extract should be the same as print, only outputting to a file rather than console

I'm rather bad at following consistent formatting of my code it seems
I'm checking for missing arguments in 3 different ways
A formatting pass looks like it'll be on the agenda if I have extra time after finishing everything else

[11:30]
Extract is done, I made a file and the format matches that of print
I ended up separating the different key/value pairs with newlines, that should be fine
I debated including a header row of "key/value" but ultimately decided against it
I figured that a header row would be unexpected and thus conflict with potential automated testing tools
For that reason, I also got rid of my header row from print
I also ended up reusing a lot of code from print_file, perhaps I could make more general methods to clean it up

Next up is create, and that means being able to write to fields
I can't use get_field directly for this, but I can reuse most of the code
It would be good practice to also check the mode the file is open in while I do this
While an incorrect open mode can only cause problems with bugs in the code, checks are useful to catch those bugs
As for actually creating the file, that should be simple
I need to create the file, then initialize the header block
This means setting the magic number to 4348PRJ3 and the next block ID to 1
As well as zeroing out the bytes of root ID to be safe
The unused bits don't need to be zeroed out since they are never accessed

On second thought, checking file mode presents a new range of problems I hadn't thought about before
I can check the file mode when getting a block for reading, that works fine
But I can't check when writing because I don't yet have the concept of writing a block
I was going to write records based on block and field index, but that would be incorrect
Instead I need to write to a block in memory, then move that block to the file when done
This also has to conform to the 3 in the chamber rule
At the current level it doesn't change much, but this make the B-tree stuff more involved
For now, I just need to also make a set block method
I don't need a reset block method for the same reason I don't need to zero out blocks before use

But I do need to initialize my storedBlocks to support modifying them

I'm having some difficulty with data types in writing to the block in memory
I tried to initialize using a byte array, but that was causing problems
I'll instead manually initialize the arrays with bytes
I was thinking about it wrong, I don't need an array for each block in memory
I only need a single variable to store the block

[12:35 am]
I got it working using a byte array that I initialize to all zeroes
I'll have to test to see if this broke print, but things look promising
Turns out I just got confused for a bit, but byte arrays work fine
After also fixing a small yet significant misspelling, and I have set_field working
Working for strings that is, now I need to make it work for ints as well

[12/5/25 12:45 am]
I finished create, or at least I think I did
At the very least, print recognized my created file as having the magic number
And with that, I finished all my goals for this session
I've done everything I can without touching B-trees
This session took slightly longer than expected
On the other hand, I'm glad nothing here had me stuck for several hours
I should have the bulk of the work done now
I'm a little worried that verifying B-tree correctness will be difficult
But that's a problem for the next session

I'm hoping I can finish this project in the next session
Then I can go clean up and comment my code
The first step looks like it will be implementing search
While I could implement search now using brute force it would be both slightly amusing and the incorrect solution
Search would give tree traversal, and that would be about 1/3 the work for insert
Another 1/3 of the work would be inserting the value itself
This step involves only the block in memory, not the blocks in the file
The last 1/3 of the work will be splitting the node when needed
Splitting should be the only time I need more than 1 node in memory at a time
And with 3 nodes in memory, it should be doable
Then load is to insert what extract was to print, not too difficult
I expect next session to go smoother than this one
