from model import (Document,IntField,BinaryField,ListField,DictField)

__author__ = 'swatford'

class CoOccurrence(Document):
    pmid = IntField(required=True)
    both_major_topic = BinaryField()
    uids = ListField(unique=True,required=True)
    uid1 = DictField()
    uid2 = DictField()
    meta = {
        "indexes": [
            "uids",
            "pmid"
        ]
    }

    def __init__(self,record,*args,**kwargs):
        Document.__init__(self,*args,**kwargs)
