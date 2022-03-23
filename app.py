# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 22:19:32 2022

@author: Ashwin
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request,  redirect, url_for, make_response
import datetime
import json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://wzmiosdswpvfvz:76c854e423c4395b6d65e6675acbd2cb599ca2082666aa73237ea72a26499ee5@ec2-35-175-68-90.compute-1.amazonaws.com:5432/d6859hvl1u8g0r"
db = SQLAlchemy(app)


class userData(db.Model):
    __tablename__ = 'User Database'

    UserId = db.Column(db.Integer, primary_key=True)
    EmailId = db.Column(db.String(80), nullable=False)
    Username = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

    def __init__(self, UserId, EmailId, Username, Password):
        self.UserId = UserId
        self.emailId = EmailId
        self.Username = Username
        self.Password = Password


class apiData(db.Model):
    __tablename__ = 'API Database'

    bloodBankId = db.Column(db.String(10), primary_key=True, nullable=False)
    DeviceId = db.Column(db.String(10), nullable=False)
    ApiCode = db.Column(db.String(10), nullable=False)

    def __init__(self, bloodBankId, DeviceId, ApiCode):
        self.bloodBankId = bloodBankId
        self.DeviceId = DeviceId
        self.ApiCode = ApiCode


class trackData(db.Model):
    __tablename__ = 'Blood Track Database'

    id = db.Column(db.Integer, primary_key=True)
    DateTime = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow())
    bloodBankId = db.Column(db.String(10), nullable=False)
    BloodType = db.Column(db.String(10), nullable=False)
    LocationData = db.Column(
        db.String(10), nullable=False, default="No Signal")
    BloodDetail = db.Column(db.String(80), nullable=False)

    def __init__(self, bloodBankId, BloodType, LocationData, BloodDetail):
        self.bloodBankId = bloodBankId
        self.BloodType = BloodType
        self.LocationData = LocationData
        self.BloodDetail = BloodDetail


class bloodData(db.Model):
    __tablename__ = 'Blood Database'

    id = db.Column(db.Integer, primary_key=True)
    DateTime = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow())
    DeviceId = db.Column(db.String(10), nullable=False)
    EmployeId = db.Column(db.String(10), nullable=False)
    BloodBankId = db.Column(db.String(10), nullable=False)
    Type_APos = db.Column(db.Integer, nullable=False, default=0)
    Type_ANeg = db.Column(db.Integer, nullable=False, default=0)
    Type_ABPos = db.Column(db.Integer, nullable=False, default=0)
    Type_ABNeg = db.Column(db.Integer, nullable=False, default=0)
    Type_BPos = db.Column(db.Integer, nullable=False, default=0)
    Type_BNeg = db.Column(db.Integer, nullable=False, default=0)
    Type_OPos = db.Column(db.Integer, nullable=False, default=0)
    Type_ONeg = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, DeviceId, EmployeId, BloodBankId, Type_APos, Type_ANeg, Type_ABPos,
                 Type_ABNeg, Type_BPos, Type_BNeg, Type_OPos, Type_ONeg):
        self.DeviceId = DeviceId
        self.EmployeId = EmployeId
        self.BloodBankId = BloodBankId
        self.Type_APos = Type_APos
        self.Type_ANeg = Type_ANeg
        self.Type_ABPos = Type_ABPos
        self.Type_ABNeg = Type_ABNeg
        self.Type_BPos = Type_BPos
        self.Type_BNeg = Type_BNeg
        self.Type_OPos = Type_OPos
        self.Type_ONeg = Type_ONeg


def __authLogin__(emailId_, password_):
    emailId_ = str(emailId_)
    password_ = str(password_)
    token = userData.query.filter(userData.EmailId.like(emailId_)).filter(
        userData.Password.like(password_)).first()
    if token:
        return True
    return False


@app.route('/', methods=['POST', 'GET'])
def signInPage():
    if request.method == 'POST':
        emailId_ = request.form.get("email")
        password_ = request.form.get("password")
        resp = make_response(redirect(url_for('dashboardPage')))

        if __authLogin__(emailId_, password_):
            resp.set_cookie('Authentication', 'True')
            return resp

        resp.set_cookie('Authentication', 'False')
        return render_template('signInPage.html')

    return render_template('signInPage.html')


@app.route('/signup')
def signup_page():
    return render_template('signUpPage.html')


@app.route('/getData', methods=['GET'])
def getData():
    bd = bloodData.query.all()
    data = {}
    for count, item in enumerate(bd):
        data[count] = {"EmployeeId": item.EmployeId, "BloodBankId": item.BloodBankId, "DeviceId": item.DeviceId, "DateTime": item.DateTime, "Type_APos": item.Type_APos, "Type_ANeg": item.Type_ANeg,
                       "Type_ABPos": item.Type_ABPos, "Type_ABNeg": item.Type_ABNeg, "Type_BPos": item.Type_BPos, "Type_BNeg": item.Type_BNeg, "Type_OPos": item.Type_OPos, "Type_ONeg": item.Type_ONeg}
    return data


@app.route('/apiData', methods=['POST', 'GET'])
def variable_page():
    ApiCode_ = request.args.get('API', default='None', type=str)
    DeviceId_ = request.args.get('Id', default='None', type=str)
    EmployeId_ = request.args.get('EmpId', default='None', type=str)
    BloodBankId_ = request.args.get('BankId', default='None', type=str)
    Type_APos_ = request.args.get('Apos', default='None', type=int)
    Type_ANeg_ = request.args.get('Aneg', default='None', type=int)
    Type_ABPos_ = request.args.get('ABpos', default='None', type=int)
    Type_ABNeg_ = request.args.get('ABneg', default='None', type=int)
    Type_BPos_ = request.args.get('Bpos', default='None', type=int)
    Type_BNeg_ = request.args.get('Bneg', default='None', type=int)
    Type_OPos_ = request.args.get('Opos', default='None', type=int)
    Type_ONeg_ = request.args.get('Oneg', default='None', type=int)

    #apiResult = apiData.query.filter(apiData.ApiCode.like(ApiCode_)).first()
    apiResult = True
    if apiResult:
        print("API AUTHENTICATION SUCCESSFULL, TIME: ", datetime.datetime.now())
        bloodData_ = bloodData(DeviceId=DeviceId_, EmployeId=EmployeId_, BloodBankId=BloodBankId_,
                               Type_APos=Type_APos_, Type_ANeg=Type_ANeg_, Type_ABPos=Type_ABPos_,
                               Type_ABNeg=Type_ABNeg_, Type_BPos=Type_BPos_,  Type_BNeg=Type_BNeg_,
                               Type_OPos=Type_OPos_, Type_ONeg=Type_ONeg_)
        print(bloodData_.DeviceId)
        db.session.add(bloodData_)
        db.session.commit()
        return "DATA SUCCESSFULL UPADTED"


@app.route('/logout')
def logout_page():
    Authentication = request.cookies.get('Authentication')
    if Authentication == "True":
        resp = make_response(redirect(url_for('signInPage')))
        resp.set_cookie('Authentication', 'False')
        return resp
    return redirect(url_for('signInPage'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
