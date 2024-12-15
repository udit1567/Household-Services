from .database import db,desc,asc

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    fullname = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    pincode = db.Column(db.Integer(), nullable=False)
    phone_no = db.Column(db.String(), nullable=False)
    service_requests = db.relationship("Service_Req", backref="customer")
    application_status = db.Column(db.String() ,nullable=False , default="Active")

class Professionals(db.Model): 
    __tablename__ = 'professionals'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    fullname = db.Column(db.String(), nullable=False)
    service_id = db.Column(db.Integer(), db.ForeignKey("services.id"))
    experience = db.Column(db.Integer(), nullable=False)
    pdf_doc = db.Column(db.LargeBinary(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    pincode = db.Column(db.Integer(), nullable=False)
    phone_no = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer())
    pricing = db.Column(db.Integer())
    service_desc = db.Column(db.String())
    time_req = db.Column(db.String())
    application_status = db.Column(db.String() ,nullable=False , default="Pending")
    service_requests = db.relationship("Service_Req", backref="professionals", cascade="all, delete-orphan")

class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer(), primary_key=True)
    service_name = db.Column(db.String(), nullable=False, unique=True)
    service_bp = db.Column(db.Integer(), nullable=False)
    time_req = db.Column(db.String(), nullable=False)
    service_desc = db.Column(db.String(), nullable=False)
    professionals = db.relationship("Professionals", backref="service", cascade="all, delete-orphan")
    

class Service_Req(db.Model):
    __tablename__ = 'service_req'
    id = db.Column(db.Integer(), primary_key=True)
    service_id = db.Column(db.Integer(), db.ForeignKey("services.id"))
    customer_id = db.Column(db.Integer(), db.ForeignKey("customer.id")) 
    professional_id = db.Column(db.Integer(), db.ForeignKey('professionals.id'))  
    date_of_request = db.Column(db.String())
    date_of_completion = db.Column(db.String())
    service_status = db.Column(db.String(), default="Requested")
    service_rating = db.Column(db.Integer(), default = 0)
    customer_remarks = db.Column(db.String())
    professional_remark = db.Column(db.String())
    service = db.relationship("Services", backref = "service_requests")
