from ming import create_datastore
from ming.odm import ThreadLocalODMSession
from litminer import config

auth = dict(config["mongodb"])
uri = auth.pop("uri",None)

session = ThreadLocalODMSession(
    bind=create_datastore(uri=uri,authenticate=auth)
)
