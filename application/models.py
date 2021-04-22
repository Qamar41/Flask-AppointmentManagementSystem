from application import db,app


appointments=db.Table('appointments',

            db.Column('doctor',db.Integer,db.ForeignKey('doctor.id')),
            db.Column('patient',db.Integer,db.ForeignKey('patient.id')),

)




class Doctor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    appointment=db.relationship('Patient',secondary=appointments,backref=db.backref('appointmentss',lazy='dynamic'))
    specialization=db.Column(db.String(100),nullable=True)
    email=db.Column(db.String(100),unique=True , default='no@email.com', nullable=True)
    password=db.Column(db.String(25),nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name

class Patient(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64))
    email=db.Column(db.String(100),unique=True,default='no@email.com',nullable=True)
    disease_description=db.Column(db.String(200),nullable=True)
    password=db.Column(db.String(25),nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name

