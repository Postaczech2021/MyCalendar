from . import *

def category_edit(category_id):
    category = EventCategory.query.get_or_404(category_id)

    if request.method == 'POST':
        category.name = request.form['name']
        db.session.commit()
        return redirect(url_for('categories_list'))

    theme = request.cookies.get('theme', 'dark')
    return render_template('category_edit.html', category=category, theme=theme)
