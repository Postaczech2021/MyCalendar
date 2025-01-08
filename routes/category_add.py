from . import *

def category_add():
    if request.method == 'POST':
        name = request.form['name']
        new_category = EventCategory(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('categories_list'))

    theme = request.cookies.get('theme', 'dark')
    return render_template('category_add.html', theme=theme)
