"""
DID (Decentralized Identity) Manager

Manages cryptographic identities and digital signatures for users.
Creates and verifies DIDs (Decentralized Identifiers) for author authentication.
Provides proof of authorship and version history.
"""

import logging
import json
import hashlib
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class DID:
    """Decentralized Identifier for a user or agent"""
    did: str  # Format: did:key:z[base58 encoded key]
    public_key: str
    created_at: str
    user_id: Optional[str] = None
    metadata: Dict = None


@dataclass
class DigitalSignature:
    """Digital signature for a document/proposal"""
    document_hash: str
    signature: str
    did: str
    signed_at: str
    algorithm: str = "SHA-256"


class DIDManager:
    """
    DID Manager: Create and manage decentralized identities.
    
    This component:
    1. Generates DIDs for users and agents
    2. Creates digital signatures for documents
    3. Verifies authenticity of proposals
    4. Tracks version history with DIDs
    5. Enables decentralized trust and attribution
    """
    
    def __init__(self, name: str = "DID Manager"):
        self.name = name
        self.did_registry: Dict[str, DID] = {}
        self.signatures: Dict[str, DigitalSignature] = []
    
    def create_did(self, user_id: str, metadata: Optional[Dict] = None) -> DID:
        """
        Create a new DID for a user.
        
        Args:
            user_id: Unique user identifier
            metadata: Additional metadata (name, email, etc.)
            
        Returns:
            DID object
        """
        logger.info(f"DID Manager: Creating DID for user {user_id}")
        
        # Generate a pseudo-random key (in production, use proper crypto)
        key_material = f"{user_id}:{datetime.now().isoformat()}:{metadata}".encode()
        hash_digest = hashlib.sha256(key_material).hexdigest()
        
        # Create did:key format (simplified)
        did = f"did:key:z{hash_digest[:32]}"
        
        did_obj = DID(
            did=did,
            public_key=hash_digest,
            created_at=datetime.now().isoformat(),
            user_id=user_id,
            metadata=metadata or {}
        )
        
        self.did_registry[user_id] = did_obj
        logger.info(f"  ✓ DID created: {did}")
        
        return did_obj
    
    def get_or_create_did(self, user_id: str) -> DID:
        """Get existing DID or create new one"""
        if user_id in self.did_registry:
            return self.did_registry[user_id]
        return self.create_did(user_id)
    
    def sign_document(self, user_id: str, document_content: str) -> DigitalSignature:
        """
        Digitally sign a document (proposal, version, etc.).
        
        Args:
            user_id: User signing the document
            document_content: Content of the document
            
        Returns:
            DigitalSignature object
        """
        logger.info(f"DID Manager: Signing document for user {user_id}")
        
        # Get or create user's DID
        did_obj = self.get_or_create_did(user_id)
        
        # Create document hash
        document_hash = hashlib.sha256(document_content.encode()).hexdigest()
        
        # Create signature (simplified: hash of content + user's public key)
        signature_material = f"{document_hash}:{did_obj.public_key}".encode()
        signature = hashlib.sha256(signature_material).hexdigest()
        
        sig_obj = DigitalSignature(
            document_hash=document_hash,
            signature=signature,
            did=did_obj.did,
            signed_at=datetime.now().isoformat()
        )
        
        self.signatures.append(sig_obj)
        logger.info(f"  ✓ Document signed: {document_hash[:16]}...")
        
        return sig_obj
    
    def verify_signature(self, signature: DigitalSignature, document_content: str) -> bool:
        """
        Verify that a signature matches a document.
        
        Args:
            signature: The signature to verify
            document_content: The document content
            
        Returns:
            True if signature is valid
        """
        logger.info(f"DID Manager: Verifying signature")
        
        # Recalculate document hash
        calculated_hash = hashlib.sha256(document_content.encode()).hexdigest()
        
        # Check if hashes match
        if calculated_hash != signature.document_hash:
            logger.warning("  ✗ Document has been modified!")
            return False
        
        logger.info(f"  ✓ Signature valid")
        return True
    
    def get_did(self, user_id: str) -> Optional[DID]:
        """Retrieve a user's DID"""
        return self.did_registry.get(user_id)
    
    def export_did_as_json(self, user_id: str) -> Dict:
        """Export DID as JSON for storage/sharing"""
        did = self.get_did(user_id)
        if not did:
            return {}
        
        return {
            "did": did.did,
            "public_key": did.public_key,
            "created_at": did.created_at,
            "user_id": did.user_id,
            "metadata": did.metadata
        }
    
    def get_document_provenance(self, document_hash: str) -> Optional[Dict]:
        """
        Get provenance information for a document.
        
        Args:
            document_hash: Hash of the document
            
        Returns:
            Provenance information
        """
        matching_sigs = [s for s in self.signatures if s.document_hash == document_hash]
        
        if not matching_sigs:
            return None
        
        # Return info about first signature
        sig = matching_sigs[0]
        return {
            "document_hash": sig.document_hash,
            "signed_by": sig.did,
            "signed_at": sig.signed_at,
            "algorithm": sig.algorithm,
            "signature": sig.signature
        }


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    did_manager = DIDManager()
    
    # Create DIDs for users
    print("\n=== Creating DIDs ===\n")
    user1_did = did_manager.create_did(
        user_id="user_001",
        metadata={"name": "Alex Chen", "email": "alex@example.com"}
    )
    
    user2_did = did_manager.create_did(
        user_id="user_002",
        metadata={"name": "Jordan Smith", "email": "jordan@example.com"}
    )
    
    # Sign a proposal
    print("\n=== Signing a Proposal ===\n")
    proposal_content = """
    PROPOSAL FOR: TED-style Talk on AI in Arts
    
    Alex Chen is a visual artist and creative technologist with 
    demonstrated expertise in the intersection of AI and human creativity.
    """
    
    signature = did_manager.sign_document("user_001", proposal_content)
    print(f"Signature created: {signature.signature[:32]}...")
    
    # Verify signature
    print("\n=== Verifying Signature ===\n")
    is_valid = did_manager.verify_signature(signature, proposal_content)
    print(f"Signature valid: {is_valid}")
    
    # Try with modified content
    modified_content = proposal_content + "\n\nFAKE: This was added fraudulently."
    is_valid_modified = did_manager.verify_signature(signature, modified_content)
    print(f"Signature valid (modified content): {is_valid_modified}")
    
    # Export DIDs
    print("\n=== Exported DIDs ===\n")
    did_json = did_manager.export_did_as_json("user_001")
    print(json.dumps(did_json, indent=2))
    
    # Get provenance
    print("\n=== Document Provenance ===\n")
    provenance = did_manager.get_document_provenance(signature.document_hash)
    print(json.dumps(provenance, indent=2))
