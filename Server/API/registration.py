from flask import current_app, jsonify, make_response, request 
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from models import db, Users, Booking, Movie, TheaterTimeSlot
from models import Users,Roles,roles_users
from API.validation import UserError, PropertyExistError
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timedelta
from security import datastore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from data_access import get_user_by_user_id

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('password2')
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' 




class registrationAPI(Resource):
     def post(self):
        args = parser.parse_args()
        name = args.get('name',None)
        email = args.get('email',None)
        password = args.get('password',None)
        password2 = args.get('password2',None) 
        expiration_time = datetime.utcnow() + timedelta(minutes=30)

        def email_check(email):
            return re.fullmatch(regex, email)
        
        def pass_check(password):
            lowchk = False
            upchk= False
            numchk = False
            specialchk = False
            spstr = ' !"#$%^&*()*+,-./:;<=>?@'
            if(re.search('[a-z]', password)):
                lowchk = True
            if (re.search('[A-Z]', password)):
                upchk = True
            if (re.search('[0-9]',password)):
                numchk = True
            for i in range(len(password)):
                if password[i] in spstr:
                    specialchk = True
                    break 
            return lowchk and upchk and numchk and specialchk    
                          

        if name is None:
            raise UserError(400, "USERERR01", "Username is required") 
        if email is None or email_check(email) == False:
            raise UserError(400, "USERERR02", "Enter a valid email address")
        if password is None or password2 is None:
            raise UserError(400, "USERERR03", "Password should be greater than 8 characters")
        if password != password2:
            raise UserError(400, "USERERR04", "Passwords do not match")
        if pass_check(password) == False:
            raise UserError(400, "USERERR05", "Password does not meet its requirements.")
        if Users.query.filter_by(email = email).first():
            raise PropertyExistError('Email already exists', 409)
        

        email_domail = email.split('@')[-1].lower()
        admin_domains = ['ticketshow.com', 'admin.app']

        if email_domail in admin_domains:
            admin_role = Roles.query.filter_by(name='admin').first()
            if not admin_role:
                admin_role = Roles(name='admin')
                db.session.add(admin_role)
                db.session.commit()
            
            new_user = datastore.create_user(username=name, email=email, password=generate_password_hash(password,method="scrypt"))
            datastore.add_role_to_user(new_user, admin_role)
            db.session.commit()
            access_token = create_access_token(identity=new_user.id)
            return {
                'message': 'Admin Role Created successfully',
                'access_token': access_token,
                'role': admin_role.name,
                'exp': expiration_time.timestamp()
            }, 201
        else:
            user_role = Roles.query.filter_by(name = 'user').first()
            if not user_role:
                user_role = Roles(name='user')
                db.session.add(user_role)
                db.session.commit()

            new_user = datastore.create_user(username=name, email=email, password=generate_password_hash(password,method="scrypt"))
            datastore.add_role_to_user(new_user, user_role)
            db.session.commit()

            access_token = create_access_token(identity=new_user.id)

            return {
                'message': 'Regular user created successfully',
                'access_token': access_token,
                'role': user_role.name,
                'exp': expiration_time.timestamp()
            }, 201


