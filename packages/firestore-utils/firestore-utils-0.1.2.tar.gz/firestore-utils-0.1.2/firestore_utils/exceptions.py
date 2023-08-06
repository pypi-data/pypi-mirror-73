class SchemaFileDoesNotExist(Exception):
    """                                                                                                
    Raised when the `firestore_collection.FirestoreCollection` class is instantiated with a value
    for the `schema_file` argument and the path doesn't exist.
    """                                                                                                
    pass                                                                                               

class FirestoreDocumentMissing(Exception):                                                             
    """                                                                                                
    Raised when we are looking for a particular Firestore document but it doesn't yet exist.           
    """                                                                                                
    pass                                                                                               
                                                                                                       
                                                                                                       
class FirestoreDocumentMissingStoragePath(Exception):                                                   
    """                                                                                                
    Raised when a Firestore document is missing the storage location while it is expected.             
    """                                                                                                
    pass
