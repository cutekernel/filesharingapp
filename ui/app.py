from flask import Flask, request, jsonify, url_for, render_template, request, render_template, session, redirect
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import os, hashlib
from datetime import datetime
from sqlalchemy.exc import *


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


# Global variables:
UPLOAD_FOLDER = '/home'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'png', 'mp3', 'txt', 'psd', 'py'}

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
        


        # Close the database connection
        # db.session.commit()
        # If the user is found, store their information in a session and redirect to the dashboard
        if user:
            userdata = {key: value for key, value in zip(queryuser.keys(), user)}
            session['loggedin'] = True
            session['username'] = username
            session['UserData'] = userdata
            session['UserID'] = userdata['UserID']


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
            # return jsonify({'Username': str(userdata['Username']),
            #                 'notifications': str(allusernotifs) ,
            #                 'files:': str(userfiles)
            #                 } )

            return render_template('dashboard.html',
                                   username=str(userdata['Username']), 
                                   email = str(userdata['Email']), 
                                   registration_date = str(userdata['RegistrationDate']), 
                                   last_login_date = str(userdata['LastLoginDate']), 
                                   user_profile = str(userdata['UserProfile']),
                                   files = userfiles,
                                   notifications =allusernotifs
                                   )  

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
            alert = 'Invalid username or password. Please try again.'
            return render_template('login.html', alert=alert)
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
        
        if (len(session['username']) > 0) and (len(session['UserData']) > 0):
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

        return render_template('dashboard.html',
                                username=str(userdata['Username']), 
                                email = str(userdata['Email']), 
                                registration_date = str(userdata['RegistrationDate']), 
                                last_login_date = str(userdata['LastLoginDate']), 
                                user_profile = str(userdata['UserProfile']),
                                files = userfiles,
                                notifications =allusernotifs
                                )  



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
        try:
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
        except IntegrityError as e:
            # Handle the duplicate entry error
            error_message = str(e)
            # You can display an error message or redirect to an error page
            return render_template('error.html', error=error_message)        
        #verify that the user is inserted
        query = "SELECT * from User WHERE Username = :username"
        insertuser = db.session.execute(text(query), {'username': username})
        if insertuser.fetchone():
            # if the inserted user already exist, redirect to login 
            # return jsonify({'message': 'user successfully inserted. Please login now'})
            return render_template('login.html')
        
        else:
            return render_template('login.html')

    return render_template('register.html')


@app.route('/getnotifications', methods=['GET', 'POST'])
def getnotifications():
    if session['UserData']:
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
    else:
        #  redirect('/login')
         return render_template('login.html')
    # get all the notifications for the logged in user and return them in a json format
    # return render_template('notifications.html')

@app.route('/getprofile', methods=['GET', 'POST'])
def getprofile():
    
    # get the user profile
    # simply display user information
    if session['username']:
        query = "SELECT * FROM User WHERE Username = :Username"    
        queryuser= db.session.execute(text(query), {"Username": session['username']})
        user = queryuser.fetchone()
        userdata = {key: value for key, value in zip(queryuser.keys(), user)} 
        # return jsonify(str(userdata))
        return render_template('profile.html', userdata=userdata)
    else:
         redirect('/login')
    

@app.route('/deleteprofile', methods=['GET', 'POST'])
@app.route('/deleteprofile/<username>', methods=['GET', 'POST'])
def deleteprofile(username=None):

    if len(str(session['UserID'])) > 0:
        # delete a profile
        # find the username and delete it from the database
        # delete the files associated with the user

        querylist = [
                        "DELETE FROM User WHERE UserID = :userid",
                        "DELETE FROM File WHERE UserID = :userid",
                        "DELETE FROM user_receives_notification WHERE UserID = :userid",
                        "DELETE FROM user_belongs_userGroup WHERE UserID = :userid",
                        "DELETE FROM UserActivity WHERE UserID = :userid"
        ]
        for query in querylist:
            db.session.execute(text(query), {"userid": session['UserID']})
            db.session.commit()

        # # delete user from user table
        # query = "DELETE * FROM User WHERE UserID = :userid"
        
        # #delete files with that userid
        # query = "DELETE * FROM File WHERE UserID = :userid"

        # #delete notifications associated with the userid
        # query = "DELETE * FROM Notification WHERE UserID = :userid"
        
        # # delete the user from a group
        # query = "DELETE * FROM user_belongs_group WHERE UserID = :userid"

        # # delete any activity related to the userid
        # query = "DELETE FROM UserActivity WHERE UserID = :userid"


    
    return redirect('/login')


