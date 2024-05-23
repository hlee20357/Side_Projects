import os 
import csv
import sys
import pandas as pd
from numpy import mean
import re

#Note
#Below code works! I just need to update it to automate some functions such as the concentrations list making as well as the inputs that people can put in. 


#BEFORE YOU RUN THIS CODE, YOU'LL NEED TO UPDATE THE CONCENTRATIONS VARIABLE. 
#The concentration needs to have a minimum of 3 numbers. For example, 5 is written as '005', and 20 is written as '020'. 

#UPDATE THIS! DON'T FORGET THE ' 
#concentrations = ['005', '500']

#Test_file_path 
#/Users/hyl025/Desktop/Python/For_Github/Sorting_through_Program_tsv_multi_conc/Sorting_through_program_test_file_and_output_multi_conc/Testing_multi_conc_sample_file.tsv

#Note: If you want to read a file, you have to change your working directory to where the file is being stored. 
#print('[change directory]')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#print ('')
#print('getcwd:      ', os.getcwd())
#print('')

#print('basename:    ', os.path.basename(__file__))
#Gives the python file name 
print('dirname:     ', os.path.dirname(__file__))
#print('')
#Gives the path to which the python file is stored 
print ('''The dirname: (text) printed is there to help you get an idea of how your file path is named. 
For example, the file path for the testing of this python script on HL's Macbook was /Users/hyl025/Desktop/Python/Scripts/Testing_EditADAR_data_compilation_csv/EditADAR_to_Prism_v4_one_conc.py
The folder path is /Users/hyl025/Desktop/Python/Scripts/Testing_EditADAR_data_compilation_csv/''')
print ('')


while True: 
    print('''Enter your FILE path of the .tsv file you want to update. 
If you want to exit the program, type in 'Exit' or 'exit' (no quotations).''')
    TSV_file_path = input('Enter the FILE path here: ')
    if TSV_file_path == 'Exit' or TSV_file_path == 'exit': 
        print ('')
        print ('You will need to kill the terminal and run the python file again.')
        exit()
    if '\\' in TSV_file_path: 
        TSV_file_path = TSV_file_path.replace ('\\', '/')
    #https://stackoverflow.com/questions/12618030/how-to-replace-back-slash-character-with-empty-string-in-python
    #How to indicate that we want to get rid fo the backslash
    #tsv_file='/Users/hyl025/Desktop/Python/Scripts/Testing_EditADAR_data_compilation_csv/Real_data_from_two_conc_032524/01355_TSV_Test.tsv'
    try: 
        # reading given tsv file
        csv_table=pd.read_table(TSV_file_path,sep='\t')
        
        # converting tsv file into csv
        tsv_to_csv = TSV_file_path.replace('.tsv', '.csv')
        csv_table.to_csv(tsv_to_csv,index=False)
        
        # output
        print ('')
        print("Successfully converted the tsv file to a csv file!")
        #print (tsv_to_csv)
        print ('')

        break 
    except: 
        print ('''Conversion failed. Please retry inputting the tsv file path.
Make sure you are inputting the right file path, including all characters''')
        print ('')


with open (tsv_to_csv, mode = 'r') as csv_file: 
    csv_reader = csv.reader(csv_file, delimiter = ',')
    #next(csv_reader, None)
    #skips the header 

    rows = list(csv_reader)
    #Save the csv as a list of rows 
    counter = 0
    starting_edit_position = rows[1][0]

    index_of_target_position = rows[0].index('target_position')
    #Find the index in the first row of rows that contains the target_position, which is the main target position that is trying to be edited. 
    #print (index_of_target_position)
            
    target_position = int(rows[1][index_of_target_position])
    #get to obtain that target_position value 

    #print (starting_edit_position)
    #print (type(starting_edit_position))

    #Code below dictates how many lines are associated with a specific editing position. The counting is done with the counter variable. 
    #Once the specific editing position ends, then the for loop breaks. 
    concentrations = []
    for i in rows[1:]:
        #Skips the first index of rows, which are the headers
        row_obtain = ''
        row_obtain = i
        print (row_obtain)
        x = row_obtain[0]
        #print (x)
        #print (type(x))
        #print (type(starting_edit_position))
        #print (row_obtain[4])
        guide_name_index = row_obtain[4].rfind('_')
        #print (guide_name_index)
        ng_index = row_obtain[4].rfind('ng')
        concentration = row_obtain[4][guide_name_index+1:ng_index]
        #print (concentration)
        if concentration not in concentrations: 
            concentrations.append(concentration)
        if x != starting_edit_position:
            break 
        counter = counter+1


number_of_files = counter

print (number_of_files)
print (concentrations)
print (starting_edit_position)
print (target_position)