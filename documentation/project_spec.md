# Specification

# Projects purpose
The project is meant to be able to look for "variables" in memory and then narrow it down so you can find the actual place where something is stored.
You should also be able to write to the addresses.


# Basic functionality
- ~~Ability to look for things numbers in memory and narrow them down~~
- ~~Automatically update the table of found addresses~~
- ~~Save the found addresses~~
- Change the underlying type in the saved address
- ~~Update the values contained in the saved address widget~~
- ~~Different scan types, <, >, !=~~
- Write to the addresses

# Future implementation ideas
- Look for floats/doubles
- Look for an array of bytes
- GDB support? Or some self-made hacky debugger ish, I kinda wanted to make one anyway, could be 
  cool
- Capstone for disassembly
