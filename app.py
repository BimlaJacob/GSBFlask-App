from flask import Flask, request
from extensions import db
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf.csrf import CSRFProtect  # Add CSRF protection
from datetime import date
from dotenv import load_dotenv
import os
from wtforms import StringField, validators
from flask_admin.form import rules


# Load .env file
load_dotenv()

# Access environment variables
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://Bimla-Asus\\SQLEXPRESS/GlassSlipperBridal?driver=ODBC+Driver+17+for+SQL+Server"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cinderella'  # Required for Flask-Admin

# Initialize the database
db.init_app(app)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Import models after db initialization to avoid circular imports
from models import Appointment, Customer, Staff

# Custom Admin Index View
class CustomAdminIndexView(AdminIndexView):
    def render(self, *args, **kwargs):
        return super().render('admin/index.html', **kwargs)

# Base class for admin views
class BaseModelView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_selectable = False
    column_filters = []
    column_sortable_list = []
    page_size = None
    list_template = 'admin/custom_list.html'

    def get_actions(self):
        return []  # No actions available

    def get_count_query(self):
        return self.session.query(self.model).with_entities(db.func.count())

# Appointment Admin View with dropdown filtering
class AppointmentAdmin(BaseModelView):
    column_list = ('AppointmentID', 'AppointmentDate', 'AppointmentTime', 'customer.Name', 'customer.Email', 'staff.Name')
    column_labels = {
        'AppointmentID': 'Apt ID',
        'AppointmentDate': 'Date',
        'AppointmentTime': 'Time',
        'customer.Name': 'Customer Name',
        'customer.Email': 'Customer Email',
        'staff.Name': 'Staff Name',
    }
    list_template = 'admin/custom_list.html'  # Use the custom list template
    create_template = 'admin/custom_create.html'  # Custom create template
    edit_template = 'admin/custom_edit.html'  # Custom edit template

    # Enable creation, editing, and deletion
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['customer.Name', 'customer.Email', 'staff.Name']

    def get_query(self):
        filter_status = request.args.get('status', 'all')
        query = self.session.query(self.model)

        if filter_status == 'upcoming':
            query = query.filter(self.model.AppointmentDate >= date.today())
        elif filter_status == 'completed':
            query = query.filter(self.model.AppointmentDate < date.today())

        return query.order_by(self.model.AppointmentDate.asc(), self.model.AppointmentTime.asc())

    def get_count_query(self):
        filter_status = request.args.get('status', 'all')
        query = self.session.query(self.model)

        if filter_status == 'upcoming':
            query = query.filter(self.model.AppointmentDate >= date.today())
        elif filter_status == 'completed':
            query = query.filter(self.model.AppointmentDate < date.today())

        return query.with_entities(db.func.count())

# Customer Admin View
class CustomerAdmin(BaseModelView):
    column_list = ('Name', 'Email')
    column_labels = {
        'Name': 'Customer Name',
        'Email': 'Email Address',
    }

    list_template = 'admin/custom_list.html'  # Use the custom list template
    create_template = 'admin/custom_create.html'  # Custom create template
    edit_template = 'admin/custom_edit.html'  # Custom edit template

    # Enable creation, editing, and deletion
    can_create = True
    can_edit = True
    can_delete = True

    def get_query(self):
        return self.session.query(self.model).order_by(self.model.Name.asc())

# Staff Admin View  
class StaffAdmin(ModelView):
    column_list = ( 'StaffID', 'Name', 'Role', 'Email', 'Phone')
    column_labels = {
        'StaffID': 'Staff ID',
        'Name': 'Staff Name',
        'Role': 'Job Role',
        'Email': 'Email Address',
        'Phone': 'Phone Number',
    }
    list_template = 'admin/staff_list.html'  # Use the staff-specific list template
    create_template = 'admin/custom_create.html'  # Use the custom create template
    edit_template = 'admin/edit_staff.html'  # Use the custom edit template

    # Override form field types
    form_overrides = {
        'Email': StringField  # Treat 'Email' as a simple text input without email validation
    }

    # Include only the fields we want
    form_columns = ['Name', 'Role', 'Email', 'Phone']

    can_create = True
    can_edit = True
    can_delete = True

        # Set up primary key reference to be used for edit and delete
    column_display_pk = True  # Makes sure primary key is shown in views

    # Note the use of 'StaffID' for primary key
    def get_query(self):
        return self.session.query(self.model).order_by(self.model.StaffID.asc())

    def get_count_query(self):
        return self.session.query(self.model).with_entities(db.func.count())

    def edit_view(self):
        # Extract the id from request args
        id = request.args.get('id')
        if id is None:
            # Handle the case where no id is provided
            return redirect(url_for('staff.index_view'))

        # Your existing logic for editing the staff member
        return super().edit_view(id=id)

    def delete_view(self):
        # Extract the id from request args
        id = request.args.get('id')
        if id is None:
            # Handle the case where no id is provided
            return redirect(url_for('staff.index_view'))

        # Your existing logic for deleting the staff member
        return super().delete_view(id=id)

# Set up Flask-Admin
admin = Admin(
    app,
    name="Admin Panel",
    index_view=CustomAdminIndexView(),
    template_mode="bootstrap4",
)

# Add models to Flask-Admin
admin.add_view(AppointmentAdmin(Appointment, db.session, endpoint="appointment"))
admin.add_view(CustomerAdmin(Customer, db.session, endpoint="customer"))
admin.add_view(StaffAdmin(Staff, db.session, endpoint="staff"))

# Import routes after app and db setup
from routes import *

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
