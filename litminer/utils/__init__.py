from gzip import GzipFile
from os import listdir
from litminer.ming_models import session
import xmltodict as xtd

from litminer.ming_models.model.mbr.descriptor import  Descriptor
from litminer.ming_models.model.mbr.qualifier import Qualifier
from litminer.ming_models.model.mbr.supplementaryconceptrecord import SupplementaryConceptRecord
# from litminer.ming_models.model.mbr import Article

__author__ = 'swatford'


class MeshImporter():
    container = []
    qualifiers = {}

    def handle_descriptor_record(self,_,desc):
        # d = Descriptor(desc,qualifiers = self.qualifiers)
        d = Descriptor(record=desc)
        self.container.append(d)
        if len(self.container)>50:
            session.flush()
            session.clear()
            self.container = []
        print(d._id)
        return True

    def handle_qualifier_record(self,_,qualifier):
        q = Qualifier(record=qualifier)
        # self.container.append(q)
        self.qualifiers[q._id] = q
        print(q._id)
        return True

    def handle_scr_record(self,_,scr):
        s = SupplementaryConceptRecord(record=scr)
        self.container.append(s)
        if len(self.container)>50:
            session.flush()
            session.clear()
            self.container = []
        print(s._id)
        return True

    def _import_descriptors(self,path):
        xtd.parse(GzipFile(path),
              item_depth=2,
              item_callback=self.handle_descriptor_record)

    def _import_qualifiers(self,path):
        xtd.parse(GzipFile(path),
              item_depth=2,item_callback=self.handle_qualifier_record)

    def _import_scrs(self,path):
        xtd.parse(GzipFile(path),
                  item_depth=2,item_callback=self.handle_scr_record)

    def __init__(self,root=None,descriptor_fn=None,qualifier_fn=None,scr_fn=None):
        self._import_qualifiers("/".join([root,qualifier_fn])) if qualifier_fn is not None else None
        session.flush()
        session.clear()

        self._import_descriptors("/".join([root,descriptor_fn])) if descriptor_fn is not None else None
        session.flush()
        session.clear()
        self.container = []

        self._import_scrs("/".join([root,scr_fn])) if scr_fn is not None else None
        session.flush()
        session.clear()
        self.container = []

# class ArticleImporter():
#
#     container = []
#     qualifiers = {}
#
#     def handle_article_record(self,_,article):
#         a = Article(article)
#         self.container.append(a)
#         print(a.pmid)
#         if len(self.container)>50:
#             Article.objects.insert(self.container)
#             self.container = []
#         return True
#
#     def _import_articles(self,path):
#         xtd.parse(GzipFile(path),
#                   item_depth=2,item_callback=self.handle_article_record)
#
#     def __init__(self,root=None):
#         for fn in listdir(root):
#             if fn.split(".")[-1] == "gz":
#                 self._import_articles("/".join([root,fn]))
#         Article.objects.insert(self.container) if len(self.container)>0 else None
#         self.container = []