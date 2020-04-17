#forms.py
#import the forms library
from flask_wtf import FlaskForm
from wtforms import (StringField,BooleanField,DateTimeField,
                    RadioField,SelectField,TextField,TextAreaField,
                    SubmitField, PasswordField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#import the  validators that will be required to build the application
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

class SafetyQuestionnaireForm(FlaskForm):
    #create the forms details
    kid_name = StringField('Please enter your name.',validators=[DataRequired()])

    difficulty_bed = RadioField('Do you think your grandparents have difficulty in getting out of bed?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    adequate_sunlight = SelectField('Where do you think the house where your grandparents lived have adequate sunlight getting through?',
                        choices=[('Stairs','Stairs'),('Bathroom','Bathroom'),('Kitchen','Bedroom'),('Others','Others')], validators=[DataRequired()])

    floor_hazard = RadioField('Do you think there always have some hazards on the floor at home?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    towel_rails = SelectField('Do your grandparents tend to hold on taps or towel rails when getting in or out of the bath or shower?',
                        choices=[('Taps','Taps'),('Tower Rails','Tower Rails'),('Wall','Wall')], validators=[DataRequired()])

    unsteady_standing = RadioField('Did your grandparents mention about the unsteady standing when they take a bath?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    water_presence = SelectField('Where do you think there is always water in your grandparents’ home?',
                        choices=[('Bathroom','Bathroom'),('Kitchen','Kitchen'),('Garden','Garden')], validators=[DataRequired()])

    bench_height = SelectField('What do you think the height of bench or counter is not at a comfortable for your grandparents?',
                        choices=[('Too High','Too High'),('Too Low','Too Low'),('Suitable','Suitable')], validators=[DataRequired()])

    kitchen_reach = RadioField('Do you think your grandparents can always reach things easily in kitchen?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    slip_products = SelectField('What slip products you think are there? Are there  any rugs and mats throughout your grandparent''s house?',
                        choices=[('Rugs','Rugs'),('Mats','Mats'),('Blankets','Blankets')], validators=[DataRequired()])

    electrical_cords = RadioField('Is there any electrical cords running across walkways in your grandparents house?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    stairs_edge = RadioField('Do you think the edge of stairs are clear in your grandparents’ house?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    stairs_handrails = RadioField('Is there any handrails for stairs and steps in your grandparents’ house?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    path_checked = RadioField('	Do you think the paths around your grandparents’ house are cracked?',
                    choices =[('Yes','Yes'),('No','No')],validators=[DataRequired()])

    submit = SubmitField('Submit Safety Assesment Questonnaire')

#form for deleting the data from the safety questionnaire table
class DeleteFromSafety(FlaskForm):
    submit = SubmitField('Clear all the data in the table')


#create a login form for the system administrator to login and perform CRUD operation son the database
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

#add the registration form for the user
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists!')

class DisasterForm(FlaskForm):
    council_name = SelectField('Select Some Area',validators=[DataRequired()])
    submit = SubmitField('Submit')
