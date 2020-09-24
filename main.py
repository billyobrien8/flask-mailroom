import os

from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation, Donor
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
# app.secret_key = 'BUDOY3MB7E3OU'
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        query = Donor.select().where(Donor.name == request.form['name'])
        if query.exists():
            donor = query.get()

            if donor and pbkdf2_sha256.verify(request.form['password'],
                                              donor.password):
                session['username'] = request.form['name']
                return redirect(url_for('all'))

        return render_template('login.jinja2',
                               error="Incorrect username or password")

    else:
        return render_template('login.jinja2')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        query = Donor.select().where(Donor.name == request.form['name'])

        if query.exists():
            donor = query.get()
            donation = Donation(donor=donor,
                                value=int(request.form['donation']))
            donation.save()

            return redirect(url_for('all'))

        return render_template('create.jinja2',
                               error="Donor not in database.")
    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
