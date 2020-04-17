from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
#import os

############################################

## SQL DATABASE SECTION ##
#date: April 10th 2020
#############################################
#setup the base dir for the database setup
#basedir = os.path.abspath(os.path.dirname(__file__))
#setup the database uri
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///' + os.path.join(basedir,'data.sqllite')
#turn off track modifications for the database
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create a db instance
db = SQLAlchemy()
#migrate db with app
#Migrate(app,db)
#create the instance of login manager
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


##################################
### MODELS ######################
################################
#create the safety questionnaire model for the application that will be integrated with the front end

class safety_questionnaire_database(db.Model):
    #set of questionnaire: reference can be checked in safety questionnaire questions
    __tablename__ = 'safety_questionnaire'
    id = db.Column(db.Integer, primary_key = True)
    kid_name = db.Column(db.Text)
    difficulty_bed = db.Column(db.Text)
    adequate_sunlight = db.Column(db.Text)
    floor_hazard = db.Column(db.Text)
    towel_rails = db.Column(db.Text)
    unsteady_standing = db.Column(db.Text)
    water_presence = db.Column(db.Text)
    bench_height = db.Column(db.Text)
    kitchen_reach = db.Column(db.Text)
    slip_products = db.Column(db.Text)
    electrical_cords = db.Column(db.Text)
    stairs_edge = db.Column(db.Text)
    stairs_handrails = db.Column(db.Text)
    path_checked = db.Column(db.Text)

    #instantiate the values that are eing put up on the forms from the front end in the init method
    #the class
    def __init__(self,kid_name,difficulty_bed, adequate_sunlight, floor_hazard, towel_rails, unsteady_standing,
    water_presence,bench_height,kitchen_reach,slip_products, electrical_cords, stairs_edge, stairs_handrails, path_checked):
        self.kid_name = kid_name
        self.difficulty_bed = difficulty_bed
        self.adequate_sunlight = adequate_sunlight
        self.floor_hazard = floor_hazard
        self.towel_rails = towel_rails
        self.unsteady_standing = unsteady_standing
        self.water_presence = water_presence
        self.bench_height = bench_height
        self.kitchen_reach = kitchen_reach
        self.slip_products = slip_products
        self.electrical_cords = electrical_cords
        self.stairs_edge = stairs_edge
        self.stairs_handrails = stairs_handrails
        self.path_checked = path_checked

    #method to return the values
    # def __repr__(self):
    #     #print("This is called")
    #     #print(f'{ self.kid_name }')
    #     return f'{self.kid_name}'
########################################################################################################
#create the user table here for validating the system administrator
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique=True, index = True)
    password_hash = db.Column(db.String(128))

    #create the instance of the db object
    def __init__(self,username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

########################################################################################################
class CouncilDisasterData(db.Model):
    __tablename__ = 'CouncilDisasterData'
    id = db.Column(db.Integer, primary_key = True)
    council = db.Column(db.Text)
    state = db.Column(db.Text)
    calamity_1 = db.Column(db.Text)
    calamity_2 = db.Column(db.Text)
    calamity_3 = db.Column(db.Text)
    calamity_4 = db.Column(db.Text)

    def __init__(self,council,state,calamity_1,calamity_2,calamity_3,calamity_4):
        self.council = council
        self.state = state
        self.calamity_1 = calamity_1
        self.calamity_2 = calamity_2
        self.calamity_3 = calamity_3
        self.calamity_4 = calamity_4
