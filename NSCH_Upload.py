"""
Version 1.0
Created on 20211012
Modified on 20211014
@author: Andrew Walker
Email: aew5044@gmail.com
Email2: awalker@wilsoncc.edu
https://walkerdataranger.com/
"""
import datetime
import pandas as pd
import os

colcode='004845'
cname='Wilson Community College'
type='SE'
look='19940101'
csvfname='NSCH Upload Generator from Person.csv'
os.chdir(r'C:\Users\aw7498\OneDrive - Wilson Community College\01_Python\NSCH Upload Generator\2021FA')

numcheck=0
toptions=['SE','CO','DA','PA','SB']

def checker():
    global numcheck
    
    if len(colcode)!=6:
        numcheck=1  
    
    if type not in toptions:
        numcheck=1
            
    if look[0:2] not in ['19','20'] and len(look)!=8:
        numcheck=1
        
    if (csvfname[-4:]) !='.csv':
        numcheck=1

checker()
        
def checker2():
    if len(colcode)!=6:
        print('ERROR: Make sure your colcode is wrapped in single quotes and contains six digits.')
    else:
        print('CORRECT: The college code is the right length.')
        
    toptions=['SE','CO','DA','PA','SB']
    
    if type in toptions:
        print('CORRECT: An appropriate NSCH upload type is selected.')
    else:
        print('ERROR: Make sure you have the correct upload type.'"\nBe sure to select either \'SE\',\'CO\',\'DA\',\'PA\',or \'SB\'")
            
    if look[0:2] in ['19','20'] and len(look)==8:
        print('CORRECT: The format and length for the date looks appropriate')
    else:
        print('ERROR: Review your "look" date, it needs to be in YYYYMMDD wrapped in single quotes.'
              '\nAfter updating, re-run the line and check the code.')
        
    if (csvfname[-4:]) !='.csv':
        print('ERROR: Be sure the csvfname is set to a .csv file.')
    else:
        print('CORRECT: Looks like a .csv file is indicated as the source data.')


cname=cname[0:39]
today = datetime.datetime.today().strftime ('%Y%m%d')

def run():
    
    #define the file location of the raw data.
    #today's date as YYYYMMDD - used for NSCH and txt output.
    
    #Import column names.
    inames=['00',cname,today,type,'I','d5']
    
    #Import process.
    
    nsch = pd.read_csv(csvfname,  header=None, skiprows=1, names=inames, dtype={'d5':str},)
    
    #reorder and create columns.  
    nsch=nsch.reindex(columns=['H1',colcode,'00',cname,today,type,'I','d1','d2','d3','d4','d5'], copy=True,fill_value='')
    
    #truncate values to ensure they do not exceed NSCH max limit.
    nsch[cname]=nsch[cname].str.slice(0,1)
    nsch['00']=nsch['00'].str.slice(0,19)
    nsch[today]=nsch[today].str.slice(0,19)
    nsch[type]=nsch[type].str.slice(0,7)
    nsch['d5']=nsch['d5'].str.slice(0,49)
    nsch['d5']=nsch['d5'].str.slice(0,49)
    
    #defines variables. 
    nsch[['H1',colcode,'d1','d2','d3','d4']]=[['D1',' ',today,look,colcode,'00']]
    
    #removes various characters from the suffix, and replace np.nan with ' '.
    nsch[type].replace(r'\W',' ',inplace=True,regex=True)
    nsch[type].fillna(' ',inplace=True)
    nsch['I'].replace(r'\D','',inplace=True,regex=True)
    
    #defines the total rows, adds two, converts the number to a string and concatenates 'T1.'
    total_rows = 'T1'+str(nsch.shape[0]+2)
    
    #builds the footer for the output file.
    d={'H1':[total_rows],colcode:' ', '00':' ', cname:' ', today:' ', type:' ', 'I':' ', 'd1':' ', 
       'd2':' ', 'd3':' ', 'd4':' ', 'd5':' '}
    
    #adds the footer to the out file.
    out=nsch.append(pd.DataFrame(data=d))
    
    #exports the data to a txt file and recodes the headers.
    out.to_csv('upload'+'_'+str(today)+'.txt', header=['H1',colcode,'00',cname,today,type,'I',' ',' ',' ',' ',' '], index=False, sep='\t', na_rep='') 
    
    #This section exports the paramaters for documentation;
    docs=[colcode, cname, type, look, csvfname]
    
    filename='Parameters used in the NSCH upload file on '+str(today)+'.txt'
    
    with open(filename,'w') as file_object:
        for doc in docs:
            file_object.write(doc+'\n')

if numcheck>0:
    
    print('\n''\n''\n''There is an error in one of the defined variables.'
          'Review the following statements to see which variable(s) need updating.''\n')
    checker2()
else:
    run()
    print('SUCCESS!!!''\n''The program ran. Look in your projects folder for '+ '\n'+"Parameters used in the NSCH upload file on "+str(today)+'.txt')
    

