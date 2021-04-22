

from application import app,api
from application.models import *
from flask import jsonify,request
from flask_restful import Resource,reqparse,abort



class doctor(Resource):
    def get(self):
        docs=Doctor.query.all()
        basket=[]
        for i in docs:  
            basket.append(i.name)
        return jsonify (Doctors=basket)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str)
        
        args = parser.parse_args()
        check=Doctor.query.filter_by(name= args['name']).first()
        if check:
            return jsonify (message = args['name'] + ' already exists !')

        new_dr=Doctor(name=args['name'])
        db.session.add(new_dr)
        db.session.commit()
        return jsonify (Doctor_Created = args['name'])
        




class patient(Resource):
    def get(self):
        docs=Patient.query.all()
        basket=[]
        for i in docs:  
            basket.append(i.name)
        return jsonify (Patients=basket)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str)
        
        args = parser.parse_args()
        check=Patient.query.filter_by(name= args['name']).first()
        if check:
            return jsonify (message = args['name'] + ' already exists !')

        new_dr=Patient(name=args['name'])
        db.session.add(new_dr)
        db.session.commit()
        return jsonify (Patient_Registerd = args['name'])


class create_appointment(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_name',type=str)
        parser.add_argument('doctor_name',type=str)
        args = parser.parse_args()
        patient_check=Patient.query.filter_by(name=args['patient_name']).first()

        if patient:
            dr_check=Doctor.query.filter_by(name=args['doctor_name']).first()
            if dr_check:
                patient_check.appointmentss.append(dr_check)
                db.session.commit()
                return jsonify(message='appointment created')
                
            else:
                return jsonify(message='Doctor Does not exist , please select another doctor')
        return jsonify(message='Patient Does not exist , please add patient first')


class appointment(Resource):
    

    def get(self,id):
        # parser = reqparse.RequestParser()
        # parser.add_argument('patient_name',type=str)

        # args = parser.parse_args()
        patient_check = Patient.query.get(id)
        if patient_check:
            appoint=patient_check.appointmentss.all()
            basket=[]
            for i in appoint:
                basket.append(i.name)
            return jsonify(appointmest=basket)
        else:
            return jsonify(message='patient does not exist')

class patient_appointment(Resource):

    def get(self, id):
       
        patient_check = Patient.query.get(id)
        if patient_check:
            appoint = patient_check.appointmentss.all()
            basket = []
            for i in appoint:
                basket.append(i.name)
            return jsonify(appointmest=basket)
        else:
            return jsonify(message='patient does not exist')

class doctor_appointment(Resource):
    def get(self, id):
        doctor_check = Doctor.query.get(id)
        if doctor_check:
            appoint = doctor_check.appointment
            basket = []
            for i in appoint:
                basket.append(i.name)
            return jsonify(appointmest=basket)
        else:
            return jsonify(message='Doctor does not exist')


# Endpoints

api.add_resource(doctor,'/doctor')
api.add_resource(patient,'/patient')
api.add_resource(create_appointment,'/create_appointment')
api.add_resource(patient_appointment ,'/patient-appointment/<string:id>')
api.add_resource(doctor_appointment ,'/doctor-appointment/<string:id>')
