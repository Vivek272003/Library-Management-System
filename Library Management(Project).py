global a
global b
a=input("Enter the Username of mysql:")
b=input("Enter the Password of mysql:")

import mysql.connector as v
conn=v.connect(host="localhost",user=a,passwd=b,charset="utf8")
if conn.is_connected():
    print("connected")
else:
    print("not connected")

mycur=conn.cursor()
mycur.execute("create database if not exists library_management")

from mysql.connector import errorcode 
from datetime import date, datetime, timedelta 
from mysql.connector import (connection) 
import os 
import platform
cnx = connection.MySQLConnection(user=a, passwd=b, 
                     host='localhost', 
                     database="library_management") 
Cursor = cnx.cursor() 
Cursor.execute("create table if not exists bookrecord(Bno integer primary key,Bname varchar(30)not null,Author varchar(40),Price decimal,publ varchar(40),qty integer,d_o_purchase date)")
Cursor.execute("create table if not exists Member(Mno integer primary key,Mname varchar(30) not null,MOB bigint(10)not null ,DOM date,ADR varchar(50))")
Cursor.execute("create table if not exists issue(Bno integer references bookrecord(bno),Mno integer references member(mno),doi date,dor date)")


def display(): 
    try: 
        os.system('cls') 
        cnx = connection.MySQLConnection(user=a, passwd=b, 
                     host='localhost', 
                     database="library_management") 
        Cursor = cnx.cursor() 
        query = ("SELECT * FROM BookRecord") 
        Cursor.execute(query)
        s=0
 
        for (Bno,Bname,Author,price,publ,qty,d_o_purchase) in Cursor:
            s+=1
            print("==============================================================") 
            print("Book Code                    : ",Bno) 
            print("Book Name                    : ",Bname) 
            print("Author of Book               : ",Author) 

 
 
            print("Price of Book                : ",price) 
            print("Publisher                    : ",publ) 
            print("Total Quantity in Hand       : ",qty) 
            print("Purchased On                 : ",d_o_purchase) 
            print("===============================================================")
        print(s,"Record(s)found")    
 
        Cursor.close() 
        cnx.close()

        print("You have done it!!!!!!") 
    except mysql.connector.Error as err: 
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
        print("Something is wrong with your user name or password") 
      elif err.errno == errorcode.ER_BAD_DB_ERROR: 
        print("Database does not exist") 
      else: 
        print(err) 
    else: 
      cnx.close()       



