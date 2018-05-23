import re
import pandas as pd
#Extract Primary Data

#Reads Files into list and adds relevant seperators
def read_file(filename,seperators="NEWDATA"):
    lines=[]
    for line in open(filename,'r'):
        info=line.rstrip('\n')
        if len(info) == 0:
            info=seperators
        lines.append(info)
        print(info)
    lines.append('ENDDATA')
    return lines
 
def Remove_Tabs(line):
    words=re.sub('\t',' ',line)
    words=re.sub('\s{2,7}','',words)
    words=re.sub(',','_',words)
    return words

def Lines_to_Dict(email,diction,pattern=":.+",step=0,seperators='NEWDATA',end_statement='ENDDATA'):
    DATA={}
    ID=re.findall(pattern,email[step])
    ID='DNF' if len(ID)==0 else Remove_Tabs(ID[0])[1:]##[1:] Removes the colon read by regex
    for i in range(step,len(email)):
        if email[i] not in [seperators,end_statement]:
            typ=re.findall('.+:',email[i])
            if len(typ)==0:
                typ=[404]
            abc=re.findall(pattern,email[i])
            if len(abc)==0:
                abc=':Data Not Found'
            else:
                abc=Remove_Tabs(abc[0])[1:]#[1:] Removes the colon read by regex
                try:
                    abc=int(abc)
                except:
                    pass
            DATA.update({typ[0]:abc})
            step+=1
        elif email[i]==end_statement:
            diction.update({ID:DATA})
            return diction
        elif email[i]==seperators:
            print(DATA)
            diction.update({ID:DATA})
          
            return Lines_to_Dict(email,diction,step=step+1)
def Dict_to_CSV(diction,filename="data.csv"):
    df=pd.DataFrame(Data)
    #figure out how to transpose the data in python
    df.to_csv(filename, sep='\t')

input_data='Test_Data.txt'
email=read_file(input_data) #filtered
DataDict=dict()
Data=Lines_to_Dict(email,DataDict)
Dict_to_CSV(Data)

'''
import csv
from itertools import izip
a = izip(*csv.reader(open("test.csv", "rb")))
csv.writer(open("output.csv", "wb")).writerows(a)
 '''
 #[print(i+'*') for i in lines if ' ' in i]


#pattern="([A-Z])*.+\w+:"
 
#Dictionary form abc##include stacking
#for i in Data
#Extract Secondary Data