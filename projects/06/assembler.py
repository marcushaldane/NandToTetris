import sys

OP_CODES = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    'M': '110000',
    '!D': '001101',
    '!A': '110001',
    '!M': '110001',
    '-D': '001111',
    '-A': '110011',
    '-M': '110011',
    'D+1': '011111',
    'A+1': '110111',
    'M+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'M-1': '110010',
    'D+A': '000010',
    'D+M': '000010',
    'D-A': '010011',
    'D-M': '010011',
    'A-D': '000111',
    'M-D': '000111',
    'D&A': '000000',
    'D&M': '000000',
    'D|A': '010101',
    'D|M': '010101'
}

DEST_CODES = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110' ,
    'AMD': '111'
}

JUMP_CODES = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

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
FUNCTION: findSymbols(line, instructionCounter)
----------------------------------------------------------------
PURPOSE: Determine if a line from the infile file object is a symbol
       + Add symbols which do not already exist in the SYMBOL_CODES dictionary
       + Symbols come in the form of a key:value pair with
            key=symbol and value=instructionCounter
----------------------------------------------------------------
RETURN: 0 if no key:value pair was added to SYMBOL_CODES, 
1 if a new key:value pair was added to SYMBOL_CODES
----------------------------------------------------------------
"""
def findSymbols(line, instructionCounter):
    openingParenthesisCharPosition = line.find('(')
    closingParenthesisCharPosition = line.find(')')
    if(openingParenthesisCharPosition != -1):
        symbol = line[openingParenthesisCharPosition+1:closingParenthesisCharPosition]
        if(symbol in SYMBOL_CODES): return 0
        else:
            shortHexAddress = hex(instructionCounter).replace('0x', '')
            extraZerosNeeded = 4 - len(shortHexAddress)
            paddedHex = '0x' + '0'*extraZerosNeeded + shortHexAddress
            SYMBOL_CODES.update({symbol: paddedHex}) # might need to check that next line is actually an instruction, not a comment or pseudo instruction
            return 1
    return 0


""" 
----------------------------------------------------------------
FUNCTION: firstPass(infile)
----------------------------------------------------------------
PURPOSE: Parse and clean lines from the infile file object.
       + Find and remove comments
       + Remove whitespace with .strip()
       + Skip lines with no instruction
       + Find symbols using the findSymbols(line, instructionCounter) function
       + Add cleaned up instruction lines to the lines list
       + Incriment instructionCounter
----------------------------------------------------------------
RETURN: lines list
----------------------------------------------------------------
"""
def firstPass(infile):
    lines = []
    instructionCounter = 0
    for line in infile:
        commentPosition = line.find('/') 
        if(commentPosition != -1): line = line[:commentPosition]
        line = line.strip() 
        if (line == ''): continue
        symbolFound = findSymbols(line, instructionCounter)
        if(symbolFound): continue
        lines.append(line)
        instructionCounter = instructionCounter + 1
    return lines


""" 
----------------------------------------------------------------
FUNCTION: parseComputeInstruction(instruction)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def parseComputeInstruction(instruction):
    equalSignCharPosition = instruction.find('=')
    dest = instruction[:equalSignCharPosition]
    op = instruction[equalSignCharPosition+1:]
    jump = 'null'
    MinOP = op.find('M')
    if(MinOP != -1):  a_bit = '1'
    else: a_bit = '0'
    return op, a_bit, dest, jump


""" 
----------------------------------------------------------------
FUNCTION: parseJumpInstruction(instruction)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: op, a_bit, dest, jump
----------------------------------------------------------------
"""
def parseJumpInstruction(instruction):
    semiColonCharPosition = instruction.find(';')
    dest = 'null'
    op = instruction[:semiColonCharPosition]
    jump = instruction[semiColonCharPosition+1:]
    MinOP = op.find('M')
    if(MinOP != -1): a_bit = '1'
    else: a_bit = '0'
    return op, a_bit, dest, jump

""" 
----------------------------------------------------------------
FUNCTION: assembleBinary(instruction, instructionType)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def assembleBinary(instruction, instructionType):
    if(instructionType == 'AddressInstruction'): return parseAddressInstruction(instruction)
    if(instructionType == 'ComputeInstruction'): op, a_bit, dest, jump = parseComputeInstruction(instruction)
    if(instructionType == 'JumpInstruction'): op, a_bit, dest, jump = parseJumpInstruction(instruction)
    c_bits = OP_CODES[op]
    d_bits = DEST_CODES[dest] 
    j_bits = JUMP_CODES[jump] 
    binaryInstruction = '111' + a_bit + c_bits + d_bits + j_bits
    return binaryInstruction


""" 
----------------------------------------------------------------
FUNCTION: parseAddressInstruction(instruction)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def parseAddressInstruction(instruction):
    atCharPosition = instruction.find('@')
    machineCodeAddress = instruction[atCharPosition+1:]
    openingParenthesisCharPosition = instruction.find('(')
    closingParenthesisCharPosition = instruction.find(')')
    if(machineCodeAddress.isdigit()): # Address is literal
        shortBinaryAddress = bin(int(machineCodeAddress)).replace('0b', '')
        extraZerosNeeded = 16 - len(shortBinaryAddress)
        binaryInstruction = '0'*extraZerosNeeded + shortBinaryAddress
    elif(openingParenthesisCharPosition == -1 and closingParenthesisCharPosition == -1):
        shortBinaryAddress = bin(int(SYMBOL_CODES[machineCodeAddress].replace('0x', ''),16)).replace('0b', '')
        extraZerosNeeded = 16 - len(shortBinaryAddress)
        binaryInstruction = '0'*extraZerosNeeded + shortBinaryAddress
    else: # Address is symbolic
        pseudoInstruction = instruction[openingParenthesisCharPosition+1:closingParenthesisCharPosition]
        binaryInstruction = bin(int(SYMBOL_CODES[pseudoInstruction].replace('0x', ''),16)).replace('0b', '')
    return binaryInstruction


""" 
----------------------------------------------------------------
FUNCTION: determineInstructionType(instruction)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def determineInstructionType(instruction):
    if '@' in instruction:
        # print('At symbol found')
        return 'AddressInstruction'
    if '=' in instruction:
        # print('Equal sign found')
        return 'ComputeInstruction'
    if ';' in instruction:
        # print('Semi-colon found')
        return 'JumpInstruction'

""" 
----------------------------------------------------------------
FUNCTION: secondPass(infile, outfile)
----------------------------------------------------------------
PURPOSE: 
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def secondPass(lines, outfile):

    for line in lines: 
        # outfile.write(line + '\n') 
        instructionType = determineInstructionType(line)
        binary = assembleBinary(line, instructionType)
        outfile.write(binary  + '\n') 
        

""" 
----------------------------------------------------------------
FUNCTION: process_file(inputFileName, outputFileName)
----------------------------------------------------------------
PURPOSE: open(inputFileName) to read lines of .asm file
       + open(outputFileName) to write lines of binary instructions into .hack file
       + Call firstPass(infile)
       + Call secondPass(infile, outfile)
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def process_file(inputFileName, outputFileName):
    """ Main file processing """
    with open(inputFileName, 'r') as infile, open(outputFileName, 'w') as outfile:
        lines = firstPass(infile)
        # print(lines)
        # print(SYMBOL_CODES)
        secondPass(lines, outfile)


process_file(sys.argv[1], sys.argv[2]) 