def insertData(): 
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host="localhost", 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        bno=input("Enter Book Code       : ") 
        bname=input("Enter Book Name       : ") 
        Auth=input("Enter Book Author's Name      : ") 
        price=int(input("Enter Book Price    : ")) 
        publ=input("Enter Publisher of Book     : ") 

 
 
        qty=int(input("Enter Quantity purchased       : ")) 
        print("Enter Date of Purchase (Date/MOnth and Year seperately) ") 
        DD=int(input("Enter Date       : ")) 
        MM=int(input("Enter Month   : ")) 
        YY=int(input("Enter Year    : ")) 
        Qry = ("INSERT INTO BookRecord VALUES (%s, %s, %s, %s, %s, %s, %s)") 
        data = (bno,bname,Auth,price,publ,qty,date(YY,MM,DD)) 
        Cursor.execute(Qry,data) 
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record Inserted..............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
 
 
def deleteBook(): 
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        bno=input("Enter Book Code of Book to be deleted from the Library     : ") 

 
 
         
        Qry =("""DELETE FROM BookRecord WHERE BNO = %s""") 
        del_rec=(bno,) 
        Cursor.execute(Qry,del_rec) 
         
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print(Cursor.rowcount,"Record(s) Deleted Successfully.............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
     
 
def SearchBookRec(): 
    try: 
        cnx = connection.MySQLConnection(user='root', 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        bno=input("Enter Book No to be Searched from the Library     : ") 
        query = ("SELECT * FROM BookRecord where BNo = %s ") 
         
        rec_srch=(bno,) 
        Cursor.execute(query,rec_srch) 

 
 
         
        Rec_count=0 
         
        for (Bno,Bname,Author,price,publ,qty,d_o_purchase) in Cursor: 
            Rec_count+=1 
            print("==============================================================") 
            print("Book Code                    : ",Bno) 
            print("Book Name                    : ",Bname) 
            print("Author of Book               : ",Author) 
            print("Price of Book                : ",price) 
            print("Publisher                    : ",publ) 
            print("Total Quantity in Hand       : ",qty) 
            print("Purchased On                 : ",d_o_purchase) 
            print("===============================================================") 
            if Rec_count%2==0: 
                input("Press any key to continue") 
                clrscreen() 
        print(Rec_count, "Record(s) found") 
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
def UpdateBook(): 
    try: 

 
 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        bno=input("Enter Book Code of Book to be Updated from the Library     : ") 
        
 
        print("***Enter new data*** ") 
        bname=input("Enter Book Name           : ") 
        Auth=input("Enter Book Author's Name   : ") 
        price=int(input("Enter Book Price      : ")) 
        publ=input("Enter Publisher of Book    : ") 
        qty=int(input("Enter Quantity purchased       : ")) 
        print("Enter Date of Purchase (Date/MOnth and Year seperately: ") 
        DD=int(input("Enter Date               : ")) 
        MM=int(input("Enter Month              : ")) 
        YY=int(input("Enter Year               : ")) 
         
                 
        Qry = ("UPDATE BookRecord SET bname=%s,Author=%s,price=%s,publ=%s,qty=%s,d_o_purchase=%s WHERE BNO=%s") 
        data = (bname,Auth,price,publ,qty,date(YY,MM,DD),bno) 
 
        Cursor.execute(Qry,data) 
        # Make sure data is committed to the database
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record(s) Updated Successfully.............") 
    except mysql.connector.Error as err:         

 
 
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err)  
        cnx.close() 

 

 
import mysql.connector 
from mysql.connector import errorcode 
from datetime import date 
from mysql.connector import (connection) 
import os 
 
def clrscreen(): 
    print('\n' *5) 

 
def ShowIssuedBooks(): 
    try: 
        os.system('cls') 
        cnx = connection.MySQLConnection(user=a, passwd=b, 
                     host='localhost', 
                     database="library_management") 
        Cursor = cnx.cursor() 
        query = ("SELECT B.bno,bname,M.mno,mname,doi,dor FROM bookRecord B,issue I,member M where B.bno=I.bno and I.mno=M.mno and dor is null") 
        Cursor.execute(query)
        count=0
        for (Bno,Bname,Mno,Mname,doi,dor) in Cursor:
            count+=1
            print("==============================================================") 

            print("Book Code                    : ",Bno) 
            print("Book Name                    : ",Bname) 
            print("Member Code                  : ",Mno) 
            print("Member Name                  : ",Mname) 
            print("Date of issue                : ",doi) 
            print("Today's Date                 : ",date.today()) 
             
            print("===============================================================") 
 
        Cursor.close() 
        cnx.close() 
        print(count,"Record(s) found") 
    except mysql.connector.Error as err: 
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
        print("Something is wrong with your user name or password") 
      elif err.errno == errorcode.ER_BAD_DB_ERROR: 
        print("Database does not exist") 
      else: 
        print(err) 
    else: 
      cnx.close() 



def ReturnedBooks(): 
    try: 
        os.system('cls') 
        cnx = connection.MySQLConnection(user=a, passwd=b, 
                     host='localhost', 
                     database="library_management") 
        Cursor = cnx.cursor() 
        query = ("SELECT B.bno,bname,M.mno,mname,doi,dor FROM bookRecord B,issue I,member M where B.bno=I.bno and I.mno=M.mno and dor is not null") 
        Cursor.execute(query)
        count=0
        for (Bno,Bname,Mno,Mname,doi,dor) in Cursor:
            count+=1
            print("==============================================================") 

            print("Book Code                    : ",Bno) 
            print("Book Name                    : ",Bname) 
            print("Member Code                  : ",Mno) 
            print("Member Name                  : ",Mname) 
            print("Date of issue                : ",doi) 
            print("Date of return               : ",dor) 
             
            print("===============================================================") 
 
        Cursor.close() 
        cnx.close() 
        print(count,"Record(s) found")
    except mysql.connector.Error as err: 
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
        print("Something is wrong with your user name or password") 
      elif err.errno == errorcode.ER_BAD_DB_ERROR: 
        print("Database does not exist") 
      else: 
        print(err) 
    else: 
      cnx.close() 
              
def deleteBooks():
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor()
        
        ch=input("Do you really want to delete all Returned Books record (Y/N):")
        if ch=="Y" or ch=="y":
            Cursor.execute("delete from issue where dor is not null")
        else:
            return
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record(s) Deleted..............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
     
 
    
 
def issueBook(): 
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        bno=int(input("Enter Book Code to issue   : ")) 
        mno=int(input("Enter Member Code          : ")) 

 
 
        print("Enter Date of Issue (Date/MOnth and Year seperately: ") 
        DD=int(input("Enter Date              : ")) 
        MM=int(input("Enter Month             : ")) 
        YY=int(input("Enter Year              : ")) 
         
        Qry = ("INSERT INTO issue (bno,mno,doi) VALUES (%s,%s,%s)") 
        data =(bno,mno,date(YY,MM,DD)) 
        Cursor.execute(Qry,data) 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record Inserted..............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
 
 
def returnBook(): 
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        bno=input("Enter Book Code of Book to be returned to the Library : ") 
        Mno=input("Enter Member Code of Member who is returning Book     : ") 

 
 
        retDate=date.today() 
        Qry =("""Update Issue set dor= %s WHERE BNO = %s and Mno= %s """) 
        rec=(retDate,bno,Mno) 
        Cursor.execute(Qry,rec) 
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record(s) Updated Successfully.............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
          
        cnx.close() 
   

import mysql.connector 
from mysql.connector import errorcode 
from datetime import date, datetime, timedelta 
from mysql.connector import (connection) 
import os 
     
def clrscreen(): 
    print('\n' *5)
     
   
def displayMember(): 
    try: 
        os.system('cls') 
        cnx = connection.MySQLConnection(user=a , passwd=b , 
                     host='localhost', 
                     database="library_management") 
        Cursor = cnx.cursor() 
        query = ("SELECT * FROM Member") 
        Cursor.execute(query)
        s=0
 
        for (Mno,Mname,MOB,DOM,ADR) in Cursor:
            s+=1
            print("==============================================================") 
            print("Member Code                    : ",Mno) 
            print("Member Name                    : ",Mname) 
            print("Mobile No.of Member            : ",MOB) 
            print("Date of Membership             : ",DOM) 
            print("Address                        : ",ADR) 
            print("===============================================================")
        print(s,"Record(s)found")
        Cursor.close() 
        cnx.close() 
        print("You have done it!!!!!!") 
    except mysql.connector.Error as err: 
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
        print("Something is wrong with your user name or password") 
      elif err.errno == errorcode.ER_BAD_DB_ERROR: 
        print("Database does not exist") 
      else: 
        print(err) 
    else: 
      cnx.close() 
       
 
 
def insertMember(): 
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        mno=input("Enter Member Code       : ") 
        mname=input("Enter Member Name       : ") 
        mob=input("Enter Member Mobile No.      : ") 
        print("Enter Date of Membership (Date/MOnth and Year seperately: ") 
        DD=int(input("Enter Date    : ")) 
        MM=int(input("Enter Month   : ")) 
        YY=int(input("Enter Year    : ")) 
        addr=input("Enter Member Adress    : ") 
        Qry = ("INSERT INTO Member VALUES (%s, %s, %s, %s, %s)") 
        data = (mno,mname,mob,date(YY,MM,DD),addr) 
        Cursor.execute(Qry,data) 
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record Inserted..............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
 
 
def deleteMember(): 
    try: 

 
 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor() 
 
        mno=input("Enter Member Code  to be deleted from the Library     : ") 
         
        Qry =("""DELETE FROM Member WHERE MNO = %s""") 
        del_rec=(mno,) 
        Cursor.execute(Qry,del_rec) 
         
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print(Cursor.rowcount,"Record(s) Deleted Successfully.............") 
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 
         
        cnx.close() 
   
 
def SearchMember(): 
    try: 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 

 
 
        Cursor = cnx.cursor() 
        print("1<---Search with Member Name")
        print("2<---Search with Member Code")
        v=int(input("Enter your choice between 1 to 2--->"))
        if v==1:
            mnm=input("Enter Member Name to be Searched from the Library     : ") 
            query = ("SELECT * FROM Member where Mname = %s ")
        elif v==2:
            mnm=input("Enter Member Number to be Searched from the Library     : ") 
            query = ("SELECT * FROM Member where Mno = %s ")
        rec_srch=(mnm,) 
        Cursor.execute(query,rec_srch) 
         
        Rec_count=0 
 
 
        for (Mno,Mname,MOB,DOM,ADR) in Cursor:
            Rec_count+=1
            print("==============================================================") 
            print("Member Code                       : ",Mno) 
            print("Member Name                       : ",Mname) 
            print("Mobile No.of Member               : ",MOB) 
            print("Date of Membership                : ",DOM) 
            print("Address                           : ",ADR) 
            print("===============================================================")      
            

        print(Rec_count, "Record(s) found") 
        # Make sure data is committed to the database 
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        
    except mysql.connector.Error as err:         
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err) 

 
 
        cnx.close()

