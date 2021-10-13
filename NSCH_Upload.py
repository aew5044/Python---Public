"""
Version 1.0
Created on 20211012
Modified on 20211013
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
lookback='19940101'
csvfname='NSCH Upload Generator from Person.csv'

#define the location of the raw data.
os.chdir(r'C:\Users\____\OneDrive - Wilson Community College\01_Python\NSCH Upload Generator\2021FA')
#today's date as YYYYMMDD - used for NSCH and txt output.
today = datetime.datetime.today().strftime ('%Y%m%d')

#Import column names.
inames=['00',cname,today,type,'I','d5']

#Import process.
nsch = pd.read_csv(csvfname,  header=None,
    skiprows=1, names=inames, dtype={'d5':str},)

#reorder and create columns.  
nsch=nsch.reindex(columns=['H1',colcode,'00',cname,today,type,'I','d1','d2','d3','d4','d5'], copy=True,fill_value='')

#only keeps the first character of the middle name.
nsch[cname]=nsch[cname].str.slice(0,1)

#defines variables. 
nsch[['H1',colcode,'d1','d2','d3','d4']]=[['D1',' ',today,lookback,colcode,'00']]

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






