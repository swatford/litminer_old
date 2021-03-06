from mongoengine import (Document,StringField,
                         ListField,DictField,DateTimeField)
from collections import OrderedDict

__author__ = 'swatford'

class MeshTerm(Document):

    uid = StringField(required=True,primary_key=True)
    name = StringField(required=True)

    # required key of cuid
    concepts = ListField(DictField())

    # years are strings
    active_mesh_years = ListField()

    date_created = DateTimeField()
    date_establisted = DateTimeField()
    date_revised = DateTimeField()

    history_note = StringField()
    online_note = StringField()
    public_mesh_note = StringField()

    # not yet implemented
    record_originators = ListField(DictField())

    meta = {
        "allow_inheritance": True,
        "indexes": [
            "uid",
            "name"
        ]
    }

    def __init__(self,record: OrderedDict = None,*args,**kwargs):

        super(MeshTerm,self).__init__(*args,**kwargs)
        if record is not None:

            if type(self).__name__ == "Descriptor":
                self.uid = record["DescriptorUI"]
                self.name = record["DescriptorName"]["String"]
            elif type(self).__name__ == "Qualifier":
                self.uid = record["QualifierUI"]
                self.name = record["QualifierName"]["String"]
            elif type(self).__name__ == "SupplementaryConceptRecord":
                self.uid = record["SupplementalRecordUI"]
                self.name = record["SupplementalRecordName"]["String"]

            if "ConceptList" in record:
                if isinstance(record["ConceptList"]["Concept"],list):
                    self.concepts = [{"cuid":c["ConceptUI"],
                                      "preferred":(0,1)[c["@PreferredConceptYN"]=="Y"]} for c in record["ConceptList"][
                        "Concept"]]
                else:
                    self.concepts = [{"cuid":record["ConceptList"]["Concept"]["ConceptUI"],"preferred":(1,0)[record[
                        "ConceptList"]["Concept"]["@PreferredConceptYN"]=="Y"]}]

            if "ActiveMeSHYearList" in record:
                if isinstance(record["ActiveMeSHYearList"]["Year"],list):
                    self.active_mesh_years = record["ActiveMeSHYearList"]["Year"]
                else:
                    self.active_mesh_years = [record["ActiveMeSHYearList"]["Year"]]

            self.date_created = ",".join([record["DateCreated"]["Year"],
                                          record["DateCreated"]["Month"],
                                          record["DateCreated"]["Day"]]) if "DateCreated" in record else None

            self.date_establisted = ",".join([record["DateEstablished"]["Year"],
                                              record["DateEstablished"]["Month"],
                                              record["DateEstablished"]["Day"]]) if "DateEstablished" in record else None

            self.date_revised = ",".join([record["DateRevised"]["Year"],
                                          record["DateRevised"]["Month"],
                                          record["DateRevised"]["Day"]]) if "DateRevised" in record else None

            self.history_note = record["HistoryNote"] if "HistoryNote" in record else None
            self.online_note = record["OnlineNote"] if "OnlineNote" in record else None
            self.public_mesh_note = record["PublicMeSHNote"] if "PublicMeSHNote" in record else None