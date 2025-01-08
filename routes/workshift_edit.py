from . import *
from datetime import datetime

def workshift_edit(workshift_id):
    workshift = Workshift.query.get_or_404(workshift_id)
    
    if request.method == 'POST':
        workshift.name = request.form['name']
        start_date_str = request.form['start_date']
        time_start_str = request.form['time_start']
        time_end_str = request.form['time_end']
        category_id = request.form['category_id']

        # Převod řetězců na objekty date a time
        workshift.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        workshift.time_start = datetime.strptime(time_start_str, '%H:%M').time()
        workshift.time_end = datetime.strptime(time_end_str, '%H:%M').time()
        workshift.category_id = category_id

        db.session.commit()
        flash('Směna byla úspěšně upravena!', 'success')
        return redirect(url_for('workshifts_list'))
    
    categories = WorkshiftsCategory.query.all()
    return render_template('workshift_edit.html', workshift=workshift, categories=categories)
