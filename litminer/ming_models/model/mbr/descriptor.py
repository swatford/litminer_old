from collections import OrderedDict

from ming import schema
from ming.odm import (FieldProperty,ForeignIdProperty,RelationProperty)
from litminer.ming_models.model.mbr.qualifier import Qualifier
from litminer.ming_models.model.mbr import MeshTerm,TermInTree

__author__ = 'swatford'

class Descriptor(MeshTerm,TermInTree):
    class __mongometa__:
        polymorphic_identity = "d"

    """Model for a MeSH Descriptor record"""

    _allowable_qualifiers = ForeignIdProperty("Qualifier",uselist=True)
    allowable_qualifiers = RelationProperty("Qualifier")

    # reference uid from descriptor
    # update to ReferenceField if create collection for PharmacologicalAction
    # pharmacological_actions = FieldProperty(schema.Array(schema.String))

    # only name. does not correspond to uid
    previous_indexings = FieldProperty(schema.Array(schema.String))

    _type = FieldProperty(schema.String(if_missing="d"))

    def __init__(self,record,*args,**kwargs):
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

            # if "PharmacologicalActionList" in record:
            #     if isinstance(record["PharmacologicalActionList"]["PharmacologicalAction"],list):
            #         self.pharmacological_actions = [
            #             pa["DescriptorReferredTo"]["DescriptorUI"]
            #             for pa in
            #             record["PharmacologicalActionList"]["PharmacologicalAction"]]
            #     else:
            #         self.pharmacological_actions = [
            #             record["PharmacologicalActionList"]["PharmacologicalAction"]["DescriptorReferredTo"]["DescriptorUI"]]

            if "PreviousIndexingList" in record:
                if isinstance(record["PreviousIndexingList"],list):
                    self.previous_indexings = record["PreviousIndexingList"]["PreviousIndexing"]
                else:
                    self.previous_indexings = [record["PreviousIndexingList"]["PreviousIndexing"]]