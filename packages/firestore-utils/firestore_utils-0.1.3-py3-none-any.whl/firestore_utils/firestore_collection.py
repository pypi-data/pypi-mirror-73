import json
import jsonschema
import jsonschema.exceptions
import logging
import os

from google.cloud import firestore

from . import exceptions

logger = logging.getLogger(__name__)

class FirestoreCollection:

    def __init__(self, collname, schema_file="", gcp_project=""):
        """
        Args:
            collname: `str`. Name of the Firestore collection.
            schema_file: `str`. Path to a JSON schema file to validate changes to existing documents
                and new documents in the specified Firestore collection "collname". 
            gcp_project: `str`. A Google Project ID. Normally this is determined automatically by 
                the Google APIs if running on a GCE VM.  But if you want to use a different 
                project, or are running on a non-GCE VM, then specify the desired gcp_project 
                that contains the specified Firestore collection.
        """
        self.schema_file = schema_file
        self.schema = self._load_schema()
        if gcp_project:
            self.coll = firestore.Client(project=gcp_project).collection(collname)
        else:
            self.coll = firestore.Client().collection(collname)

    def _load_schema(self):
        if not self.schema_file:
            return None
        if not os.path.exists(self.schema_file):
            errmsg = f"Error while instantiating class `firestore_collection.FirestoreCollection`: "
            errmsg += f"The value provided to the `schema_file` argument '{self.schema_file}' does not exist."
            raise SchemaFileDoesNotExist(errmsg)
        return json.load(open(self.schema_file)) 

    def validate_payload(self, payload):
        """
        Validates the provided payload against the JSON schema defined in `self.schema` if set.
        If there isn't a schama set, then no validation will be performed. 

        Returns:
            `None`: Either the schema is valid or no schema was set in `self.schema`. 

        Raises:
            `jsonschema.exceptions.ValidationError`: Payload is not valid. 
        """
        if not self.schema:
            return
        jsonschema.validate(payload, self.schema) 

    def get(self, docid):
        """
        Retrieves a document in the Firestore collection that has the given entry name.

        Args:
            docid: `str`. The ID of a Firestore Document in the collection at hand.

        Returns: `dict`. 

        Raises:
            `exceptions.FirestoreDocumentMissing`: A corresponding Firestore document
                could not be found for the provided message.
        """

        logger.info(f"Querying Firestore for a document with ID '{docid}'")
        docref = self.coll.document(docid) # google.cloud.firestore_v1.document.DocumentReference
        doc = docref.get().to_dict() # dict
        if not doc:
            msg = f"No Firestore document exists with ID '{docid}'."
            logger.critical(msg)
            raise exceptions.FirestoreDocumentMissing(msg)
        logger.info("Success")
        return doc

    def new(self, docid, payload):
        """
        Args:
            docid: `str`. The ID of a Firestore Document in the collection at hand.
            payload: `dict`. The properties to set in the Firestore Document.
        """
        self.validate_payload(payload)
        self.coll.document(docid).set(payload)


    def update(self, docid, payload):
        """
        Args:
            docid: `str`. The ID of a Firestore Document in the collection at hand.
            payload: `dict`. The properties to set in the Firestore Document.

        Raises:
            `google.api_core.exceptions.NotFound` if there isn't already a document with an ID
            that's equal to the specified docid.
        """
        self.validate_payload(payload)
        self.coll.document(docid).update(payload)
