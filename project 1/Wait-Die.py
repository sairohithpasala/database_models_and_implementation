import sys
import re

TranSact_List = []  #All the transactions are stored in this listt
Inp_Fil = sys.argv[1] 
Oup_Fil = sys.argv[2] 
OP_File = open(Oup_Fil, 'w')
with open(Inp_Fil,'r') as fil_pars:  #File reading
    for Scan_Line in fil_pars.readlines():
        
        TranSact_List.append(Scan_Line)
        TranSact_List = [TranSact_Row_IP.split(';')[0] for TranSact_Row_IP in TranSact_List]
         
print(*TranSact_List,sep="\n")


TranSact_Table_to_list=[] #Storing Transaction table as a data structure list
Lock_Transact_Table_toList=[]   #Storing Lock_Transact_Table_toList as list
Counter_Time_Stamp=1

   

def Initiate_Transact_Begin(TranSact_Row_IP):  #This function is called when it encounters the transaction 'b'.
    global Counter_Time_Stamp
    Table_Contents_Data=[(TranSact_Row_IP[1]),Counter_Time_Stamp,'active',[None],[]] #each Transaction is stored as a the list
    Counter_Time_Stamp=Counter_Time_Stamp+1
    TranSact_Table_to_list.append(Table_Contents_Data) #Adding list to Transaction table
    print("Initate/Begin transaction: T"+str(TranSact_Row_IP[1])+"\n ")
    OP_File.write("Initate/Begin transaction: T"+str(TranSact_Row_IP[1])+"\n ")
    OP_File.write('\n')


