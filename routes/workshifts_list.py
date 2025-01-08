from . import *

def workshifts_list():
    workshifts = Workshift.query.all()
    return render_template('workshifts_list.html', workshifts=workshifts)
