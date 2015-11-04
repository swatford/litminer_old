from ming import schema
from ming.odm import (FieldProperty,RelationProperty,ForeignIdProperty)

from litminer.ming_models.model.mbr import (MeshTerm,TermInTree)

__author__ = 'swatford'

class Qualifier(TermInTree,MeshTerm):
    class __mongometa__:
        polymorphic_identity = "q"

    annotation = FieldProperty(schema.String)

    tree_nodes_allowed = FieldProperty(schema.Array(schema.String))

    tree_numbers = FieldProperty(schema.Array(schema.String))

    # used for querying tree ex. db.descriptor.find({parents:"A02"})
    parents = FieldProperty(schema.Array(schema.String),index=True)

    _type = FieldProperty(schema.String(if_missing="q"))

    def __init__(self,*args,**kwargs):
        record = kwargs.get("record",None)
        super(Qualifier,self).__init__(*args,**kwargs)
        if record is not None:
            if "TreeNodeAllowedList" in record:
                if isinstance(record["TreeNodeAllowedList"]["TreeNodeAllowed"],list):
                    self.tree_nodes_allowed = record["TreeNodeAllowedList"]["TreeNodeAllowed"]
                else:
                    self.tree_nodes_allowed = [record["TreeNodeAllowedList"]["TreeNodeAllowed"]]

            if "Annotation" in record:
                self.annotation = record["Annotation"]