def Initiate_Reading_Of_Transaction(TranSact_Row_IP):

    # Indiviual_Transaction_Data_Item - data item to be read
    # Tansaction_id - read operation's transaction id
    global TranSact_Table_to_list
    global Lock_Transact_Table_toList
    Indox_Of_TranSact_Row_IP=0   #index for TranSact_Table_to_list
    Indox_Of_Lock_Table=0  #index for Lock_Transact_Table_toList
    FlaG_Item_Detected=0
    FlaG_TranSaction_Detected=0
    Count_TimeStamp_OF_First_Transaction=0
    Count_TimeStamp_OF_Second_Transaction=0
    
    ID_For_Transact=str(TranSact_Row_IP[1])
    Indiviual_Transaction_Data_Item=TranSact_Row_IP.split('(')[1][0]
   # print(ID_For_Transact)
    for k in range(len(TranSact_Table_to_list)):
        #If the requesting transaction is blocked, it is added to the waitlist for execution.
        if((TranSact_Table_to_list[k][0]==ID_For_Transact) and (TranSact_Table_to_list[k][2]=='Blocked')):
            TranSact_Table_to_list[k][4].append(TranSact_Row_IP)
         #checking the status ,if Transaction is active then perform the Read request based on certain conditions.   
        if((TranSact_Table_to_list[k][0]==ID_For_Transact) and (TranSact_Table_to_list[k][2]=='active')):
            FlaG_TranSaction_Detected=1
            Indox_Of_TranSact_Row_IP=k
            
            if len(Lock_Transact_Table_toList)==0: #if no data_items present in the Lock_Transact_Table_toList
                Locked_Content=[Indiviual_Transaction_Data_Item,TranSact_Row_IP[0],[TranSact_Row_IP[1]]] 
                Lock_Transact_Table_toList.append(Locked_Content)  #add the data_items to the Lock_Transact_Table_toList
                print("ITEM "+str(Indiviual_Transaction_Data_Item)+" is read locked by T"+str(TranSact_Row_IP[1])+"\n ")
                OP_File.write("ITEM "+str(Indiviual_Transaction_Data_Item)+" is read locked by T"+str(TranSact_Row_IP[1])+"\n ")
                OP_File.write('\n')
            else:
                for k in range(len(Lock_Transact_Table_toList)):#if Indiviual_Transaction_Data_Item present
                    f=len(Lock_Transact_Table_toList)
                    if(k>=f):
                        return 0
                    if Lock_Transact_Table_toList[k][0]==Indiviual_Transaction_Data_Item:
                        FlaG_Item_Detected=1  
                        Indox_Of_Lock_Table=k
                        #If Individual_Transaction_Data_Item is in 'Readmode' and is already locked by another transaction, add it to the list requesting Read.
                        if Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='r' and ID_For_Transact not in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                            Lock_Transact_Table_toList[Indox_Of_Lock_Table][2].append(TranSact_Row_IP[1])
                            print("T"+str(TranSact_Row_IP[1])+" is added to the read lock list of Data item "+str(Indiviual_Transaction_Data_Item)+"\n ")
                            OP_File.write("T"+str(TranSact_Row_IP[1])+" is added to the read lock list of Data item "+str(Indiviual_Transaction_Data_Item)+"\n ")
                            OP_File.write('\n')
                        #When the Individual_Transaction_Data_Item is in 'Readmode' and contains the same Transaction ID   
                        elif Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='r' and ID_For_Transact in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                            print("The Requesting Data item already Read locked."+"\n ")
                        #When the Individual_Transaction_Data_Item is in 'writemode' and locked by same Transaction ID    
                        elif Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='w' and ID_For_Transact in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                            print("The Requesting Data item is write locked by the Same Transaction"+"\n ")
                        #When the Individual_Transaction_Data_Item is in 'writemode' and locked by different Transaction ID 
                        #We implement the wait die protocol by comparing timestamps in TranSact_List.
                        elif Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='w' and ID_For_Transact not in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:#wait die protocol
                            t1=TranSact_Table_to_list[Indox_Of_TranSact_Row_IP][0]
                            t2=Lock_Transact_Table_toList[Indox_Of_Lock_Table][2][0]
                            for Part_Of_list in TranSact_Table_to_list:
                                if(Part_Of_list[0]==t1):
                                    Count_TimeStamp_OF_First_Transaction=Part_Of_list[1]
                                if(Part_Of_list[0]==t2):
                                    Count_TimeStamp_OF_Second_Transaction=Part_Of_list[1]

                            if(Count_TimeStamp_OF_First_Transaction>Count_TimeStamp_OF_Second_Transaction): # if requesting transition is younger ...kill it.
                                print("Abort T"+str(t1)+" as it is younger than T"+str(t2)+"\n ")
                                OP_File.write("Abort T"+str(t1)+" as it is younger than T"+str(t2)+"\n ")
                                OP_File.write('\n')
                                Halt_TransacT(t1)
                 
                            elif(Count_TimeStamp_OF_First_Transaction<Count_TimeStamp_OF_Second_Transaction):#if requesting transaction is older, block it.
                                print("BLOCK T"+str(t1)+" as ITEM "+str(Indiviual_Transaction_Data_Item)+" is held by T"+str(t2)+" and T"+str(t1)+" is older than T"+str(t2)+"\n ")
                                OP_File.write("BLOCK T"+str(t1)+" as ITEM "+str(Indiviual_Transaction_Data_Item)+" is held by T"+str(t2)+" and T"+str(t1)+" is older than T"+str(t2)+"\n ")
                                OP_File.write('\n')
                                Blocking_the_Transact(t1,t2,TranSact_Row_IP)
                                
                if(FlaG_Item_Detected==0): #If there is no Individual_Transaction_Data_Item found, then add directly to the Lock_Transact_Table_to List with mode'R'.
                    print("ITEM "+str(Indiviual_Transaction_Data_Item)+" is read locked by T"+str(TranSact_Row_IP[1])+"\n ")
                    OP_File.write("ITEM "+str(Indiviual_Transaction_Data_Item)+" is read locked by T"+str(TranSact_Row_IP[1])+"\n ")
                    OP_File.write('\n')
                    Locked_Content=[Indiviual_Transaction_Data_Item,TranSact_Row_IP[0],[TranSact_Row_IP[1]]] 
                    Lock_Transact_Table_toList.append(Locked_Content)

    if(FlaG_TranSaction_Detected==0):
        print("T"+ID_For_Transact+" hasn't begun(must have been aboreted) or is not in active state"+"\n ")
        OP_File.write("T"+ID_For_Transact+" hasn't begun (must have been aboreted) or is not in active state"+"\n ")
        OP_File.write('\n')


  

