from mongoengine import (StringField,ListField,DateTimeField)
from model.mbr import MeshTerm
from collections import OrderedDict

__author__ = 'swatford'

class Qualifier(MeshTerm):

    annotation = StringField()

    tree_nodes_allowed = ListField()

    def __init__(self,record: OrderedDict = None,*args,**kwargs):

        super(Qualifier,self).__init__(record,*args,**kwargs)
        if record is not None:
            if "TreeNodeAllowedList" in record:
                if isinstance(record["TreeNodeAllowedList"]["TreeNodeAllowed"],list):
                    self.tree_nodes_allowed = record["TreeNodeAllowedList"]["TreeNodeAllowed"]
                else:
                    self.tree_nodes_allowed = [record["TreeNodeAllowedList"]["TreeNodeAllowed"]]

            self.annotation = record["Annotation"] if "Annotation" in record else None
