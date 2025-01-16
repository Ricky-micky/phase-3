from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Doctor, Animal, Owner  # Import models

app = Flask(__name__)

# Database URL (Make sure this points to the correct path)
DATABASE = 'sqlite:////home/charles-njoroge/Desktop/FullStack/FullStack3/Backend/dr_Tembo.sqlite'
data_engine = create_engine(DATABASE)
data_session = sessionmaker(bind=data_engine)
mysession = data_session()

# Create all tables (if they don't exist yet)
Base.metadata.create_all(data_engine)

# Add a new doctor
@app.route('/api/doctors', methods=['POST'])
def add_doctor():
    try:
        data = request.json
        new_doctor = Doctor(
            name=data['name'],
            age=data['age'],
            location=data['location']  # Match location to the Doctor model
        )
        mysession.add(new_doctor)
        mysession.commit()
        return {'message': 'Doctor created successfully!'}
    except Exception as e:
        return {'error': str(e)}

# Get all doctors
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        doctors = mysession.query(Doctor).all()  # Fetch all doctors
        results = []
        for doctor in doctors:
            doctor_info = {
                "id": doctor.id,
                "name": doctor.name,
                "age": doctor.age,
                "location": doctor.location,  # Match location to the Doctor model
                "animals": [{"id": p.id, "name": p.name, "type": p.a_type} for p in doctor.animals]
            }
            results.append(doctor_info)
        return {'doctors': results}
    except Exception as e:
        return {'error': str(e)}

# Delete a doctor
@app.route('/api/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    try:
        doctor = mysession.query(Doctor).get(id)
        if not doctor:
            return {'error': 'Doctor not found'}
        mysession.delete(doctor)
        mysession.commit()
        return {'message': 'Doctor deleted successfully'}
    except Exception as e:
        return {'error': str(e)}

# Add a new animal
@app.route('/api/animals', methods=['POST'])
def add_animal():
    try:
        data = request.json
        new_animal = Animal(
            name=data['name'],
            a_type=data['a_type'],
            doctor_id=data['doctor_id'],
            owner_id=data['owner_id']
        )
        mysession.add(new_animal)
        mysession.commit()
        return {'message': 'Animal created successfully!'}
    except Exception as e:
        return {'error': str(e)}

# Add a new owner
@app.route('/api/owners', methods=['POST'])
def add_owner():
    try:
        data = request.json
        new_owner = Owner(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            location=data['location']
        )
        mysession.add(new_owner)
        mysession.commit()
        return {'message': 'Owner created successfully!'}
    except Exception as e:
        return {'error': str(e)}

# Get all animals
@app.route('/api/animals', methods=['GET'])
def get_animals():
    try:
        animals = mysession.query(Animal).all()  # Fetch all animals
        results = []
        for animal in animals:
            animal_info = {
                "id": animal.id,
                "name": animal.name,
                "type": animal.a_type,
                "doctor": {"id": animal.doctor.id, "name": animal.doctor.name},
                "owner": {"id": animal.owner.id, "name": animal.owner.name}
            }
            results.append(animal_info)
        return {'animals': results}
    except Exception as e:
        return {'error': str(e)}

# Get all owners
@app.route('/api/owners', methods=['GET'])
def get_owners():
    try:
        owners = mysession.query(Owner).all()  # Fetch all owners
        results = []
        for owner in owners:
            owner_info = {
                "id": owner.id,
                "name": owner.name,
                "email": owner.email,
                "phone_number": owner.phone_number,
                "location": owner.location,
                "animals": [{"id": p.id, "name": p.name, "type": p.a_type} for p in owner.animals]
            }
            results.append(owner_info)
        return {'owners': results}
    except Exception as e:
        return {'error': str(e)}

# Print all registered routes
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
