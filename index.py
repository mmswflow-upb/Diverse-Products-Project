from flask import Flask,redirect,render_template,url_for,request,flash,session
import mysql.connector
from datetime import datetime
from datetime import timedelta
import os
from werkzeug.utils import secure_filename

db = mysql.connector.connect(#Defining the connection with our data base

    host = "127.0.0.1",
    port = "3306",
    user = "root",
    password = "root",
    database = "DiverseProductsDB")

cursor = db.cursor()#used to execute commands on our database 


app = Flask(__name__)#Our flask web application instance
app.permanent_session_lifetime = timedelta(days = 1)#Setting the lifetime of cookies
app.secret_key = "magusproducts"#Secret key necessary for flash messaging

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
uploadDirectory = os.path.join(APP_ROOT, 'static', 'images')

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = uploadDirectory

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/marketplace", methods = ["POST", "GET"])
def marketplace():

    if request.method == "POST":

        user = session["user"]

        if "logOut" in request.form:

            return redirect (url_for("logOut"))

        elif "pdb" in request.form:

            return redirect (url_for("productManagement"))

        elif "deleteAccount" in request.form:

            return redirect(url_for("deleteAccount"))

        elif "dbl" in request.form:

            return redirect (url_for("dataBaseLogs"))

        elif "searchButton" in request.form:

            no_results = 0#Number of results.
            searchInput = request.form.get("searchProduct")
            
            op = request.form.get("filterOption")

            if op == "All":

                    cursor.execute(f"SELECT username,address FROM associates WHERE username LIKE '%{searchInput}%' || address LIKE '%{searchInput}%';")
                    users = cursor.fetchall()
                    
                    if users:

                        data = []

                        for usr in users:#[names,..]

                            data2 = []

                            cursor.execute(f"SELECT prod_name,prod_price,prod_image FROM products_{usr[0]} WHERE prod_name LIKE '%{searchInput}%';")
                            data3 = cursor.fetchall()

                            if data3:#Products and user exists

                                no_results = no_results + len(data3)
                                data2.append(data3)
                                data2.append(usr)
                                data.append(data2)

                                #Users(DATA): [ #Usertable(DATA2): [ [#Products(DATA3): [] ] ,[user,address] ]
                        data.sort()
                        flash(f"Logged In As '{user}'.")
                        flash(f"{no_results} Results For '{searchInput}':",'info')
                        return render_template("marketplace.html",users = data)

                    flash(f"Logged In As '{user}'.")
                    flash(f"No Products Available.",'info')
                    return render_template("marketplace.html")

            elif op == "Product Name":    

                    cursor.execute(f"SELECT username,address FROM associates;")
                    users = cursor.fetchall()
                    
                    if users:

                        data = []

                        for usr in users:#[names,..]

                            data2 = []

                            cursor.execute(f"SELECT prod_name,prod_price,prod_image FROM products_{usr[0]} WHERE prod_name LIKE '%{searchInput}%';")
                            data3 = cursor.fetchall()

                            if data3:#Products and user exists

                                no_results = no_results + len(data3)#Adding number of new products
                                data2.append(data3)
                                data2.append(usr)
                                data.append(data2)

                                #Users(DATA): [ #Usertable(DATA2): [ [#Products(DATA3): [] ] ,[user,address] ]
                        data.sort()
                        flash(f"Logged In As '{user}'.")
                        flash(f"{no_results} Results For '{searchInput}' Products:",'info')
                        return render_template("marketplace.html",users = data, productSelect = 'selected')

                    flash(f"Logged In As '{user}'.")
                    flash(f"No Products Available.",'info')
                    return render_template("marketplace.html")

            elif op == "Store Name":

                    cursor.execute(f"SELECT username,address FROM associates WHERE username LIKE '%{searchInput}%';")
                    users = cursor.fetchall()
                    
                    if users:

                        data = []

                        for usr in users:#[names,..]

                            data2 = []

                            cursor.execute(f"SELECT prod_name,prod_price,prod_image FROM products_{usr[0]};")
                            data3 = cursor.fetchall()

                            if data3:#Products and user exists

                                no_results = no_results + len(data3)
                                data2.append(data3)
                                data2.append(usr)
                                data.append(data2)

                                #Users(DATA): [ #Usertable(DATA2): [ [#Products(DATA3): [] ] ,[user,address] ]

                        flash(f"Logged In As '{user}'.")
                        flash(f"{no_results} Results For Store/User '{searchInput}':",'info')
                        return render_template("marketplace.html",users = data,creatorSelect = 'selected')

                    flash(f"Logged In As '{user}'.")
                    flash(f"No Products Available.",'info')
                    return render_template("marketplace.html")

            elif op == "Store Location":

                    cursor.execute(f"SELECT username,address FROM associates WHERE address LIKE '%{searchInput}%';")
                    users = cursor.fetchall()
                    
                    if users:

                        data = []

                        for usr in users:#[names,..]

                            data2 = []

                            cursor.execute(f"SELECT prod_name,prod_price,prod_image FROM products_{usr[0]};")
                            data3 = cursor.fetchall()

                            if data3:#Products and user exists

                                no_results = no_results + len(data3)
                                data2.append(data3)
                                data2.append(usr)
                                data.append(data2)

                                #Users(DATA): [ #Usertable(DATA2): [ [#Products(DATA3): [] ] ,[user,address] ]

                        flash(f"Logged In As '{user}'.")
                        flash(f"{no_results} Results For Location '{searchInput}':",'info')
                        return render_template("marketplace.html",users = data,locationSelect = 'selected')

                    flash(f"Logged In As '{user}'.")
                    flash(f"No Products Available.",'info')
                    return render_template("marketplace.html")

    else: #GET HTTP METHOD

        if "user" in session:

            no_results = 0

            session["currentSearch"] = ""

            user = session["user"]

            cursor.execute("SELECT username,address FROM associates;")
            users = cursor.fetchall()
            
            if users:

                data = []

                for usr in users:#[names,..]

                    data2 = []

                    cursor.execute(f"SELECT prod_name,prod_price,prod_image FROM products_{usr[0]};")
                    data3 = cursor.fetchall()

                    if data3:#Products and user exists

                        no_results = no_results + len(data3)
                        data2.append(data3)
                        data2.append(usr)
                        data.append(data2)

                        #Users(DATA): [ #Usertable(DATA2): [ [#Products(DATA3): [] ] ,[user,address] ]
                
                data.sort()
                flash(f"Logged In As '{user}'.")
                flash(f"{no_results} Available Products:",'info')
                return render_template("marketplace.html",users = data)

            flash(f"Logged In As '{user}'.")
            flash(f"No Products Available.",'info')
            return render_template("marketplace.html")

        else:
            flash("You cannot access the marketplace, log into your account first.")
            return redirect(url_for("loginPage"))


