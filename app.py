from flask import Flask , render_template, request, redirect, session, flash
from config import Config
from models import db, User , Trek, Booking , Announcement

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods =(["GET", "POST"]))
def login():
    if request.method == "POST":
        email= request.form["email"]
        password= request.form["password"]
         
        
        user = User.query.filter_by(email=email).first()
        
        if not user :
            flash("Email Doesn't exists", "danger")
            return redirect("/login")
        if user.password!= password:
            flash("Incorrect password.", "danger")
            return redirect("/login")
        if not user.active:
            flash("Your account has been deactivated by Admin.", "danger")
            return redirect("/login")
        session["user_id"] = user.id
        session["role"] = user.role
        
        
        if user.role == "admin":
            return redirect("/admin")
        
        if user.role == "staff":
            if not user.approved:
                flash("Your staff account is waiting for Admin approval.", "warning")
                return redirect("/login")
            return redirect("/staff")
        
        if user.role == "user":
            return redirect("/user")
    return render_template("login.html")

@app.route("/deactivate/<int:id>")
def deactivate(id):

    if session.get("role") != "admin":
        return redirect("/login")

    user = User.query.get(id)

    if user:
        user.active = False
        db.session.commit()

    return redirect(request.referrer)


@app.route("/activate/<int:id>")
def activate(id):

    if session.get("role") != "admin":
        return redirect("/login")

    user = User.query.get(id)

    if user:
        user.active = True
        db.session.commit()

    return redirect(request.referrer)

@app.route("/register", methods = ["GET", "POST"])
def register():    
    if request.method == "POST" :
        
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        
        print(name)
        print(email)
        print(password)
        print(role)
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered.", "danger")
            return redirect("/register")
        
        
        new_user= User(
            name=name,
            email=email,
            password=password,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect("/login")
    return render_template("register.html")



@app.route("/admin")
def admin():
    
    if session.get("role") !="admin":
        return redirect("/login")
    
    search = request.args.get("search")
    difficulty = request.args.get("difficulty")

    treks = Trek.query
    if search:
        treks = treks.filter(
            (Trek.name.ilike(f"%{search}%")) |
            (Trek.location.ilike(f"%{search}%"))
        )

    if difficulty and difficulty != "All":
        treks = treks.filter_by(difficulty=difficulty)

    treks = treks.all()
    
    staff_search = request.args.get("staff_search", "")            
    pending_staff = User.query.filter_by(
        role="staff",
        approved=False
    )

    if staff_search:
        pending_staff = pending_staff.filter(
            (User.name.ilike(f"%{staff_search}%")) |
            (User.email.ilike(f"%{staff_search}%"))
        )

    pending_staff = pending_staff.all()
    
    announcement = Announcement.query.first()
    
    
   
    
    
    total_treks = Trek.query.count()
    total_staff = User.query.filter_by(role="staff").count()
    total_users = User.query.filter_by(role="user").count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin_dashboard.html",
        treks=treks,
        pending_staff=pending_staff,
        total_treks=total_treks,
        total_staff=total_staff,
        total_users=total_users,
        total_bookings=total_bookings,
        announcement=announcement,
        search=search,
        staff_search=staff_search,
        back_url="/admin"
    )
    
    
@app.route("/staff")
def staff():
    
    if session.get("role") == "user":
        return redirect("/login")
    
    user_id = session["user_id"]
    staff = User.query.get(user_id) 
    treks = Trek.query.filter_by(staff_id = user_id).all()
    announcement = Announcement.query.first()
    
    return render_template("staff_dashboard.html" , staff=staff, treks=treks, announcement=announcement, back_url="/staff")

