from utils import MeshImporter
from utils import ArticleImporter
from gzip import GzipFile
import xmltodict as xtd
from os import listdir

__author__ = 'swatford'


def main(*args,**kwargs):

    from ming_models.model.mbr.descriptor import Descriptor
    from ming_models.model.mbr.qualifier import Qualifier
    from ming_models.model.mbr import MeshTerm
    from ming_models.model import session

    def handle_d(_,desc):
        d = Descriptor(desc)
        print(d._id)
        return True

    def handle_q(_,qual):
        q = Qualifier(qual)
        print(q._id)
        return True

    # xtd.parse(GzipFile("/media/swatford/elements/medline/mesh/desc2015.xml.gz"),
    #           item_depth=2,item_callback=handle_d)

    xtd.parse(GzipFile("/media/swatford/elements/medline/mesh/qual2015.xml.gz"),
              item_depth=2,item_callback=handle_q)

    session.flush()
    session.clear()
    session.close()

    # MESH_PATH = "/media/swatford/elements/medline/mesh"

    # mi = MeshImporter(MESH_PATH,"desc2015.xml.gz","qual2015.xml.gz","supp2015.xml.gz")
    # mi = MeshImporter(MESH_PATH,scr_fn="supp2015.xml.gz")

    # FULL_XML_PATH = "/media/swatford/elements/medline/full_xml"
    # ai = ArticleImporter(FULL_XML_PATH)

    # def handle_article(_,article):
    #     print(article)
    #     # if article["PMID"]["#text"] == "15916834":
    #     #     pass
    #     return True
    #
    # for fn in listdir(FULL_XML_PATH):
    #     if fn.split(".")[-1] == "gz":
    #         xtd.parse(GzipFile("/".join([FULL_XML_PATH,fn])),
    #                   item_depth=2,item_callback=handle_article)

if __name__ == "__main__":
    main()