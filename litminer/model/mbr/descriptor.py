from collections import OrderedDict

from mongoengine import (ListField,ReferenceField)

from litminer.model.mbr import MeshTerm
from litminer.model.mbr import Qualifier

__author__ = "swatford"

class Descriptor(MeshTerm):
    """Model for a MeSH Descriptor record"""

    allowable_qualifiers = ListField(ReferenceField(Qualifier))

    # reference uid from descriptor
    # update to ReferenceField if create collection for PharmacologicalAction
    pharmacological_actions = ListField()

    # only name. does not correspond to uid
    previous_indexings = ListField()

    tree_numbers = ListField()

    # used for querying tree ex. db.descriptor.find({parents:"A02"})
    parents = ListField()

    meta = {
        "indexes": [
            "tree_numbers"
        ]
    }

    def __init__(self,record: OrderedDict = None,*args,**kwargs):
        """Constructor for the MeSH Descriptor Record.
        Takes OrderedDict object from xmltodict output.
        Original source is xml download of descXXXX
        renamed and compressed to descXXXX.xml.gz"""
        qualifers = kwargs.pop("qualifiers",None)
        super(Descriptor,self).__init__(record,*args,**kwargs)
        if record is not None:
            if "AllowableQualifiersList" in record:
                if "qualifiers" is not None:
                    if isinstance(record["AllowableQualifiersList"]["AllowableQualifier"],list):
                        self.allowable_qualifiers = [qualifers[q["QualifierReferredTo"]["QualifierUI"]]
                                                     for q in record[
                                                         "AllowableQualifiersList"][
                                                         "AllowableQualifier"]]
                    else:
                        self.allowable_qualifiers = [qualifers[record["AllowableQualifiersList"]["AllowableQualifier"][
                                                         "QualifierReferredTo"]["QualifierUI"]]]

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