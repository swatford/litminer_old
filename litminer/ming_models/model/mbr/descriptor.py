from collections import OrderedDict

from ming import schema
from ming.odm import (FieldProperty)
from litminer.ming_models.model.mbr import MeshTerm,TermInTree,TermPreviouslyIndexed

class Descriptor(TermInTree,TermPreviouslyIndexed,MeshTerm):
    """Model for a MeSH Descriptor record"""
    class __mongometa__:
        polymorphic_identity = "d"

    # reference uid from qualifier
    allowable_qualifiers = FieldProperty(schema.Array(schema.String))

    # reference uid from descriptor
    pharmacological_actions = FieldProperty(schema.Array(schema.String))

    tree_numbers = FieldProperty(schema.Array(schema.String))

    # used for querying tree ex. db.descriptor.find({parents:"A02"})
    parents = FieldProperty(schema.Array(schema.String),index=True)

    previous_indexings = FieldProperty(schema.Array(schema.String))

    _type = FieldProperty(schema.String(if_missing="d"))

    def __init__(self,*args,**kwargs):
        """Constructor for the MeSH Descriptor Record.
        Takes OrderedDict object from xmltodict output.
        Original source is xml download of descXXXX
        renamed and compressed to descXXXX.xml.gz"""

        record = kwargs.get("record",None)
        super(Descriptor,self).__init__(*args,**kwargs)

        if record is not None:
            if "AllowableQualifiersList" in record:
                if "qualifiers" is not None:
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