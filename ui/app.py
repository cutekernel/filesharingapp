from flask import Flask, request, jsonify, render_template, request, render_template, session, redirect
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import os

#  chnage the mariadb:3306 to your IP for example 127.0.0.1:3306
MARIADB_URL = os.environ.get("MARIADB_URL", "mariadb:3306")

#change the username and password to yours
MARIADB_USER="root"
MARIADB_PASSWORD="password"

# the .sql file used is the make-banking.sql from a previous homework
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://"+ MARIADB_USER + ":" + MARIADB_PASSWORD + "@" + MARIADB_URL + "/filesharingdb"
# mysql+pymysql://username:password@host:port/database_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.debug = True
app.secret_key = 'your_secret_key'

db = SQLAlchemy()
db.init_app(app)

# Define the login route
@app.route('/', methods=["POST", "GET"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Get the user input
        username = request.form['username']
        password = request.form['password']




        # Execute the SQL query to retrieve the user with the given username and password
        # query = "INSERT INTO customer (customer_name, customer_city, customer_street) VALUES (:customer_name, :customer_city, :customer_street)"
        # db.session.execute(text(query), {"customer_name": customer_name, "customer_city": customer_city, "customer_street": customer_street})     
        query = "SELECT * FROM User WHERE Username = :Username AND Password = :Password"    
        queryuser= db.session.execute(text(query), {"Username": username, "Password": password})
        user = queryuser.fetchone()
        userdata = {key: value for key, value in zip(queryuser.keys(), user)}




        # Close the database connection
        # db.session.commit()
        # If the user is found, store their information in a session and redirect to the dashboard
        if user:
            session['loggedin'] = True
            session['username'] = username
            session['UserData'] = userdata


            # # # query more information for this user
            query = "SELECT * FROM File WHERE UserID = :userid"    
            queryuserfiles= db.session.execute(text(query), {"userid": userdata['UserID']})
            files = queryuserfiles.fetchall()

            userfiles = {key: value for key, value in zip(queryuserfiles.keys(), files)}

            query = "SELECT * FROM user_receives_notification WHERE UserID = :userid"   
            queryusernotifs= db.session.execute(text(query), {"userid": userdata['UserID']})
            notifs = queryusernotifs.fetchall()

            return jsonify({'message': str(notifs) + str(files) + str(userdata['Username'])} )

            # usernotifs = {key: value for key, value in zip(queryusernotifs.keys(), notifs)}

            # return render_template('dashboard.html',
            #                        username=str(userdata['Username']), 
            #                        email = str(userdata['Email']), 
            #                        registration_date = str(userdata['RegistrationDate']), 
            #                        last_login_date = str(userdata['LastLoginDate']), 
            #                        user_profile = str(userdata['UserProfile']),
            #                        files = str(userfiles),
            #                        notifications =str(usernotifs)
            #                        )  
            # return redirect('/dashboard')
        # If the user is not found, show an error message

        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    # If the request method is GET, show the login form
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
        return render_template('dashboard.html')

    

@app.route("/displaydowntown", methods=["POST", "GET"])
def displaydowntown():

    # Construct the SQL query string to retrieve the desired data
    # query = "SELECT DISTINCT c.customer_name, c.customer_city FROM customer c JOIN depositor d ON c.customer_name = d.customer_name JOIN account a ON d.account_number = a.account_number JOIN branch b ON a.branch_name = b.branch_name WHERE b.branch_name = 'Downtown'"
    
    # # Execute the query and retrieve the results
    # result = db.session.execute(text(query))

    # # If rows are returned, format the data as a list of dictionaries and return it
    # if result.rowcount > 0:
    #     rows = result.fetchall()
    #     data = [{'name': row[0], 'city': row[1], 'branch': 'Downtown'} for row in rows]
    #     return jsonify(data)
    # else:
    #     return jsonify({'message': 'No matching data found'})
    return jsonify({'message': 'success path'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

