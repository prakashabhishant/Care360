# import libraries
import os
from forms.forms import SafetyQuestionnaireForm, DeleteFromSafety, LoginForm, RegistrationForm, DisasterForm
from models.model import safety_questionnaire_database, db, login_manager, User, CouncilDisasterData
from flask import Flask, render_template, url_for, redirect, session, flash, abort, request
from flask_sqlalchemy import SQLAlchemy
#database migrate import
from flask_migrate import Migrate
from flask_login import login_user, login_required, logout_user
from io import TextIOWrapper
import csv

#imports ended
########################################################################################################
#configuring the application for the secret key and database related sqlalchemy
app = Flask(__name__)

#configure the secret key

app.config['SECRET_KEY'] = 'mysecretkey'

#set the base directory for the flask database
basedir = os.path.abspath(os.path.dirname(__file__))

#setup the database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
#turn off track modifications for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create a db instance
db.init_app(app)
#migrate db with app
Migrate(app,db)

#configure the login manager
login_manager.init_app(app)
login_manager.login_view = 'login'

########################################################################################################
#view for the main page
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

########################################################################################################
#view for the general home safety page
@app.route('/homesafety')
def homesafety():
    return render_template('homesafety.html',title='Home Safety')


########################################################################################################
#view for the safety questionnaire
@app.route('/safety_questionnaire',methods=['GET','POST'])
def safety_questionnaire():
    form = SafetyQuestionnaireForm()

    if form.validate_on_submit():
        # get the data in the session object for the client side
        session['kid_name'] = form.kid_name.data
        session['difficulty_bed'] = form.difficulty_bed.data
        session['adequate_sunlight'] = form.adequate_sunlight.data
        session['floor_hazard'] = form.floor_hazard.data
        session['towel_rails'] = form.towel_rails.data
        session['unsteady_standing'] = form.unsteady_standing.data
        session['water_presence'] = form.water_presence.data
        session['bench_height'] = form.bench_height.data
        session['kitchen_reach'] = form.kitchen_reach.data
        session['slip_products'] = form.slip_products.data
        session['electrical_cords'] = form.electrical_cords.data
        session['stairs_edge'] = form.stairs_edge.data
        session['stairs_handrails'] = form.stairs_handrails.data
        session['path_checked'] = form.path_checked.data

        # this is for the data to be pushed into the database
        kid_name = form.kid_name.data
        difficulty_bed = form.difficulty_bed.data
        adequate_sunlight =form.adequate_sunlight.data
        floor_hazard = form.floor_hazard.data
        towel_rails = form.towel_rails.data
        unsteady_standing = form.unsteady_standing.data
        water_presence = form.water_presence.data
        bench_height = form.bench_height.data
        kitchen_reach = form.kitchen_reach.data
        slip_products = form.slip_products.data
        electrical_cords = form.electrical_cords.data
        stairs_edge = form.stairs_edge.data
        stairs_handrails = form.stairs_handrails.data
        path_checked = form.path_checked.data

        #create new object to insert in the database
        new_entry = safety_questionnaire_database(kid_name, difficulty_bed, adequate_sunlight, floor_hazard,
                    towel_rails, unsteady_standing, water_presence,bench_height, kitchen_reach,
                     slip_products, electrical_cords, stairs_edge, stairs_handrails, path_checked )

        #add new entry to the database
        db.session.add(new_entry)
        db.session.commit()

        #return after successful completion to the database
        return redirect(url_for('safety_questionnaire_feedback'))

    #render the template for the current view
    return render_template('safetquestionnairepage.html', form=form, title='Safety Questionnaire')

########################################################################################################

#render template for safety questionnaire feedback
@app.route('/safety_questionnaire_feedback')
def safety_questionnaire_feedback():
    return render_template('safety_questionnaire_feedback.html')

########################################################################################################
#page to query the database and check whether entries are pushing or not
@app.route('/safety_questionnaire_query')
@login_required
def safety_questionnaire_query():
    questionnaire = safety_questionnaire_database.query.all()[-5:]#list only the last five records inserted in the table
    return render_template('safety_questionnaire_answers.html',questionnaire= questionnaire)

########################################################################################################
#template to delete all the data in the safety questionnaire table
@app.route('/delete_questionnaire_data',methods=['GET','POST'])
@login_required
def delete_questionnaire():
    form = DeleteFromSafety()
    if form.validate_on_submit():
        try:
            db.session.query(safety_questionnaire_database).delete()
            db.session.commit()
        except:
            db.session.rollback()
    return render_template('delete_questionnaire_data.html', form = form)


########################################################################################################
#view that will be seen by when user logins to the system
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

########################################################################################################
#logout view for the admin
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged Out")
    return redirect(url_for('index'))

########################################################################################################
#login view for the system administrator
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Sucessfully')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next =url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)


########################################################################################################
#view for the admin to create another administrator
@app.route('/register',methods=['GET','POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("thank you for registering")
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

########################################################################################################
#view for inserting the council d  ata by the system administrator into the CouncilDisasterData
@app.route('/uploadcouncildisaster', methods=['GET','POST'])
@login_required
def uploadcouncildisaster():
    print(CouncilDisasterData.query.all()[-1:])
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file.save(os.path.join(basedir, csv_file.filename))
        with open(csv_file.filename,'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                council_data = CouncilDisasterData(council = row[0], state=row[1], calamity_1 = row[2], calamity_2 = row[3], calamity_3 = row[4], calamity_4 = row[5])
                db.session.add(council_data)
                db.session.commit()
        return redirect(url_for('uploadcouncildisaster'))
    return render_template('uploadcouncildisaster.html')

#query all the council query data
########################################################################################################
@app.route('/councilquery')
@login_required
def councilquery():
    councildata = CouncilDisasterData.query.all()[0:5]#list only the last five records inserted in the table
    return render_template('councilquery.html',councildata= councildata)

########################################################################################################
@app.route('/safetybycouncil',methods=['GET','POST'])
def safetybycouncil():
    form = DisasterForm()
    # CouncilDisasterData.query.filter(CouncilDisasterData.council == 'ï»¿Alpine').update({"council":"Alpine"})
    # db.session.commit()
    form.council_name.choices = [(c.council,c.council) for c in CouncilDisasterData.query.with_entities(CouncilDisasterData.council).all()]
    if form.validate_on_submit():
        council_input = form.council_name.data
        queried_data = CouncilDisasterData.query.filter_by(council = council_input).first()
        session['council'] = queried_data.council
        session['state'] = queried_data.state
        session['calamity_1'] = queried_data.calamity_1
        session['calamity_2'] = queried_data.calamity_2
        session['calamity_3'] = queried_data.calamity_3
        session['calamity_4'] = queried_data.calamity_4
        return redirect(url_for('disasterrecommendation'))
    return render_template('safetybycouncil.html',form=form)


@app.route('/disasterrecommendation')
def disasterrecommendation():
    return render_template('disasterrecommendation.html')



########################################################################################################
#default page error hander
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))



########################################################################################################

#run the main file
if __name__ == '__main__':
    app.run(debug=True)