@app.route("/dataBaseLogs", methods = ["POST","GET"])
def dataBaseLogs():

    if request.method == "POST":

        user = session["user"]
        filterOption = request.form.get("filterOption")
        
        if "logOut" in request.form:

            return redirect (url_for("logOut"))

        elif "pdb" in request.form:

            return redirect (url_for("productManagement"))

        elif "deleteAccount" in request.form:

            return redirect(url_for("deleteAccount"))

        elif "marketplace" in request.form:

            return redirect(url_for("marketplace"))

        searchLog = request.form.get(" searchLog")

        if filterOption == "View All Logs":
            
            if "clearLogs" in request.form:

                session["currentSearch"] = ""

                cursor.execute(f"DELETE FROM logs_{user};")
                db.commit()
                flash(f"Logged In As '{user}'.")
                flash("WARNING: ALL LOGS HAVE BEEN ERASED.",'warning')
                return render_template("dataBaseLogs.html")

            elif "search" in request.form:#We don't need to apply any filters here.So we will actually search for both products and 
                                          #Operations.

                session["currentSearch"] = searchLog

                cursor.execute(f"SELECT * FROM logs_{user} WHERE product LIKE '%{searchLog}%' || command LIKE '%{searchLog}%';")
                flash(f"Logged In As '{user}'.")
                flash(f"Results of '{searchLog}':",'info')
                return render_template("dataBaseLogs.html",logs = cursor.fetchall())

        elif filterOption == "Specific Product":


            if "clearLogs" in request.form:
                
                searchLog = session["currentSearch"]

                cursor.execute(f"DELETE FROM logs_{user} WHERE product LIKE '%{searchLog}%';")
                db.commit()
                cursor.execute(f"SELECT * FROM logs_{user};")

                session["currentSearch"] = ""

                flash(f"Logged In As '{user}'.")
                flash(f"WARNING: ALL LOGS OF USER '{searchLog}' HAVE BEEN ERASED.",'warning')

                return render_template("dataBaseLogs.html",logs = cursor.fetchall(),selectedProduct = "selected")

            elif "search" in request.form:

                session["currentSearch"] = searchLog

                cursor.execute(f"SELECT * FROM logs_{user} WHERE product LIKE '%{searchLog}%';")
                flash(f"Logged In As '{user}'.")
                flash(f"Results for user '{searchLog}':",'info')

                return render_template("dataBaseLogs.html",logs = cursor.fetchall(),selectedProduct = "selected")

        elif filterOption == "Specific Command":

            if "clearLogs" in request.form:
                
                searchLog = session["currentSearch"]

                cursor.execute(f"DELETE FROM logs_{user} WHERE command LIKE '%{searchLog}%';")
                db.commit()
                cursor.execute(f"SELECT * FROM logs_{user};")

                flash(f"Logged In As '{user}'.")
                flash(f"WARNING: DELETED '{searchLog}' LOGS.",'warning')

                session["currentSearch"] = ""

                return render_template("dataBaseLogs.html", logs = cursor.fetchall(),selectedCommand= "selected")

            elif "search" in request.form:

                session["currentSearch"] = searchLog

                cursor.execute(f"SELECT * FROM logs_{user} WHERE command LIKE '%{searchLog}%';")
                flash(f"Logged In As '{user}'.")
                flash(f"Results for command: '{searchLog}'.",'info')
                return render_template("dataBaseLogs.html",logs = cursor.fetchall(),selectedCommand= "selected")
        
    else:#Get request

        if "user" in session:

            session["currentSearch"] = ""

            user = session["user"]
            cursor.execute(f"SELECT * FROM logs_{user};")

            flash(f"Logged In As '{user}'.")

            return render_template("dataBaseLogs.html",logs = cursor.fetchall())

        else:
            flash("You cannot access the data base logs, log into your account first.")
            return redirect(url_for("loginPage"))

