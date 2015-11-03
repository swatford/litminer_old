from collections import OrderedDict

from ming import schema
from ming.odm import (FieldProperty)

from litminer.ming_models.model.mbr import MeshTerm

__author__ = 'swatford'

class Descriptor(MeshTerm):
    class __mongometa__:
        polymorphic_identity = "d"

    _type = FieldProperty(schema.String(if_missing="d"))

    def __init__(self,record:OrderedDict=None,*args,**kwargs):
        super(Descriptor,self).__init__(record=record,*args,**kwargs)