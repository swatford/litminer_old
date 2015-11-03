from ming_models.model import session
from ming import schema
from ming.odm import (MappedClass,FieldProperty)
from collections import OrderedDict
from datetime import datetime

__author__ = 'swatford'

class TermInTree(MappedClass):
    tree_numbers = FieldProperty(schema.Array(schema.String))

    # used for querying tree ex. db.descriptor.find({parents:"A02"})
    parents = FieldProperty(schema.Array(schema.String))

    def __init__(self,record):
        super(TermInTree,self).__init__()
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
                                self.parents.append(previous_node)
                            else:
                                self.parents.append(node)
                                previous_node = node


class MeshTerm(MappedClass):
    class __mongometa__:
        session = session
        name = "mesh"
        polymorphic_on = "_type"
        polymorphic_identity = "base"

    _id = FieldProperty(schema.String)

    name = FieldProperty(schema.String)
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

    def __init__(self,record):
        super(MeshTerm,self).__init__(record)
        if record is not None:

            if type(self).__name__ == "Descriptor":
                self._id = record["DescriptorUI"]
                self.name = record["DescriptorName"]["String"]
            elif type(self).__name__ == "Qualifier":
                self._id = record["QualifierUI"]
                self.name = record["QualifierName"]["String"]
            elif type(self).__name__ == "SupplementaryConceptRecord":
                self.uid = record["SupplementalRecordUI"]
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

            self.date_created = datetime.strptime(" ".join([record["DateCreated"]["Year"],
                                          record["DateCreated"]["Month"],
                                          record["DateCreated"]["Day"]]),
                                                  "%Y %m %d") if "DateCreated" in record else None

            self.date_establisted = datetime.strptime(" ".join([record["DateEstablished"]["Year"],
                                              record["DateEstablished"]["Month"],
                                              record["DateEstablished"]["Day"]]),
                                                      "%Y %m %d") if "DateEstablished" in record else None

            self.date_revised = datetime.strptime(" ".join([record["DateRevised"]["Year"],
                                          record["DateRevised"]["Month"],
                                          record["DateRevised"]["Day"]]),
                                                  "%Y %m %d") if "DateRevised" in record else None

            self.history_note = record["HistoryNote"] if "HistoryNote" in record else None
            self.online_note = record["OnlineNote"] if "OnlineNote" in record else None
            self.public_mesh_note = record["PublicMeSHNote"] if "PublicMeSHNote" in record else None