def Transaction_Write_Data(TranSact_Row_IP): #When the 'w' variable is encountered with an individual transaction data item
    global TranSact_Table_to_list
    global Lock_Transact_Table_toList
    Indox_Of_TranSact_Row_IP=0
    Indox_Of_Lock_Table=0
    FlaG_Item_Detected=0
    Count_TimeStamp_OF_First_Transaction=0
    Count_TimeStamp_OF_Second_Transaction=0
    FlaG_TranSaction_Detected=0
    ID_For_Transact=str(TranSact_Row_IP[1])
    Indiviual_Transaction_Data_Item=TranSact_Row_IP.split('(')[1][0]
    
    
    for k in range(len(TranSact_Table_to_list)):
        #Add the transaction to the list of waiting operations if it is blocked
        if((TranSact_Table_to_list[k][0]==ID_For_Transact) and (TranSact_Table_to_list[k][2]=='Blocked')):
            TranSact_Table_to_list[k][4].append(TranSact_Row_IP)
         #When Transaction is in active status, then following 'write' requests are permitted based on the following conditions
        if((TranSact_Table_to_list[k][0]==ID_For_Transact) and (TranSact_Table_to_list[k][2]=='active')):
            FlaG_TranSaction_Detected=1
            Indox_Of_TranSact_Row_IP=k
            
            if len(Lock_Transact_Table_toList)==0: #When Lock_Transact_Table_to_List does not contain any data items
                print("lock table empty,  read the data item first"+"\n ")
            else:
                for m in range(len(Lock_Transact_Table_toList)):#if Indiviual_Transaction_Data_Item is found
                    f=len(Lock_Transact_Table_toList)
                    if(m>=f):
                        return 0
                    if Lock_Transact_Table_toList[m][0]==Indiviual_Transaction_Data_Item:
                        FlaG_Item_Detected=1
                        Indox_Of_Lock_Table=m
                        #When requesting Indiviual_Transaction_Data_Item is write locked by the same transaction
                        if Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='w' and ID_For_Transact in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                            print("This Data item has already been write locked by this transaction"+"\n ")
                       #When requesting Indiviual_Transaction_Data_Item is write locked by the different transaction
                        elif Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='w' and ID_For_Transact not in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:# wait die protocol
                            t1=TranSact_Table_to_list[Indox_Of_TranSact_Row_IP][0]
                            t2=Lock_Transact_Table_toList[Indox_Of_Lock_Table][2][0]

                            for Part_Of_list in TranSact_Table_to_list:
                                    if(Part_Of_list[0]==t1):
                                        Count_TimeStamp_OF_First_Transaction=Part_Of_list[1]
                                    if(Part_Of_list[0]==t2):
                                        Count_TimeStamp_OF_Second_Transaction=Part_Of_list[1]
                            #Implementing the wait die protocol by comparing timestamps
                            if(Count_TimeStamp_OF_First_Transaction>Count_TimeStamp_OF_Second_Transaction):# if requesting transition is younger ...kill it.
                                print("Abort T"+str(t1)+" as it is younger than T"+str(t2)+"\n ")
                                OP_File.write("Abort T"+str(t1)+" as it is younger than T"+str(t2)+"\n ")
                                OP_File.write('\n')
                                Halt_TransacT(t1)

                            elif(Count_TimeStamp_OF_First_Transaction<Count_TimeStamp_OF_Second_Transaction):#if requesting transaction is older, block it.
                                print("BLOCK T"+str(t1)+" as ITEM "+str(Indiviual_Transaction_Data_Item)+" is held by T"+str(t2)+" and T"+str(t1)+" is older than T"+str(t2)+"\n ")
                                OP_File.write("BLOCK T"+str(t1)+" as ITEM "+str(Indiviual_Transaction_Data_Item)+" is held by T"+str(t2)+" and T"+str(t1)+" is older than T"+str(t2)+"\n ")
                                OP_File.write('\n')
                                Blocking_the_Transact(t1,t2,TranSact_Row_IP)
                                
                        #Requesting Individual_Transaction_Data_Item by the Transaction if it is not Read-locked first
                        elif Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='r' and ID_For_Transact not in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                            print("Read lock the data item first"+"\n ")
                        #Indiviual_Transaction_Data_Items that are read-locked by the same transaction are updated to 'write' mode
                        elif Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]=='r' and ID_For_Transact in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                            if len(Lock_Transact_Table_toList[Indox_Of_Lock_Table][2])==1:#verifying only one Transaction has read lock
                                Lock_Transact_Table_toList[Indox_Of_Lock_Table][1]='w'
                                print("Read lock upgraded to write lock on ITEM "+str(Indiviual_Transaction_Data_Item)+" by T"+str(TranSact_Row_IP[1])+"\n ")
                                OP_File.write("Read lock upgraded to write lock on ITEM "+str(Indiviual_Transaction_Data_Item)+" by T"+str(TranSact_Row_IP[1])+"\n ")
                                OP_File.write('\n')
                            
                            elif (len(Lock_Transact_Table_toList[Indox_Of_Lock_Table][2])>1):#if two many TranSact_List
                                t1=ID_For_Transact

                                for Part_Of_list in TranSact_Table_to_list:#Implement the wait die protocol by iterating through a for loop to compare timestamps
                                    if(Part_Of_list[0]==t1):
                                        Count_TimeStamp_OF_First_Transaction=Part_Of_list[1]

                                for lock_table_tid in Lock_Transact_Table_toList[Indox_Of_Lock_Table][2]:
                                    if(lock_table_tid!=ID_For_Transact):
                                        t2=lock_table_tid
                                        
                                        for Part_Of_list in TranSact_Table_to_list:
                                            if(Part_Of_list[0]==t2):
                                                Count_TimeStamp_OF_Second_Transaction=Part_Of_list[1]
                                        
                                        if(Count_TimeStamp_OF_First_Transaction>Count_TimeStamp_OF_Second_Transaction):# kill it if the requesting transaction is younger.
                                            print("Abort T"+str(t1)+" as it is younger than T"+str(t2)+"\n ")
                                            OP_File.write("Abort T"+str(t1)+" as it is younger than T"+str(t2)+"\n ")
                                            OP_File.write('\n')
                                            Halt_TransacT(t1)           
                                        elif(Count_TimeStamp_OF_First_Transaction<Count_TimeStamp_OF_Second_Transaction):#block it if the requesting transaction is older.
                                            print("BLOCK T"+str(t1)+" as ITEM "+str(Indiviual_Transaction_Data_Item)+" is held by T"+str(t2)+" and T"+str(t1)+" is older than T"+str(t2)+"\n ")
                                            OP_File.write("BLOCK T"+str(t1)+" as ITEM "+str(Indiviual_Transaction_Data_Item)+" is held by T"+str(t2)+" and T"+str(t1)+" is older than T"+str(t2)+"\n ")
                                            OP_File.write('\n')
                                            Blocking_the_Transact(t1,t2,TranSact_Row_IP)
                
                                            # Data item, lock mode, and transaction id of older transactions are updated
                                            for Part_Of_list in TranSact_Table_to_list:
                                                if(Part_Of_list[0]==t1 and Part_Of_list[2]=='active'):
                                                    Transact_EXecute(TranSact_Row_IP) 
                                                                       
                if(FlaG_Item_Detected==0): #The requesting transaction should 'Read' lock it first if it did not find the Individual_Transaction_Data_Item
                    print("item not in lock table"+"\n ")
                    print("Read lock the data item first"+"\n ")

    if(FlaG_TranSaction_Detected==0):
        print("T"+ID_For_Transact+" hasn't begun or is not in active state"+"\n ")
        OP_File.write("T"+ID_For_Transact+" hasn't begun or is not in active state"+"\n ")
        OP_File.write('\n')



