#This program is used to append a select number of base pairs in order to reach the minimum number of nucleotides needed to order gblocks. 
#Depending on your initial response, the number of nucleotides added will vary. 

import os 
import csv
import sys


print ('''READ FOR FIRST TIME USERS!
       
This program is used to append a select number of base pairs at the end of guide sequences in order to reach the minimum number of nucleotides needed to order gblocks. 
- If you are going to use IDT, then 30 base pairs will be appended to the end of the guide sequence. 
- if you are going to use Twist Biosciences, then 200 base pairs will be appended to the end of the guide sequence. 

Note: Confirmed that filler sequence used for appending bases (whether it's 30 bp or 200 bp) do not contain BsaI overhangs. 

In addition, the guide sequences you are manipulating must have the Golden Gate cloning overhangs (BsaI overhangs) already.
       
This program will 
1. Ask if you are ordering from Twist Biosciences or IDT. 
2. Ask if the .csv file you are working with is 
    - an unedited (raw) .csv file (such as a Geneious Prime exported .csv file but it'll work on a .csv file with least 3 columns with 2 of the column headers being "Name" and "Sequence" ) 
    - or an edited .csv file (which only has two columns with header names  "Name" and "Sequence").

    - NOTE: YOUR .csv file MUST BE a COMMA SEPARATED VALUES (.csv) file AND NOT A CSV UTF-8 (COMMA DELIMITED) (.csv) file
    - NOTE: This issue will only appear when you are given an Excel doc and you are converting it into a .csv file. Geneious export files are saved in the right .csv format. 
3. Ask the file path of the .csv file you want to manipulate. 
4. Ask where you want to save your updated .csv file. 
    - You can choose to save the updated .csv file in the same folder as the .csv file you asked to manipulate in step 3
    - Or you can choose to save the updated .csv file in a different file path. 
    - Your updated .csv file will contain your updated guide sequences.
5. At the end, the link to either IDT or Twist Biosciences will be printed on the screen so that you can immediately go to IDT or Twist Biosciences.''')
print ('')

#For reference: 

#30 bp IDT addition
#GGAGTGCTTAGCGCGTGATTACTGCTGGAG

#200 bp Twist Biosciences addition
#GGAGTGCTTAGCGCGTGATTACTGCTGGAGGATTGGAATTGGCGATTCTTACGCGGAACCACGATAACGAGATAACGTTAAGTCGCTAGACTTAAGGCGGCACGCGATCGAGCAACTCCTCACTACGATAGGTGAGCGCAGTCCAGTGTAGCTCAGTCGGCCAATTACGGTTCTATTAGACAGTTGCACGTTGACATCAC

#Note: If you want to read a file, you have to change your working directory to where the file is being stored. 
#print('[change directory]')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#print ('')
#print('getcwd:      ', os.getcwd())
#print('')

#print('basename:    ', os.path.basename(__file__))
#Gives the python file name 
print('dirname:     ', os.path.dirname(__file__))
#Gives the path to which the python file is stored 
print ('''The dirname: (text) printed is there to help you get an idea of how your file path is named.
For example, the file path for the testing of this python script on HL's Macbook was /Users/hyl025/Desktop/Python/For_Github/Appending_basepairs''')
print ('')

#PART 1
#Determine whether user is ordering through IDT or Twist Biosciences


while True: 
    response = input('Are you ordering gblocks through IDT or Twist Biosciences? Either enter IDT or Twist Biosciences: ')
    print ('')
    response = response.strip()
    response = response.lower()
    #print (response)
    if response == 'idt' or response == 'twist biosciences': 
    #For future reference, always make your if statement what you want to achieve if the right response/answer is given 
        break
    else: 
        print ('Please enter an appropriate response.')
        print ('')


if response == 'idt': 
    addition = 'GGAGTGCTTAGCGCGTGATTACTGCTGGAG'
if response == 'twist biosciences': 
    addition = 'GGAGTGCTTAGCGCGTGATTACTGCTGGAGGATTGGAATTGGCGATTCTTACGCGGAACCACGATAACGAGATAACGTTAAGTCGCTAGACTTAAGGCGGCACGCGATCGAGCAACTCCTCACTACGATAGGTGAGCGCAGTCCAGTGTAGCTCAGTCGGCCAATTACGGTTCTATTAGACAGTTGCACGTTGACATCAC'

#PART 2
#Determine whether user is going to use an unedited or edited .csv file

