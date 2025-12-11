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
Also adding more edge case error checking would be nice

[12/10/25 2:00 pm]
This session I plan to do the work I outlined at the end of the last session
That being, search->insert->load
I'm hoping I can get this done smoothly in around 2-3 hours

First I need to do search by traversing the B-tree
The tree will be searched using keys and child pointers, meaning I can ignore the values field
First I'll look at the keys, then the pointers, then use that to find the next block
This will follow the assumption that blocks are stored sequentially based on ID

Things are going fairly smoothly, just needing some bug fixes as I test it
It would be useful to include a debug method to print blocks as they are accessed
And it's a good thing I did so, since it shows my search had some wacky stuff going on

My generic print_block method doesn't play nice with the special header block
However since it's just a debug too, it's fine that the fields are mislabeled
The test.idx file has an odd bit at the end of the block pointers section, no clue how it got there
However it's outside the block size, so it shouldn't matter
The current issue is that some value are found while others are not, this is why I made a debug method
Search is not finding values 52-60 or 82-100, its like those blocks don't exist

For 52-60, it's because they are on a block with ID 0
I check for ID 0 as a stopping condition, but it appears that needs more refinement
I now check if the block size is 0, however this doesn't solve the problem

For the range 52-60 that fall on block 0, block 0 is the root
This causes either an infinite loop of searching, or simply failing to find the value, depending on implementation
printing all the values does show that these ranges do exist on the file
The question then is where they actually are

By combining print_block with the print method, I have my answer
Block ID 0 is the 7th block, and block ID 13 is the 10th
These blocks having mismatched ID and location explain why my search algorithm couldn't find them
At the same time, it is good to know that my search algorithm was running properly by not finding them

This now leads to the question of where do I go from here
According to the instructions, ID is determined by order in the file
This means that ID 0 is misplaced, and ID 13 is simply invalid and should be 10
If IDs are unordered, then there is no easy way to search for a specific ID
So I want to believe that the test.idx file is incorrect here
I don't want to believe the provided material is wrong, but I don't know how I would proceed otherwise
This means I'll be going forward without an test file to work with
It will be harder to verify correctness, but I should still be able once insert is working

The next task is to do insert, and it comes in 3 parts
First I need to find the location to insert the value
I can do this with a modified version of search that stops at leaf nodes
I can check if a node is a leaf if its first 2 child pointers are 0
Next I need to shift values to the right to put in the new one
This can be done entirely in memory using get_field and set_field
Next is the tricky part where I need to split a node if needed, by looking at the numKeys field
I can create a new node by looking at the next node spot in the header
Then having both old and new nodes in memory as I fill the new node with half the old node
The question is how I will promote the middle value
In the worst case, I'll be promoting a node to an already full parent
This will involve inserting in a new key/value pair, and a new pointer
Luckily, with 3 blocks in memory I can remember the 2 child nodes and the parent node
So I can check if the parent is full when promoting
Then I can check the keys of the parent to know where the promoted key will go
And from the header I know the ID of the node that will be created from the split
Then I can set the parent IDs of the children and drop them from memory
Then I can actually split the parent, and we can continue for however many levels needed
Also I'll need to check if the node is the root by looking at the header

I'll have to make sure to test all my methods a second time before submission with how much I edit them
This will come from testing on the CS machines

I should have the basic non split case for insert done
I don't need to explicitly make the initial root node since it has block ID 0 and 0 keys to start

Looks like set_field doesn't play nice with blocks I obtain from get_block
This likely comes from differences in datatypes between initialized and found blocks
The problem stems from trying to read a block that doesn't exist

I solved the problem by manually setting the value in memory if a read turns up empty
While not the most elegant solution, it works for this case
Now I'm having issues with set_block overwriting the header
I suspect this is from seek not being valid to set where to write

I solved this problem by changing the mode I use to open the file
Now the issue is actually inserting the key/value
Incrementing block size works fine, it's the other values that are a problem
It doesn't help that the workflow to check changes is delete file->creat->insert->print
At least print_block let me get rid of the last print step

The blocks in memory are of proper format now after some tweaking
Now the issue is they don't get written to the file properly
At least it no longer is interfering with the header block

Print is not working because I don't increment the next block ID when making the root
This again runs into the issue of reading the file in a different data type than I write to it
I'll have to solve this issue to progress

The root of my problems was that the byte object is immutable
By simply reading blocks as bytearrays, my problems are solved
Except for print not working anymore, but basic insertion is good now
And search works too now with my inserted values, yippee
And I can fix the print error with a minor tweak

[12/10/25 6:00 pm]
I'm calling the second session here due to a prior commitment
I did not accomplish my goal of completing the project, so I will need to do a third session
I may end up cutting it tight on time
This means I may not clean the code or test it on the CS machines
This session had some unexpected roadblocks, but now I am over them
The roadblocks came from an incorrect foundation from stuff I did in the last session
So going forwards I should have a more solid foundation to prevent future roadblocks

Next session I need to finish the project, and there will be a somewhat tight time constraint
First I'll do load to help with future testing for insertion
Load should be simple to do
I'll also make a modified load that will create a fresh file to load into to help test
Then it'll be splitting nodes for insert, then promoting values
If things go smoothly the remaining work shouldn't take too long
However judging by how this session went, I'm not sure that will be the case
Regardless, I have a clear idea of what remains to be done and now I just need to follow through

