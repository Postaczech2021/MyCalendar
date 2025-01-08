from . import *

def categories_list():
    categories = EventCategory.query.all()
    theme = request.cookies.get('theme', 'dark')
    return render_template('categories_list.html', categories=categories, theme=theme)
