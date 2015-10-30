import xmltodict as xtd
from gzip import GzipFile
from utils.handler import handle_descriptor_record

__author__ = 'swatford'


def main(*args,**kwargs):
    xtd.parse(GzipFile("/media/swatford/elements/medline/mesh/desc2015.xml.gz"),
              item_depth=2,
              item_callback=handle_descriptor_record)


if __name__ == "__main__":
    main()