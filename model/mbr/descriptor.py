from mongoengine import (StringField,ListField,DateTimeField,DictField)
from model.mbr import MeshTerm
from collections import OrderedDict

__author__ = "swatford"

class Descriptor(MeshTerm):
    """Model for a MeSH Descriptor record"""

    allowable_qualifiers = ListField()

    # reference uid from descriptor
    # update to ReferenceField if create collection for PharmacologicalAction
    pharmacological_actions = ListField()

    # only name. does not correspond to uid
    previous_indexings = ListField()

    def __init__(self,record: OrderedDict = None,*args,**kwargs):
        """Constructor for the MeSH Descriptor Record.
        Takes OrderedDict object from xmltodict output.
        Original source is xml download of descXXXX
        renamed and compressed to descXXXX.xml.gz"""

        super(Descriptor,self).__init__(record,*args,**kwargs)
        if record is not None:
            if "AllowableQualifiersList" in record:
                if isinstance(record["AllowableQualifiersList"]["AllowableQualifier"],list):
                    self.allowable_qualifiers = [q["QualifierReferredTo"]["QualifierUI"]
                                                 for q in record[
                                                     "AllowableQualifiersList"][
                                                     "AllowableQualifier"]]
                else:
                    self.allowable_qualifiers = [record["AllowableQualifiersList"]["AllowableQualifier"][
                                                     "QualifierReferredTo"]["QualifierUI"]]

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