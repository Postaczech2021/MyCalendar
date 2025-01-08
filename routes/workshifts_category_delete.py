from . import *

def workshifts_category_delete(category_id):
    category = WorkshiftsCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Kategorie byla úspěšně smazána!', 'success')
    return redirect(url_for('workshifts_categories_list'))