def UpdateMember(): 
    try: 

 
 
        cnx = connection.MySQLConnection(user=a, 
                                         passwd=b, 
                                         host='localhost', 
                                         database="library_management") 
        Cursor = cnx.cursor()
        mno=input("Enter Member Code to be Updated from the Library     : ")


        print("***Enter new data*** ")  
        mname=input("Enter Member Name         : ") 
        mob=input("Enter Member Mobile No.     : ") 
        print("Enter Date of Membership (Date/MOnth and Year seperately: ") 
        DD=int(input("Enter Date               : ")) 
        MM=int(input("Enter Month              : ")) 
        YY=int(input("Enter Year               : ")) 
        adr=input("Enter Member Adress         : ") 
        

        Qry = ("UPDATE member SET mname=%s,mob=%s,dom=%s,adr=%s WHERE mno=%s") 
        data = (mname,mob,date(YY,MM,DD),adr,mno) 
 
        Cursor.execute(Qry,data) 
        # Make sure data is committed to the database
        cnx.commit() 
        Cursor.close() 
        cnx.close() 
        print("Record(s) Updated Successfully.............") 
    except mysql.connector.Error as err:         

 
 
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
            print("Something is wrong with your user name or password") 
        elif err.errno == errorcode.ER_BAD_DB_ERROR: 
            print("Database does not exist") 
        else: 
            print(err)  
        cnx.close() 

 


