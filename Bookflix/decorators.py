from functools import wraps
from flask import current_app, url_for, flash, redirect
from flask_login import current_user


def full_login_required():
    def wrapper(view_function):

        @wraps(view_function)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            #user must be logged in
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            #user must have selected a profile
            if (not current_user.current_profile()):
                # Redirect to the unauthorized page
                flash('Please choose a profile before accessing the app.', 'info')
                return redirect(url_for('users.profile_selection')) #lo que sea que llamen la funcion de la ruta para elegir perfil

            # It's OK to call the view
            return view_function(*args, **kwargs)
        return decorator
    return wrapper


def admin_required():
    def wrapper(view_function):
        @wraps(view_function)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            #user must be logged in
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            # User must be of account type Admin
            if (not current_user.accountType == 'Admin'):
                # Redirect to the unauthorized page
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.home'))

            # It's OK to call the view
            return view_function(*args, **kwargs)
        return decorator
    return wrapper