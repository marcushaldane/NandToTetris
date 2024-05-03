#!/bin/bash
echo "================="
declare -a filePaths=( "./add/" "./max/" "./rect/")
declare -a fileNames=( "my_Add.hack" "Add.hack" "my_Max.hack" "Max.hack" "my_Rect.hack" "Rect.hack" )
idx=0
for filePath in "${filePaths[@]}" ; do 
    echo "Checking the following files:"
    my_assembler_output_file_name="${filePath}${fileNames[idx]}"
    echo ${my_assembler_output_file_name}
    test_hack_file_name="${filePath}${fileNames[((idx+1))]}"
    echo ${test_hack_file_name}
    echo "-----------------"
    differences=$(sort $my_assembler_output_file_name $test_hack_file_name | uniq -u)
    if [ -z "$differences" ] ; then 
        echo "No Differences Found"
    else
        echo -e "Differences Found:\r\n$differences"
    fi
    echo "================="
    ((idx+=2))
done