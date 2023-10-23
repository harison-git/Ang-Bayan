from flask import Blueprint, url_for, redirect, request, session, flash, render_template, jsonify, make_response, g
from main.models.dbModel import User, Community, Program, Subprogram, Role, Upload
from main import db
from main import Form
from flask import Response


dbModel_route = Blueprint('dbModel', __name__)


@dbModel_route.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check the username and password against the database (replace with actual database query)
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Store the user's ID in the session to keep them logged in
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dbModel.dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
        

    return render_template("login.html")
@dbModel_route.route("/admin_dashboard")
def dashboard():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("dashboard.html")


def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = User.query.get(session['user_id'])
        if user:
            return user.firstname, user.role
    return None, None
@dbModel_route.before_request
def before_request():
    g.current_user, g.current_role = get_current_user()

@dbModel_route.context_processor
def inject_current_user():
    return dict(current_user=g.current_user, current_role=g.current_role)

@dbModel_route.route("/clear_session")
def clear_session():
    # Clear the user's session
    session.clear()
    
    # Redirect the user to the login page
    return redirect(url_for('dbModel.login'))

@dbModel_route.route("/result")
def programCSVresult():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return redirect(url_for('randomForest.programOneRow'))

#FOR USER CRUD

@dbModel_route.route("/manage_account")
def manage_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = User.query.all()
    role = Role.query.all()
    program8 = Program.query.all()
    return render_template("manage_account.html", users = all_data, role = role, program8=program8)

@dbModel_route.route("/add_account", methods=["POST"])
def add_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        role = request.form.get("role")
        program = request.form.get("program")
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            # Create a new user without hashing the password
            new_user = User(username=username, firstname=firstname, lastname=lastname, password=password, role = role, program = program)

            try: 
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the account. Please try again.', 'error')
                # You may also want to log the exception for debugging purposes
    return redirect(url_for('dbModel.manage_account'))

@dbModel_route.route('/edit_account', methods=['POST'])
def edit_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        user_id = request.form.get('id')  # Get the user ID from the form
        new_username = request.form['new_username']
        new_firstname = request.form['new_firstname']
        new_lastname = request.form['new_lastname']
        new_password = request.form['new_password']
        new_role = request.form['new_role']
        new_program = request.form['new_program']
        
        
        # Query the user by ID
        user = User.query.get(user_id)
        
        if user:
            # Update the user's information
            user.username = new_username
            user.firstname = new_firstname
            user.lastname = new_lastname
            user.password = new_password
            user.role = new_role
            user.program = new_program

            # Commit the changes to the database
            db.session.commit()
            flash('Account updated successfully!', 'success')
        else:
            flash('User not found. Please try again.', 'error')

        return redirect(url_for('dbModel.manage_account'))