while True: 
    response2 = input('''Will the .csv file you will be edited (where .csv file contains two columns Name and sequence) or will it be unedited?
Unedited means that you exported the .csv file from Geneious and didn't edit it.  
Enter "edited" or "unedited" (without the quotations) as a response: ''')
    print ('')
    response2 = response2.strip()
    response2 = response2.lower()
    #print (response)
    if response2 == 'edited' or response2 == 'unedited': 
    #For future reference, always make your if statement what you want to achieve if the right response/answer is given 
        break
    else: 
        print ('Please enter an appropriate response.')
        print ('')


#My test .csv to read
#file_path = 'C:/Users/hlee2/OneDrive/Documents/Python Scripts/Side Projects/Testing to see if this works.csv' for windows 

#For mac, my file_path was /Users/hyl025/Desktop/Python/Code Testing/Testing to see if this works.csv

#PART 3
#Reading the .csv file you want to eventually manipulate (by appending base pairs)

while True: 
    print('''Enter your file path of the .csv file you want to update. 
If you want to exit the program, type in 'Exit' or 'exit' (no quotations). 
An example of why you want to exit is because you typed in the wrong type of file version (edited vs unedited).''')
    print ('Your response was "'+ response2 + '".')
    file_path = ''
    file_path = input('Enter the file path here: ')
    if file_path == 'Exit' or file_path == 'exit': 
        print ('')
        print ('You will need to kill the terminal and run the python file again.')
        exit()
    if '\\' in file_path: 
        file_path = file_path.replace ('\\', '/')
    #https://stackoverflow.com/questions/12618030/how-to-replace-back-slash-character-with-empty-string-in-python
    #How to indicate that we want to get rid fo the backslash
    if response2 =='edited': 
        try: 
            with open (file_path, mode = 'r') as csv_file: 
                csv_reader = csv.reader(csv_file, delimiter = ',')
                storage = []
                count = 0 
                for row in csv_reader:
                    if len(row)>2: 
                        print ('')
                        print ('You may be accessing an unedited .csv file but have the edited response selected.')
                        print ('Do you want to change your response from edited to unedited?')
                        while True: 
                            response2 = input('Enter "unedited" (no quotations) if you want to work with an unedited file: ')
                            response2 = response2.strip()
                            response2 = response2.lower()
                            #print (response)
                            if response2 == 'unedited':
                            #For future reference, always make your if statement what you want to achieve if the right response/answer is given 
                                break
                            else: 
                                print ('Please enter an appropriate response.')
                                print ('')
                        print ('')
                        print ('First, the exception will be raised.')
                        print ('Then, because of the structure of the code, your file will now be completely read.')
                        print ('')
                        sys.exit()
                    if count == 0:
                        storage.append(row)
                        count = count + 1
                    else: 
                        manipulate_gRNA_name = ""
                        manipulate_gRNA_name = row[0]
                        #Save the output from row[index containing gRNA name] as a different variable so it can be manipulated 

                        manipulate_gRNA_name = manipulate_gRNA_name.replace('(', '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace(')', '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace(',', '.')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('+','')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace("'", '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('-', '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('/', '.')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace("\\", '.')
                        #Do a lot of manipulations to the name to get rid of (),+'-/\

                        length_of_name = len(manipulate_gRNA_name)
                        if manipulate_gRNA_name[-1] == '_':
                            manipulate_gRNA_name = manipulate_gRNA_name[0:length_of_name - 1]

                        row[1] = row[1] + (addition)
                        #print (addition)
                        #print (row[1])

                        combo = (manipulate_gRNA_name, row[1])
                        storage.append(combo)
            print ('File has been read!')
            print ('')
            break
        except: 
            print ('')
            print ('''Wrong file path. Please try again. 
There could be several reasons why it failed. 
You may have forgotten to add .csv at the end of your file path. 
You may have inserted a slightly wrong address. Every letter and punctuation must be included!
You may have use the wrong backslash or forward slash. For Windows and Mac, the input must be with (/) to separate levels.
In the rare occassion, your .csv file is NOT a comma separated values (.csv) file but rather a different type of .csv file (indicated by the presence of (\ + ufeff)). 
If so, you would have to exit out the program and resave your starting excel file as a comma separated values (.csv) file.''')
            print ('')
    if response2 == 'unedited': 
        try: 
            with open (file_path, mode = 'r') as csv_file: 
                csv_reader = csv.reader(csv_file, delimiter = ',')
                storage = []
                count = 0
                for row in csv_reader:
                    if len(row)<=2: 
                        print ('')
                        print ('You may be accessing an edited .csv file but have the unedited response selected.')
                        print ('Do you want to change your response from unedited to edited?')
                        while True: 
                            response2 = input('Enter "edited" (no quotations) if you want to work with an unedited file: ')
                            response2 = response2.strip()
                            response2 = response2.lower()
                            #print (response)
                            if response2 == 'edited':
                            #For future reference, always make your if statement what you want to achieve if the right response/answer is given 
                                break
                            else: 
                                print ('Please enter an appropriate response.')
                                print ('')
                        print ('')
                        print ("First, the statement 'The headers 'Name' and 'Sequence' could not be found...The headers in the first row...' will be printed")
                        print ('Second, the exception will be raised, stating that you have the wrong file path.')
                        print ('Then, because of the structure of the code, you will be asked to put in the file path of the .csv you want to read.')
                        print ('')
                    if count == 0:
                        try:
                            column1_ideal_name_index = row.index('Name')
                            #for lists, list_name.index(x) format is used to find the index of element name x from the list with list_name
                            #print (column1_ideal_name_index)
                            column2_ideal_sequence_name_index= row.index('Sequence')
                            #print (column2_ideal_sequence_name_index)
                        except: 
                            print ('')
                            print ('The headers "Name" and "Sequence" could not be found in the .csv file you specified.')
                            print ('The headers in the first row of the .csv file you specified are ', row)
                        combo = (row[column1_ideal_name_index], row[column2_ideal_sequence_name_index])
                        storage.append(combo)
                        count = count + 1
                    else: 
                        manipulate_gRNA_name = ""
                        manipulate_gRNA_name = row[column1_ideal_name_index]
                        #Save the output from row[index containing gRNA name] as a different variable so it can be manipulated 

                        manipulate_gRNA_name = manipulate_gRNA_name.replace('(', '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace(')', '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace(',', '.')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('+','')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace("'", '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('-', '')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('/', '.')
                        manipulate_gRNA_name = manipulate_gRNA_name.replace('\\', '.')
                        #Do a lot of manipulations to the name to get rid of (),+'-/\

                        length_of_name = len(manipulate_gRNA_name)
                        if manipulate_gRNA_name[-1] == '_':
                            manipulate_gRNA_name = manipulate_gRNA_name[0:length_of_name - 1]
                        #For getting rid of _ at the end of each sequence name 

                        row[column2_ideal_sequence_name_index] = row[column2_ideal_sequence_name_index] + (addition)
                        combo = (manipulate_gRNA_name, row[column2_ideal_sequence_name_index])
                        storage.append(combo)
            print ('File has been read!')
            print ('')
            break
        except: 
            print ('')
            print ('''Wrong file path. Please try again. 
There could be several reasons why it failed. 
You may have forgotten to add .csv at the end of your file path. 
You may have inserted a slightly wrong address. Every letter and punctuation must be included!
You may have use the wrong backslash or forward slash. For Windows and Mac, the input must be with (/) to separate levels. 
In the rare occassion, your .csv file is NOT a comma separated values (.csv) file but rather a different type of .csv file (indicated by presence of (\ + ufeff)). 
If so, you would have to exit out the program and resave your starting excel file as a comma separated values (.csv) file.''')
            print ('')


#Idea was based off of https://www.geeksforgeeks.org/update-column-value-of-csv-in-python/#
#Essentially, you store your changes in the storage list, but the file you read remains the same. 
#Then, with the storage list, you write in a new .csv file. 
#https://realpython.com/python-csv/ gives info about reading and writing csv files. Gives insights about deliimters 

print (storage)

#PART 4
#Generating a new .csv file that has the addition of base pairs at the end of each guide sequence

print ('')
while True: 
    last_index = file_path.rfind('/')
    folder_path = file_path[0:last_index]
    print (folder_path)
    print('')
    print ('Do you want your new, updated .csv file in the same folder as the file you specified earlier?')
    print ('Acceptable responses are only "Yes" or "No" (excluding the quotations).')
    print ('For reference, the folder that containted the .csv file you made me read is ' + folder_path)
    response3 = input('Enter your response here: ')
    print ('')
    response3 = response3.strip()
    response3 = response3.lower()
    #print (response)
    if response3 == 'yes': 
    #For future reference, always make your if statement what you want to achieve if the right response/answer is given 
        print ('')
        print (response3)
        print ('What would you like to name your file? Your file name must include .csv at the end!')
        new_csv_file_name = input('Enter your file name here: ')
        x = new_csv_file_name.find('.csv')
        if x == -1:
            new_csv_file_name  = new_csv_file_name  + '.csv'
        new_updated_csv_file_path = folder_path + '/' + new_csv_file_name 
        print (new_updated_csv_file_path)
        break
    elif response3 == 'no':
        print ('')
        print ('What folder would you like to store your new .csv file in?')
        print ('For reference, the folder contained the .csv file you made me read was ' + folder_path)
        print ('When entering your new folder path, DO NOT PUT / at the end!')
        new_folder_path = input('Enter your new folder path here: ')

        #Ensure that there are no \ characters and that / is not at the end 
        if new_folder_path[-1] == '/': 
            new_folder_path = new_folder_path[0:len(new_folder_path)-1]
        if '\\' in new_folder_path: 
            new_folder_path = new_folder_path.replace('\\', '/')
    
        print ('')
        print('Now that we have specified the folder path, what would you like to name your new file? Your file name must include .csv at the end')
        new_csv_file_name = input('Enter your file name here: ')
        x = new_csv_file_name.find('.csv')
        if x == -1:
            new_csv_file_name  = new_csv_file_name  + '.csv'
        new_updated_csv_file_path = new_folder_path + '/' + new_csv_file_name 
        print (new_updated_csv_file_path)
        break
    else: 
        print ('Please enter an appropriate response.')
        print ('')

print ('')

while True: 
    if '.csv' in new_updated_csv_file_path: 
        try: 
            with open (new_updated_csv_file_path, mode = 'w', newline = '') as csv_file2: 
            #newline = '' eliminates the empty rows that were originally created when I was writing in each row. 
            #https://stackoverflow.com/questions/4521426/delete-blank-rows-from-csv
                csv_writer = csv.writer(csv_file2, delimiter = ',')
                for row in storage: 
                    csv_writer.writerow(row)
                print ('')
                print ('.csv file was created!')
                print ('')
            break
        except: 
            print ('')
            print ('An error occurred. Maybe you did not input a complete file path. Try again.')
            print ('')
            print ('You will have to enter a new file path. For reference, a file path looks like /Users/hyl025/Desktop/Python/Updated Side Project Appending Base pairs/Code Testing v2/gblocks.csv') 
            print ('In your scenario, scroll through the TERMINAL (where all the text is being printed onto the screen) to find out what a file path looks like in your case.')
            new_updated_csv_file_path = input('Enter an appropriate file path that includes / to separate folders and .csv at the end: ')
            if '\\' in new_updated_csv_file_path: 
                new_updated_csv_file_path  = new_updated_csv_file_path.replace('\\', '/')
    else: 
            print ('')
            print ('An error occurred. Maybe you did not input a complete file path. Try again.')
            print ('')
            print ('You will have to enter a new file path. For reference, a file path looks like /Users/hyl025/Desktop/Python/Updated Side Project Appending Base pairs/Code Testing v2/gblocks.csv') 
            print ('In your scenario, scroll through the TERMINAL (where all the text is being printed onto the screen) to find out what a file path looks like in your case.')
            new_updated_csv_file_path = input('Enter an appropriate file path that includes / to separate folders and .csv at the end: ')
            if '\\' in new_updated_csv_file_path: 
                new_updated_csv_file_path  = new_updated_csv_file_path.replace('\\', '/')
 

print ('Even if you put in the wrong file path for your .csv file and the .csv file was created, the file will be located in the same folder as where you ran this program.')
print ('')

if response == 'idt': 
    print ('The website to order your gblocks from IDT (login required) is https://www.idtdna.com/pages')
if response == 'twist biosciences': 
    print ('The website to order your gblocks from Twist Biosciences (login required) is https://id.twistdna.com/signin')

print ('')
print ('Thank you for using me and have a great day!')


#Testing phase 1.14.2024 
#Worked with 
# - able to reroute from edited to unedited when describing what the .csv file I wanted to manipulate 
# - a .csv file using columns 0 and 13 for name and sequence, respectively
# - using the same folder path 
# - not putting .csv at the end when putting in the name of file 
# - file outputted at the end had the correct name changes (no ()-+',) and longer sequences from the original sequence 

#Worked with 
# - a .csv file using columns 0 and 15 for name and sequence, respectively
# - choosing a different folder path and including the / at the end. The program was able to catch the / I added and deleted it 
# - On a separate attempt, also forgot to add .csv at the end. The program was able to catch the missing .csv and added it at the end. 
# - file outputted at the end had longer sequences from the original sequences and was placed in the folder I specified

#Fixed issue when trying to write into csv_file2
# - if you had the wrong new_updated_csv_file_path, before, you would end up in an infinite loop or just reach the end of the code without actually getting the right updated .csv file 
# - Now, the else statement after the except statement acts as a check. 
#       When going through the while loop, if you fail the try block, then you get to the except block.
#       Now, if you fail the except block, you'll go to the else statement within the while loop 
#       If you keep failing, you will always go to the else statement 
#       The only way out is if you have the right file path or just input .csv at the end

#Saw issue and came up with resolution when you have the wrong .csv format. 
# - You need a comma separated values (.csv) format NOT a CSV UTF-8 (comma delimited(.csv) format
# - Just want to make it clear across document that you need a specific .csv format and that this issue is rare. 