@app.route('/updateprofile', methods=['GET', 'POST'])
def updateprofile():
    notification=''
    if request.method == 'POST':
        if session['username']:
            # Retrieve the updated profile information from the form
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            userprofile = request.form['userprofile']
            
            # Construct the SQL query dynamically based on the provided values
            query = "UPDATE User SET"
            params = {}

            if username:
                query += " Username = :username,"
                params['username'] = username

            if email:
                query += " Email = :email,"
                params['email'] = email
            
            if password:
                query += " Password = :password,"
                params['password'] = password
            
            if userprofile:
                query += " UserProfile = :userprofile,"
                params['userprofile'] = userprofile
            
            # Remove the trailing comma from the query
            query = query.rstrip(',')
            

            
            if bool(params):
                # Append the WHERE clause to update the specific user BY DEFAULT
                query += " WHERE UserID = :userid"
                params['userid'] = session['UserID']                

                # Execute the SQL query to update the user profile information
                db.session.execute(text(query), params)
                db.session.commit()
                session['username'] = username

                del params['userid']
                alert = 'Information updated is: ' + str(params)
                return render_template('profile.html', username=session['username'], alert=alert)
            else:
                alert = 'Please enter information to update. '
                return render_template('profile.html', username=session['username'], alert=alert)                
        else:
            # Redirect to the profile page
            return redirect('/updateprofile')
    
    # If the request method is GET, show the profile update form
    return render_template('profile.html', username=session['username'])



