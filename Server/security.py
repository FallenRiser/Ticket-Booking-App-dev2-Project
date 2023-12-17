from flask_security import Security, SQLAlchemyUserDatastore
from models import db, Users, Roles

datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security()