@app.route("/all_staff")
def all_staff():

    if session.get("role") != "admin":
        return redirect("/login")

    search = request.args.get("search", "")

    staff = User.query.filter_by(role="staff")

    if search:

        staff = staff.filter(
            (User.name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    staff = staff.all()

    return render_template(
        "all_staff.html",
        staff=staff,
        search=search
    )

@app.route("/all_users")
def all_users():

    if session.get("role") != "admin":
        return redirect("/login")

    search = request.args.get("search", "")

    users = User.query.filter_by(role="user")

    if search:

        users = users.filter(
            (User.name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    users = users.all()

    return render_template(
        "all_users.html",
        users=users,
        search=search
    )
    
@app.route("/user")
def user():
    
    if session.get("role") != "user":
        return redirect("/login")
    search = request.args.get("search")
    difficulty = request.args.get("difficulty")

    treks = Trek.query.filter_by(status="Open")
    if search:
        treks = treks.filter(
            (Trek.name.ilike(f"%{search}%")) |
            (Trek.location.ilike(f"%{search}%"))
        )

    if difficulty and difficulty != "All":
        treks = treks.filter_by(difficulty=difficulty)

    treks = treks.all()
    return render_template("user_dashboard.html", treks=treks)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        user.name = request.form["name"]

        password = request.form["password"]

        if password:
            user.password = password

        db.session.commit()

        flash("Profile updated successfully.", "success")

        if user.role == "user":
            return redirect("/user")

        elif user.role == "staff":
            return redirect("/staff")

    return render_template("edit_profile.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/approve/<int:id>")
def approve(id):   
    staff = User.query.get(id)
    
    if staff:
        staff.approved = True
        
        db.session.commit()
        
    return redirect("/admin")


@app.route("/add_trek", methods = ["GET" , "POST"])
def add_trek():
    
    staff_members = User.query.filter_by(
        role="staff",
        approved=True
    ).all()
    
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        status = request.form["status"]
        total_slots = request.form["total_slots"]
        duration = request.form["duration"]
        staff_id=request.form["staff_id"]
        
        new_trek = Trek(
            name=name,
            location = location,
            difficulty =difficulty,
            status = status,
            total_slots=total_slots,
            available_slots = total_slots,
            duration = duration,
            staff_id=staff_id
        )
        db.session.add(new_trek)
        db.session.commit()
        return redirect("/admin")
    return render_template("add_trek.html", staff_members=staff_members)

@app.route("/edit_trek/<int:id>", methods = ["GET","POST"])
def edit_trek(id):
    
    staff_members = User.query.filter_by(role="staff",  approved=True).all()
    
    trek = Trek.query.get(id)
    if request.method == "POST":
        trek.name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = request.form["duration"]
        trek.total_slots = request.form["total_slots"]
        trek.available_slots = request.form["available_slots"]
        trek.status = request.form.get("status")
        trek.staff_id = request.form["staff_id"]
        db.session.commit()
    
        return redirect("/admin")
    return render_template("edit_trek.html", trek=trek, staff_members=staff_members)
    
    
@app.route("/delete_trek/<int:id>")
def delete_trek(id):
     
     trek= Trek.query.get(id)
     
     if trek:
         db.session.delete(trek)
         db.session.commit()
         return redirect("/admin")


@app.route("/announcement", methods=["POST"])
def announcement():

    message = request.form["message"]

    announcement = Announcement.query.first()

    if announcement:
        announcement.message = message
    else:
        announcement = Announcement(message=message)
        db.session.add(announcement)

    db.session.commit()

    return redirect("/admin")


@app.route("/book_trek/<int:id>")
def book_trek(id):
    if session.get("role") != "user":
        flash("Only users can book treks.", "danger")
        return redirect("/login")

    trek = Trek.query.get(id)
    user_id = session["user_id"]

    if trek.status != "Open":
        flash("This trek is currently closed for booking.", "warning")
        return redirect("/user")

    existing_booking = Booking.query.filter_by(
        user_id=user_id,
        trek_id=id
    ).first()

    if existing_booking:
        flash("You have already booked this trek.", "warning")
        return redirect("/user")

    if trek.available_slots <= 0:
        flash("No seats available for this trek.", "danger")
        return redirect("/user")

    booking = Booking(
        user_id=user_id,
        trek_id=id
    )

    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()
    flash("Trek booked successfully!", "success")

    return redirect("/user")     
    
@app.route("/my_bookings")
def my_booking():

    user_id = session["user_id"]

    current_bookings = Booking.query.filter_by(
        user_id=user_id,
        booking_status="Booked"
    ).all()

    history = Booking.query.filter_by(
        user_id=user_id,
        booking_status="Completed"
    ).all()

    return render_template(
        "my_bookings.html",
        current_bookings=current_bookings,
        history=history
    )

@app.route("/cancel_booking/<int:id>")
def cancel_booking(id):
    booking=Booking.query.get(id)
    
    if booking :
        trek = Trek.query.get(booking.trek_id)
        trek.available_slots +=1
        db.session.delete(booking)
        db.session.commit()
    return redirect("/my_bookings")


@app.route("/start_trek/<int:id>")
def start_trek(id):
    trek = Trek.query.get(id)
    
    if trek:
        trek.status = "Started"
        db.session.commit()
    return redirect("/staff")

@app.route("/complete_trek/<int:id>")
def complete_trek(id):

    trek = Trek.query.get(id)

    if trek:

        trek.status = "Completed"

        bookings = Booking.query.filter_by(trek_id=id).all()

        for booking in bookings:
            booking.booking_status = "Completed"
            booking.payment_status = "Paid"
        db.session.commit()

    return redirect("/staff")

@app.route("/trek_bookings/<int:id>")
def trek_bookings(id):
    if session.get("role") == "user":
       return redirect("/login")
    bookings = Booking.query.filter_by(trek_id=id).all()
    
    return render_template("all_bookings.html", bookings=bookings , back_url = "/staff" )


@app.route("/all_bookings")
def all_bookings():
    
    bookings = Booking.query.all()
    
    return render_template("all_bookings.html", bookings=bookings ,  back_url="/admin")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(role = "admin").first()
        
        if not admin:
            admin = User(
                name = "Admin", 
                email="admin@gmail.com",
                password="admin123",
                role="admin",
                approved= True                
            )
            
            db.session.add(admin)
            db.session.commit()
        
    app.run(debug=True)