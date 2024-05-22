import os 
import csv
import sys
import pandas as pd
from numpy import mean
import re
from statistics import mean

#Note
#This code works if you only have one concentration and you use Grouped graph format for Prism. 

#Note: If you want to read a file, you have to change your working directory to where the file is being stored. 
#print('[change directory]')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#print ('')
#print('getcwd:      ', os.getcwd())
#print('')

print('basename:    ', os.path.basename(__file__))
#Gives the python file name 
print('dirname:     ', os.path.dirname(__file__))
print('')
#Gives the path to which the python file is stored 
print ('''The dirname: (text) printed is there to help you get an idea of how your file path is named. 
The basename: (text) printed gives the name of the file. 
For example, the file path for the testing of this python script on HL's Macbook was /Users/hyl025/Desktop/Python/For_Github/Sorting_through_Program_tsv_one_conc/GitHub_A_to_Prism_v4_one_conc_copy.py
The folder path is ''', os.path.dirname(__file__))
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
    #tsv_file=
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
    for i in rows[1:]:
        #Skips the first index of rows, which are the headers
        row_obtain = ''
        row_obtain = i
        x = row_obtain[0]
        if x != starting_edit_position:
            break 
        counter = counter+1
        break

list_of_names_obtained = []
dictionary = {}
with open (tsv_to_csv, mode = 'r') as csv_file: 
    csv_reader = csv.reader(csv_file, delimiter = ',')
    next(csv_reader, None)
    #skips the header line
    for row in csv_reader: 
        dict = {}
        row_obtain = ''
        row_obtain = row
        x = int(row_obtain[0])
        if x > (target_position): 
        #Stop the loop once you've reached the end of the target_position 
        #Therefore you don't have to go through the rest of the rows of the csv and creating extra work 
            break
        #print (row)
        if x == target_position:

            #editing name of the sequence to get rid of everything before the first '.'
            name_of_sequence_unedited = row_obtain[4]
            index_of_period = name_of_sequence_unedited.find('.')
            name_of_sequence_edited = name_of_sequence_unedited[0:index_of_period]

                #Note: Running into issues where 50 ng is found before 750 ng. Then, the name is manipulated prematurely.
                #Note: I don't think I can do it in the format of prism where you have one guide name and the columns correspond to the values of a specific concentration 
                #I think I'll have to have each line in the .csv to be a guide at a specific concentration 
                #The only way I can see if I can circumvent this issue is to change the whole naming convention. Instead of _50ng_, you would have to do _050ng_, and then you can search for exactly 050 instead of 50. That way, 050 is different from 750

            if name_of_sequence_edited not in list_of_names_obtained: 
                dictionary[name_of_sequence_edited] = []
                list_of_names_obtained.append(name_of_sequence_edited)
            #if the name of the sequence edited is not in the list_of_names_obtained, then a key with name_of_sequence_edited is created with an empty value of a list. 
            #Also, the name_of_sequence_edited gets appened to the list_of_names so that a key of the same name doesn't get created. 

            edit_value = float(row_obtain[2])
            dictionary[name_of_sequence_edited].append(edit_value)
            #The edit_value is obtained when going through a row. 
            #To the specific key, the edit value is appened to the end of the list. 

#print ('')
#print (list_of_names_obtained)
#print ('')
#print (dictionary)
print ('')

list_to_write_to_all_values = []
for i in dictionary: 
    y = [i] + [''] + dictionary[i]
    list_to_write_to_all_values.append(y)
#The i represents the key, the '' represents an empty value that will become an empty cell in the final .csv file, and the dictionary[i] represents the values from the key 
#You have all the values in one line so that it's easily written into the empty .csv file. 

#print (list_to_write_to_all_values)

list_to_write_to_averages = []
for i in dictionary: 
    #print (i)
    x = mean(dictionary[i])
    #Output is a float number
    #Take the mean of all the dictionary values associated with dictionary key i
    mean_to_list = []
    mean_to_list.append(x)
    #Essentially converting float number to list 
    full_row_to_write = [i] + [''] +mean_to_list
    #Concatenating the lists of name and the mean so that they are together as one list. 
    #This helps for the output of the csv file. 

    list_to_write_to_averages.append(full_row_to_write) 

print (list_to_write_to_averages)

new_updated_csv_file_path = tsv_to_csv.replace('.csv', '_Compiled_Data.csv')

beginning_header = ('Name of guide', 'Benchling Registered Name (User inputted)', 'Values obtained for that specific guide and concentration')
middle_header = ('Guide', 'Benchling Registered Name (User inputted)', 'Average On-Target editing of Guide')
with open (new_updated_csv_file_path, mode = 'w', newline = '') as csv_file2: 
#newline = '' eliminates the empty rows that were originally created when I was writing in each row. 
#https://stackoverflow.com/questions/4521426/delete-blank-rows-from-csv
    csv_writer = csv.writer(csv_file2, delimiter = ',')
    csv_writer.writerow(beginning_header)
    for row in list_to_write_to_all_values: 
        csv_writer.writerow(row)
    #Write the rows into the csv file of all the values associated with the dictionary keys 

    csv_writer.writerow('')
    #write an empty line to separate all the values section to only  the average value section 
    csv_writer.writerow(middle_header)
    for row in list_to_write_to_averages: 
        csv_writer.writerow(row)

print ('')
print ('''Compiled Data .csv file has been made successfully!
It has the file path of ''', new_updated_csv_file_path)

print ('')

print ('Thanks for using me! If you have any questions/concerns/comments, let Henry know! ')
print ('Also, hope your analysis goes well! ')

#Note 
#Worked with two separate files 
