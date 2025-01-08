from . import *

def workshifts_category_add():
    if request.method == 'POST':
        name = request.form['name']
        new_category = WorkshiftsCategory(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Kategorie byla úspěšně přidána!', 'success')
        return redirect(url_for('workshifts_categories_list'))
    
    return render_template('workshifts_category_add.html')
