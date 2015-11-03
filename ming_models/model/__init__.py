from ming import create_datastore
from ming.odm import ThreadLocalODMSession

__author__ = 'swatford'

session = ThreadLocalODMSession(
    bind=create_datastore("mongodb://localhost:27017/litminer")
)

