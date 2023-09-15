from datetime import datetime
from config import db, ma
from marshmallow import fields

class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(
        db.Integer,
        primary_key = True
    )
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow
    )
    notes = db.relationship(
        'Note',
        backref='person',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Note.timestamp)'
    )

    def update(self):
        db.session.merge(self)
        db.session.commit()

        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return self
    
    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
    
    def create_note(self):
        db.session.commit()

        return self

class PersonNoteSchema(ma.SQLAlchemyAutoSchema):
    note_id = fields.Int()
    person_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        sqla_session = db.session
    
    notes = fields.Nested(PersonNoteSchema, many = True)