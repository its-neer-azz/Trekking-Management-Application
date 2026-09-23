from app import app
from models import db, User, Trek

with app.app_context():
    db.create_all()

    # ------------------ Admin ------------------

    admin = User.query.filter_by(email="admin@gmail.com").first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password="admin123",
            role="admin",
            approved=True
        )

        db.session.add(admin)

    # ------------------ Staff ------------------

    staff_data = [

        ("Rahul Sharma", "rahul.staff@gmail.com"),
        ("Aman Verma", "aman.staff@gmail.com"),
        ("Priya Singh", "priya.staff@gmail.com"),
        ("Karan Mehta", "karan.staff@gmail.com"),
        ("Neha Kapoor", "neha.staff@gmail.com"),
        ("Rohan Gupta", "rohan.staff@gmail.com"),
        ("Simran Kaur", "simran.staff@gmail.com")

    ]

    for name, email in staff_data:

        if not User.query.filter_by(email=email).first():

            staff = User(

                name=name,
                email=email,
                password="qwer",
                role="staff",
                approved=True

            )

            db.session.add(staff)

    # Pending Staff

    if not User.query.filter_by(email="arjun.staff@gmail.com").first():

        pending = User(

            name="Arjun Patel",
            email="arjun.staff@gmail.com",
            password="qwer",
            role="staff",
            approved=False

        )

        db.session.add(pending)

    # ------------------ Users ------------------

    users = [

        ("Aarav Singh","aarav@gmail.com"),
        ("Ananya Gupta","ananya@gmail.com"),
        ("Vivaan Sharma","vivaan@gmail.com"),
        ("Diya Patel","diya@gmail.com"),
        ("Kabir Verma","kabir@gmail.com"),
        ("Ishita Kapoor","ishita@gmail.com"),
        ("Aryan Mehta","aryan@gmail.com"),
        ("Meera Joshi","meera@gmail.com"),
        ("Aditya Mishra","aditya@gmail.com"),
        ("Sneha Yadav","sneha@gmail.com")

    ]

    for name,email in users:

        if not User.query.filter_by(email=email).first():

            user = User(

                name=name,
                email=email,
                password="qwer",
                role="user",
                approved=True

            )

            db.session.add(user)

    db.session.commit()

    # ------------------ Treks ------------------

    staff = User.query.filter_by(role="staff", approved=True).all()

    trek_data = [

        ("Triund Trek","Himachal Pradesh","Easy",2,25),
        ("Kedarkantha","Uttarakhand","Easy",5,30),
        ("Hampta Pass","Himachal Pradesh","Medium",6,20),
        ("Valley of Flowers","Uttarakhand","Easy",4,35),
        ("Sandakphu","West Bengal","Medium",7,18),
        ("Brahmatal","Uttarakhand","Medium",6,22),
        ("Kuari Pass","Uttarakhand","Medium",5,25),
        ("Rupin Pass","Himachal Pradesh","Hard",8,15),
        ("Goechala","Sikkim","Hard",10,12),
        ("Kashmir Great Lakes","Kashmir","Hard",8,20)

    ]

    for i, trek in enumerate(trek_data):

        name, location, difficulty, duration, slots = trek

        if not Trek.query.filter_by(name=name).first():

            new_trek = Trek(

                name=name,
                location=location,
                difficulty=difficulty,
                duration=duration,
                total_slots=slots,
                available_slots=slots,
                status="Open",
                staff_id=staff[i % len(staff)].id

            )

            db.session.add(new_trek)

    db.session.commit()

    print("Dummy data inserted successfully.")