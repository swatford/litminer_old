from collections import OrderedDict

from mongoengine import (StringField,ListField)

from litminer.model.mbr import MeshTerm

__author__ = 'swatford'

class Qualifier(MeshTerm):

    annotation = StringField()

    tree_nodes_allowed = ListField()

    tree_numbers = ListField()

    # used for querying tree ex. db.descriptor.find({parents:"A02"})
    parents = ListField()

    meta = {
        "indexes": [
            "tree_numbers"
        ]
    }

    def __init__(self,record: OrderedDict = None,*args,**kwargs):

        super(Qualifier,self).__init__(record,*args,**kwargs)
        if record is not None:
            if "TreeNodeAllowedList" in record:
                if isinstance(record["TreeNodeAllowedList"]["TreeNodeAllowed"],list):
                    self.tree_nodes_allowed = record["TreeNodeAllowedList"]["TreeNodeAllowed"]
                else:
                    self.tree_nodes_allowed = [record["TreeNodeAllowedList"]["TreeNodeAllowed"]]

            self.annotation = record["Annotation"] if "Annotation" in record else None

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
