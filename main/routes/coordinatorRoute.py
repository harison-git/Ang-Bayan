from flask import Blueprint, url_for, redirect, session, flash, render_template, jsonify, make_response, g
from main.models.dbModel import User, Community,Upload



coordinator_route = Blueprint('coordinator', __name__)


# COORDINATOR SESSION
@coordinator_route.route("/co-dashboard")
def def_coordinator():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("coordinator_dashboard.html")


# COMMUNITY PROJECTS
@coordinator_route.route("/co_projects")
def def_co_project():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template("coordinator_project.html")


def get_current_user():
    if 'user_id' in session:
        # Assuming you have a User model or some way to fetch the user by ID
        user = User.query.get(session['user_id'])
        if user:
            return user.firstname, user.role
    return None, None


@coordinator_route.before_request
def before_request():
    g.current_user, g.current_role = get_current_user()

@coordinator_route.context_processor
def inject_current_user():
    return dict(current_user=g.current_user, current_role=g.current_role)


##################  COMMUNITY  #######################
@coordinator_route.route("/get_community_data")
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

@coordinator_route.route("/clear_session")
def clear_session():
    # Clear the user's session
    session.clear()
    
    # Redirect the user to the login page
    return redirect(url_for('dbModel.login'))



# -------------------------   DL FILES-----------------
@coordinator_route.route('/co-files')
def co_files():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    upload_data = Upload.query.all()
    return render_template("coordinatorfiles.html", upload_data=upload_data)

#--------------------CHANGE PASSWORD ---------------
@coordinator_route.route('/co-changepassword')
def def_changepass():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    return render_template('co-changepassword.html')