from ast import Import
import smtplib
from email.message import EmailMessage
from flask import jsonify, request, render_template, redirect, url_for, flash
from app import app, db
from models import Appointment, Customer, Staff
from datetime import datetime
from sqlalchemy.sql import text
from extensions import db

EMAIL_ADDRESS = 'bimlaruth@gmail.com'
EMAIL_PASSWORD = 'xato vzfg sode eppo'

# Available time slots
TIME_SLOTS = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

@app.route('/test-db', methods=['GET'])
def test_db_connection():
    try:
        # Use text('SELECT 1') for the query
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Database connection successful!'}), 200
    except Exception as e:
        return jsonify({'message': f'Database connection error: {e}'}), 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/appointment')
def appointment_page():
    return render_template('appointment.html')

@app.route('/appointments', methods=['POST'])
def create_appointment():
    try:
        data = request.json

        # Validate input data
        if not all([data.get('name'), data.get('email'), data.get('date'), data.get('time')]):
            return jsonify({'message': 'Invalid data. Please fill out all fields.'}), 400

        # Check for duplicate appointments
        existing_appointment = Appointment.query.filter_by(
            AppointmentDate=data['date'], AppointmentTime=data['time']
        ).first()
        if existing_appointment:
            return jsonify({'message': 'This time slot is already booked. Please choose another time.'}), 400

        # Find or create customer
        customer = Customer.query.filter_by(Email=data['email']).first()
        if not customer:
            customer = Customer(Name=data['name'], Email=data['email'])
            db.session.add(customer)
            db.session.commit()

        # Determine staff based on the time slot
        staff_id = select_staff(data['time'])
        if not staff_id:
            return jsonify({'message': 'Invalid time slot selected.'}), 400

        # Fetch the staff details
        staff = Staff.query.filter_by(StaffID=staff_id).first()
        if not staff:
            return jsonify({'message': 'Staff member not found. Please try again.'}), 500

        # Create the appointment
        new_appointment = Appointment(
            CustomerID=customer.CustomerID,
            StaffID=staff_id,
            AppointmentDate=data['date'],
            AppointmentTime=data['time']
        )
        db.session.add(new_appointment)
        db.session.commit()

        # Send confirmation email
        send_confirmation_email(
            to_email=data['email'],
            customer_name=customer.Name,
            consultant_name=staff.Name,
            consultant_phone=staff.Phone,
            date=data['date'],
            time=data['time']
        )

        return jsonify({'message': 'Appointment created successfully! Confirmation email sent.'}), 201

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'message': 'An error occurred while booking your appointment.'}), 500

@app.route('/api/timeslots', methods=['GET'])
def get_available_timeslots():
    try:
        # Retrieve the date parameter
        date = request.args.get('date')
        if not date:
            return jsonify({'message': 'Date is required'}), 400

        # Parse the date
        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format. Expected YYYY-MM-DD.'}), 400

        # Explicit SQL query to fetch booked slots
        query = text("SELECT AppointmentTime FROM Appointments WHERE AppointmentDate = :date")
        result = db.session.execute(query, {'date': date}).fetchall()

        # Extract booked times from query results
        booked_times = [row[0] for row in result]

        # Determine available slots
        available_slots = [slot for slot in TIME_SLOTS if slot not in booked_times]

        return jsonify({'available_slots': available_slots}), 200

    except Exception as e:
        print(f"Error querying the database: {e}")
        return jsonify({'message': 'Error querying the database.'}), 500

@app.route('/admin/appointment/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # Update appointment fields from the form
            appointment.AppointmentDate = request.form['AppointmentDate']
            appointment.AppointmentTime = request.form['AppointmentTime']
            appointment.CustomerID = request.form['CustomerID']
            appointment.StaffID = request.form['StaffID']

            db.session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appointment.index_view'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating appointment: {e}', 'danger')

    return render_template('admin/custom_edit.html', appointment=appointment)

@app.route('/admin/appointment/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting appointment: {e}', 'danger')

    return redirect(url_for('appointment.index_view'))

@app.route('/admin/customer/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.Name = request.form['Name']
        customer.Email = request.form['Email']

        try:
            db.session.commit()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customer.index_view'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating customer: {e}', 'danger')

    return render_template('admin/custom_edit.html', customer=customer)

@app.route('/admin/customer/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting customer: {e}', 'danger')

    return redirect(url_for('customer.index_view'))

@app.route('/staff/edit/<int:id>', methods=['GET', 'POST'])
def edit_staff(id):
    staff_member = Staff.query.get_or_404(id)
    if request.method == 'POST':
        staff_member.Name = request.form['Name']
        staff_member.Role = request.form['Role']
        staff_member.Email = request.form['Email']
        staff_member.Phone = request.form['Phone']
        
        try:
            db.session.commit()
            flash('Staff member updated successfully!', 'success')
            return redirect(url_for('staff.index_view'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating staff member: {e}', 'danger')
    return render_template('admin/edit_staff.html', staff=staff_member)

@app.route('/admin/staff/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    staff_member = Staff.query.get_or_404(id)
    try:
        db.session.delete(staff_member)
        db.session.commit()
        flash('Staff member deleted successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting staff member: {e}', 'danger')

    return redirect(url_for('staff.index_view'))

def select_staff(time):
    if time in ['10 AM', '1 PM']:
        return 2
    elif time in ['11 AM', '2 PM']:
        return 3
    elif time in ['12 PM', '3 PM']:
        return 4
    else:
        return None

def send_confirmation_email(to_email, customer_name, consultant_name, consultant_phone, date, time):
    msg = EmailMessage()
    msg['Subject'] = 'Appointment Confirmation'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    # Construct the email content
    msg.set_content(
        f"Dear {customer_name},\n\n"
        f"Congratulations, you have successfully booked your appointment at Glass Slipper Bridal.\n"
        f"Your consultant will be {consultant_name} (Phone: {consultant_phone}).\n\n"
        f"Here are your appointment details:\n"
        f"Date: {date}\n"
        f"Time: {time}\n\n"
        f"We look forward to serving you!\n\n"
        f"Best regards,\n"
        f"Glass Slipper Bridal Team"
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
