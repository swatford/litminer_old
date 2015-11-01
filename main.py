from utils import MeshImporter

__author__ = 'swatford'


def main(*args,**kwargs):

    MESH_PATH = "/media/swatford/elements/medline/mesh"

    mi = MeshImporter(MESH_PATH,"desc2015.xml.gz","qual2015.xml.gz")


    # FULL_XML_PATH = "/media/swatford/elements/medline/full_xml"
    #
    # def handle_article(_,article):
    #     print(article)
    #     if article["PMID"]["#text"] == "15916834":
    #         pass
    #     return True
    #
    # def handle_scr(_,scr):
    #     print(scr.__class__)
    #     return True

    # xtd.parse(GzipFile("/media/swatford/elements/medline/mesh/supp2015.xml.gz"),
    #           item_depth=2,item_callback=handle_scr)

    # for fn in listdir(FULL_XML_PATH):
    #     if fn.split(".")[-1] == "gz":
    #         xtd.parse(GzipFile("/".join([FULL_XML_PATH,fn])),
    #                   item_depth=2,item_callback=handle_article)

if __name__ == "__main__":
    main()