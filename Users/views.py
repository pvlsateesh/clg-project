

from os import system
import os
from flask import Blueprint, app, flash, redirect, render_template, request, session, url_for

from Users.model import UserRegistrationModel,db
from .dataProcesing import prediction_image


userViews=Blueprint('userViews',__name__)

@userViews.route('/userRegister',methods=['POST',"GET"])
def userRegister():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        locality = request.form['locality']
        state = request.form['state']
        try:
            # Creating a new entry for user registration
            userreg = UserRegistrationModel(
                name=name,
                email=email,
                loginid=username,
                password=password,  # Consider hashing the password for security
                mobile=mobile,
                locality=locality,
                state=state
            )

            # Adding the entry to the database
            db.session.add(userreg)
            db.session.commit()

            flash('Registration successful!', 'success')
            return render_template('register.html')
        except:
            pass
            flash('inavalid details ', 'fail to store data ')
            return render_template('register.html')
        
    else:
        flash('inavalid details ', 'fail to store data ')
        return render_template('register.html')
    
@userViews.route('/userLoginCheck' ,methods=["POST","GET"])
def userLoginCheck():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']

        print(username+password)
        try:

            ulc=UserRegistrationModel.query.filter_by(loginid=username,password=password).first()

            print(ulc.name)
            if ulc.status=='activated':
                return render_template('users/userHome.html')
            else:
                flash('status not activated details ')
                return render_template('login.html')
        except Exception as e:
            flash('Invalid creadiatial details ')
            return render_template('login.html')

    

    

        
@userViews.route('/userHome')
def userHome():
    return render_template('users/userHome.html')

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'  # Ensure this directory exists
OUTPUT_FOLDER = 'static/output'  # Ensure this directory exists

@userViews.route('/prediction', methods=['POST', 'GET'])
def prediction():
    if request.method == 'POST' and 'image' in request.files:
        image_file = request.files['image']
        if image_file:
            # Save uploaded image temporarily
            filename = secure_filename(image_file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(input_path)

            # Perform prediction (replace with your model prediction logic)
            annotated_image = prediction_image(input_path)  # This should return the output image path
            print(f"Annotated image saved at: {annotated_image}")

            # Convert the full path to relative path for use in the template
            relative_output_path = annotated_image.replace("static/", "")  # Remove 'static/' prefix
            print(f"Relative path for template: {relative_output_path}")

            return render_template('users/prediction.html', image_path=relative_output_path)

    else:
        flash('Invalid file type. Please upload an image.')
        return render_template('users/prediction.html', predd="Invalid file type.")

    return render_template('users/prediction.html', predd=None)

      