class loginAPI(Resource):

    def email_check(email):
            return re.fullmatch(regex, email)
        
    def pass_chk(password):
        lowchk = False
        upchk= False
        numchk = False
        specialchk = False
        spstr = ' !"#$%^&*()*+,-./:;<=>?@'
        if(re.search('[a-z]', password)):
            lowchk = True
        if (re.search('[A-Z]', password)):
            upchk = True
        if (re.search('[0-9]',password)):
            numchk = True
        for i in range(len(password)):
            if password[i] in spstr:
                specialchk = True
                break 
        return lowchk and upchk and numchk and specialchk

    @jwt_required()
    def get(self,user_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        current_user_id = get_jwt_identity()
        user_id = user_id
        print(user_id)
        user = get_user_by_user_id(user_id)
        roles = user.roles
        role_names = [role.name for role in roles]
        user_details = {
            'user_id': user.id,
            'user_name': user.username,
            'user_email': user.email,
            'user_date_joined' : user.date_joined,
            'user_role' : role_names
        }
        return make_response(jsonify(user_details),200)

    def post(self):
        args = parser.parse_args()
        email = args.get('email',None)
        print(email)
        password = args.get('password',None)
        print(repr(password))
        if email is None or password is None:
            raise UserError(400, "USERERR06", "Email and password are required")
        
        user = Users.query.filter_by(email = email).first()
        if user is None:
            raise UserError(400, "USERERR07", "Invalid email or password")        
        
        role = [role.name for role in user.roles]

        expiration_time = datetime.utcnow() + timedelta(minutes=60)

        #password = generate_password_hash(password,method="scrypt")
        if not user or user is None or not check_password_hash(user.password, password):
            raise UserError(400, "USERERR07", "Invalid email or password")
        user_id = user.id
        user_name = user.username
        access_token = create_access_token(identity=user.id)
        print("exp:",expiration_time.timestamp())
        return {
                'access_token': access_token,
                'role': role,
                'user_id': user_id,
                'user_name': user_name,
                'exp': expiration_time.timestamp()
            }, 200

    @jwt_required()
    def put(self, user_id):
        def email_check(email):
            return re.fullmatch(regex, email)
        
        def pass_chk(password):
            lowchk = False
            upchk = False
            numchk = False
            specialchk = False
            spstr = ' !"#$%^&*()*+,-./:;<=>?@'
            if re.search('[a-z]', password):
                lowchk = True
            if re.search('[A-Z]', password):
                upchk = True
            if re.search('[0-9]', password):
                numchk = True
            for i in range(len(password)):
                if password[i] in spstr:
                    specialchk = True
                    break 
            return lowchk and upchk and numchk and specialchk

        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return make_response(jsonify({"message": "You are not authorized to edit this user"}), 403)

        user = get_user_by_user_id(user_id)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        args = parser.parse_args()
        new_username = args.get('name', user.username)
        new_email = args.get('email', user.email)
        new_password = args.get('password', None)
        new_password2 = args.get('password2', None)

        if new_username == user.username and new_email == user.email and not new_password:
            return make_response(jsonify({"message": "No changes were made"}), 200)

        if new_username != user.username:
            user.username = new_username

        if new_email != user.email:
            if not email_check(new_email):
                return make_response(jsonify({"message": "Invalid Email"}), 400)

            if Users.query.filter_by(email=new_email).first():
                return make_response(jsonify({"message": "Email already exists"}), 409)

            user.email = new_email

            email_domail = new_email.split('@')[-1].lower()
            admin_domains = ['ticketshow.com', 'admin.app']

            if email_domail in admin_domains:
                admin_role = Roles.query.filter_by(name='admin').first()
                if not admin_role:
                    admin_role = Roles(name='admin')
                    db.session.add(admin_role)
                    db.session.commit()

                user.roles = [admin_role]  
            else:
                user_role = Roles.query.filter_by(name='user').first()
                if not user_role:
                    user_role = Roles(name='user')
                    db.session.add(user_role)
                    db.session.commit()

                user.roles = [user_role]  

        if new_password and new_password2:
            if new_password != new_password2:
                return make_response(jsonify({"message": "Passwords do not match"}), 400)

            if not pass_chk(new_password):
                return make_response(jsonify({"message": "Password does not meet its requirements."}), 400)

            user.password = generate_password_hash(new_password, method="scrypt")

        db.session.commit()
        return make_response(jsonify({"message": "User updated successfully"}), 200)


        
    
    @jwt_required()
    def delete(self, user_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return make_response(jsonify({"message": "You are not authorized to delete this user"}), 403)

        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        book = Booking.query.filter_by(user_id=user_id).all()
        for entry in book:
            db.session.delete(entry)

        roles_to_delete = user.roles
        for role in roles_to_delete:
            user.roles.remove(role)
            db.session.commit()


        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({"message": "User deleted successfully"}), 200)


        