[12/10/25 9:45 pm]
I am now beginning session 3 with roughly 2 hours left to finish the project
If things go smoothly this will be enough time
In the interest of saving time, I'll be making less frequent commits
The current goal is full functionality, extra things can come after that

First I need to implement load, this should be simple enough 
As it happens, I have code for reading a csv from my databases project
I should be able to use this 

Load works fine, but insertion doesn't put the values at the correct location
Instead it is putting it at the end of the block
Some tweaking fixed this, although I don't know why
But it works for now, and that is good enough

[11:10 pm]
I got node splitting to work, now I just need to promote nodes
I don't know if I'll make the deadline

I have promoting to the root working

I'm making good progress, but will end up with a late submission unfortunately

Some more tweaking and I have normal promotions working as well
Now all I need to do is recursive promotions

[12:10 pm]
I missed the deadline unfortunately
At least this gives me an excuse to write a simple script to generate a large csv
And include more methods for debugging

A difficulty of testing recursive promotions is just how many values I need to work with
This is because the problem only occurs when the root is split for the second time
In order to split the root twice requires a large csv file
Another difficulty is just how many fields I'm accessing to perform the operation

I'm getting confused so I'll try a fresh start for promotion

[1:15 am]
I have discovered why my insertion stopped working
I was getting the wrong field to check if the tree was still just the root
This was sneakily causing a lot of problems since it would prevent updating the header

That's one problem solved, there are still more
For example, there are insertions not from the csv that break ordering within nodes
I don't know where they come from, but that is another problem to solve

I'm slowly reimplementing functionality as things work
The new problem is that blocks are forgetting the parent ID assigned to them
So now it's another witch hunt to try to find where it is being overridden
And that witch hunt has uncovered some very odd behavior
Block ID 0 is getting all the insertions, and once full it flushes itself
And there still are the shadow inserts that aren't on the csv
Now I'm confused how this even is working for the first promotion
Wherever the values are getting inserted, it sure isn't the first block
Split is the one putting the values on the file, not insert

[2:15 am]
One tweak latter and I can actually insert values into children of the root
Now I can try to find the source of the shadow inserts
Also, it looks like values at the middle of the swap don't go on the correct sides

The shadow numbers appear to be spawned by the way I shift the nodes to insert new values
The shadow numbers replace a regular insertion with that value
The problem stems from my set_field function
It is not converting from decimal to hex properly, the to_bytes function to be exact
Once a value passes ~5000, it no longer displays properly
While python can decode this value just fine still, it loses some context when I store it to memory
Without that context, python no longer knows how to read the bytes and thus gives a wrong answer
It's a good thing I'm testing with large enough values, otherwise I wouldn't have caught this

I can't determine why this happens, although I have found it to be a property of Python
The solution is to convert the bytes to hex when using them since that doesn't get messed up
However this involves rewriting my foundation methods again
Hopefully not too much breaks

[3:10 am]
Bytes are represented not as hex, but as ASCII
This causes the problematic bytes to display as a space
However spaces in byte form have meaning
This meaning gets confused and we lose the value we were storing, that is the root of the problem
This is because I remove the spaces from bytes when I retrieve them
I forgot the original motivation behind removing spaces, but I was able to safely undo it
And with just a minor change, this goose hunt come to an end
Next up is fixing the middle values of swaps

Yet when I reintroduced promotion, the middle values were already correct
This means I can finally go on to working on features again

The current issue is that my condition for creating a new root is flawed
The question I need to solve is how I will know that a promotion is going to create a new root
Rather, how do I differentiate an existing root from a newly created one
The clunky solution is to use a flag for this
I have a special case for the first new root creation
Then set the flag as needed when promoting

With that flag, I now have the ability to promote multiple nodes to the root
The problem now is that it's not picking the correct nodes
Only the first promotion actually creates a parent that follows the B-tree structure
The splitting itself looks fine
The issue is once again data being overwritten somewhere

The actual issue is that insertions ignore the root after the second split
Instead they insert directly into the latest block
Because I'm looking at the header's next ID, rather than root ID
But if I look at the root ID, now it tries to insert into the header

By moving around how I traverse the tree I was able to resolve this
This may become a problem for search
Luckily now that I missed the deadline, I have plenty of time to test on the CS machines

After testing a csv with 200 rows, I can somewhat confidently say that promotion works
Now the final task is to have recursive promotions
I may be able to utilize split_node for this

Recursive promotion is somewhat working, some keys are sneaking into the wrong blocks
It looks like internal nodes suffer from not respecting the roots pointers
Also node 0 forgets some values and sometimes doesn't respect its parent
Also one lead node looks like it was accepting 2 separate ranges
But other than those issues, recursive promotion worked

I'll start by solving node 0 since it should only have to do with the split algorithm
Node 0 has the smallest values of the tree due to how it is structured
It seems it has difficulty when the values get too small

Small keys are instead replaced by the size of the block, and the related value is lost
I don't know what came together to cause this

[5:00 am]
I have solved the problem of using the block size as a key
When shifting the keys, the stopping condition was the first number smaller than the key
It just so happened that this also was checking the block size
And for the vast majority of values I use, they are larger than the block size
But for block 0 specifically, there was a chance that it would have a value smaller than the block size
This is because the smallest values in the B-tree go on block 0
This was solved with a simple check on if we reached the block size field so we can stop before it
