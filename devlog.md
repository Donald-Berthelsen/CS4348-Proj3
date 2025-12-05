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