@app.route("/productManagement", methods = ["POST","GET"])#Defining the product management page, we also use here 2 methods, GET for 
                                                          #loading the page and we're not trying to execute some commands.
                                                          #POST is for executing commands such as: redirection, logging out, searching, deleting, etc..
def productManagement():

    if request.method == "POST":

        now = datetime.now()
        date_time = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

        user = session["user"]
        no_results = session["no_results"]

        if "back" in request.form:

            if session["currentCompleteResult"]:
                
                if len(session["currentCompleteResult"]) >= 1:

                    if session["currentPage"] > 1:

                        session["currentPage"] = session["currentPage"]  -1
                        currentPage = session["currentPage"]

                        session["currentProduct"] = session["currentCompleteResult"][currentPage-1]
                        currentProduct = session["currentProduct"]
                        currentSearch = session["currentSearch"]

                        flash(f"Logged In As '{user}'.")
                        flash(f"{no_results} Results For: '{currentSearch}':",'info')

                        return render_template("productManagement.html", page = currentPage, prod_no = currentProduct[0],
                        prod_name = currentProduct[1],prod_price = currentProduct[2], 
                        prod_inStock = currentProduct[3], prod_image = currentProduct[4])

                    currentSearch = session["currentSearch"]
                    currentProduct = session["currentProduct"]

                    flash(f"Logged In As '{user}'.")
                    flash(f"{no_results} Results For: '{currentSearch}':",'info')

                    return render_template("productManagement.html", page = "1", prod_no = currentProduct[0],
                    prod_name = currentProduct[1],prod_price = currentProduct[2], 
                    prod_inStock = currentProduct[3], prod_image = currentProduct[4])

            flash(f"Logged In As '{user}'.")
            flash("No Results.",'info')
            return render_template("productManagement.html",page = "0")
            
        elif "next" in request.form:

            if session["currentCompleteResult"]:
                
                if len(session["currentCompleteResult"]) > session["currentPage"]:

                        session["currentPage"] = session["currentPage"] +1
                        currentPage = session["currentPage"] 

                        session["currentProduct"] = session["currentCompleteResult"][currentPage-1]
                        currentProduct = session["currentProduct"]
                        currentSearch = session["currentSearch"]

                        flash(f"Logged in as '{user}'.")
                        flash(f"{no_results} Results For: '{currentSearch}':",'info')

                        return render_template("productManagement.html", page = currentPage, prod_no = currentProduct[0],
                        prod_name = currentProduct[1],prod_price = currentProduct[2], 
                        prod_inStock = currentProduct[3], prod_image = currentProduct[4])

                if session["currentProduct"]:

                    currentSearch = session["currentSearch"]
                    currentProduct = session["currentProduct"]
                    currentPage = session["currentPage"]

                    flash(f"Logged In As '{user}'.")
                    flash(f"{no_results} Results For: '{currentSearch}':",'info')

                    return render_template("productManagement.html", page = currentPage, prod_no = currentProduct[0],
                    prod_name = currentProduct[1],prod_price = currentProduct[2], 
                    prod_inStock = currentProduct[3], prod_image = currentProduct[4])
            
            flash(f"Logged In As '{user}'.")
            flash("No Results.",'info')
            return render_template("productManagement.html",page = "0")

        session["currentCompleteResult"] = []
        session["currentPage"] = 0
        session["currentProduct"] = []
        session["currentSearch"] = ""
        session["no_results"] = 0

        if "logOut" in request.form:

            return redirect (url_for("logOut"))

        elif "dbl" in request.form:
        
            return redirect (url_for("dataBaseLogs"))

        elif "deleteAccount" in request.form:

            return redirect(url_for("deleteAccount"))

        elif "marketplace" in request.form:
            
            return redirect(url_for("marketplace"))

        elif "search" in request.form:

            prod_nm = request.form["searchProduct"]

            cursor.execute(f"SELECT * FROM products_{user} WHERE prod_name LIKE '%{prod_nm}%';")
            data = cursor.fetchall()
           
            if data:

                no_results = len(data)

                for d in data:

                    cursor.execute(f"INSERT INTO logs_{user} VALUES('SEARCH', '{d[1]}','{date_time}');")
                    db.commit()

                flash(f"Logged In As '{user}'.")
                flash(f"{no_results} Results For: '{prod_nm}':",'info')
            
                session["currentCompleteResult"] = data
                session["currentPage"] = 1
                session["currentProduct"] = data[0]
                session["currentSearch"] = prod_nm
                session["no_results"] = no_results

                return render_template("productManagement.html",page = "1",
                prod_no = data[0][0],
                prod_name = data[0][1],
                prod_price = data[0][2],
                prod_inStock = data[0][3],
                prod_image = data[0][4])

            else:

                flash(f"Logged In As '{user}'.")
                flash(f"ERROR: '{prod_nm}' NOT FOUND!",'error')
                return render_template("productManagement.html",page = 0)

        elif "updateProduct" in request.form:

            rf = request.form
            updt = [rf.get("productNO"),rf.get("productName"),rf.get("productPrice"),rf.get("productStock"),request.files.get("productImage")]

            if not updt[0]:

                flash(f"Logged In As '{user}'.")
                flash("ERROR: NO PRODUCT SELECTED TO UPDATE!",'error')
                return render_template("productManagement.html",page = 0)

            cursor.execute(f"SELECT prod_name FROM products_{user} WHERE prod_no = {updt[0]};")
            oldProdName = cursor.fetchone()[0]

            if  updt[1]:#Check if the name should be updated:

                cursor.execute(f"SELECT * FROM products_{user} WHERE prod_name = '{updt[1]}' AND prod_no <> {updt[0]};")
                dup = cursor.fetchone()

                if dup:

                    flash(f"Logged In As '{user}'.")
                    flash(f"ERROR: DUPLICATE NAMES!",'error')
                    return render_template("productManagement.html", page = 0)
                
                cursor.execute(f"INSERT INTO logs_{user} VALUES('UPDATE PROD_NAME','{updt[1]}','{date_time}');")
                db.commit()
                cursor.execute(f"UPDATE products_{user} SET prod_name = '{updt[1]}' WHERE prod_no = {updt[0]};")
                db.commit()

            if updt[2]:
                
                    cursor.execute(f"INSERT INTO logs_{user} VALUES('UPDATE PROD_PRICE','{updt[1]}','{date_time}');")
                    db.commit()
                    cursor.execute(f"UPDATE products_{user} SET prod_price = '{updt[2]}' WHERE prod_no = {updt[0]};")
                    db.commit()

            if updt[3]:

                cursor.execute(f"INSERT INTO logs_{user} VALUES('UPDATE PROD_STOCK','{updt[1]}','{date_time}');")
                db.commit()
                cursor.execute(f"UPDATE products_{user} SET prod_instock = '{updt[3]}' WHERE prod_no = {updt[0]};")
                db.commit()

            file = updt[4]

            if file:

                if file.filename == "":

                    flash("ERROR: IMAGE NAME INVALID!",'error')
                    flash(f"'Logged In As {user}'.")
                    return render_template("productManagement.html", page = 0)

                cursor.execute(f"SELECT prod_image FROM products_{user} WHERE prod_no = {updt[0]};")#Getting the name of the image, (we do this to get the extension too)
                imgName = cursor.fetchone()[0]

                if file and allowed_file(file.filename):

                    os.remove(os.path.join(app.config["UPLOAD_FOLDER"],imgName))#Removing the old picture.

                    filename = secure_filename(file.filename)#Adding the new picture.
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))

                    updt[4] = filename#Re-adding the file name into the list.

                    cursor.execute(f"SELECT prod_name FROM products_{user} WHERE prod_no = {updt[0]};")

                    prod_nm = cursor.fetchone()[0]
                
                    cursor.execute(f"INSERT INTO logs_{user} VALUES('UPDATE PROD_IMAGE', '{prod_nm}','{date_time}');")
                    db.commit()
                    cursor.execute(f"UPDATE products_{user} SET prod_image = '{updt[4]}' WHERE prod_no = {updt[0]};")
                    db.commit()

                    lastIndex = updt[0]
                        
                    ext = os.path.splitext(filename)[1]
                    updt[4] = f"{user}_{lastIndex}{ext}"
                    os.rename(os.path.join(app.config["UPLOAD_FOLDER"],filename),updt[4])
                    os.replace(updt[4], os.path.join(app.config["UPLOAD_FOLDER"],updt[4]))

                    cursor.execute(f"UPDATE products_{user} SET prod_image = '{updt[4]}' WHERE prod_no = {lastIndex};")#Updating the image name in the database
                    db.commit()

                    session["currentCompleteResult"] = [updt]
                    session["currentPage"] = 1
                    session["currentProduct"] = updt
                    session["currentSearch"] = updt[1]
                else:

                    flash("ERROR: UNAPPROVED FILE EXTENSION",'error')
                    flash(f"Logged In As {user}.")
                    return render_template("productManagement.html",page = 0)

            
            flash(f"Logged In As '{user}'.")
            flash(f"WARNING: UPDATED DATA OF '{oldProdName}':",'warning')

            cursor.execute(f"SELECT * FROM products_{user} WHERE prod_no = {updt[0]};")
            updt = cursor.fetchone()

            return render_template("productManagement.html",page = 1,prod_no = updt[0],
            prod_name = updt[1],
            prod_price = updt[2],
            prod_inStock = updt[3],
            prod_image = updt[4])

        elif "addProduct" in request.form:#Adding a new product, prod_no is not an indetifier, the name is.

            rf = request.form
            new = [rf.get("productName"),rf.get("productPrice"),rf.get("productStock"), request.files["productImage"]]

            cursor.execute(f"SELECT * FROM products_{user} WHERE prod_name = '{new[0]}';")
            dup = cursor.fetchone()

            if dup:

                flash(f"Logged In As '{user}'.")
                flash(f"ERROR: DUPLICATE NAMES!",'error')
                return render_template("productManagement.html", page = 0)

            if (not new[0]) or (not new[1]) or (not new[2]):

                flash(f"Logged In As '{user}'.")
                flash(f"ERROR: INSERTED INVALID DATA",'error')
                return render_template("productManagement.html" , page = 0)

            if "productImage" in request.files:

                file = request.files["productImage"]

                if file.filename == "":

                    flash("ERROR: IMAGE NAME INVALID!",'error')
                    flash(f"Logged In As {user}.")
                    return render_template("productManagement.html", page = 0)

                if file and allowed_file(file.filename):

                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"] ,filename))
                    
                    new[3] = filename 

                    cursor.execute(f"INSERT INTO logs_{user} VALUES('CREATE','{new[0]}','{date_time}');")
                    db.commit()
                    cursor.execute(f"INSERT INTO products_{user}(prod_name,prod_price,prod_instock,prod_image) VALUES('{new[0]}','{new[1]}','{new[2]}','{new[3]}');")
                    db.commit()

                    lastIndex = cursor.lastrowid
                    
                    ext = os.path.splitext(filename)[1]
                    new[3] = f"{user}_{lastIndex}{ext}"
                    os.rename(os.path.join(app.config["UPLOAD_FOLDER"],filename),new[3])
                    os.replace(new[3], os.path.join(app.config["UPLOAD_FOLDER"],new[3]))

                    cursor.execute(f"UPDATE products_{user} SET prod_image = '{new[3]}' WHERE prod_no = {lastIndex};")
                    db.commit()

                    new2 = [lastIndex, new[0], new[1] , new[2], new[3]]

                    session["currentCompleteResult"] = [new2]
                    session["currentPage"] = 1
                    session["currentProduct"] = new2
                    session["currentSearch"] = new2[1]

                    flash(f"Logged In As '{user}'.")
                    flash(f"Success: Added '{new[0]}':",'info')

                    return render_template("productManagement.html",page = 1,prod_no = lastIndex,prod_name = new[0],
                    prod_price = new[1],
                    prod_inStock = new[2],
                    prod_image = new[3]
                    )
                
                flash("ERROR: UNAPPROVED FILE EXTENSION",'error')
                flash(f"Logged In As {user}.")
                return render_template("productManagement.html",page = 0)
                
            
            flash("ERROR: NO SELECTED IMAGE!",'error')
            flash(f"Logged In As {user}.")
            return render_template("productManagement.html",page = 0)

        elif "deleteProduct" in request.form:

            prod_nm = request.form["productName"]

            if not prod_nm:

                flash(f"Logged In As '{user}'.")
                flash(f"ERROR: NO SELECTED PRODUCT TO DELETE!",'error')
                return render_template("productManagement.html", page = 0)

            prodNO = request.form.get("productNO")

            cursor.execute(f"SELECT prod_image FROM products_{user} WHERE prod_no = {prodNO};")

            prodImgName = cursor.fetchone()[0]

            os.remove(os.path.join(app.config["UPLOAD_FOLDER"],prodImgName))

            cursor.execute(f"INSERT INTO logs_{user} VALUES('DELETE','{prod_nm}','{date_time}');")
            db.commit()
            cursor.execute(f"DELETE FROM products_{user} WHERE prod_name = '{prod_nm}';")
            db.commit()

            lastIndex = cursor.lastrowid 

            if lastIndex <= 1:
                lastIndex = 2
                    
            cursor.execute(f"ALTER TABLE products_{user} AUTO_INCREMENT = {lastIndex - 1};")

            flash(f"Logged In As '{user}'.")
            flash(f"WARNING: '{prod_nm}' Data Deleted!",'warning')
            return render_template("productManagement.html", page = 0)
            
        elif "deleteAll" in request.form:#Deleting all products.

                deleteImages()

                cursor.execute(f"INSERT INTO logs_{user} VALUES('DELETE','ALL PRODUCTS','{date_time}');")
                db.commit()
                cursor.execute(f"DELETE FROM products_{user};")
                db.commit()
                cursor.execute(f"ALTER TABLE products_{user} AUTO_INCREMENT = 1;")
                db.commit()

                flash(f"Logged In As '{user}'.")
                flash("WARNING: DELETED ALL PRODUCTS!",'warning')

                return render_template("productManagement.html", page = 0)
    else:#Get request

        if "user" in session:

            session["currentCompleteResult"] = []
            session["currentProduct"] = []
            session["currentPage"] = 0
            session["currentSearch"] = ""
            session["no_results"] = 0

            user = session["user"]
            flash(f"Logged In As '{user}'.")
            flash("No Results.",'info')
            return render_template("productManagement.html", page = 0)
            
        else:
            flash("You cannot access the products data base, log into your account first.")
            return redirect(url_for("loginPage"))