def Transact_Commit(TranSact_Row_IP):
    global TranSact_Table_to_list
    global Lock_Transact_Table_toList
    ID_For_Transact=str(TranSact_Row_IP[1])
    OP_Blocked=[]
    Status_Of_Commit=0
    
    for m in range(len(TranSact_Table_to_list)):
        #Add the transaction to the list of waiting operations if it is blocked
        if((TranSact_Table_to_list[m][0]==ID_For_Transact) and (TranSact_Table_to_list[m][2]=='Blocked')):
            TranSact_Table_to_list[m][4].append(TranSact_Row_IP)

    for Part_Of_list in TranSact_Table_to_list:
        if(Part_Of_list[0]==ID_For_Transact):
            if(Part_Of_list[2]=='active'):
                Status_Of_Commit=1

    if(Status_Of_Commit==1):
        
        # tid - It is the transaction id of the transaction that is to be committed

        #  By removing all of the locks held by the transaction to be committed, update the lock table
    
        #Reading the lock table items

        for Part_Of_list in reversed(Lock_Transact_Table_toList):
            for lock_table_tid in Part_Of_list[2]:

                # Validating whether or not the transaction is holding a lock on any data items
                if ID_For_Transact == lock_table_tid:

                    # Verifying that that data item only has one lock

                    if len(Part_Of_list[2])==1:
                        # removing all entry fields (data item, lock mode, and TID)
                        Lock_Transact_Table_toList.remove(Part_Of_list)
                    # Verifying if other transactions have also locked that data item
                    else:
                        # removing t-id of only the committing transaction
                        Part_Of_list[2].remove(ID_For_Transact)
 
        # Keeping the transaction table updated 

        # Reading the items from the transaction table

        for n in range(len(TranSact_Table_to_list)):
            if TranSact_Table_to_list[n][0]==ID_For_Transact:
                # Transaction table status changed to 'Committed'
                TranSact_Table_to_list[n][2]='Committed'

            #  Making sure that the committing transaction doesn't block any other transaction
            if(TranSact_Table_to_list[n][2]=='Blocked' and TranSact_Table_to_list[n][3]==ID_For_Transact):

                # Changing the status of the next blocked transaction to 'Active'
                TranSact_Table_to_list[n][2]='active'
                TranSact_Table_to_list[n][3] = None
                for O_P in TranSact_Table_to_list[n][4]:
                    OP_Blocked.append(O_P)
                TranSact_Table_to_list[n][4]=[]
        
        print("Transaction T"+str(TranSact_Row_IP[1])+" committed successfully"+"\n ")
        OP_File.write("Transaction T"+str(TranSact_Row_IP[1])+" committed successfully"+"\n ")
        OP_File.write('\n')

        for O_P in OP_Blocked:
            Transact_EXecute(O_P)
    
    else:
        print("Transaction is in a state of Abort or Block"+"\n ")
        OP_File.write("Transaction is in a state of Abort or Block"+"\n ")
        OP_File.write('\n')

  
