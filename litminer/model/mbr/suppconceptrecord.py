from collections import OrderedDict

from mongoengine import (IntField,ListField,GenericReferenceField,StringField)

from litminer.model.mbr import MeshTerm
from litminer.model.mbr import Descriptor
from litminer.model.mbr import Qualifier

__author__ = 'swatford'

class SupplementaryConceptRecord(MeshTerm):
    frequency = IntField()
    note = StringField()
    mapped_to_headings = ListField(GenericReferenceField())
    sources = ListField()

    # only name. does not correspond to uid
    previous_indexings = ListField()

    def __init__(self,record: OrderedDict = None,*args,**kwargs):
        super(SupplementaryConceptRecord,self).__init__(record,*args,**kwargs)

        if record is not None:
            self.frequency = record["Frequency"] if "Frequency" in record else None
            self.note = record["Note"] if "Note" in record else None

            if "PreviousIndexingList" in record:
                if isinstance(record["PreviousIndexingList"],list):
                    self.previous_indexings = record["PreviousIndexingList"]["PreviousIndexing"]
                else:
                    self.previous_indexings = [record["PreviousIndexingList"]["PreviousIndexing"]]

            if "HeadingMappedToList" in record:
                descriptors = []
                qualifiers = []
                refs = []
                heading_mapped_to_list = record["HeadingMappedToList"]["HeadingMappedTo"]
                if isinstance(heading_mapped_to_list,list):
                    for ref in heading_mapped_to_list:
                        if "DescriptorReferredTo" in ref:
                            descriptors.append(ref["DescriptorReferredTo"]["DescriptorUI"].replace("*",""))
                        elif "QualifierReferredTo" in ref:
                            qualifiers.append(ref["QualifierReferredTo"]["QualifierUI"].replace("*",""))
                else:
                    if "DescriptorReferredTo" in heading_mapped_to_list:
                        descriptors.append(heading_mapped_to_list["DescriptorReferredTo"]["DescriptorUI"])
                    if "QualifierReferredTo" in heading_mapped_to_list:
                        qualifiers.append(heading_mapped_to_list["QualifierReferredTo"]["QualifierUI"])
                if len(descriptors)>0:
                    for d in Descriptor.objects(uid__in=descriptors):
                        refs.append(d)
                    (refs.append(d) for d in Descriptor.objects(uid__in=descriptors))
                if len(qualifiers)>0:
                    (refs.append(q) for q in Qualifier.objects(uid__in=qualifiers))
                if len(refs)>0:
                    self.mapped_to_headings = refs

            if "SourceList" in record:
                if isinstance(record["SourceList"]["Source"],list):
                    self.sources = record["SourceList"]["Source"]
                else:
                    self.sources = [record["SourceList"]["Source"]]