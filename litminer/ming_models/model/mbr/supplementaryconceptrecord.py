from litminer.ming_models.model.mbr import MeshTerm,TermPreviouslyIndexed
from ming import schema
from ming.odm import (FieldProperty)

class SupplementaryConceptRecord(TermPreviouslyIndexed,MeshTerm):

    frequency = FieldProperty(schema.Int)
    note = FieldProperty(schema.String)
    mapped_to_headings = FieldProperty(schema.Array(schema.String))
    sources = FieldProperty(schema.Array(schema.String))

    previous_indexings = FieldProperty(schema.Array(schema.String))
    _type = FieldProperty(schema.String(if_missing="c"))

    def __init__(self,*args,**kwargs):

        record = kwargs.get("record",None)
        super(SupplementaryConceptRecord,self).__init__(*args,**kwargs)

        if record is not None:
            self.frequency = int(record["Frequency"]) if "Frequency" in record else None
            self.note = record["Note"] if "Note" in record else None

            if "HeadingMappedToList" in record:
                heading_mapped_to_list = record["HeadingMappedToList"]["HeadingMappedTo"]
                if isinstance(heading_mapped_to_list,list):
                    for ref in heading_mapped_to_list:
                        if "DescriptorReferredTo" in ref:
                            self.mapped_to_headings.append(ref["DescriptorReferredTo"]["DescriptorUI"].replace("*",""))
                        elif "QualifierReferredTo" in ref:
                            self.mapped_to_headings.append(ref["QualifierReferredTo"]["QualifierUI"].replace("*",""))
                else:
                    if "DescriptorReferredTo" in heading_mapped_to_list:
                        self.mapped_to_headings.append(
                            heading_mapped_to_list["DescriptorReferredTo"]["DescriptorUI"].replace("*",""))
                    if "QualifierReferredTo" in heading_mapped_to_list:
                        self.mapped_to_headings.append(
                            heading_mapped_to_list["QualifierReferredTo"]["QualifierUI"].replace("*",""))

            if "SourceList" in record:
                if isinstance(record["SourceList"]["Source"],list):
                    self.sources = record["SourceList"]["Source"]
                else:
                    self.sources = [record["SourceList"]["Source"]]