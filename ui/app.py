from flask import Flask, request, jsonify, render_template, request, render_template, session, redirect
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

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
            
            #get the files associated with a userID
            queryuserfiles= db.session.execute(text(query), {"userid": userdata['UserID']})
            files = queryuserfiles.fetchall()
            userfiles = []
            # store each file in a list with its corresponding attributes
            for file in files:
                 m_file={key: value for key, value in zip(queryuserfiles.keys(), file)}
                 userfiles.append(m_file)


            # get the notifications associated with a user and create a list
            query = "SELECT * FROM user_receives_notification WHERE UserID = :userid"   
            queryusernotifs= db.session.execute(text(query), {"userid": userdata['UserID']})
            notifids = queryusernotifs.fetchall()
            allusernotifs=[]

            #once you get the list make sure you display the notifications as items in a list
            for notif in notifids:
                 sub_query= "SELECT * FROM Notification WHERE NotificationID = :notifid"
                 sub_queryusernotifs= db.session.execute(text(sub_query), {"notifid": notif[1]})
                 resusernotifs = sub_queryusernotifs.fetchone()
                 usernotifs = {key: value for key, value in zip(sub_queryusernotifs.keys(), resusernotifs)}
                 allusernotifs.append(usernotifs)


            # return jsonify({'message': str(notifs) + str(files) + str(userdata['Username']),
            return jsonify({'Username': str(userdata['Username']),
                            'notifications': str(allusernotifs) ,
                            'files:': str(userfiles)
                            } )


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


# Route for logging out
@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the login page
    return redirect('/login')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
        
        if session['username'] and session['UserData']:
            username = session['username']
            userdata = session['UserData']

            # # # query more information for this user
            query = "SELECT * FROM File WHERE UserID = :userid"    
            
            #get the files associated with a userID
            queryuserfiles= db.session.execute(text(query), {"userid": userdata['UserID']})
            files = queryuserfiles.fetchall()
            userfiles = []
            # store each file in a list with its corresponding attributes
            for file in files:
                    m_file={key: value for key, value in zip(queryuserfiles.keys(), file)}
                    userfiles.append(m_file)

            # get the notifications associated with a user and create a list
            query = "SELECT * FROM user_receives_notification WHERE UserID = :userid"   
            queryusernotifs= db.session.execute(text(query), {"userid": userdata['UserID']})
            notifids = queryusernotifs.fetchall()
            allusernotifs=[]

            #once you get the list make sure you display the notifications as items in a list
            for notif in notifids:
                    sub_query= "SELECT * FROM Notification WHERE NotificationID = :notifid"
                    sub_queryusernotifs= db.session.execute(text(sub_query), {"notifid": notif[1]})
                    resusernotifs = sub_queryusernotifs.fetchone()
                    usernotifs = {key: value for key, value in zip(sub_queryusernotifs.keys(), resusernotifs)}
                    allusernotifs.append(usernotifs)
        else:
             return redirect('/login')

        return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'email' in request.form and 'username' in request.form and 'password' in request.form and 'user_profile'  in request.form:
        # Get user information from the form
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        userprofile = request.form['user_profile']

        # insert user information into the database
        query = """
            INSERT INTO User (Username, Email, Password, RegistrationDate, LastLoginDate, UserProfile)
            VALUES (:Username, :Email, :Password, :RegistrationDate, :LastLoginDate, :UserProfile)
        """

        db.session.execute(
            text(query),
            {
                'Username': username,
                'Email': email,
                'Password': password,
                'RegistrationDate': datetime.now(),
                'LastLoginDate': datetime.now(),
                'UserProfile': userprofile,
            }
        )
        db.session.commit()
        
        #verify that the user is inserted
        query = "SELECT * from User WHERE Username = :username"
        insertuser = db.session.execute(text(query), {'username': username})
        if insertuser.fetchone():
            # need to redirect to login
            return jsonify({'message': 'user successfully inserted. Please login now'})
        else:
            return render_template('login.html')

    return render_template('login.html')


@app.route('/getnotifications', methods=['GET', 'POST'])
def getnotifications():

    # get the notifications associated with a user and create a list
    query = "SELECT * FROM user_receives_notification WHERE UserID = :userid"   
    queryusernotifs= db.session.execute(text(query), {"userid": session['UserData']['UserID']})
    notifids = queryusernotifs.fetchall()
    allusernotifs=[]

    #once you get the list make sure you display the notifications as items in a list
    for notif in notifids:
            sub_query= "SELECT * FROM Notification WHERE NotificationID = :notifid"
            sub_queryusernotifs= db.session.execute(text(sub_query), {"notifid": notif[1]})
            resusernotifs = sub_queryusernotifs.fetchone()
            usernotifs = {key: value for key, value in zip(sub_queryusernotifs.keys(), resusernotifs)}
            allusernotifs.append(usernotifs)

    return jsonify({'notification': str(allusernotifs)})
    # get all the notifications for the logged in user and return them in a json format
    # return render_template('notifications.html')

@app.route('/getprofile', methods=['GET', 'POST'])
def getprofile():
    
    # get the user profile
    # simply display user information
    return render_template('profile.html')
    

@app.route('/deleteprofile', methods=['GET', 'POST'])
def deleteprofile():
    # delete a profile
    # find the username and delete it from the database
    # delete the files associated with the user
    pass


@app.route('/updateprofile', methods=['GET', 'POST'])
def updateprofile():
    # update the user profile information
    pass
    return render_template('profile.html')


@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
    # upload a file == add an record to the File table
    # if it has the same name as another file, search for that name in the File table and if found make it the latestversion of that file
    pass
    return render_template('upload.html')


@app.route('/getfiledetails', methods=['GET', 'POST'])
def getfiledetails():
    # display the file details of a specific version
    pass
    return render_template('filedetails.html')


@app.route('/getfileversionhistory', methods=['GET', 'POST'])
def getfileversionhistory():
    # display the file version history
    pass
    return render_template('fileversionhistory.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # search a file by name and/or other attributes
    pass
    return render_template('search.html')


@app.route('/addusertogroup', methods=['GET', 'POST'])
def addusertogroup():
    # add a user to a group
    pass
    return render_template('user_group_management.html')


@app.route('/addtags', methods=['GET', 'POST'])
def addtags():
    # add tags to a file
    pass  
    return render_template('tag_management.html')


@app.route('/removetags', methods=['GET', 'POST'])
def removetags():
    pass        
    return render_template('tag_management.html')



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

