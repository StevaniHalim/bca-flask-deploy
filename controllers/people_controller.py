from flask import abort
from models.note_model import Note
from models.person_model import Person, PersonSchema

def read_all():
    # Create the list of people from our data
    people = Person.query.outerjoin(Note).all()

    # Serialize the data for the response
    person_schema = PersonSchema(many = True)
    return person_schema.dump(people)

def read_one(person_id):
    # Build the initial query
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )
    
    if person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        person_schema = PersonSchema()
        return person_schema.dump(person)

def update(person_id, person_data):
    updated_person = Person.query.get(person_id)

    if updated_person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        person_schema = PersonSchema()
        updated_person.fname = person_data['fname']
        updated_person.lname = person_data['lname']
        update = updated_person.update()
        return person_schema.dump(update)
    
def delete(person_id):
    deleted_person = Person.query.get(person_id)

    if deleted_person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    else:
        person_schema = PersonSchema()
        delete = deleted_person.delete()
        return person_schema.dump(delete)
    
def create(person_data):
    person_schema = PersonSchema()
    new_person = Person(
        fname = person_data['fname'],
        lname = person_data['lname']
    )
    create = new_person.create()
    return person_schema.dump(create)