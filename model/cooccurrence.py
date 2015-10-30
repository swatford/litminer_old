from mongoengine import Document,StringField,IntField,FloatField

__author__ = 'swatford'

class CoOccurrence(Document):
    uid1 = StringField(required=True)
    uid2 = StringField(required=True)