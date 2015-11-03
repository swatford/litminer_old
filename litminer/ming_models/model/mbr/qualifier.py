from ming import schema
from ming.odm import (FieldProperty)

from litminer.ming_models.model.mbr import (MeshTerm,TermInTree)

__author__ = 'swatford'

class Qualifier(MeshTerm,TermInTree):
    class __mongometa__:
        polymorphic_identity = "q"

    annotation = FieldProperty(schema.String)

    tree_nodes_allowed = FieldProperty(schema.Array(schema.String))

    _type = FieldProperty(schema.String(if_missing="q"))

    def __init__(self,record,*args,**kwargs):
        super(Qualifier,self).__init__(record,*args,**kwargs)
        if record is not None:
            if "TreeNodeAllowedList" in record:
                if isinstance(record["TreeNodeAllowedList"]["TreeNodeAllowed"],list):
                    self.tree_nodes_allowed = record["TreeNodeAllowedList"]["TreeNodeAllowed"]
                else:
                    self.tree_nodes_allowed = [record["TreeNodeAllowedList"]["TreeNodeAllowed"]]

            self.annotation = record["Annotation"] if "Annotation" in record else None