def Blocking_the_Transact(blocked_tid,blocked_by_tid,blocked_operation):

    global TranSact_Table_to_list

    # blocked_tid - The transaction id of the transaction that should be blocked
    # blocked_by_tid - The transaction id of the transaction causing the block 
    # blocked_operation - Operation that should be blocked

    # Keeping the transaction table updated  
    # Reading the items from the transaction table

    for p in range(len(TranSact_Table_to_list)):
        if TranSact_Table_to_list[p][0] == blocked_tid:
            if TranSact_Table_to_list[p][2] == 'active':
                # Changing the status of the transaction table to 'blocked'
                TranSact_Table_to_list[p][2] = 'Blocked'
                
                # 'blocked by' list for that transaction is updated
                TranSact_Table_to_list[p][3] = blocked_by_tid
                
                # The operation is stored in the 'Blocked Operations' list
                TranSact_Table_to_list[p][4].append(blocked_operation)


def Halt_TransacT(abort_tid):

    global TranSact_Table_to_list
    global Lock_Transact_Table_toList
    OP_Blocked=[]
    
    for l in range(len(TranSact_Table_to_list)):

        if TranSact_Table_to_list[l][0]==abort_tid:
            
            if(TranSact_Table_to_list[l][2]!='committed' and TranSact_Table_to_list[l][2]!='aborted'):
                
                #updating the TranSact_Table_to_list

                TranSact_Table_to_list[l][2]='aborted'
                TranSact_Table_to_list[l][3]=None
                TranSact_Table_to_list[l][4]=[]

                #updating the Lock_Transact_Table_toList

                for q in range(len(Lock_Transact_Table_toList)):
                    if abort_tid in Lock_Transact_Table_toList[q][2]:
                        if len(Lock_Transact_Table_toList[q][2])==1:
                            Lock_Transact_Table_toList.remove(Lock_Transact_Table_toList[q])
                        else:
                            Lock_Transact_Table_toList[q][2].remove(abort_tid)

    for r in range(len(TranSact_Table_to_list)):

        if TranSact_Table_to_list[r][3]==abort_tid:

                # Examining whether the aborting transaction has blocked any transactions
                if(TranSact_Table_to_list[r][2]=='Blocked'):

                    # The next blocked transaction will be executed and its status will be 'Active'
                    TranSact_Table_to_list[r][2]='active'
                    TranSact_Table_to_list[r][3] = None
                for O_P in TranSact_Table_to_list[r][4]:
                    OP_Blocked.append(O_P)
                TranSact_Table_to_list[r][4]=[]

    for O_P in OP_Blocked:
        Transact_EXecute(O_P)

 
