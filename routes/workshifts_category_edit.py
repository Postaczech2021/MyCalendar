from . import *

def workshifts_category_edit(category_id):
    category = WorkshiftsCategory.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form['name']
        db.session.commit()
        flash('Kategorie byla úspěšně upravena!', 'success')
        return redirect(url_for('workshifts_categories_list'))
    
    return render_template('workshifts_category_edit.html', category=category)
