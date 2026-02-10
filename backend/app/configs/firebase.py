import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Path to your Firebase service account key
SERVICE_ACCOUNT_PATH = Path(__file__).parent.parent.parent / "serviceAccountKey.json"
# Initialize Firebase app (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()


def get_firestore():
    """Get Firestore client instance."""
    return db


async def get_collection(collection_name: str):
    """Get all documents from a collection."""
    docs = db.collection(collection_name).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


async def get_document(collection_name: str, doc_id: str):
    """Get a single document by ID."""
    doc = db.collection(collection_name).document(doc_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None


async def create_document(collection_name: str, data: dict, doc_id: str = None):
    """Create a new document in a collection."""
    if doc_id:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.set(data)
    else:
        doc_ref = db.collection(collection_name).add(data)[1]
    return {"id": doc_ref.id, **data}


async def update_document(collection_name: str, doc_id: str, data: dict):
    """Update an existing document."""
    doc_ref = db.collection(collection_name).document(doc_id)
    doc_ref.update(data)
    updated_doc = doc_ref.get()
    return {"id": updated_doc.id, **updated_doc.to_dict()}


async def delete_document(collection_name: str, doc_id: str):
    """Delete a document."""
    db.collection(collection_name).document(doc_id).delete()
    return {"message": f"Document {doc_id} deleted successfully"}


def check_firebase_connection() -> dict:
    """Check if Firebase connection is alive."""
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