def deleteImages():

    user = session["user"]

    cursor.execute(f"SELECT prod_image FROM products_{user};")
    data = cursor.fetchall()

    if data:

        print(data)

        for imgName in data:

            os.remove(os.path.join(app.config["UPLOAD_FOLDER"],imgName[0]))

@app.route("/deleteAccount")
def deleteAccount():

    session["currentCompleteResult"] = []
    session["currentPage"] = 0
    session["currentProduct"] = []
    session["currentSearch"] = ""
    session["no_results"] = 0

    deleteImages()

    user = session["user"]

    cursor.execute(f"DROP TABLE products_{user};")
    cursor.execute(f"DROP TABLE logs_{user};")
    cursor.execute(f"DELETE FROM associates WHERE username = '{user}';")
    db.commit()

    session.permanent = False
    session.pop("user", None)

    flash(f"WARNING: ACCOUNT DELETED!")
    flash(f"WARNING: LOGGED OUT FROM '{user}'!")

    return redirect (url_for("loginPage"))

@app.route("/logout")
def logOut():

    session["currentCompleteResult"] = []
    session["currentPage"] = 0
    session["currentProduct"] = []
    session["currentSearch"] = ""

    session.permanent = False
    user = session["user"]
    session.pop("user", None)
    flash(f"WARNING: LOGGED OUT FROM '{user}'!")
    return redirect (url_for("loginPage"))