def MenuBook(): 
    while True: 
     
        print("\t\t\t Book Record Management\n") 
        print("==============================================================") 
        print("1. Add Book Record              ") 
        print("2. Display Book Records         ") 
        print("3. Search Book Record           ") 
        print("4. Delete Book Record           ") 
        print("5. Update Book Record           ") 
        print("6. Return to Main Menu          ") 
        print("===============================================================") 
        choice=int(input("Enter Choice between 1 to 6-------> :  ")) 
        if choice==1: 
            insertData() 
        elif choice==2: 
            display()   
        elif choice==3: 
            SearchBookRec() 
        elif choice==4: 
            deleteBook() 
        elif choice==5: 
            UpdateBook() 
        elif choice==6: 
            return 
        else: 
            print("Wrong Choice......Enter Your Choice again") 
            x=input("Enter any key to continue") 
#----------------------------------------------------------------------------------------        
def MenuMember(): 
    while True:  
        
        print("\t\t\t Member Record Management\n") 
        print("==============================================================") 
        print("1. Add Member Record              ") 
        print("2. Display Member Records         ") 
        print("3. Search Member Record           ") 
        print("4. Delete Member Record           ") 
        print("5. Update Book Record             ") 
        print("6. Return to Main Menu            ") 
        print("===============================================================") 
        choice=int(input("Enter Choice between 1 to 6-------> :  ")) 
        if choice==1: 
            insertMember() 
        elif choice==2: 
            displayMember()     
        elif choice==3: 
            SearchMember() 
        elif choice==4: 
            deleteMember() 
        elif choice==5: 
            UpdateMember() 
        elif choice==6: 
            return 
        else: 
            print("Wrong Choice......Enter Your Choice again") 
            x=input("Enter any key to continue") 
#---------------------------------------------------------------------------------------- 
def MenuIssueReturn(): 
    while True: 
      
        print("\t\t\t ISSUE BOOK MANAGEMENT \n") 
        print("==============================================================") 
        print("1. Issue Book                   ") 
        print("2. Display Issued Book Records  ") 
        print("3. Return Issued Book           ")
        print("4. Show All Returned Books               ")
        print("5. Delete All Returned Books Data              ")
        print("6. Return to Main Menu          ") 

 
 
        print("===============================================================") 
        choice=int(input("Enter Choice between 1 to 4-------> :  ")) 
        if choice==1: 
            issueBook() 
        elif choice==2: 
            ShowIssuedBooks()     
        elif choice==3: 
            returnBook()
        elif choice==4:
            ReturnedBooks()
        elif choice==5: 
            deleteBooks()
        elif choice==6:
            return
        else: 
            print("Wrong Choice......Enter Your Choice again") 
            x=input("Enter any key to continue") 
 

 
while True: 
    
    print("\t\t\t Library Management\n") 
    print("==============================================================") 
    print("1. Book Management              ") 
    print("2. Members Management         ") 
    print("3. Issue/Return Book                   ") 
    print("4. Exit                         ") 
    print("===============================================================") 
    choice=int(input("Enter Choice between 1 to 4-------> :  ")) 
    if choice==1: 
        MenuBook() 
    elif choice==2: 
        MenuMember()    
    elif choice==3: 
        MenuIssueReturn() 
    elif choice==4: 
        exit()
    else: 
        print("Wrong Choice......Enter Your Choice again") 
        x=input("Enter any key to continue") 



