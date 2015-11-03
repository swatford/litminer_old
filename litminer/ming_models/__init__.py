from ming import create_datastore
from ming.odm import ThreadLocalODMSession
import configparser
from litminer import PROJECT_PATH

config = configparser.ConfigParser()
config.read("\\".join([PROJECT_PATH,"dev_config.ini"]))

auth = dict(config["mongodb"])
uri = auth.pop("uri",None)

session = ThreadLocalODMSession(
    bind=create_datastore(uri=uri,authenticate=auth)
)