@app.route("/signUp", methods = ["POST","GET"])
def signUp():

    if request.method == "POST":#POST METHOD

        if "logIn" in request.form:

            return redirect(url_for("loginPage"))

        elif "submit" in request.form:

            newUser = request.form.get("newUsername")
            newPass = request.form.get("newPassword")
            confPass = request.form.get("confirmPassword")
            newEmail = request.form.get("email")
            newAddress = request.form.get("address")

            cursor.execute(f"SELECT * FROM associates WHERE username = '{newUser}';")

            data = cursor.fetchone()

            if newUser.find(' ') >= 0:

                flash("ERROR: USERNAME CANNOT CONTAIN SPACE!")
                flash("Create a new account to manage your own database.")
                return render_template("signUp.html")

            if data:#We check if the username is already in-use

                flash("ERROR: USERNAME ALREADY USED!")
                flash("Create a new account to manage your own database.")
                return render_template("signUp.html")

            if newPass == confPass:

                cursor.execute(f"INSERT INTO associates VALUES('{newUser}','{newPass}','{newEmail}','{newAddress}');")
                db.commit()
                cursor.execute(f"CREATE TABLE products_{newUser}(prod_no int PRIMARY KEY AUTO_INCREMENT, prod_name varchar(60), prod_price float, prod_instock int, prod_image varchar(400));")
                db.commit()
                cursor.execute(f"CREATE TABLE logs_{newUser}(command varchar(20), product varchar(60), dateTime datetime);")
                flash("Success: Account created successfully!")
                return redirect(url_for("loginPage"))

            flash("ERROR: PASSWORDS NOT MATCHING!")
            flash("Create a new account to manage your own database.")
            return render_template("signUp.html")

    else:#GET METHOD

        if "user" in session:
            return redirect (url_for("loginPage"))
        else:
            flash("Create a new account to manage your own database.")
            return render_template("signUp.html")

