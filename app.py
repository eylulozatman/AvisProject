from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Location, Office, User,Car
from sqlalchemy import text
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy.util import OrderedSet
from sqlalchemy import create_engine, MetaData


app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avis2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


def generate_database_schema():
    engine = create_engine('sqlite:///avis2.db')  # Replace with your actual database URI
    metadata = MetaData(bind=engine)

    graph = create_schema_graph(metadata=metadata)
    graph.write_png('database_schema.png')


def delete_location_data():
  with app.app_context():
    db.session.query(Location).delete()
    db.session.commit() 

def delete_office_data():
 with app.app_context():
    db.session.query(Office).delete()
    db.session.commit() 

def drop_user_table():
    with app.app_context():
        # This command drops the 'users' table
        db.session.execute(text('DROP TABLE IF EXISTS "users";'))

        # Commit the changes
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

@app.route('/updateCar/<int:car_id>', methods=['PUT'])
def updateCar(car_id):
    if request.method == 'PUT':
        data = request.json
        car = Car.query.filter_by(id=car_id).first()
        if car:
            car.transmission = data.get('transmission', car.transmission)
            car.deposit = data.get('deposit', car.deposit)
            car.mileage = data.get('mileage', car.mileage)
            car.age = data.get('age', car.age)
            car.cost = data.get('cost', car.cost)
            car.img = data.get('img', car.img)
            car.office_id = data.get('office_id', car.office_id)

            db.session.commit()
            return 'Car updated successfully'
        else:
            return 'Car not found'
    else:
        return 'Invalid request method'

@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        city = request.form['city']
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            username=username,
            password=password,
            city=city
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
        user_firstname=user.name
        user_city = user.city
        if user:
            flash('Login successful', 'success')
            return redirect(url_for('home', user_firstname=user_firstname,user_city=user_city))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')
@app.route('/logout')
def logout():
    return redirect(url_for('register'))

@app.route('/get-city', methods=['POST'])
def get_city():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    city = "New York"

    return jsonify({'city': city})

@app.route('/home')
@app.route('/home/<user_firstname>/<user_city>')
def home(user_firstname=None, user_city=None):

    locations = Location.query.all()
    if user_firstname:
       return render_template('homepage.html', locations=locations, user_firstname=user_firstname, user_city=user_city)
    
    else:
     return render_template('homepage.html')


@app.route('/getOfficesByCity', methods=['POST'])
def get_offices_by_city():
    city_id = request.json['city_id']
    offices = Office.query.filter_by(city_id=city_id).all()
    return jsonify([{'id': office.id, 'officename': office.officename} for office in offices])


@app.route('/getCarsByInfo', methods=['GET'])
def getCarsByInfo():
    office_id = request.args.get('office_id')
    dropoff_id = request.args.get('dropoff_id')
    total_days = int(request.args.get('total_days'))

    # Fetch cars based on the selected office_id
    cars = Car.query.filter_by(office_id=office_id).all()

    # Fetch office names
    ao = Office.query.get(office_id)
    ao_name = ao.officename if ao else None

    to = Office.query.get(dropoff_id)
    to_name = to.officename if to else None

    # Split images string into a list
    for car in cars:
        car.images = car.img.split(',')

    # Apply sorting if specified in the form
    transmission = request.args.get('transmission')
    cost = request.args.get('cost')

    if transmission and transmission != 'all':
        cars = [car for car in cars if car.transmission == transmission]

    if cost == 'asc':
        cars = sorted(cars, key=lambda x: x.cost)
    elif cost == 'desc':
        cars = sorted(cars, key=lambda x: x.cost, reverse=True)

    return render_template('carDetails.html', cars=cars, total_days=total_days, ao_name=ao_name, to_name=to_name)

    
if __name__ == '__main__':

    app.run()

'''
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
'''