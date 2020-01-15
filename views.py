from main import app, db
from flask import render_template, request, url_for, redirect, flash
from models import Request, Admin
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
import ipinfo
from flask_googlemaps import Map

# Defines Home Page
@app.route("/")
def index():
    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        user_ip = request.remote_addr
    # user_ip = getrequest.remote_addr
    req = Request(ip_address=user_ip)
    db.session.add(req)
    db.session.commit()
    return render_template('home.html')

# 404 error page
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

# Admin Login Page
@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin is not None:
            if check_password_hash(admin.password, form.password.data):
                login_user(admin)
                if admin.is_fresh_login is True:
                    admin.is_fresh_login = False
                    db.session.commit()
                    return redirect(url_for('admin_reset_password'))
                else:
                    return redirect(url_for('admin_dashboard'))
            else:
                flash(u"Invalid credentails.", "danger")    
        else:
            flash(u"Invalid credentails.", "danger")
    return render_template('admin/login.html', form=form)

# Admin dashboard
@app.route('/admin/')
@login_required
def admin_dashboard():
    ip_markers = []
    # get all request ip
    requests = Request.query.all()
    if requests is not None:
        for req in requests:
            location = get_loc_by_ip(req.ip_address)
            if location is not None:
                ip_markers.append(location)

        map = Map("admin-google-map",lat=17.685895,lng=77.158687, zoom=3,markers=ip_markers)
    else:
        map = Map("admin-google-map",lat=17.685895,lng=77.158687, zoom=3)
    return render_template('admin/dashboard.html', map=map)

# Password Reset if admin loggins for first time
@app.route('/admin/reset-password', methods=['GET', 'POST'])
@login_required
def admin_reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        admin_id = current_user.id
        admin = Admin.query.get(int(admin_id))
        admin.password = generate_password_hash(form.password.data)
        admin.is_pw_changed = True
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/reset_password.html', form=form)

# Logout View
@app.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


def get_loc_by_ip(ip):
    handler = ipinfo.getHandler(app.config['IPINFO_TOKEN'])
    data = handler.getDetails(ip)
    if data is not None:
        location = data.loc.split(",")
        marker = { "lat": float(location[0]), "lng": float(location[1]), "infobox": ip }
        return marker
    else:
        return None