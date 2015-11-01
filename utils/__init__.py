import xmltodict as xtd
from gzip import GzipFile
from model.mbr.descriptor import Descriptor
from model.mbr.qualifier import Qualifier
from model.mbr import MeshTerm

__author__ = 'swatford'


class MeshImporter():
    container = []

    def handle_descriptor_record(self,_,desc):
        d = Descriptor(desc)
        # d._created = True
        self.container.append(d)
        if len(self.container)>50:
            MeshTerm.objects.insert(self.container)
            self.container = []
        print(d.uid)
        return True

    def handle_qualifier_record(self,_,qualifier):
        q = Qualifier(qualifier)
        # q._created = True
        self.container.append(q)
        if len(self.container)>50:
            MeshTerm.objects.insert(self.container)
            self.container = []
        print(q.uid)
        return True

    def _import_descriptors(self,path):
        xtd.parse(GzipFile(path),
              item_depth=2,
              item_callback=self.handle_descriptor_record)

    def _import_qualifiers(self,path):
        xtd.parse(GzipFile(path),
              item_depth=2,item_callback=self.handle_qualifier_record)

    def _import_scrs(path):
        pass

    def __init__(self,root=None,descriptor_fn=None,qualifier_fn=None,scr_fn=None):
        self._import_descriptors("/".join([root,descriptor_fn])) if descriptor_fn is not None else None
        MeshTerm.objects.insert(self.container) if len(self.container)>0 else None
        self.container = []
        self._import_qualifiers("/".join([root,qualifier_fn])) if qualifier_fn is not None else None
        Qualifier.objects.insert( self.container) if len(self.container)>0 else None
        self.container = []
        self._import_scrs("/".join([root,scr_fn])) if scr_fn is not None else None

