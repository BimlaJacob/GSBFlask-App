from app import db


class Customer(db.Model):
    __tablename__ = 'Customers'  # Explicitly specify the correct table name
    CustomerID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)


class Staff(db.Model):
    __tablename__ = 'Staff'
    StaffID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)


class Appointment(db.Model):
    __tablename__ = 'Appointments'  # Matches the database table name
    AppointmentID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, nullable=False)
    StaffID = db.Column(db.Integer, nullable=False)
    AppointmentDate = db.Column(db.Date, nullable=False)  # Matches column name in database
    AppointmentTime = db.Column(db.String(10), nullable=False)  # Matches column name in database



