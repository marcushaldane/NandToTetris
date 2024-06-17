#!/usr/bin/env python3
import sys # used to get argv[] values
import os # used to get current working directory
import glob # used to get *.vm files in specified directory

SEGMENT = {
    'argument': 'ARG',
    'local': 'LCL',
    'static': '',
    'constant': '',
    'this': 'THIS',
    'that': 'THAT',
    'pointer': '',
    'temp': ''
}

INSTRUCTION_TRANSLATION = {
    'push constant': '\n// push constant {} \n@{} \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1'
}

ARITHMETIC_INSTRUCTIONS = {
    'sub':  '\n// sub \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nM=M-D \n@SP \nM=M+1', 
    'add':  '\n// add \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nM=M+D \n@SP \nM=M+1', 
    'neg':  '\n// neg \n@SP \nAM=M-1 \nM=!M \nM=M+1 \n@SP \nM=M+1', 
    'eq':  '\n// eq_{} \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nMD=M-D \n@SP \nM=M+1 \n@EQ_{} \nD;JEQ \n@NEQ_{} \n0;JMP \n(EQ_{}) \n@0 \nD=!A \n@CONTINUE_EQ_{} \n0;JMP \n(NEQ_{}) \n@0 \nD=A \n@CONTINUE_EQ_{} \n0;JMP \n(CONTINUE_EQ_{}) \n@SP \nAM=M-1 \nM=D \n@SP \nM=M+1',
    'gt':  '\n// gt_{} \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nMD=M-D \n@SP \nM=M+1 \n@GT_{} \nD;JGT \n@NGT_{} \n0;JMP \n(GT_{}) \n@0 \nD=!A \n@CONTINUE_GT_{} \n0;JMP \n(NGT_{}) \n@0 \nD=A \n@CONTINUE_GT_{} \n0;JMP \n(CONTINUE_GT_{}) \n@SP \nAM=M-1 \nM=D \n@SP \nM=M+1',
    'lt':  '\n// lt_{} \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nMD=M-D \n@SP \nM=M+1 \n@LT_{} \nD;JLT \n@NLT_{} \n0;JMP \n(LT_{}) \n@0 \nD=!A \n@CONTINUE_LT_{} \n0;JMP \n(NLT_{}) \n@0 \nD=A \n@CONTINUE_LT_{} \n0;JMP \n(CONTINUE_LT_{}) \n@SP \nAM=M-1 \nM=D \n@SP \nM=M+1',
    'and':  '\n// and_{} \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nM=D&M \n@SP \nM=M+1', 
    'or':  '\n// or_{} \n@SP \nAM=M-1 \nD=M \n@SP \nAM=M-1 \nM=D|M \n@SP \nM=M+1',
    'not':  '\n// not_{} \n@SP \nAM=M-1 \nM=!M \n@SP \nM=M+1' 
}

ARITHMETIC_INSTRUCTIONS_COUNT = {
    'sub': 0,
    'add': 0,
    'neg': 0,
    'eq': 0,
    'gt': 0,
    'lt': 0,
    'and': 0,
    'or': 0,
    'not': 0
}

""" 
----------------------------------------------------------------
FUNCTION: translateVMtoAssembly(lines)
----------------------------------------------------------------
PURPOSE: Generate and return a list of assembly command lines 
       + By translating each of the vm lines provided in 
       + the lines arg into corresponding assembly commands.
----------------------------------------------------------------
RETURN: assemblyLinesList list
----------------------------------------------------------------
"""
def translateVMtoAssembly(lines):
    assemblyLinesList = []
    for i, line in enumerate(lines): 
        # print('line', i, line, sep=': ')

        assemblyLines = ''
        num = ''.join(char for char in line if char.isdigit())
        instruction = ''.join(char for char in line if not(char.isdigit())).strip()

        if(num == ''): # if a VM line is an arithmetic instruction, translate that instruction to assembly and incriment the corresponding ARITHMETIC_INSTRUCTIONS_COUNT by 1 (ensures uniqueness of assembly jump label symbols)
            assemblyLines = ARITHMETIC_INSTRUCTIONS[line].replace('{}', str(ARITHMETIC_INSTRUCTIONS_COUNT[line]))
            # print('[ARITHMETIC_INSTRUCTIONS: {}]'.format(assemblyLine))
            ARITHMETIC_INSTRUCTIONS_COUNT[line] = ARITHMETIC_INSTRUCTIONS_COUNT[line] + 1
            # print(ARITHMETIC_INSTRUCTIONS_COUNT)
        elif(instruction == 'push constant'): # if a VM line is the 'push constant' instruction, translate that instruction to assembly 
            assemblyLines = INSTRUCTION_TRANSLATION[instruction].replace('{}', str(num))
            # print(INSTRUCTION_TRANSLATION[instruction].replace('{}', str(num)))
        assemblyLinesList.append(assemblyLines) # add assembly code to the assemblyLinesList 
        # space = instruction.find(' ')
        # if(space != -1):
        #     segment = instruction[space+1:]
        #     instruction = instruction[:space]
        # print('instruction: [{}]'.format(instruction))
        # print('segment: [{}]'.format(segment))
        # print('num: [{}]'.format(num))
    return assemblyLinesList
          

""" 
----------------------------------------------------------------
FUNCTION: cleanVMfile(infile)
----------------------------------------------------------------
PURPOSE: Generate and return a list of vm file lines without any 
       + empty lines
       + comments
       + leading spaces
       + trailing spaces
----------------------------------------------------------------
RETURN: lines list
----------------------------------------------------------------
"""
def cleanVMfile(infile):
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
FUNCTION: process_file(inputDirectoryName, outputFileName)
----------------------------------------------------------------
PURPOSE: Get a list of VM files from user command line input (some specified directory)
       + open(inputDirectoryName) to read lines of .vm file(s)
       + open(outputFileName) to write lines of assembly instructions into .asm file
       + Call cleanVMfile(vmfile)
       + cleanVMfile(vmfile) returns a list of vm lines with non-instruction characters removed 
       + Call translateVMtoAssembly(cleanLines)
       + translateVMtoAssembly(cleanLines) returns a list of assembly lines
       + Write assembly lines to outputFileName
----------------------------------------------------------------
RETURN: None
----------------------------------------------------------------
"""
def process_file(inputDirectoryName, outputFileName): 
    # print('arg1: {}'.format(inputDirectoryName) + '\narg2: {}'.format(outputFileName))
    cwd = os.getcwd()
    # print('cwd: {}'.format(cwd))
    # informative video on glob: https://www.youtube.com/watch?v=tATFQUx0Zx0
    fileList = glob.iglob('{}/*.vm'.format(inputDirectoryName),
                          root_dir = cwd,
                          recursive = True)
    # print('fileList: {}'.format(fileList))
    for i, file in enumerate(fileList, 1):
        # print(i, file, sep=': ')
        with open(file, 'r') as vmfile, open(outputFileName, 'w') as outfile: # can change to {open(outputFileName, 'a')} append mode to handle multiple vm files later
            cleanLines = cleanVMfile(vmfile)
            assemblyLines = translateVMtoAssembly(cleanLines)
            # print(assemblyLines)
            for line in assemblyLines:
                outfile.write(line) 
            # print('===============================')

if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2]) 
    
    
