from docs import update2 as update
import re
from write import writeout
"""
CREATE TABLE planes (
      Status  varchar(100),
      Owner  varchar(50),
      CN varchar(50),
      Reg  varchar(10),
      Address  varchar(100),
      Manu  varchar(50), 
      Type  varchar(50), 
      ICAO  varchar(50), 
      Hex  varchar(50), 
      Date_Reg  varchar(50), 
      Canx_To  varchar(50), 
      Date_Canx varchar(50));
"""

import pymysql
# Open database connection
# DB is Dead Now
db = pymysql.connect(host="sql9.freemysqlhosting.net", user="sql9268306", passwd="HljwpGFLAV", db="sql9268306")
# Is a bad to store plaintext password in a program  YES
# does this yes database expire in a week YES
mycursor = db.cursor()

class Register():
    def __init__(self,Reg):
        self.Reg = Reg
        self.delete = False
        mycursor.execute(f"SELECT * FROM planes WHERE Reg = '{Reg}'")
        self.exists = len(mycursor.fetchall()) != 0
        #Check if in Databases
        self.Updates = {
        "Aircraft Newly Registered": self.Register,
        "Aircraft Cancelled":self.Cancel,
        "Aircraft Re-Registered":self.ReRegister,
        "Change of Status":self.UpdateStatus,
        "Change of Owner":self.UpdateOwner,
        "Change of Address":self.UpdateAddress,
        "Aircraft Newly Reserved": self.Register,
        }
    def send(self):
        del self.Updates
        exists = self.exists
        delete = self.delete
        del self.exists
        del self.delete
        columns = str(self.__dict__.keys())[11:-2]
        data = str(self.__dict__.values())[13:-2]
        columns = columns.replace("'", "")
        #DELETE FROM planes WHERE Reg = '23456'
        if exists and delete:
            mycursor.execute(f"DELETE FROM planes WHERE Reg = '23456'")
            db.commit()
            writeout(f"**********{self.Reg} DELETED SUCCESSFULLY**********",color='green') 
            return
        elif(delete):
            writeout(f"WARNING: {self.Reg} DIDNT EXIST. DELETION CONSIDERED SUCCESSFULL",color='yellow') 
            return

        if exists:
            Reg = self.Reg
            del self.Reg
            for key in self.__dict__:
                mycursor.execute(f"UPDATE planes SET {key} = '{self.__dict__[key]}' WHERE Reg = {Reg}")
                db.commit()
                writeout("**********UPDATE SENT SUCCESSFULLY**********",color='green')  
        else:
            try:
                request = f"INSERT INTO planes ({columns}) VALUES ({data})"
                mycursor.execute(request)
                db.commit()
                writeout("**********INSERTION SENT SUCCESSFULLY**********",color='green')  
            except:
                writeout("ERROR: FAILED TO UPLOAD REQUEST:\n" + request,color='red')
        

    def Register(self,key,data):
        if key == None:
            return 
        key = key.replace(" ", "_")
        self.__dict__[key] = data
        writeout(f"REGISTER '{self.Reg}' IS STORING: {key}, {data}" ,sep='')
    def ReRegister(self,key,data):
        if key == None:
            return 
        key = key.replace(" ", "_")
        pass
    def Cancel(self,key,data):
        if key == None:
            return 
        key = key.replace(" ", "_")
        self.delete = True
    def UpdateStatus(self,key,data):
        if key == None:
            return 
        key = key.replace(" ", "_")
        if key == "New Status":
            self.Status = data
            writeout(f"UPDATED STATUS OF '{self.Reg}' to '{data}'",color='green')
    def UpdateOwner(self,key,data):
        if key == None:
            return 
        key = key.replace(" ", "_")
        if key == "New Owner":
            self.Owner = data
            writeout(f"UPDATED OWNER OF '{self.Reg}' to '{data}'",color='green')
    def UpdateAddress(self,key,data):
        if key == None:
            return 
        key = key.replace(" ", "_")
        if key == "New Address":
            self.Address = data
            writeout(f"UPDATED ADDRESS OF '{self.Reg}' to '{data}'",color='green')   
                
email = update.split('\n')
get_title = r"\|.+?\|"
a = re.compile(get_title)

Get_New_Section = True
Current_Section =  None
Current_Header = None
Current_Reg = None
Data_Read = None
DATAq = None # Update
DATAque = [[None,None]]
ignore = False
for line in email:
    if not line:
        if DATAq != None:
            DATAq.send()
            DATAq = None
            
        continue
    if not ignore and (line != 'None'): #Line is relevant and not empty
        if "====" in line:
            Get_New_Section = True 
            continue
        if Get_New_Section:
            try:
                Current_Section = a.match(line)[0][1:-1]
                Current_Section = Current_Section.strip()
                writeout("SECTION CHANGED TO: " + Current_Section,color="blue")
            except TypeError:
                writeout("WARNING: NO HEADER DEFINED WHEN READING: \n"+line,color='yellow')
                continue
            Get_New_Section = False
            ignore = True 
            continue
        try:
            Current_Header,Data_Read = line.split(':',1)
            Current_Header = Current_Header.strip()
            Data_Read = Data_Read.strip()
        except ValueError:
            writeout("ERROR: FAILED TO EXTRACT HEADER/DATA FROM:\n" + line,color='red')
            DATAque[0][1]+=" " + line
            writeout(f"WARNING: DATA '{line}' WAS APPENDED TO THE LAST '{DATAque[0][0]}' RESULTING IN \n{DATAque[0][1]}",color="yellow" )

        if Current_Header == "Reg":
            Current_Reg = Data_Read
            DATAq = Register(Data_Read)
            writeout(f"NEXT AIRCRAFT: {DATAq.Reg}",color="blue")
            continue

        if Current_Header != None:
            release = DATAque.pop(0)
            DATAq.Updates[Current_Section](release[0],release[1])
        else:
            pass
        DATAque.append([Current_Header,Data_Read])
        Current_Header = None
        Data_Read = None
    ignore = False
    continue

