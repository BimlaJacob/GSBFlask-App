from extensions import db

class Customer(db.Model):
    __tablename__ = 'Customers'
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
    __tablename__ = 'Appointments'
    AppointmentID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('Customers.CustomerID'), nullable=False)
    StaffID = db.Column(db.Integer, db.ForeignKey('Staff.StaffID'), nullable=False)
    AppointmentDate = db.Column(db.Date, nullable=False)
    AppointmentTime = db.Column(db.String(10), nullable=False)

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('appointments', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('appointments', lazy=True))
