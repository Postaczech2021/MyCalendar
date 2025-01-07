from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from models import EventCategory
import re

def validate_date_format(form, field):
    if not re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', field.data):
        raise ValidationError('Datum musí být ve formátu d.m.Y')

class EventForm(FlaskForm):
    name = StringField('Název', validators=[DataRequired()])
    description = TextAreaField('Popis', validators=[Optional()])
    category = SelectField('Kategorie', choices=[], coerce=int, validators=[DataRequired()])
    start_date = StringField('Začátek', validators=[DataRequired(), validate_date_format], render_kw={"placeholder": "d.m.Y"})
    end_date = StringField('Konec', validators=[DataRequired(), validate_date_format], render_kw={"placeholder": "d.m.Y"})
    done = BooleanField('Dokončeno')
    submit = SubmitField('Uložit')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in EventCategory.query.all()]
