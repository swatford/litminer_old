from collections import OrderedDict

from mongoengine import (Document,EmbeddedDocument, IntField,StringField,DateTimeField,
                         ListField, BooleanField,EmbeddedDocumentListField)

__author__ = 'swatford'

class Article(Document):
    pmid = IntField(required=True,primary_key=True)
    version = IntField()
    mesh_terms = EmbeddedDocumentListField()
    date_created = DateTimeField()
    date_completed = DateTimeField()
    date_revised = DateTimeField()
    chemicals = ListField()

    def __init__(self,record:OrderedDict=None,*args,**kwargs):

        super(Article,self).__init__(*args,**kwargs)

        if record is not None:
            self.pmid = record["PMID"]["#text"]
            self.version = record["PMID"]["@Version"] if "@Version" in record["PMID"] else None

            self.date_created = ",".join([record["DateCreated"]["Year"],
                                          record["DateCreated"]["Month"],
                                          record["DateCreated"]["Day"]]) if "DateCreated" in record else None

            self.date_establisted = ",".join([record["DateEstablished"]["Year"],
                                              record["DateEstablished"]["Month"],
                                              record["DateEstablished"]["Day"]]) if "DateEstablished" in record else None

            self.date_revised = ",".join([record["DateRevised"]["Year"],
                                          record["DateRevised"]["Month"],
                                          record["DateRevised"]["Day"]]) if "DateRevised" in record else None

            if "ChemicalList" in record:
                if isinstance(record["ChemicalList"]["Chemical"],list):
                    self.chemicals = [uid["NameOfSubstance"]["@UI"] for uid in record["ChemicalList"]["Chemical"]]
                    # uids = [uid["NameOfSubstance"]["@UI"] for uid in record["ChemicalList"]["Chemical"]]
                    # (self.chemicals.append(c) for c in MeshTerm.objects(uid__in=uids))
                else:
                    self.chemicals.append(record["ChemicalList"]["Chemical"][
                        "NameOfSubstance"]["@UI"])
                    # (self.chemicals.append(MeshTerm.objects(uid=record["ChemicalList"]["Chemical"][
                    #     "NameOfSubstance"]["@UI"])))

            # if "MeshHeadingList" in record:
            #     uids = []
            #     # if isinstance(record["MeshHeadingList"]["MeshHeading"],list):
            #     for term in record["MeshHeadingList"]["MeshHeading"]:
            #         if "DescriptorName" in term:
            #             uids.append(term["DescriptorName"]["@UI"])
            #             if "QualifierName" in term:
            #                 uids.append(term["QualifierName"]["@UI"])
            #     terms = {}
            #     for term in MeshTerm.objects(uid__in=uids):
            #         terms[term.uid] = term
            #     for term in record["MeshHeadingList"]["MeshHeading"]:
            #         tag = MeshTag()
            #         if "DescriptorName" in term:
            #             tag.descriptor = terms[term["DescriptorName"]["@UI"]]
            #             tag.descriptor_major_topic = (1,0)[term["DescriptorName"]["@MajorTopicYN"] == "Y"]
            #             if "QualifierName" in term:
            #                 tag.qualifier = terms[term["QualifierName"]["@UI"]]
            #                 tag.qualifier_major_topic = (1,0)[term["QualifierName"]["@MajorTopic"] == "Y"]
            #                 uids.append(term["QualifierName"]["@UI"])
            #         self.mesh_terms.append(tag)

            if "MeshHeadingList" in record:
                # uids = []
                # if isinstance(record["MeshHeadingList"]["MeshHeading"],list):
                # for term in record["MeshHeadingList"]["MeshHeading"]:
                #     if "DescriptorName" in term:
                #         uids.append(term["DescriptorName"]["@UI"])
                #         if "QualifierName" in term:
                #             uids.append(term["QualifierName"]["@UI"])
                # terms = {}
                # for term in MeshTerm.objects(uid__in=uids):
                #     terms[term.uid] = term
                for term in record["MeshHeadingList"]["MeshHeading"]:
                    tag = None
                    if "DescriptorName" in term:
                        tag.descriptor = term["DescriptorName"]["@UI"]
                        tag.descriptor_major_topic = (1,0)[term["DescriptorName"]["@MajorTopicYN"] == "Y"]
                        if "QualifierName" in term:
                            tag.qualifier = term["QualifierName"]["@UI"]
                            tag.qualifier_major_topic = (1,0)[term["QualifierName"]["@MajorTopic"] == "Y"]
                    self.mesh_terms.append(tag)