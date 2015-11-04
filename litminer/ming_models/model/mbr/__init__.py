from ming import schema
from ming.odm import (MappedClass,FieldProperty)
from datetime import datetime
from litminer.ming_models import session

__author__ = 'swatford'

class TermPreviouslyIndexed():

    def __init__(self,*args,**kwargs):
        record = kwargs.get("record",None)
        super(TermPreviouslyIndexed,self).__init__(*args,**kwargs)
        if record is not None:
            if "PreviousIndexingList" in record:
                if isinstance(record["PreviousIndexingList"]["PreviousIndexing"],list):
                    self.previous_indexings = record["PreviousIndexingList"]["PreviousIndexing"]
                else:
                    self.previous_indexings = [record["PreviousIndexingList"]["PreviousIndexing"]]
class TermInTree():

    def __init__(self,*args,**kwargs):
        record = kwargs.get("record",None)
        super(TermInTree,self).__init__(*args,**kwargs)
        if record is not None:
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
                                if previous_node not in self.tree_numbers:
                                    self.parents.append(previous_node)
                            else:
                                if node not in self.tree_numbers:
                                    self.parents.append(node)
                                    previous_node = node


class MeshTerm(MappedClass):
    class __mongometa__:
        session = session
        name = "mesh"
        polymorphic_on = "_type"
        polymorphic_identity = "base"

    _id = FieldProperty(schema.String)
    uid = FieldProperty(schema.String,index=True)

    name = FieldProperty(schema.String,index=True)
    concepts = FieldProperty(schema.Array(schema.Object({
        "cuid": schema.String,
        "preferred": schema.Bool
    })))
    active_mesh_years = FieldProperty(schema.Array(schema.String))

    date_created = FieldProperty(schema.DateTime)
    date_established = FieldProperty(schema.DateTime)
    date_revised = FieldProperty(schema.DateTime)

    history_note = FieldProperty(schema.String)
    online_note = FieldProperty(schema.String)
    public_mesh_note = FieldProperty(schema.String)

    # not yet implemented
    record_originators = FieldProperty(schema.Array(schema.Object({})))

    _type = FieldProperty(schema.String(if_missing="base"))

    def __init__(self,*args,**kwargs):

        record = kwargs.pop("record",None)
        super(MeshTerm,self).__init__()

        if record is not None:

            if type(self).__name__ == "Descriptor":
                self._id = record["DescriptorUI"]
                self.uid = self._id
                self.name = record["DescriptorName"]["String"]
            elif type(self).__name__ == "Qualifier":
                self._id = record["QualifierUI"]
                self.uid = self._id
                self.name = record["QualifierName"]["String"]
            elif type(self).__name__ == "SupplementaryConceptRecord":
                self._id = record["SupplementalRecordUI"]
                self.uid = self._id
                self.name = record["SupplementalRecordName"]["String"]

            if "ConceptList" in record:
                if isinstance(record["ConceptList"]["Concept"],list):
                    self.concepts = [{"cuid":c["ConceptUI"],
                                      "preferred":(c["@PreferredConceptYN"]=="Y")} for c in record[
                        "ConceptList"][
                        "Concept"]]
                else:
                    self.concepts = [{"cuid":record["ConceptList"]["Concept"]["ConceptUI"],
                                      "preferred":(record[
                        "ConceptList"]["Concept"]["@PreferredConceptYN"]=="Y")}]

            if "ActiveMeSHYearList" in record:
                if isinstance(record["ActiveMeSHYearList"]["Year"],list):
                    self.active_mesh_years = record["ActiveMeSHYearList"]["Year"]
                else:
                    self.active_mesh_years = [record["ActiveMeSHYearList"]["Year"]]

            if "DateCreated" in record:
                self.date_created = datetime.strptime(" ".join([record["DateCreated"]["Year"],
                                              record["DateCreated"]["Month"],
                                              record["DateCreated"]["Day"]]),
                                                      "%Y %m %d")
            if "DateEstablished" in record:
                self.date_establisted = datetime.strptime(" ".join([record["DateEstablished"]["Year"],
                                                  record["DateEstablished"]["Month"],
                                                  record["DateEstablished"]["Day"]]),
                                                          "%Y %m %d")

            if "DateRevised" in record:
                self.date_revised = datetime.strptime(" ".join([record["DateRevised"]["Year"],
                                                                record["DateRevised"]["Month"],
                                                                record["DateRevised"]["Day"]]),
                                                                "%Y %m %d")

            if "HistoryNote" in record:
                self.history_note = record["HistoryNote"]

            if "OnlineNote" in record:
                self.online_note = record["OnlineNote"]

            if "PublicMeSHNote" in record:
                self.public_mesh_note = record["PublicMeSHNote"]