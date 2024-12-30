from flask import Flask, render_template, request, jsonify
import psycopg2
from database import get_all_persons, get_all_contacts, get_all_addresses, get_all_donors, get_all_recipients, get_all_branches
app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    dbname="BloodBankMS",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/old')
def old_user():
    return render_template('old.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        # Render the registration form
        return render_template('new.html')
    elif request.method == 'POST':
        # Handle form submission via JSON API
        data = request.json
        try:
            # Insert into Person table
            cursor.execute("""
                INSERT INTO Person (Aadhar_number, Name, Date_of_birth, Gender, Blood_Type)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['aadharNo'], data['fullName'], data['dob'], data['gender'],
                data['bloodGroup']
            ))
            
            # Insert into Contact table
            cursor.execute("""
                INSERT INTO Contact (Aadhar_number, Contact_Number)
                VALUES (%s, %s)
            """, (
                data['aadharNo'], data['phone']
            ))
            
            # Insert into Address table
            cursor.execute("""
                INSERT INTO Address (Aadhar_number, D_no, Street_Name, City, State)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['aadharNo'], data['D_no'], data['Street_Name'], data['City'], data['State']
            ))
            
            conn.commit()
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'GET':
        # Render the donation form
        return render_template('donor.html')
    elif request.method == 'POST':
        # Handle donation form submission via JSON API
        data = request.json
        try:
            # Insert into Donor table
            cursor.execute("""
                INSERT INTO Donor (Aadhar_number, Last_Donation_Date)
                VALUES (%s, %s)
                RETURNING Donor_ID
            """, ( data['aadhar'], data['donationDate']))
            donor_id = cursor.fetchone()[0]

            # Insert into Transactions table
            cursor.execute("""
                INSERT INTO Transactions (Donor_ID, Donation_Date, Blood_ID)
                VALUES (%s, %s, (SELECT Blood_ID FROM Blood_Management WHERE Blood_Type=%s LIMIT 1))
            """, (
                donor_id, data['donationDate'], data['bloodType']
            ))

            conn.commit()
            return jsonify({"message": "Donation recorded successfully"}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400


@app.route('/receive', methods=['GET', 'POST'])
def receive():
    if request.method == 'GET':
        # Render the recipient form
        return render_template('recipient.html')
    elif request.method == 'POST':
        # Handle recipient form submission via JSON API
        data = request.json
        try:
            # Insert into Recipient table
            cursor.execute("""
                INSERT INTO Recipient (Aadhar_number, Quantity_Required,blood_type)
                VALUES (%s, 1,%s)  -- Assuming a default quantity for simplicity
                RETURNING Recipient_ID
            """, (data['aadhar'],data['bloodType']))

            recipient_id = cursor.fetchone()[0]

            # Insert into Transactions table
            cursor.execute("""
                INSERT INTO Transactions (Recipient_ID, Donation_Date, Blood_ID)
                VALUES (%s, %s, (SELECT Blood_ID FROM Blood_Management WHERE Blood_Type=%s LIMIT 1))
            """, (
                recipient_id, data['donationDate'], data['bloodType']
            ))

            conn.commit()
            return jsonify({"message": "Recipient recorded successfully"}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/total_persons')
def total_persons():
    # Assuming you have a function get_all_persons() that fetches all persons from the database
    persons = get_all_persons()
    return jsonify(persons)

@app.route('/contacts')
def contacts():
    # Assuming you have a function get_all_contacts() that fetches all contacts from the database
    contacts = get_all_contacts()
    return jsonify(contacts)

@app.route('/addresses')
def addresses():
    addresses = get_all_addresses()
    return jsonify(addresses)

@app.route('/donors')
def donors():
    donors = get_all_donors()
    return jsonify(donors)

@app.route('/recipients')
def recipients():
    recipients = get_all_recipients()
    return jsonify(recipients)

@app.route('/branches')
def branches():
    branches = get_all_branches()
    return jsonify(branches)

if __name__ == '__main__':
    app.run(debug=True)