def Transact_EXecute(TranSact_Row_IP):
        OP_File.write('Operation is: '+str(TranSact_Row_IP)+"\n ")
        OP_File.write('\n')
        print("Operation is",TranSact_Row_IP)
        print("\n")
        if TranSact_Row_IP[0]=='b':
            Initiate_Transact_Begin(TranSact_Row_IP)
        if TranSact_Row_IP[0]=='r':
            Initiate_Reading_Of_Transaction(TranSact_Row_IP)
        if TranSact_Row_IP[0]=='w':
            Transaction_Write_Data(TranSact_Row_IP)
        if TranSact_Row_IP[0]=='e':
            Transact_Commit(TranSact_Row_IP) 
        OP_File.write("------------------------------------------------------------------------------------------\n")
        OP_File.write("#########################################################################################\n")
        OP_File.write("------------------------------------------------------------------------------------------\n")
        OP_File.write('Transaction Table:\n'+"TID;TSTMP;STATE;BLKED_BY;BLKED_OPS\n"+str(TranSact_Table_to_list)+"\n \t \t \t")
        OP_File.write('\n')
        OP_File.write("------------------------------------------------------------------------------------------\n")
        OP_File.write('Lock Table: \n'+"ITEM;MODE_LOCK;TID\n"+str(Lock_Transact_Table_toList)+"\n \t \t \t")
        OP_File.write('\n')
        OP_File.write("------------------------------------------------------------------------------------------\n")
        OP_File.write("#########################################################################################\n")
        OP_File.write("------------------------------------------------------------------------------------------\n")
        OP_File.write('\n')
        print("------------------------------------------------------------------------------------------")
        print("#########################################################################################")
        print("------------------------------------------------------------------------------------------")
        print("Transaction Table:\n\n"+"TID;TSTMP;STATE;BLKED_BY;BLKED_OPS\n")
        print(*TranSact_Table_to_list,sep="\n")
        print("------------------------------------------------------------------------------------------")
        print("\n Lock Table: \n"+"ITEM;MODE_LOCK;TID\n")
        print(*Lock_Transact_Table_toList,sep="\n")
      
        print("------------------------------------------------------------------------------------------")
        print("#########################################################################################")
        print("------------------------------------------------------------------------------------------")


for TranSact_Row_IP in TranSact_List:
    Transact_EXecute(TranSact_Row_IP)

OP_File.close()
