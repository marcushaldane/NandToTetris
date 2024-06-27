#!/usr/bin/env python3
import sys # used to get argv[] values
import os # used to get current working directory
import glob # used to get *.vm files in specified directory

PUSH_POP_INSTRUCTION_TRANSLATIONS = {
    'push constant': '\n// push constant {} \n@{} \nD=A \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push argument': '\n// push argument {} \n@{} \nD=A \n@ARG \nA=M+D \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push local':    '\n// push local {} \n@{} \nD=A \n@LCL \nA=M+D \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push static':   '\n// push static {} \n@{} \nD=A \n@16 \nA=D+A \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push this':     '\n// push this {} \n@{} \nD=A \n@THIS \nA=M+D \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push that':     '\n// push that {} \n@{} \nD=A \n@THAT \nA=M+D \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push pointer':  '\n// push pointer {} \n@{} \nD=A \n@THIS \nA=D+A \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'push temp':     '\n// push temp {} \n@{} \nD=A \n@5 \nA=D+A \nD=M \n@SP \nA=M \nM=D \n@SP \nM=M+1',
    'pop argument':  '\n// pop argument {} \n@{} \nD=A \n@ARG \nD=M+D \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D',
    'pop local':     '\n// pop local {} \n@{} \nD=A \n@LCL \nD=M+D \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D',
    'pop static':    '\n// pop static {} \n@{} \nD=A \n@16 \nD=D+A \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D',
    'pop this':      '\n// pop this {} \n@{} \nD=A \n@THIS \nD=M+D \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D',
    'pop that':      '\n// pop that {} \n@{} \nD=A \n@THAT \nD=M+D \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D',
    'pop pointer':   '\n// pop pointer {} \n@{} \nD=A \n@THIS \nD=D+A \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D',
    'pop temp':      '\n// pop temp {} \n@{} \nD=A \n@5 \nD=D+A \n@R13 \nM=D \n@SP \nM=M-1 \nA=M \nD=M \n@R13 \nA=M \nM=D'
}

ARITHMETIC_INSTRUCTION_TRANSLATIONS = {
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

ARITHMETIC_INSTRUCTION_COUNT = {
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

LABEL_TRANSLATIONS = {
    'label': '\n// label {} \n({})',
    'goto': '\n// goto {} \n@{} \n0;JMP',
    'if-goto': '\n// if-goto {} \n@SP \nAM=M-1 \nD=M \n@{} \nD;JNE'
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
        assemblyLines = ''
        num = ''.join(char for char in line if char.isdigit())
        instruction = ''.join(char for char in line if not(char.isdigit())).strip()        
        if(instruction in ARITHMETIC_INSTRUCTION_TRANSLATIONS): # if a VM line is an arithmetic instruction, translate that instruction to assembly and incriment the corresponding ARITHMETIC_INSTRUCTION_COUNT by 1 (ensures uniqueness of assembly jump label symbols)
            assemblyLines = ARITHMETIC_INSTRUCTION_TRANSLATIONS[line].replace('{}', str(ARITHMETIC_INSTRUCTION_COUNT[line]))
            ARITHMETIC_INSTRUCTION_COUNT[line] = ARITHMETIC_INSTRUCTION_COUNT[line] + 1
        elif(instruction in PUSH_POP_INSTRUCTION_TRANSLATIONS): # if a VM line is a push or pop instruction, translate that instruction to assembly 
            assemblyLines = PUSH_POP_INSTRUCTION_TRANSLATIONS[instruction].replace('{}', str(num))
        else: 
            spacePosition = instruction.find(' ')
            labelCommand = instruction[:spacePosition]
            label = instruction[spacePosition+1:]
            assemblyLines = LABEL_TRANSLATIONS[labelCommand].replace('{}', label)
        assemblyLinesList.append(assemblyLines) # add assembly code to the assemblyLinesList 
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
    cwd = os.getcwd()
    fileList = glob.iglob('{}/*.vm'.format(inputDirectoryName),
                          root_dir = cwd,
                          recursive = True)
    for i, file in enumerate(fileList, 1):
        with open(file, 'r') as vmfile, open(outputFileName, 'w') as outfile: # can change to {open(outputFileName, 'a')} append mode to handle multiple vm files later
            cleanLines = cleanVMfile(vmfile)
            assemblyLines = translateVMtoAssembly(cleanLines)
            for line in assemblyLines:
                outfile.write(line) 
    
if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[2]) 
    
    
