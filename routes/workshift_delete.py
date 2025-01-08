from . import *

def workshift_delete(workshift_id):
    workshift = Workshift.query.get_or_404(workshift_id)
    db.session.delete(workshift)
    db.session.commit()
    flash('Směna byla úspěšně smazána!', 'success')
    return redirect(url_for('workshifts_list'))
