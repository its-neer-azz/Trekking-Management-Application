from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String(100), nullable = False)
    
    email = db.Column(db.String(120), unique=True , nullable= False)
    
    password = db.Column(db.String(120), nullable = False)
    
    role = db.Column(db.String(20), nullable = False)
    
    approved = db.Column(db.Boolean, default = False)
    
    blacklisted = db.Column(db.Boolean, default = False)
    active = db.Column(db.Boolean, default=True)
    
    
    
class Trek(db.Model):
    
    __tablename__ = "treks"
    
    #primary key 
    id = db.Column(db.Integer, primary_key = True)
    
    #TrekName
    name = db.Column(db.String(100) , nullable = False)
    
    location = db.Column(db.String(100), nullable=False)
    
    #Easy/Medium/Hard
    difficulty = db.Column(db.String(100), nullable = False)
    
    #Duration In days
    duration = db.Column(db.Integer, nullable= False)
    
    #Maximum Seats for users
    total_slots = db.Column(db.Integer , nullable = False)
    
    #Remaing Seats 
    available_slots = db.Column(db.Integer , nullable = False)
    
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    staff = db.relationship("User", backref="treks")
    
    #open/closed/started/completed treks shows by status 
    status = db.Column(db.String(100), default = "Open")
    
 
class Booking(db.Model):
    __tablename__ = "bookings"
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)

    booking_status = db.Column(db.String(20), default="Booked")

    payment_status = db.Column(db.String(20), default="Pending")
    
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    trek = db.relationship("Trek", backref= "bookings")
    user = db.relationship("User", backref="bookings")
   
   
class Announcement(db.Model):

    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.String(500), nullable=False)