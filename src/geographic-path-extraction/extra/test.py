import pyfn.marshalling.unmarshallers.framenet as framenet
import os

FULLTEXT_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources',
                                 'splits', 'fulltext', 'fulltext.xml')

fulltext_annosets_list = list(framenet._unmarshall_fulltext_xml(FULLTEXT_XML_FILE, {}))

print("it works")