@app.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile(): 
    alert = {}
    categories = get_categories()
    tags = get_tags()
    if request.method == 'POST':
        # Check if a file was provided in the request
        if 'file' not in request.files:
            # flash('No file selected.')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if a filename was provided
        if file.filename == '':
            # flash('No file selected.')
            return redirect(request.url)
        
        # Check if the file extension is allowed
        if not allowed_file(file.filename):
            # flash('Invalid file format.')
            return redirect(request.url)
        
        # Save the file to the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Generate the hash of the file using SHA-256
        with open(file_path, 'rb') as f:
            file_hash = int(hashlib.sha256(f.read()).hexdigest(), 16) % 2147483647       

        # Get the file extension
        file_extension = get_file_extension(file.filename)
        
        # Query the FileFormat table to get the format ID based on the file extension
        query = "SELECT FormatID FROM FileFormat WHERE FormatName = :extension"
        format_id = db.session.execute(text(query), {"extension": file_extension}).fetchone()
        
        if format_id is None:
            # The file format is not supported, handle accordingly
            return redirect(request.url)
        
        format_id = format_id[0]  # Extract the format ID from the result
        

        # Check if a file with the same name already exists in the File table
        query = "SELECT * FROM File WHERE FileName = :filename"
        queryfile = db.session.execute(text(query), {"filename": file.filename})
        resfile= queryfile.fetchone()

        
        if resfile:
            existing_file={key: value for key, value in zip(queryfile.keys(), resfile)}
            # Update the existing file to the latest version
            update_query = "UPDATE File SET UploadDate = :upload_date, FileSize = :file_size WHERE FileID = :file_id"
            db.session.execute(
                text(update_query),
                {
                    "upload_date": datetime.now(),
                    "file_size": os.path.getsize(file_path),
                    "file_id": existing_file['FileID']
                }
            )
            db.session.commit()
        else:
            # Create a new record(file version) for the file in the File table
            insert_version = """
                INSERT INTO FileVersion (VersionNumber,VersionDescription, VersionSize, VersionUploadDate)
                VALUES (:version_number, :version_description, :version_size, :version_upload_date);
            """
            result=db.session.execute(
                text(insert_version),
                {
                    "version_number": file_hash,  
                    "version_description": "Initial version",  # Replace with the appropriate value
                    "version_size": os.path.getsize(file_path),
                    "version_upload_date": datetime.now(),
                }
            )
            db.session.commit()
            version_id = result.lastrowid

                        
            insert_query = """
                INSERT INTO File (FileName, FileSize, UploadDate, LatestVersionID, UserID, FormatID)
                VALUES (:filename, :file_size, :upload_date, :latest_version_id, :user_id, :format_id)
            """
            result = db.session.execute(
                text(insert_query),
                {
                    "filename": file.filename,
                    "file_size": os.path.getsize(file_path),
                    "upload_date": datetime.now(),
                    "latest_version_id": version_id,  # Replace with the appropriate value
                    "user_id": session['UserID'],  # Replace with the appropriate value
                    "format_id": format_id
                        # Replace with the appropriate value
                }
            )

            # the size is in Bytes
            db.session.commit()
            alert['operation'] = 'insertion'
            alert['inserted_data'] = { "filename": file.filename, "file_size": os.path.getsize(file_path), "upload_date": datetime.now(), "latest_version_id": version_id, "user_id": session['UserID'],  "format_id": format_id  }


            # operations on selected checkboxes
    
            selected_checkboxes = request.form.getlist('tags')
            app.logger.debug(selected_checkboxes)
            for selection in selected_checkboxes:
                #get the tagid from the name
                query = "SELECT TagID FROM Tag WHERE TagName = :tagname"
                tagid=db.session.execute(text(query), {"fileid": result.lastrowid, "tagname": selection}).fetchone()[0]
                app.logger.debug(tagid)
                
                #insert the tag id with fileid
                query = "INSERT INTO file_has_tag (fileID, tagID) VALUES (:fileid, :tagid) "
                db.session.execute(text(query), {"fileid": result.lastrowid, "tagid": tagid})
                db.session.commit()
            alert['tags'] = selected_checkboxes


            if 'category' in request.form:
                categoryname = request.form.get('category')  
                fileid = result.lastrowid
                query = "SELECT CategoryID FROM FileCategory WHERE CategoryName = :categoryname "
                querycat = db.session.execute(text(query), {"categoryname": categoryname})
                categoryid = querycat.fetchone()[0]
                # app.logger.debug(categoryid)
                # insert into the file_has_category table
                query = "INSERT INTO file_has_filecategory (fileID, categoryID) VALUES (:fileid, :categoryid) "
                querycat = db.session.execute(text(query), {"fileid": fileid, "categoryid": categoryid})
                db.session.commit()
                alert['category'] = categoryname




        
        return render_template('upload.html', categories=categories, tags=tags, alert=alert)
    return render_template('upload.html', categories=categories, tags=tags)
    
    # If the request method is GET, show the file upload form
    return render_template('upload.html')
def get_categories():
    query = "SELECT CategoryName FROM FileCategory"
    result = db.session.execute(text(query))
    categories = [row[0] for row in result.fetchall()]
    return categories

def get_tags():
    query = "SELECT TagName FROM Tag"
    result = db.session.execute(text(query))
    tags = [row[0] for row in result.fetchall()]
    return tags

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else None


@app.route('/getfiledetails', methods=['GET', 'POST'])
def getfiledetails():
    # display the file details of the latest version
    # Retrieve the file details of a specific file using SQL statements
    fileid = request.args.get('file_id')
    session['FileID'] = fileid
    # app.logger.debug(session['FileID'])

    query = "SELECT * FROM File WHERE FileID = :file_id AND UserID = :userid"
    result = db.session.execute(text(query), {'file_id': fileid, 'userid': session['UserID']})
    m_filedetails = result.fetchone()
    # store each file in a list with its corresponding attributes
    m_file={key: value for key, value in zip(result.keys(), m_filedetails)}


    query = "SELECT ruleID  FROM file_has_ac_rule WHERE FileID = :file_id"
    result = db.session.execute(text(query), {'file_id': fileid})
    m_ruleids = [str(t[0]) for t in result.fetchall()]
    # ruleids = {key: value for key, value in zip(result.keys(), m_ruleids)}
    allrules = []
   
    # app.logger.debug( [t[0] for t in m_ruleids])
    for ruleid in m_ruleids:
        query = "SELECT RuleName, RuleDescription, AccessLevel  FROM AccessControlRule WHERE RuleID = :ruleid"
        result = db.session.execute(text(query), {'ruleid': ruleid})
        ruleid = result.fetchone()        
        allrules.append(ruleid)


    # Render the template and pass the file details as a parameter
    return render_template('filedetails.html', file_details=m_file, ruleids=allrules)
    # return render_template('filedetails.html')


