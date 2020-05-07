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
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title= 'Login')

if __name__ == '__main__':
        app.run(debug=True)