from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import input_required


class MetadataRecordForm(FlaskForm):

    collection_key = StringField(
        label='Metadata collection',
        validators=[input_required()],
    )

    schema_key = StringField(
        label='Metadata schema',
        validators=[input_required()],
    )

    metadata = TextAreaField(
        label='Metadata dictionary',
        validators=[input_required()],
    )

    doi = StringField(
        label='DOI',
    )

    auto_assign_doi = BooleanField(
        label='Auto-assign DOI?',
    )
