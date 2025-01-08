from . import *

def workshifts_categories_list():
    categories = WorkshiftsCategory.query.all()
    return render_template('categories_list.html', categories=categories)
