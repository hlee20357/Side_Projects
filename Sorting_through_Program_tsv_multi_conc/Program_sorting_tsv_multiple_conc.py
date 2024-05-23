import os 
import csv
import sys
import pandas as pd
from numpy import mean
import re



#BEFORE YOU RUN THIS CODE, YOU'LL NEED TO UPDATE THE CONCENTRATIONS VARIABLE. 
#The concentration needs to have a minimum of 3 numbers. For example, 5 is written as '005', and 20 is written as '020'. 

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
print ('''The dirname: (text) printed is there to help you get an idea of how your folder path is named. To the folder path, you just append the name of your file. 
For example, the file path for the testing of this python script on HL's Macbook was /Users/hyl025/Desktop/Python/For_Github/Sorting_through_Program_tsv_multi_conc/Program_sorting_tsv_multiple_conc.py
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


#PART 1
#Determine concentrations you are working with, how many files you are working with, and target editing position. 

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
    #In addition, code below obtains the concentrations that were tested by finding the concentration amounts in the names of the sequences. 
    concentrations = []
    for i in rows[1:]:
        #Skips the first index of rows, which are the headers
        row_obtain = ''
        row_obtain = i
        #print (row_obtain)
        x = row_obtain[0]

        guide_name_index = row_obtain[4].rfind('_')
        ng_index = row_obtain[4].rfind('ng')
        concentration = row_obtain[4][guide_name_index+1:ng_index]
        if concentration not in concentrations: 
            concentrations.append(concentration)
    
        if x != starting_edit_position:
            break 
        counter = counter+1


number_of_files = counter



#print (number_of_files)
#print (concentrations)

#PART 2 
#Make a list of dictionaries that contain the editing values of your guides at the multiple concentrations

list_of_names_obtained = []
list_of_dictionaries = []
counter = 1
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

        if counter <= number_of_files:
        #Want to use this if statement to generate the full list of dictionaries of lists to fill in before reaching the target position
            name_of_sequence_unedited = row_obtain[4]
            index_of_period = name_of_sequence_unedited.find('.')
            name_of_sequence_edited = name_of_sequence_unedited[0:index_of_period]

            #Looking to see if the concentration exists in the name 
            for i in concentrations: 
                index_of_concentration = name_of_sequence_edited.find('_' + i + 'ng')
                if index_of_concentration != -1: 
                #-1 indicates that index_of_concentration was not found
                    break
            
            #For cases of GFP and NTC. I still want to add them to the list of dictionaries 
            if index_of_concentration == -1: 
                if name_of_sequence_edited not in list_of_names_obtained: 
                    dict['Name'] = name_of_sequence_edited
                    dict['Target Position'] = target_position
                    dict['Registered Name']= 'NA'
                    for i in concentrations: 
                        for j in range (1,5): 
                            dict['Value ' + str(j) + ' at ' + i + 'ng'] = ''
                    #By doing this, you are adding to the dictionary with the keys of "name" and "Value x at y ng" for all y concentrations
                    list_of_dictionaries.append(dict)

                    list_of_names_obtained.append(name_of_sequence_edited)

            #For all the concentrations. Also avoiding repeats of dictionaries so that one guide has its own dictionary
            #Within that dictionary, you will be able to input the values. 
            else: 
                name_of_sequence_edited_without_conc_name = name_of_sequence_edited[0:index_of_concentration]
                if name_of_sequence_edited_without_conc_name not in list_of_names_obtained: 
                    dict['Name'] = name_of_sequence_edited_without_conc_name
                    dict['Target Position'] = target_position
                    dict['Registered Name']= ''
                    for i in concentrations: 
                        for j in range (1,5): 
                            dict['Value ' + str(j) + ' at ' + i + 'ng'] = ''
                    #By doing this, you are adding to the dictionary with the keys of "name" and "Value x at y ng"
                    list_of_dictionaries.append(dict)
                    list_of_names_obtained.append(name_of_sequence_edited_without_conc_name)
            counter = counter + 1

        #Once we reach the target position, fill in the values 
        if x == target_position: 
            edit_value = ''
            index_position_within_name_list = ''
            name_of_sequence_unedited = row_obtain[4]
            index_of_period = name_of_sequence_unedited.find('.')
            name_of_sequence_edited = name_of_sequence_unedited[0:index_of_period]

            #Looking to see if the concentration exists in the name 
            for i in concentrations: 
                index_of_concentration = name_of_sequence_edited.find('_' + i + 'ng')
                if index_of_concentration != -1: 
                    break

            #For cases of GFP and NTC. I still want to add them to the list of dictionaries 
            if index_of_concentration == -1: 
                edit_value = float(row_obtain[2])
                index_position_within_name_list = list_of_names_obtained.index(name_of_sequence_edited)


                #Updating Registered Name to either GFP or No Transfection Control
                if 'GFP' in name_of_sequence_edited: 
                    list_of_dictionaries[index_position_within_name_list]['Registered Name'] = 'GFP'
                else: 
                    list_of_dictionaries[index_position_within_name_list]['Registered Name'] = 'No Transfection Control'

                #Below finds the first empty key-value pair and then updates that key with the edit_value obtained
                for i in list_of_dictionaries[index_position_within_name_list]: 
                   if list_of_dictionaries[index_position_within_name_list][i] == '': 
                       empty_key_value_pair = i 
                       break 
                
                list_of_dictionaries[index_position_within_name_list][empty_key_value_pair] = edit_value

            #For all cases other than GFP and NTC
            else: 
                edit_value = float(row_obtain[2])

                #Now need to figure out what concentration we are currently dealing with in the row. 

                length_of_edited_seq_name = len(name_of_sequence_edited)
                concentration_being_looked_at = name_of_sequence_edited[index_of_concentration+1:length_of_edited_seq_name]
                #Did the +1 to index of concentration to get rid of _
                #concentration in name must be surrounded by _ anyways 

                name_of_sequence_edited_without_conc_name = name_of_sequence_edited[0:index_of_concentration]
                index_position_within_name_list = list_of_names_obtained.index(name_of_sequence_edited_without_conc_name)

                #Code below updates the first empty key_value_pair for a given guide (which is indicated with the index_position_within_name_list)
                #However, need to account for times when you don't have a full list of values for a concentration
                #The above comment is resolved by the "if concentration_being_looked_at in i"
                #By doing this, you only focus on keys of a specific concentration  
                for i in list_of_dictionaries[index_position_within_name_list]: 
                    if concentration_being_looked_at in i: 
                        if list_of_dictionaries[index_position_within_name_list][i] == '':
                            empty_key_value_pair = i 
                            #print ('This is i:', i)
                            break 
                
                list_of_dictionaries[index_position_within_name_list][empty_key_value_pair] = edit_value



                



#The Checks 
#print (list_of_dictionaries)
#print ('')
#print ('This is the list of names obtained', list_of_names_obtained)
#print ('')
#print (counter)
print ('Successfully made dictionary containing all the editing values.')            

#PART 3 
#Take the list of dictionary values and use them to obtain the average editing value per concentration and guide. 

average_value_dictionary = []
for i in list_of_dictionaries: 
#Goes through every index of list_of_dictionaries, and every index is a dictionary within itself. Each index represents a guide. 
    empty_dictionary_to_append = {}
    empty_dictionary_to_append['Name'] = i['Name']
    empty_dictionary_to_append['Registered Name'] = i['Registered Name']
    for z in concentrations: 
        name = 'Average On-Target Editing Value at '+ z+'ng'
        empty_dictionary_to_append[name] = ''

    average_value_dictionary.append(empty_dictionary_to_append)

length_of_list_of_dictionaries = len(list_of_dictionaries)

for i in concentrations: 
#Iterate through the concentrations list 
    for j in range(length_of_list_of_dictionaries): 
    #Iterate through the indicies of the list, going from 0, 1, 2, and so forth 
        list_of_values = []
        value = ''
        current_processing_average = ''
        #Rest list_of_values, value, and current_processing_average to ensure that you are getting the right averages
        for k in range (1,5): 
        #Iterating through k = 1 to k = 4 to access the specific keys in the dictionary that are labeled as "Value 1/2/3/4 at [concentration]ng"
            #print (k)
            value = list_of_dictionaries[j]['Value ' + str(k) + ' at ' + i +'ng']
            if value != '': 
                list_of_values.append(value)
            #To ensure that you are not putting '' into the list when you do the mean function 
            if k == 4:
                #print (list_of_values)
                #print ('I got here!')
                #Checks to make sure I'm getting it right. 

                current_processing_average = mean(list_of_values)
                #print (current_processing_average)
                average_value_dictionary[j]['Average On-Target Editing Value at ' + i + 'ng'] = current_processing_average

#In the example I have, with two concentrations, 
#I go through the first concentration, which is 005 ng. 
#At that first concentration, I go through each list_of_dictionaries' index, where each index is a unique dictionary 
#At that particular index, I go through the keys' value that are specified for that particular concentration, which is ['Value ' + str(k) + ' at ' + i +'ng']
#Once k ==4, which means all the particular keys' values were accessed, then I get the average and update the respective key-value pair in the average_list_dictionary
#Once I have gone through the whole dictionary for one concentration, I go through the whole dictionary again at the second concentration. And so forth. 

print ('')
#print (average_value_dictionary)
print ('Successfully created the dictionary containing the average editing values.')

#PART 4
#Write the two dictionaries (of Part 2 and Part 3) into a singular csv file 

fields_for_2nd_dictionary = list(average_value_dictionary[0].keys())


new_updated_csv_file_path = tsv_to_csv.replace('.csv', '_Compiled_Data.csv')

# my data rows as dictionary objects

#Note: Even if one of the keys had an empty value, it was reflected in the csv. That value was left empty. 
 
# field names
fields = list(list_of_dictionaries[0].keys())
#Obtain all the keys from dictionary index 0 and make it as a list 

#Below is the written out version of the keys
#fields = ['Name', 'Target Position', 'Registered Name', 'Value 1 at 050ng', 'Value 2 at 050ng', 'Value 3 at 050ng', 'Value 4 at 050ng', 'Value 1 at 750ng', 'Value 2 at 750ng', 'Value 3 at 750ng', 'Value 4 at 750ng']
 
# writing to csv file
with open(new_updated_csv_file_path, 'w', newline = '') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)
 
    # writing headers (field names)
    writer.writeheader()
 
    # writing data rows
    writer.writerows(list_of_dictionaries)

    writer.writerow({})
    #Have to write an empty dictionary as a row to separate between dictionary that contains all the editing values and the dictionary that contains the average editing values. 

    #Below consists of the writing of the average editing value dictionary
    writer2 = csv.DictWriter(csvfile, fieldnames=fields_for_2nd_dictionary)

    writer2.writeheader()

    writer2.writerows(average_value_dictionary)

print ('')
print ('csv file with all the editing values and the average editing values was created!')
print ('It has the file path of ', new_updated_csv_file_path)

print ('')

print ('Thanks for using me! If you have any questions/concerns/comments, let Henry know! ')
print ('Also, hope your analysis goes well! ')
