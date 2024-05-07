import sys

SYMBOL_CODES = {
    'SP': '0x0000',
    'LCL': '0x0001',
    'ARG': '0x0002',
    'THIS': '0x0003',
    'THAT': '0x0004',
    'R0': '0x0000',
    'R1': '0x0001',
    'R2': '0x0002',
    'R3': '0x0003',
    'R4': '0x0004',
    'R5': '0x0005',
    'R6': '0x0006',
    'R7': '0x0007',
    'R8': '0x0008',
    'R9': '0x0009',
    'R10': '0x000a',
    'R11': '0x000b',
    'R12': '0x000c',
    'R13': '0x000d',
    'R14': '0x000e',
    'R15': '0x000f',
    'SCREEN': '0x4000',
    'KBD': '0x6000',
}


""" 
----------------------------------------------------------------
FUNCTION: 
----------------------------------------------------------------
PURPOSE:
----------------------------------------------------------------
RETURN: 
----------------------------------------------------------------
"""



""" 
----------------------------------------------------------------
FUNCTION: determineInstructionType(instruction)
----------------------------------------------------------------
PURPOSE: Search for key characters ('@' or '=' or ';') in instruction
       + and return the corresponding instruction type 
       + as a string identifier.
----------------------------------------------------------------
RETURN: String declaring instruction type
----------------------------------------------------------------
"""
def determineInstructionType(instruction):
    if '@' in instruction: return 'AddressInstruction'
    if '=' in instruction: return 'ComputeInstruction'
    if ';' in instruction: return 'JumpInstruction'


""" 
----------------------------------------------------------------
FUNCTION: secondPass(lines, outfile)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def secondPass(lines, outfile):
    nextRAMAvailable = 16
    for line in lines: 
        # instructionType = determineInstructionType(line)
        outfile.write(line  + '\n') 
          

""" 
----------------------------------------------------------------
FUNCTION: firstPass(infile)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: lines list
----------------------------------------------------------------
"""
def firstPass(infile):
    lines = []
    for line in infile:
        commentPosition = line.find('/') 
        if(commentPosition != -1): line = line[:commentPosition]
        line = line.strip() 
        if (line == ''): continue
        lines.append(line)
    return lines


""" 
----------------------------------------------------------------
FUNCTION: process_file(inputFileName, outputFileName)
----------------------------------------------------------------
PURPOSE: open(inputFileName) to read lines of .vm file(s)
       + open(outputFileName) to write lines of assembly instructions into .asm file
       + Call firstPass(infile)
       + firstPass() returns a list of lines 
       + Call secondPass(lines, outfile)
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def process_file(inputFileName, outputFileName): 
    with open(inputFileName, 'r') as infile, open(outputFileName, 'w') as outfile:
        lines = firstPass(infile)
        secondPass(lines, outfile)

if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2]) 
