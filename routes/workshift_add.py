from . import *
from datetime import datetime

def workshift_add():
    if request.method == 'POST':
        name = request.form['name']
        start_date_str = request.form['start_date']
        time_start_str = request.form['time_start']
        time_end_str = request.form['time_end']
        category_id = request.form['category_id']

        # Převod řetězců na objekty date a time
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        time_start = datetime.strptime(time_start_str, '%H:%M').time()
        time_end = datetime.strptime(time_end_str, '%H:%M').time()

        new_workshift = Workshift(name=name, start_date=start_date, time_start=time_start, time_end=time_end, category_id=category_id)
        db.session.add(new_workshift)
        db.session.commit()
        flash('Směna byla úspěšně přidána!', 'success')
        return redirect(url_for('workshifts_list'))
    
    categories = WorkshiftsCategory.query.all()
    return render_template('workshift_add.html', categories=categories)