@app.route("/loginPage",methods = ["POST","GET"])#Defining the login page with 2 http methods: POST for loggin into accounts and GET for loading the page 
                                                 #when we access it from a different one and we haven't logged in yet.
def loginPage():

    if request.method == "POST":#The method is post, so we verify the credentials: 

        if "signUp" in request.form:#If user wants to access the sign up page.

            return redirect(url_for("signUp"))

        adminUser = request.form["associateUsername"]
        adminPassword = request.form["associatePassword"]

        cursor.execute(f"SELECT password FROM associates WHERE username = '{adminUser}';")
        passSearch = cursor.fetchone()
        
        if passSearch:#IF the username was found in the database we continue with verifying the password
          
            if adminPassword == passSearch[0]:#password was also found so it is correct.
                
                rem = request.form.get("rememberMe")#we get the value of "remember me" checkbox 

                if rem == "on":#Save cookie for 1 day if checkbox is on
                    session.permanent = True

                session["user"] = adminUser
                return redirect(url_for("productManagement"))#By Default we will redirect the newly logged in user into products management

            else:#password was incorrect so we alert the person trying to log in.
              
                flash("ERROR: INVALID PASSWORD!")
                return render_template("index.html")

        else:#username was incorrect so we alret the client
       
            flash("ERROR: INVALID USERNAME!")
            return render_template("index.html")

    else:#Get Request, We're not logged in or trying to do so, we're just loading the page
        if "user" in session:

            return redirect (url_for("productManagement"))

        else:
            flash("Use this page to log in into your admin account and get access to your own products' database.")
            return render_template(template_name_or_list="index.html")

if __name__ == "__main__" :#Running the web application
    app.run()
