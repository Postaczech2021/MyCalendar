from . import *

def set_theme():
    theme = request.form.get('theme')
    response = redirect(request.referrer)
    response.set_cookie('theme', theme)
    return response
