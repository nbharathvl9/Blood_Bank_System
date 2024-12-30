import psycopg2

def get_all_persons():
    conn = psycopg2.connect(
        dbname="BloodBankMS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # Fetch all persons
    cursor.execute("SELECT Name, Date_of_birth, Gender, Blood_Type FROM Person")
    persons = cursor.fetchall()
    
    conn.close()
    
    # Convert to desired format
    return [
        {
            'name': row[0],
            'dob': row[1],
            'gender': row[2],
            'age': calculate_age(row[1]),  # Convert date of birth to age
            'bloodType': row[3]
        } 
        for row in persons
    ]

def get_all_contacts():

    conn = psycopg2.connect(
        dbname="BloodBankMS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.Name, c.Aadhar_number, c.Contact_Number 
        FROM Contact c
        JOIN Person p ON c.Aadhar_number = p.Aadhar_number
    """)
    contacts = cursor.fetchall()
    conn.close()
    return [{'name': row[0], 'aadhar': row[1], 'contactNumber': row[2]} for row in contacts]
def get_all_addresses():

    conn = psycopg2.connect(
        dbname="BloodBankMS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.Aadhar_number, 
            a.D_no, 
            a.Street_Name, 
            a.City, 
            a.State, 
            p.Name
        FROM Address a
        JOIN Person p ON a.Aadhar_number = p.Aadhar_number
    """)
    addresses = cursor.fetchall()
    cursor.close()
    
    print(addresses)  # Debug print to verify data
    
    return [
        {
            'aadhar': row[0],
            'd_no': row[1],
            'streetName': row[2],
            'city': row[3],
            'state': row[4],
            'name': row[5]
        }
        for row in addresses
    ]

def get_all_donors():
    conn = psycopg2.connect(
        dbname="BloodBankMS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.Aadhar_number, p.Name, d.Last_Donation_Date 
        FROM Donor d
        JOIN Person p ON d.Aadhar_number = p.Aadhar_number
    """)
    donors = cursor.fetchall()
    conn.close()
    
    return [
        {
            'aadhar': row[0],
            'name': row[1],
            'lastDonationDate': row[2]
        }
        for row in donors
    ]

def get_all_recipients():
    conn = psycopg2.connect(
        dbname="BloodBankMS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.Aadhar_number, p.Name, r.Quantity_Required, r.blood_type 
        FROM Recipient r
        JOIN Person p ON r.Aadhar_number = p.Aadhar_number
    """)
    recipients = cursor.fetchall()
    conn.close()
    
    return [
        {
            'aadhar': row[0],
            'name': row[1],
            'quantityRequired': row[2],
            'bloodType': row[3]
        }
        for row in recipients
    ]

def get_all_branches():
    conn = psycopg2.connect(
        dbname="BloodBankMS",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Branch_ID, Location, Inauguration_Date, Storage_Capacity FROM Branch
    """)
    branches = cursor.fetchall()
    conn.close()
    
    return [
        {
            'branchId': row[0],
            'location': row[1],
            'inaugurationDate': row[2],
            'storageCapacity': row[3]
        }
        for row in branches
    ]

def calculate_age(dob):
    from datetime import date
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