@dbModel_route.route('/delete_account/<int:id>', methods=['GET'])
def delete_account(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    user = User.query.get(id)

    if user:
        try:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')

    return redirect(url_for('dbModel.manage_account'))



##################  FOR COORDINATOR  #######################
@dbModel_route.route("/coordinator")
def coordinator():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("coordinator.html")



##################  FOR COMMUNITY CRUD  #######################
@dbModel_route.route("/get_community_data")
def get_community_data():
    try:
        community_data = [
        {
            'community': record.community,
            'program': record.program,
            'subprogram': record.subprogram,
            'week': record.week,
            'totalWeek': record.totalWeek,
            'user': record.user
            # Add other fields here
        }
        for record in Community.query.all()
    ]
        return jsonify(community_data)
    except Exception as e:
        # Log the error for debugging
        print(str(e))
        return make_response("Internal Server Error", 500)

@dbModel_route.route("/manage_community")
def manage_community():
    form = Form()
    placeholder_choice = ("", "-- Select Program --")
    form.program.choices = [placeholder_choice[1]] + [program.program for program in Program.query.all()]
    form.program.default = ""
    form.process()
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Community.query.all()
    program8 = Program.query.all()
    user1 = User.query.all()
    return render_template("community.html", community = all_data, form=form, program8=program8, user1 = user1)

@dbModel_route.route("/subprogram/<get_subprogram>")
def subprogram(get_subprogram):
    sub = Subprogram.query.filter_by(program=get_subprogram).all()
    subArray = [program.subprogram for program in sub]  # Extract the subprograms from the query result
    return jsonify({'subprogram': subArray})

#fetch for user
@dbModel_route.route("/subprogram1/<get_program>")
def get_program(get_program):
    sub = User.query.filter_by(program=get_program).all()
    subArray = [user.username for user in sub]  
    return jsonify({'user': subArray})


@dbModel_route.route("/add_community", methods=["POST"])
def add_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        community = request.form.get("community")
        program = request.form.get("program")
        subprogram = request.form.get("subprogram")
        week = request.form.get("week")
        totalWeek = request.form.get("totalWeek")
        user = request.form.get("user")

        # Check if a community with the same values for 'community' and 'subprogram' already exists
        existing_community = Community.query.filter_by(community=community, subprogram=subprogram).first()

        if existing_community:
            flash('This combination of community and subprogram already exists. Please choose a different combination.', 'error')
        else:
            new_community = Community(community=community, program=program, subprogram=subprogram, week=week, totalWeek=totalWeek, user=user)

            try:
                db.session.add(new_community)
                db.session.commit()
                flash('Community created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the community. Please try again.', 'error')
                # You may also want to log the exception for debugging purposes

    return redirect(url_for('dbModel.manage_community'))



@dbModel_route.route('/edit_community', methods=['POST'])
def edit_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        user_id = request.form.get('id')  # Get the user ID from the form
        new_community = request.form['new_community']
        new_program = request.form['new_program']
        new_subprogram = request.form['new_subprogram']
        new_week= request.form['new_week']
        new_totalWeek = request.form['new_totalWeek']
        new_user = request.form['new_user']
        
        # Query the user by ID
        user = Community.query.get(user_id)
        
        if user:
            # Update the user's information
            user.community = new_community
            user.program = new_program
            user.subprogram = new_subprogram
            user.week = new_week
            user.totalWeek = new_totalWeek
            user.user = new_user

            # Commit the changes to the database
            db.session.commit()
            flash('Account updated successfully!', 'success')
        else:
            flash('User not found. Please try again.', 'error')

        return redirect(url_for('dbModel.manage_community'))

@dbModel_route.route('/delete_community/<int:id>', methods=['GET'])
def delete_community(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    community = Community.query.get(id)
    if community:
        try:
            # Delete the user from the database
            db.session.delete(community)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('dbModel.manage_community'))


############# UPDATE WEEK BASED FROM Subprogram ##############
# Flask Route
@dbModel_route.route('/update_week', methods=['POST'])
def update_week():
    data = request.get_json()
    subprogram = data['subprogram']
    totalCheckboxes = data['totalCheckboxes']

    # Query the database to get records with the specified subprogram
    communities = Community.query.filter_by(subprogram=subprogram).all()

    for community in communities:
        # Update the "week" column to match the totalCheckboxes
        community.week = totalCheckboxes

    db.session.commit()

    return jsonify({'message': 'Week column updated for the specified subprogram.'})

# -------------------------   DL FILES
@dbModel_route.route('/files')
def files():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    upload_data = Upload.query.all()
    return render_template("dlfiles.html", upload_data=upload_data)

@dbModel_route.route('/uploadfile', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # Read the file and insert it into the database
            data = file.read()
            upload_entry = Upload(filename=file.filename, data=data)
            db.session.add(upload_entry)
            db.session.commit()
    return redirect(url_for('dbModel.files'))


@dbModel_route.route('/view/<int:file_id>')
def view(file_id):
    upload_entry = Upload.query.get(file_id)
    if upload_entry:
        # Determine the content type based on the file extension
        content_type = "application/octet-stream"
        filename = upload_entry.filename.lower()

        if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            content_type = "image"

        # Serve the file with appropriate content type and Content-Disposition
        response = Response(upload_entry.data, content_type=content_type)

        if content_type.startswith("image"):
            # If it's an image, set Content-Disposition to inline for display
            response.headers["Content-Disposition"] = "inline"
        else:
            # For other types, set Content-Disposition to attachment for download
            response.headers[
                "Content-Disposition"] = f'attachment; filename="{upload_entry.filename}"'
        if filename.endswith(".pdf"):
            response = Response(upload_entry.data,
                                content_type="application/pdf")
        return response
    return "File not found", 404

@dbModel_route.route('/delete_file/<int:id>', methods=['GET'])
def delete_file(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    upload = Upload.query.get(id)
    if upload:
        try:
            # Delete the user from the database
            db.session.delete(upload)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('dbModel.files'))