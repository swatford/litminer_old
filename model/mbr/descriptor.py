from mongoengine import (Document,StringField,ListField,DateTimeField,
                         ReferenceField,DictField)
from collections import OrderedDict

__author__ = "swatford"

class Descriptor(Document):
    """Model for a MeSH Descriptor record"""

    uid = StringField(required=True,primary_key=True)
    name = StringField(required=True,unique=True)

    # change to ReferenceField
    allowable_qualifiers = ListField()

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

    # reference uid from descriptor
    # update to ReferenceField if create collection for PharmacologicalAction
    pharmacological_actions = ListField()

    # only name. does not correspond to uid
    previous_indexings = ListField()

    # not yet implemented
    record_originators = ListField(DictField())

    tree_numbers = ListField()

    # used for querying tree ex. db.descriptor.find({parents:"A02"})
    parents = ListField()

    def __init__(self,record: OrderedDict = None,*args,**kwargs):
        """Constructor for the MeSH Descriptor Record.
        Takes OrderedDict object from xmltodict output.
        Original source is xml download of descXXXX
        renamed and compressed to descXXXX.xml.gz"""

        Document.__init__(self,*args,**kwargs)

        self.uid = record["DescriptorUI"]
        self.name = record["DescriptorName"]["String"]

        if "AllowableQualifiersList" in record:
            if isinstance(record["AllowableQualifiersList"]["AllowableQualifier"],list):
                self.allowable_qualifiers = [q["QualifierReferredTo"]["QualifierUI"]
                                             for q in record[
                                                 "AllowableQualifiersList"][
                                                 "AllowableQualifier"]]
            else:
                self.allowable_qualifiers = [record["AllowableQualifiersList"]["AllowableQualifier"][
                                                 "QualifierReferredTo"]["QualifierUI"]]

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

        if "PharmacologicalActionList" in record:
            if isinstance(record["PharmacologicalActionList"]["PharmacologicalAction"],list):
                self.pharmacological_actions = [
                    pa["DescriptorReferredTo"]["DescriptorUI"]
                    for pa in
                    record["PharmacologicalActionList"]["PharmacologicalAction"]]
            else:
                self.pharmacological_actions = [
                    record["PharmacologicalActionList"]["PharmacologicalAction"]["DescriptorReferredTo"]["DescriptorUI"]]
        if "PreviousIndexingList" in record:
            if isinstance(record["PreviousIndexingList"],list):
                self.previous_indexings = record["PreviousIndexingList"]["PreviousIndexing"]
            else:
                self.previous_indexings = [record["PreviousIndexingList"]["PreviousIndexing"]]

#         self.record_originators

        if "TreeNumberList" in record:
            if isinstance(record["TreeNumberList"]["TreeNumber"],list):
                self.tree_numbers = record["TreeNumberList"]["TreeNumber"]
            else:
                self.tree_numbers = [record["TreeNumberList"]["TreeNumber"]]

            self.parents = []
            for tn in self.tree_numbers:
                previous_node = None
                for node in tn.split("."):
                    if previous_node is not None:
                        previous_node = ".".join([previous_node,node])
                        self.parents.append(previous_node)
                    else:
                        self.parents.append(node)
                        previous_node = node