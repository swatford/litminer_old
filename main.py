from litminer.utils import MeshImporter
from litminer import config
# from utils import ArticleImporter
# from os import listdir
import xmltodict as xtd
from gzip import GzipFile
from litminer.ming_models import session

def main(*args,**kwargs):

    # MESH_PATH = "/media/swatford/elements/medline/mesh"
    MESH_PATH = config["data"]["mesh"]
    from litminer.ming_models.model.mbr.qualifier import Qualifier

    # mi = MeshImporter(root=MESH_PATH,qualifier_fn="qual2015.xml.gz",
    #                   descriptor_fn="desc2015.xml.gz",
    #                   scr_fn="supp2015.xml.gz")
    # mi = MeshImporter(root=MESH_PATH,scr_fn="supp2015.xml.gz")

    FULL_XML_PATH = config["data"]["medline_full"]
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