import sys
from Bookflix import create_app
from flask import Flask, render_template
app = Flask(__name__, template_folder='Bookflix/templates')

#Hay que encontrar la manera de importar las rutas  y los forms para no tener
#el código de abajo en este archivo. Creo que se puede con la librería sys pero
#no estoy seguro todavía. A solucionar.

#                                               -Enzo

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title= 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password and try again.', 'danger')
    return render_template('login.html', title= 'Login', form=form)

if __name__ == '__main__':
        app.run(debug=True)