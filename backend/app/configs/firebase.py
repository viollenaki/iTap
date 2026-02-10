import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Path to your Firebase service account key
SERVICE_ACCOUNT_PATH = Path(__file__).parent.parent.parent / "serviceAccountKey.json"

# Lazy initialization
_db = None
_initialized = False


def _init_firebase():
    """Initialize Firebase lazily."""
    global _db, _initialized
    if _initialized:
        return _db
    
    _initialized = True
    
    if not SERVICE_ACCOUNT_PATH.exists():
        return None
    
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    except Exception:
        pass
    
    return _db


def get_firestore():
    """Get Firestore client instance."""
    return _init_firebase()


async def get_collection(collection_name: str):
    """Get all documents from a collection."""
    db = get_firestore()
    if not db:
        return []
    docs = db.collection(collection_name).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


async def get_document(collection_name: str, doc_id: str):
    """Get a single document by ID."""
    db = get_firestore()
    if not db:
        return None
    doc = db.collection(collection_name).document(doc_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None


async def create_document(collection_name: str, data: dict, doc_id: str = None):
    """Create a new document in a collection."""
    db = get_firestore()
    if not db:
        raise Exception("Firebase not initialized")
    if doc_id:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.set(data)
    else:
        doc_ref = db.collection(collection_name).add(data)[1]
    return {"id": doc_ref.id, **data}


async def update_document(collection_name: str, doc_id: str, data: dict):
    """Update an existing document."""
    db = get_firestore()
    if not db:
        raise Exception("Firebase not initialized")
    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.update(data)
    updated_doc = doc_ref.get()
    return {"id": updated_doc.id, **updated_doc.to_dict()}


async def delete_document(collection_name: str, doc_id: str):
    """Delete a document."""
    db = get_firestore()
    if not db:
        raise Exception("Firebase not initialized")
    db.collection(collection_name).document(doc_id).delete()
    return {"message": f"Document {doc_id} deleted successfully"}


def check_firebase_connection() -> dict:
    """Check if Firebase connection is alive."""
    db = get_firestore()
    if not db:
        return {
            "status": "disconnected",
            "service": "firebase",
            "error": "Firebase not initialized - serviceAccountKey.json missing or invalid"
        }
    try:
        # Try to access Firestore to verify connection
        collections = list(db.collections())
        return {
            "status": "connected",
            "service": "firebase",
            "collections_count": len(collections),
        }
    except Exception as e:
        return {"status": "disconnected", "service": "firebase", "error": str(e)}