@app.route('/getfileversionhistory', methods=['GET', 'POST'])
def getfileversionhistory():
    # display the file version history
    pass
    return render_template('fileversionhistory.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # search a file by name and/or other attributes
    # only show files based on ac rules (=shared files)
    # if the user has admin access level then no restriction
    # if the user has employee access lvel then certiain file categories are ignored.
    if request.method == 'POST':
        # Get the search query from the form
        name = request.form.get('name')
        size_operator = request.form.get('size_operator')
        size = request.form.get('size')
        category = request.form.get('category')
        fileformat = request.form.get('format')


        query = """
                SELECT f.FileID, f.FileName, f.FileSize, f.UploadDate, f.UserID, f.FormatID 
                FROM File AS f
                JOIN FileFormat AS ff ON f.FormatID = ff.FormatID
                JOIN file_has_filecategory AS fc ON f.FileID = fc.FileID
                JOIN FileCategory AS ca ON fc.categoryID = ca.CategoryID
                WHERE 1=1
                """        

        params = {}

        if name:
            query += " AND f.FileName = :name"
            params['name'] = name

        if size and size_operator:
            if size_operator == 'greater':
                query += " AND f.FileSize > :size"
            elif size_operator == 'less':
                query += " AND f.FileSize < :size"
            elif size_operator == 'equal':
                query += " AND f.FileSize = :size"

            params['size'] = size

        if category:
            query += " AND ca.CategoryName = :category"
            params['category'] = category

        if fileformat:
            query += " AND ff.FormatName = :format"
            params['format'] = fileformat

        # Execute the query and fetch results
        results =  db.session.execute(text(query), params)  # Replace with your database library
        resfiles= results.fetchall()
        allfiles=[]
        search_attributes = ["fileid", "filename", "filesize", "uploaddate", "username", "formatname"]
        #TODO: query username and format ID so that its username and extension name

 # Replace with your database library

        for resfile in resfiles:
            query = "SELECT Username FROM User WHERE UserID = :userid"
            resusername =  db.session.execute(text(query), {'userid': resfile[4]}).fetchone()[0]  # Replace with your database library

            query = "SELECT FormatName FROM FileFormat WHERE FormatID = :formatid"
            resformatid =  db.session.execute(text(query), {'formatid': resfile[5]}).fetchone()[0] 

            m_file = {
                       "fileid": resfile[0],
                       "filename": resfile[1],
                       "filesize": resfile[2],
                       "uploaddate": resfile[3],
                       "username": resusername,
                       "formatname": resformatid
                           }
            allfiles.append(m_file)


            # # access control
            # query = """
            # SELECT CASE
            #     WHEN EXISTS (
            #         SELECT 1
            #         FROM file_has_ac_rule AS far
            #         INNER JOIN AccessControlRule AS acr ON far.ruleID = acr.RuleID
            #         INNER JOIN File AS f ON far.fileID = f.FileID
            #         WHERE acr.RuleName = :rulename
            #         AND f.FileName = :filename 
            #         AND acr.UserID = :userid 
            #     )
            #     THEN 'Access allowed'
            #     ELSE 'Access denied'
            #     END AS AccessStatus;
            # """
            # acquery = db.session.execute(text(query), {"rulename": rulename, "filename": filename, "userid": userid})

            app.logger.debug(m_file)

        # Sort the results by upload date (assuming it's a datetime column)
        # results.sort(key=lambda x: x.upload_date)

        return render_template('search.html', categories=get_categories(), fileformats=get_fileformats(), search_results=allfiles, search_attributes=search_attributes)

    # If the request method is GET or no search query is provided, render the search page
    return render_template('search.html', categories=get_categories(), fileformats=get_fileformats())

def get_categories():
    # Query the database to retrieve the list of categories
    # You can customize this part to retrieve the categories based on your database schema and criteria

    # Example: Retrieve categories from a Categories table
    query = "SELECT CategoryName FROM FileCategory"
    result = db.session.execute(text(query))
    categories = [row[0] for row in result.fetchall()]

    return categories

def get_fileformats():
    # Query the database to retrieve the list of fileformats
    # You can customize this part to retrieve the fileformats based on your database schema and criteria

    # Example: Retrieve fileformats from a fileformat table
    query = "SELECT FormatName FROM FileFormat"
    result = db.session.execute(text(query))
    fileformats = [row[0] for row in result.fetchall()]

    return fileformats

@app.route('/manageusers', methods=['GET', 'POST'])
def manageusers():
    # add a user to a group
    query = " SELECT * FROM UserGroup"
    querygroups = db.session.execute(text(query))
    resgroups = querygroups.fetchall()

    # find group members
    query= "SELECT * FROM user_belongs_userGroup "
    querymembers = db.session.execute(text(query))
    resmembers = querymembers.fetchall()
    memberdata = []
    for member in resmembers:
        # app.logger.debug(str(resmembers[0]))
        # get user information
        subquery = "SELECT Username from User WHERE UserID = :userid"
        querymember = db.session.execute(text(subquery), {"userid": member[0]})
        resmember = querymember.fetchone()[0]
        # get grop information
        subgquery = "SELECT GroupName from UserGroup WHERE GroupID = :UserGroup"
        querygroup = db.session.execute(text(subgquery), {"UserGroup": member[1]})
        resgroup = querygroup.fetchone()[0] 
        memberdata.append({"username": resmember, "groupname": resgroup})
        group_id = member[1]
    arranged_group_members = group_members(memberdata)

    jsonify(memberdata)

    return render_template('user_group_management.html', groups=resgroups, memberdata=arranged_group_members)

def group_members(members):
  """
  Groups members of the same group together.

  Args:
    members: A list of dictionaries, where each dictionary contains the following keys:
      * username: The username of the user.
      * groupname: The name of the group that the user belongs to.

  Returns:
    A list of dictionaries, where each dictionary contains the following keys:
      * groupname: The name of the group that the user belongs to.
      * members: A list of strings, where each string is the username of a user who belongs to the group.
  """

  # Create a list comprehension that yields the groups and their members.
  groups = [member['groupname'] for member in members]
  members_by_group = {group: [member['username'] for member in members if member['groupname'] == group] for group in set(groups)}

  # Create a dictionary comprehension that yields the grouped members.
  return {group: members for group, members in members_by_group.items()}




@app.route('/addmember', methods=['GET', 'POST'])
def addmember():
    groupnames = get_groupnames()
    usernames = get_usernames()
    alert = {}
    if request.method == 'POST' and 'username' in request.form and 'groupname' in request.form:
        # add a user to a group
        username = request.form.get('username')
        groupname = request.form.get('groupname')
        # query the userid
        query = "SELECT UserID from User WHERE Username = :username"
        userid = db.session.execute(text(query), {'username':username}).fetchone()[0]
        alert['userid'] = userid
        # query the groupid based on the groupName
        query = "SELECT GroupID from UserGroup WHERE GroupName = :groupname"
        groupid = db.session.execute(text(query), {'groupname':groupname}).fetchone()[0]
        alert ['groupid'] = groupid

        query = """
            INSERT INTO user_belongs_userGroup (UserID, groupID)
            VALUES (:userid, :groupid)
        """
        
        db.session.execute(
            text(query),
            {
                'userid': userid,
                'groupid': groupid
            }
        )
        db.session.commit()
        
        return render_template('addmember.html', groupnames=groupnames, usernames=usernames, alert=alert)
    return render_template('addmember.html', groupnames=groupnames, usernames=usernames)
def get_groupnames():

    query = "SELECT GroupName FROM UserGroup"
    result = db.session.execute(text(query))
    groupnames = [row[0] for row in result.fetchall()]

    return groupnames

def get_usernames():

    query = "SELECT Username FROM User"
    result = db.session.execute(text(query))
    usernames = [row[0] for row in result.fetchall()]

    return usernames

@app.route('/removemember', methods=['GET', 'POST'])
def removemember():
    alert = {}
    groupnames = get_groupnames()
    usernames = get_usernames()
    if request.method == 'POST' and 'username' in request.form and 'groupname' in request.form:
        # add a user to a group
        username = request.form.get('username')
        groupname = request.form.get('groupname')
        # query the userid
        query = "SELECT UserID from User WHERE Username = :username"
        userid = db.session.execute(text(query), {'username':username}).fetchone()[0]
        alert['userid'] = userid
        # query the groupid based on the groupName
        query = "SELECT GroupID from UserGroup WHERE GroupName = :groupname"
        groupid = db.session.execute(text(query), {'groupname':groupname}).fetchone()[0]
        alert['groupid'] = groupid

        query = """
            DELETE FROM user_belongs_userGroup WHERE UserID = :userid AND groupID = :groupid
        """
        
        db.session.execute(
            text(query),
            {
                'userid': userid,
                'groupid': groupid
            }
        )
        db.session.commit()
        return render_template('removemember.html', groupnames=groupnames, usernames=usernames, alert=alert)
    return render_template('removemember.html', groupnames=groupnames, usernames=usernames)

@app.route('/addgroup', methods=['GET', 'POST'])
def addgroup():
    # add  a group
    alert = {}
    

    if request.method == 'POST'  and 'groupdescription' in request.form and 'groupname' in request.form:
        groupname = request.form.get('groupname')
        groupdescription = request.form.get('groupdescription')

        query = """
            INSERT INTO UserGroup (GroupName, GroupDescription)
            VALUES (:groupname, :groupdescription)
        """
        app.logger.debug(groupname)
        app.logger.debug(groupdescription)
        db.session.execute(
            text(query),
            {
                'groupname': groupname,
                'groupdescription': groupdescription
            }
        )
        db.session.commit()
        alert['operation'] = insertion
        alert['groupname'] = groupname
        alert['groupdescription'] = groupdescription
        return render_template('addgroup.html', alert=alert )
    return render_template('addgroup.html' )


@app.route('/removegroup', methods=['GET', 'POST'])
def removegroup():
    groupnames = get_groupnames()

    if request.method == 'POST'  and 'groupname' in request.form:
        groupname = request.form.get('groupname')

        query = """
            DELETE FROM UserGroup
            WHERE GroupName = :groupname
        """
        app.logger.debug(groupname)
        db.session.execute(
            text(query),
            {
                'groupname': groupname,
            }
        )
        db.session.commit()
    return render_template('removegroup.html', groupnames=groupnames)




# @app.route('/addtags', methods=['GET', 'POST'])
# def addtags():
#     # add tags to a file
#     pass  
#     return render_template('tag_management.html')


# @app.route('/removetags', methods=['GET', 'POST'])
# def removetags():
#     pass        
#     return render_template('tag_management.html')


@app.route('/addac', methods=['GET', 'POST'])
def addac():
    acrules = get_acrules()
    if request.method == 'POST' and 'acrule' in request.form:
        acrule = request.form.get('acrule')
        query = "SELECT RuleID from AccessControlRule WHERE RuleName = :rulename"
        acruleid = db.session.execute(text(query), {'rulename':acrule}).fetchone()[0]

        query = """
            INSERT INTO file_has_ac_rule (fileID, ruleID) 
            VALUES (:fileid, :ruleid)
        """
        
        db.session.execute(
            text(query),
            {
                'fileid': session['FileID'],
                'ruleid': acruleid
            }
        )
        db.session.commit()
    return render_template('addac.html', acrules=acrules)

def get_acrules():

    query = "SELECT RuleName FROM AccessControlRule"
    result = db.session.execute(text(query))
    acrules = [row[0] for row in result.fetchall()]

    return acrules


@app.route('/removeac', methods=['GET', 'POST'])
def removeac():
    acrules = get_acrules()
    if request.method == 'POST' and 'acrule' in request.form:
        acrule = request.form.get('acrule')
        query = "SELECT RuleID from AccessControlRule WHERE RuleName = :rulename"
        acruleid = db.session.execute(text(query), {'rulename':acrule}).fetchone()[0]

        query = """
            DELETE FROM file_has_ac_rule WHERE fileID = :fileid AND  ruleID = :ruleid 

        """
        
        db.session.execute(
            text(query),
            {
                'fileid': session['FileID'],
                'ruleid': acruleid
            }
        )
        db.session.commit()
    return render_template('removeac.html', acrules=acrules)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

