from flask import Flask, flash, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = [ 'png', 'jpg', 'jpeg','gif','jfif' ]
app.config['UPLOAD_FOLDER'] = "static\VEHICLE_IMAGES"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = "this_is_my_secret_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///vehicle.db"

db = SQLAlchemy(app)

class vehicle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Name  = db.Column(db.String(50))
    Model = db.Column(db.String(50))
    Transmision = db.Column(db.String(50) )
    Year = db.Column(db.Integer())
    Fuel = db.Column(db.String(50))
    Location = db.Column(db.String(50))
    Engine = db.Column(db.String(50))
    Milage = db.Column(db.Integer())
    Price = db.Column(db.Integer())
    Image1  = db.Column(db.String(75))
    Image2  = db.Column(db.String(75)) 
    Image3  = db.Column(db.String(75))

class Mechant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(50))
    First_Name  = db.Column(db.String(50))
    Last_Name  = db.Column(db.String(50))
    Email  = db.Column(db.String(50))
    Phone_Number = db.Column(db.String(50))
    Car_id = db.Column(db.Integer())

class Images(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Car_id = db.Column(db.Integer)
    Title  = db.Column(db.String(50)) 

def ext_checker(name):
    if "." in name:        
        string = name.split(".")
        ext = string[1]
        if ext in [ 'png', 'jpg', 'jpeg','gif','jfif' ]:
            return True
        else:
            return False
    else:
        return False    

@app.route("/")
def index():
    showroom = vehicle.query.all()
    return render_template("home.html",showroom = showroom)

@app.route("/buy_process",methods = ['POST','GET'])
def buy_process():
    if request.method =='POST':
        Name = request.form['Name'].capitalize()
        Model = request.form['Model'].capitalize()
        Transmission = request.form['Transmission'].capitalize()
        Fuel = request.form['Fuel'].capitalize()
       
        vehicles = vehicle.query.filter_by(Name = Name,Model = Model,Transmision = Transmission,Fuel =Fuel).all()
        db.session.commit()
        
    
    return render_template('buy_vehicle.html',vehicles = vehicles)

@app.route("/More_Details/<string:id>")
def More_Details(id):
    mechant = Mechant.query.filter_by(id=id).first()
    Vehicle = vehicle.query.filter_by(id=id).first()
    return render_template('moredetails.html',mechant = mechant,Vehicle = Vehicle)

@app.route("/ext",methods = ['POST','GET'])
def ext():
    if request.method =='POST':  
        image  = request.files['image']
        img_name = image.filename
        if "." in img_name:        
            string = img_name.split(".")
            ext = string[1]
            if ext in [ 'png', 'jpg', 'jpeg','gif','jfif' ]:
                return "extension allowed"
            else:
                return render_template("error.html")
        else:
            return render_template("error.html")

@app.route("/sell_process",methods = ['POST','GET'])
def sell_process():
    if request.method =='POST':     
        Name = request.form['Name'].capitalize()
        Model = request.form['Model'].capitalize()
        Year = request.form['Year']
        Transmission = request.form['Transmission']
        Fuel = request.form['Fuel'].capitalize()
        Milage =  request.form['Milage']
        Engine = request.form['Engine'].capitalize()
        Location = request.form['Location'].capitalize()
        Price = request.form['Price']
        Title = request.form['Title'].capitalize()
        First_Name = request.form['First_Name'].capitalize()
        Last_Name = request.form['Last_Name'].capitalize()
        Email = request.form['Email']
        Phone_Number = request.form['Phone_Number']

        if request.files:
            image1  = request.files['image-1']
            image2  = request.files['image-2']
            image3  = request.files['image-3']  

            print(image1.filename)
            if not ext_checker(image1.filename) and not ext_checker(image2.filename) and not ext_checker(image3.filename):
                return render_template("error.html")
            else:
                imagename1 =  secure_filename(image1.filename)
                imagename2 =  secure_filename(image2.filename)
                imagename3 = secure_filename(image3.filename)
                image1.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename1))
                image2.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename2))
                image3.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename3))

                Vehicle = vehicle(Name = Name,Model = Model,Transmision = Transmission,
                Year = Year,Fuel = Fuel,Milage = Milage,Engine = Engine,Location = Location,
                Price = Price,Image1 = "/static/VEHICLE_IMAGES/" +imagename1,Image2 = "/static/VEHICLE_IMAGES/" +imagename2,
                Image3 = "/static/VEHICLE_IMAGES/" +imagename3)   
        
                db.session.add(Vehicle)
                vz = vehicle.query.filter_by(Name = Name,Model = Model,Transmision = Transmission,Year = Year,Fuel = Fuel,Milage = Milage,Engine = Engine,Location = Location,Price = Price).first()
                mechant = Mechant(Title = Title,First_Name = First_Name,Last_Name  = Last_Name,Email = Email,Phone_Number = Phone_Number,Car_id = vz.id)
                image_1 = Images(Car_id = vz.id, Title = imagename1)
                image_2 = Images(Car_id = vz.id, Title = imagename2)
                image_3 = Images(Car_id = vz.id, Title = imagename3)
                db.session.add(image_1)
                db.session.add(image_2)
                db.session.add(image_3)
                db.session.add(mechant)
                db.session.commit()
       
    return index()

@app.route("/search",methods = ['POST','GET'])
def search():
    if request.method =='POST':     
        Search = request.form['search'].capitalize()
        search_vehicle1 = vehicle.query.filter_by(Name = Search).all()
        search_vehicle2 = vehicle.query.filter_by(Model = Search).all()
        search_vehicle3 = vehicle.query.filter_by(Transmision = Search).all()
        search_vehicle4 = vehicle.query.filter_by(Fuel =Search).all()
    return render_template("search.html", sv1 = search_vehicle1, sv2 = search_vehicle2, 
    sv3 = search_vehicle3, sv4 = search_vehicle4)

@app.route("/buy")
def buy():
    return render_template("buy.html")

@app.route("/carlot/<int:num>")
def carlot(num):
    carlot = vehicle.query.paginate(per_page = 5, page = num, error_out = True)
    return render_template("carlot.html",carlot = carlot )

@app.route("/sell")
def sell():
    return render_template("sell.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

if __name__ == '__main__':

    app.run(debug = True,host = '0.0.0.0')
