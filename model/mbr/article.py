from model import (Document,IntField,
                   DateTimeField,StringField,ListField)

__author__ = 'swatford'

class Article(Document):
    pmid = IntField(primary_key=True)
    version = IntField()
    title = StringField()
    date_created = DateTimeField()
    date_completed = DateTimeField()
    date_revised = DateTimeField()
    chemicals = ListField()
