"""Python TAXII 2 Client"""

# flake8: noqa

DEFAULT_USER_AGENT = "taxii2-client/2.2.0"
MEDIA_TYPE_STIX_V20 = "application/vnd.oasis.stix+json; version=2.0"
MEDIA_TYPE_TAXII_V20 = "application/vnd.oasis.taxii+json; version=2.0"
MEDIA_TYPE_TAXII_V21 = "application/taxii+json; version=2.1"

from .v21 import *  # This import will always be the latest TAXII 2.X version
from .version import __version__
