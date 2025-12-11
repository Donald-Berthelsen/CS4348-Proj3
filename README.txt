The project can be ran from the command line using "py main.py <command> <arguments>"
Commands are all lowercase, and follow the format specified by the instructions
The project should not require modifications to the environment outside of being able to run python
All code is included in main.py, no additional files are required

In the source code there is a offset variable on line 4
This specifies how many bytes to skip before creating the B-tree
This was created because the test.idx file provided had some offset when downloaded
The offset should have no impact on the behavior of the B-tree, outside of file sizes
The only exception is if the offset is modified since it will make any files created under a different offset unreadable

The source code also contains a print_block method for debugging 
It will read a block at a given point in memory, and print it to console in a more human readable format
It is not used by default and can only be enabled by modifying the source code

All functionality has been implemented
The B-tree was tested to hold for up to 10,000 insertions
Beyond that and performance starts to become a concern
Load was designed for csv files with 2 columns separated by a comma, and records separated by new lines

The code includes comments to explain logic

During splits, the node to promote is chosen from the left child
