OP_CODES = {
    '0': "101010",
    '1': "111111",
    '-1': "111010",
    'D': "001100",
    'A': "110000",
    'M': "110000",
    '!D': "001101",
    '!A': "110001",
    '!M': "110001",
    '-D': "001111",
    '-A': "110011",
    '-M': "110011",
    'D+1': "011111",
    'A+1': "110111",
    'M+1': "110111",
    'D-1': "001110",
    'A-1': "110010",
    'M-1': "110010",
    'D+A': "000010",
    'D+M': "000010",
    'D-A': "010011",
    'D-M': "010011",
    'A-D': "000111",
    'M-D': "000111",
    'D&A': "000000",
    'D&M': "000000",
    'D|A': "010101",
    'D|M': "010101"
}

DEST_CODES = {
    'null': "000",
    'M': "001",
    'D': "010",
    'MD': "011",
    'A': "100",
    'AM': "101",
    'AD': "110" ,
    'AMD': "111"
}

JUMP_CODES = {
    'null': "000",
    'JGT': "001",
    'JEQ': "010",
    'JGE': "011",
    'JLT': "100",
    'JNE': "101",
    'JLE': "110",
    'JMP': "111"
}

def parse_address_instruction(instruction):
    print("parse_address_instruction")
    return

def parse_compute_instruction(instruction):
    # print("parse_compute_instruction")
    op, a_bit, dest, jump = "","","",""
    equalSignCharPosition = instruction.find("=")
    semiColonCharPosition = instruction.find(";")
    if(semiColonCharPosition != -1): # SemiColon was found in string search
        dest = "null"
        op = instruction[:semiColonCharPosition]
        jump = instruction[semiColonCharPosition+1:]
        # print("Jump Command")
        # print(instruction[semiColonCharPosition])
    elif(equalSignCharPosition != -1): # Equal sign was found in string search
        dest = instruction[:equalSignCharPosition]
        op = instruction[equalSignCharPosition+1:]
        jump = "null"
        # print("Calculation Command")
        # print(instruction[equalSignCharPosition])
    MinOP = op.find("M")
    if(MinOP != -1): # M is found in the op string
        a_bit = "1"
    else:
        a_bit = "0"
    # print("dest: {}".format(dest))
    # print("op: {}".format(op))
    # print("jump: {}".format(jump))
    # print("a_bit: {}".format(a_bit))
    # print("\n")
    return op, a_bit, dest, jump

def assemble_compute(instruction):
    if(instruction[0] == "@"):
        parse_address_instruction(instruction)
    else:
        op, a_bit, dest, jump = parse_compute_instruction(instruction)
    c_bits = OP_CODES[op]
    d_bits = DEST_CODES[dest] # "".join([DEST_CODES.get(d, '0') for d in dest])  # Build destination bits
    j_bits = JUMP_CODES[jump] #JUMP_CODES.get(jump, '000')  # https://www.w3schools.com/python/ref_dictionary_get.asp
    # print("c_bits: {}".format(c_bits))
    # print("d_bits: {}".format(d_bits))
    # print("j_bits: {}".format(j_bits))
    binaryInstruction = "111" + a_bit + c_bits + d_bits + j_bits
    # print("binaryInstruction: {}".format(binaryInstruction))
    return binaryInstruction

def process_file(filename):
    """ Main file processing """
    with open(filename, 'r') as infile, open("my_assembler_c_instruction_only.hack", 'w') as outfile:
        for line in infile:
            # print(line.strip())
            binary = assemble_compute(line.strip())
            outfile.write(binary  + '\n') 

process_file("assembler_c_instruction_only.asm")
