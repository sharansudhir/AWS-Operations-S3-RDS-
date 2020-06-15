import pymysql
import boto3

def insert(UserID,password):

    conn = pymysql.connect(host = "database-1.cbfs64hpz5de.us-east-1.rds.amazonaws.com", user ="admin", password = "admin12345678" , db ="assignment", charset="utf8mb4")

    if conn:
        try:

            cursor = conn.cursor()

            insert_query = 'INSERT INTO details (UserID,password) VALUES (%s,%s);'

            cursor.execute(insert_query,(UserID,password))

            conn.commit()

            print("INSERT SUCCESSFUL")
        
        finally:
            conn.close()    
    else:
        print("INSERT ERROR")



def retrieve(UserID):

    conn = pymysql.connect(host = "database-1.cbfs64hpz5de.us-east-1.rds.amazonaws.com", user ="admin", password = "admin12345678" , db ="assignment", charset="utf8mb4")

    if conn:
        try:
            cursor = conn.cursor()

            retreive_query = "select * from details where UserID = %s"

            cursor.execute(retreive_query,(UserID))
            result = cursor.fetchone()

        finally:
            conn.close()
    else:
        print("SEARCH QUERY NOT FOUND")

    return(result)

def s3_content(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.all():
        content = obj.get()['Body'].read().decode('utf-8')

    i=21
    e = {}
    d = {}
    while(i<151):

        e[content[i:i+4].split('\t')[0]] = content[i:i+4].split('\t')[1] 
        d[content[i:i+4].split('\t')[1]] = content[i:i+4].split('\t')[0]
        i= i+5;

    return e,d

def encryption(enc,passwd):
    
    s=""

    for i in passwd:
        s = s + enc[i]

    return s

def decryption(dec,password):
    i=0;
    decrypt = ""
    while(i<len(password)):        
        s = password[i:i+2]
        decrypt = decrypt + dec[s]
        i=i+2;

    return(decrypt)

enc,dec = s3_content('bucket01-sharan')

while(True):

    print("**********")
    print('1. INSERT')    
    print('2. SEARCH')
    print('3. EXIT')
    print("**********")
    choice = int(input('\nENTER CHOICE '))

    if(choice == 1):
        UserID = input('Enter UserID: ')
        password = input('Enter Password: ')
        print("\nBefore Encryption: {}\n".format(password))
        password = encryption(enc,password)
        print("\nAfter Encryption: {}\n".format(password))
        insert(UserID,password)
    
    elif(choice == 2):
        searchID = input('\nEnter UserID: ')
        x = retrieve(searchID)
        

        if x == None:
            print("SEARCH QUERY NOT FOUND")
        else:
            password = decryption(dec,x[1])
            print('ID = '+searchID + " Password = "+password) 
    
    elif(choice == 3):
        exit()
    else:
        print("\nWrong Choice\n")

