from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Location, Office, User,Car

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avis2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


def add_location():
 with app.app_context():
    db.session.add(Location(cityname='İstanbul'))
    db.session.add(Location(cityname='İzmir'))
    db.session.add(Location(cityname='Ankara'))
    db.session.commit()

def add_office():
 with app.app_context():
    db.session.add(Office(city_id=1, officename='İstanbul Airport'))
    db.session.add(Office(city_id=1, officename='Sabiha Gökçen Airport'))
    db.session.add(Office(city_id=1, officename='Taksim Office'))
    db.session.add(Office(city_id=1, officename='İstinye Office'))

    db.session.add(Office(city_id=2, officename='Alsancak Office'))
    db.session.add(Office(city_id=2, officename='Bornova Office'))
    db.session.add(Office(city_id=2, officename='Adnan Menderes Airport'))

    db.session.add(Office(city_id=3, officename='Yenimahalle Office'))
    db.session.add(Office(city_id=3, officename='Esenboğa Airport'))
    db.session.add(Office(city_id=3, officename='Atlantis Mall'))

    db.session.commit()


def delete_location_data():
  with app.app_context():
    db.session.query(Location).delete()
    db.session.commit() 

def delete_office_data():
 with app.app_context():
    db.session.query(Office).delete()
    db.session.commit() 

@app.route('/addCar', methods=['POST'])
def addCar():
    if request.method == 'POST':
        data = request.json 
        new_car = Car(
            brand=data.get('brand'),
            transmission=data.get('transmission'),
            deposit=data.get('deposit'),
            mileage=data.get('mileage'),
            age=data.get('age'),
            cost=data.get('cost'),
            img=data.get('img'),
            office_id=data.get('office_id')
        )
        db.session.add(new_car)
        db.session.commit()
        return 'Car added successfully'
    else:
        return 'No data provided'

@app.route('/getCarsByOfficeId/<int:office_id>', methods=['GET'])
def getCarsByOfficeId(office_id):
    cars = Car.query.filter_by(office_id=office_id).all()

    if cars:
        car_list = []
        for car in cars:
            car_dict = {
                'car_id': car.id,
                'brand': car.brand,
                'transmission': car.transmission,
                'deposit': car.deposit,
                'mileage': car.mileage,
                'age': car.age,
                'cost': car.cost,
                'office_id': car.office_id,
                'img': car.img
            }
            car_list.append(car_dict)

        return jsonify({'cars': car_list})
    else:
        return 'No cars found for the given office ID'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        new_user = User(
            name=name,
            surname=surname,
            email=email,
            username=username,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('You are registered and can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)

