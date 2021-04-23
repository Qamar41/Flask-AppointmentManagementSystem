

from application import app,api
from application.models import *
from flask import jsonify,request,make_response
from flask_restful import Resource,reqparse
import  jwt
import datetime
from functools import wraps




app.config['SECRET_KEY']='somesecret'



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
        parser.add_argument('specialization',type=str)
        parser.add_argument('email',type=str)
        parser.add_argument('password',type=str)
        
        args = parser.parse_args()
        check=Doctor.query.filter_by(name= args['email']).first()
        if check:
            return jsonify (message = args['email'] + ' already exists !')

        new_dr=Doctor(name=args['name'],specialization=args['specialization'],email=args['email'],password=args['password'])
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
        parser.add_argument('email',type=str)
        parser.add_argument('disease_description',type=str)
        parser.add_argument('password',type=str)

        args = parser.parse_args()
        check=Patient.query.filter_by(name= args['name']).first()
        if check:
            return jsonify (message = args['name'] + ' already exists !')

        new_dr=Patient(name=args['name'],email=args['email'],disease_description=args['disease_description'],password=args['password'])
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


def token_required_dr(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token :
            return jsonify ({'message': 'token is missing'}),401
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            current_user_dr=Doctor.query.filter_by(id=data['id']).first()

        except:
            return jsonify({'message': 'token is invalid '}), 401
        return f(current_user_dr,*args,**kwargs)

    return decorated







def Patient_token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        if not token :
            return jsonify ({'message': 'token is missing'}),401
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            current_user_pt=Patient.query.filter_by(id=data['id']).first()

        except:
            return jsonify({'message': 'token is invalid '}), 401
        return f(current_user_pt,*args,**kwargs)

    return decorated











# Login 


class doctor_login(Resource):
    def get(self):
        auth=request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify ',401,{'WWW.Authenticate':"Basic-realm='Login Required !'"})
        user=Doctor.query.filter_by(email=auth.username).first()
        if not user:
            return make_response('Could not verify ', 401, {'WWW.Authenticate': "Basic-realm='Login Required !'"})

        if user.password==auth.password:
            token=jwt.encode({"id":user.id,"exp": datetime.datetime.now() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
            return jsonify({"doctor token , put it in headers with key x-access-token":token.decode('UTF-8')})
        return make_response('Could not verify ', 401, {'WWW.Authenticate': "Basic-realm='Login Required !'"})






class patient_login(Resource):
    def get(self):
        auth=request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify ',401,{'WWW.Authenticate':"Basic-realm='Login Required !'"})
        user=Patient.query.filter_by(email=auth.username).first()
        if not user:
            return make_response('Could not verify ', 401, {'WWW.Authenticate': "Basic-realm='Login Required !'"})

        if user.password==auth.password:
            token=jwt.encode({"id":user.id,"exp": datetime.datetime.now() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
            return jsonify({"Patient token":token.decode('UTF-8')})
        return make_response('Could not verify ', 401, {'WWW.Authenticate': "Basic-realm='Login Required !'"})








@app.route('/patient-appointments')
@Patient_token_required
def patient_appointmentss(current_user_patient ):

    doctor_check = Patient.query.get(current_user_patient.id)
    print(doctor_check)
    # x=current_user_dr.id
    # print('id is==>' , x)
    # doctor_check = Doctor.query.get(current_user_dr)
    # # if doctor_check:
    appoint = doctor_check.appointmentss
    basket = []
    for i in appoint:
        basket.append({"Dr": i.name , "Specialist":i.specialization})
    return jsonify({"appointmest":basket})




@app.route('/doctor-appointment')
@token_required_dr
def hello(current_user_dr):
    appoint=current_user_dr.appointment
    basket=[]
    for i in appoint:
        # basket.append(i.name + ' and disease is ' + str(i.disease_description)) 
        basket.append({'patient':i.name , 'disease' : str(i.disease_description)}  ) 

    
    
    return jsonify(appointment=basket)






# Endpoints

api.add_resource(doctor,'/doctor')
api.add_resource(patient,'/patient')
api.add_resource(create_appointment,'/create_appointment')
api.add_resource(doctor_login ,'/doctor-login')
api.add_resource(patient_login ,'/patient-login')
