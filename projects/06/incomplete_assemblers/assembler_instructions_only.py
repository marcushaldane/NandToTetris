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

def parse_compute_instruction(instruction):
    op, a_bit, dest, jump = '','','',''
    equalSignCharPosition = instruction.find('=')
    semiColonCharPosition = instruction.find(';')
    if(semiColonCharPosition != -1): # SemiColon was found in string search
        dest = 'null'
        op = instruction[:semiColonCharPosition]
        jump = instruction[semiColonCharPosition+1:]
    elif(equalSignCharPosition != -1): # Equal sign was found in string search
        dest = instruction[:equalSignCharPosition]
        op = instruction[equalSignCharPosition+1:]
        jump = 'null'
    MinOP = op.find('M')
    if(MinOP != -1): # M is found in the op string
        a_bit = '1'
    else:
        a_bit = '0'
    return op, a_bit, dest, jump

def parse_address_instruction(instruction):
    atCharPosition = instruction.find('@')
    machineCodeAddress = instruction[atCharPosition+1:]
    if(machineCodeAddress.isdigit()): # Address is literal
        shortBinaryAddress = bin(int(machineCodeAddress)).replace('0b', '')
        extraZerosNeeded = 16 - len(shortBinaryAddress)
        binaryInstruction = '0'*extraZerosNeeded + shortBinaryAddress
    else: # Address is symbolic
        print("Symbolic Address")
        binaryInstruction = "0000111100001111"
    return binaryInstruction


def assemble_binary(instruction):
    binaryInstruction = ''
    if(instruction[0] == '@'):
        binaryInstruction = parse_address_instruction(instruction)
    else:
        op, a_bit, dest, jump = parse_compute_instruction(instruction)
        c_bits = OP_CODES[op]
        d_bits = DEST_CODES[dest] 
        j_bits = JUMP_CODES[jump] 
        binaryInstruction = '111' + a_bit + c_bits + d_bits + j_bits
    return binaryInstruction

def process_file(inputFileName, outputFileName):
    """ Main file processing """
    with open(inputFileName, 'r') as infile, open(outputFileName, 'w') as outfile:
        for line in infile:
            commentPosition = line.find('/') # str.find() will return -1 if no comment symbol is found. 
            # Using slice notation like is done three lines below will result in a string with the last char removed as such: 
            #  line starts as '@R0';  string slicing like this ->  line[:-1]   turns line string into this -> line = '@R'{0};  where  {0} is removed
            if(commentPosition != -1): # comment symbol '/' is found in the line string
                line = line[:commentPosition] # if no comment is found on a line, no need to shorten string to get rid of comment. Strip will remove all whitespace. 
            line = line.strip()
            if (line == ''): continue  # check for comment only lines 
            binary = assemble_binary(line)
            outfile.write(binary  + '\n') 

process_file(sys.argv[1], sys.argv[2]) # run process_file() function on filename passed in as argv[1]. argv[2] should be the name of the output file with .hack extension