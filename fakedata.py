import psycopg2
from datetime import datetime, timedelta
from faker import Faker
import random

fake=Faker()
conn = psycopg2.connect(
    dbname='blood_bank',
    user='Muhammad_Ishaq',
    password='ishaq156',
    host='localhost',
    port='5432'
)
cur=conn.cursor()

def cnic_gender_based(gender):
    base=f"{fake.random_int(13000, 48000)}-{fake.random_int(1000000, 9999999)}"
    last_digit=random.choice([1,3,5,7,9]) if gender == 'Male' else random.choice([0,2,4,6,8])
    return f"{base}-{last_digit}"

blood_group=['A+','A-','B+','B-','AB+','AB-','O+','O-']
staff_role=['Doctor','Nurse','Technician']
blood_bank=['Blood Bank','Blood Center','Life Sever','Donor Hub']
hospital=['Health Care Center','Hospital','Medical Center','Wellness Center']
admin_role=['Database Administrator','System DBA','Data Analyst','Database Security Administrator','Supervisor']

# Fetch donor_ids data.................
cur.execute("SELECT donor_id FROM donor")
donor_ids=[row[0] for row in cur.fetchall()]

# Fetch Recipient_ids data..............
cur.execute("SELECT recipient_id FROM recipient")
recipient_ids=[row[0] for row in cur.fetchall()]

#Select blood bank id from the table.................................
cur.execute("SELECT blood_bank_ID FROM blood_bank")
blood_bank_ids=[row[0] for row in cur.fetchall()]

#Fetch hospital_id from hospital table.................................
cur.execute("SELECT Hospital_ID FROM hospital")
hospital_ids=[row[0] for row in cur.fetchall()]

#Statues.............................
Statuses=['Pending', 'Approved', 'Rejected']

# #Donor Fake data......................................................
# for i in range(100000):
#     gender=random.choice(['Male','Female'])
#     name=fake.first_name_male() if gender == 'Male' else fake.first_name_female()
#     cnic= cnic_gender_based(gender)
#     contact= '+923'+str(random.randint(0,4))+fake.msisdn()[3:10]
#     cur.execute("""
                
#         INSERT INTO donor(Name,Age,Gender,CNIC,Blood_Group,Contact,Address,Last_Donation_Date,Medical_History)
#         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
#     """,(
#         name,random.randint(18,50),gender,cnic,random.choice(blood_group),contact,fake.address(),fake.date_between(start_date='-1y',end_date='today'),fake.text(max_nb_chars=100)
#     ))
#     print ("Hello",i)
    

# #Recipient Fake data..................................................
# for i in range(100000):
#     gender=random.choice(['Male','Female'])
#     name=fake.first_name_male() if gender=='Male' else fake.first_name_female()
#     cnic=cnic_gender_based(gender)
#     contact='+923'+str(random.randint(0,4))+fake.msisdn()[3:10]
#     cur.execute("""
#        INSERT INTO recipient(Name,Age,Gender,CNIC,Blood_Group,Contact,Address,required_blood_amount,emergency_status)
#         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
#     """,(
#         name,random.randint(1,80),gender,cnic,random.choice(blood_group),contact,fake.address(),round(random.uniform(0.5,2.5),2),random.choice(['True','False'])
#     ))
#     print("Hello2",i)



# for i in range(100000):
#     name=fake.last_name()+" "+random.choice(blood_bank)
#     contact='+923'+str(random.randint(0,4))+fake.msisdn()[3:10]
#     cur.execute("""
#         INSERT INTO blood_bank(name,location,Contact)
#         VALUES(%s,%s,%s)
#     """,(
#         name,fake.address(),contact
#     ))
#     print("Hello  ",i)


# for i in range(100000):
#     name=fake.last_name()+" "+random.choice(hospital)
#     contact='+923'+str(random.randint(0,4))+fake.msisdn()[3:10]
#     cur.execute("""
#         INSERT INTO hospital(name,location,Contact)
#         VALUES(%s,%s,%s)
#     """,(
#         name,fake.address(),contact
#     ))
#     print("Hello  ",i)

# #Staff Table Fake data................................................

# for i in range(100000):
#     gender=random.choice(['Male','Female'])
#     name=fake.first_name_male() if gender=='Male' else fake.first_name_female()
#     cnic=cnic_gender_based(gender)
#     contact='+923'+str(random.randint(0,4))+fake.msisdn()[3:10]
#     blood_bank_id=random.choice(blood_bank_ids)  
#     cur.execute("""
#        INSERT INTO staff(Name,Gender,CNIC,role,blood_bank_id,Contact)
#         VALUES(%s,%s,%s,%s,%s,%s)
#     """,(
#         name,gender,cnic,random.choice(staff_role),blood_bank_id,contact)
#     )
#     print("Hello2",i)


# #Add fake data in admin table...........................................

# for i in range(100000):
#     gender=random.choice(['Male','Female'])
#     name=fake.first_name_male() if gender=='Male' else fake.first_name_female()
#     cnic=cnic_gender_based(gender)
#     contact='+923'+str(random.randint(0,4))+fake.msisdn()[3:10]  
#     cur.execute("""
#        INSERT INTO admin(Name,Gender,CNIC,role,Contact)
#         VALUES(%s,%s,%s,%s,%s)
#     """,(
#         name,gender,cnic,random.choice(admin_role),contact)
#     )
#     print("Hello2",i)

#Add fake data in reception table.....................................

for i in range(100000):
    donor_id=random.choice(donor_ids)

    recipient_id=random.choice(recipient_ids) if random.random() < 0.5 else None

    donation_date=fake.date_between(start_date='-2y',end_date='today')

    blood_quantity=round(random.uniform(0.3,0.6),2)

    cur.execute("""
        INSERT INTO reception(Donor_ID,Recipient_ID,Donation_Date,Blood_Quantity)
        VALUES (%s,%s,%s,%s)
    """,(donor_id,recipient_id,donation_date,blood_quantity))

    print("Helllo3 ",i)

#Add Fake data in blood_request table.................................

for i in range(100000):
    request_type=random.choice(['Hospital', 'Recipient'])
    hospital_id=None
    recipient_id=None

    if request_type=='Hospital':
        hospital_id=random.choice(hospital_ids)
    else:
        recipient_id=random.choice(recipient_ids)
    
    blood_type=random.choice(blood_group)
    quantity=random.randint(1,5)
    status=random.choice(Statuses)
    request_date=fake.date_between(start_date='-1y',end_date='today')

    cur.execute("""
        INSERT INTO blood_request(Hospital_ID,Recipient_ID,Requester_Type,Blood_Type,Requested_Quantity,Request_Status,Request_Date)
        VALUES(%s,%s,%s,%s,%s,%s,%s)""",(hospital_id,recipient_id,request_type,blood_type,quantity,status,request_date))
    
    print("Hello",i)



print("Inserts done. Committing...")
conn.commit()
cur.close()
conn.close()
print("Fake data inserted successfully!")