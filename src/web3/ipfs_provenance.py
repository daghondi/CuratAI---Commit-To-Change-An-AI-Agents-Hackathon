"""
IPFS Provenance Manager

Stores proposal versions and metadata on IPFS for immutable provenance tracking.
Provides content addressing and version history.
Enables decentralized access to proposal documentation.
"""

import logging
import json
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class IPFSContent:
    """Represents content stored on IPFS"""
    cid: str  # Content Identifier (IPFS hash)
    content: str
    content_type: str
    stored_at: str
    metadata: Dict = None


@dataclass
class ProposalVersion:
    """Tracks versions of a proposal on IPFS"""
    version_number: int
    proposal_id: str
    ipfs_cid: str
    stored_at: str
    author_did: str
    description: str = ""
    metadata: Dict = None


class IPFSProvenanceManager:
    """
    IPFS Provenance Manager: Store and track proposal versions.
    
    This component:
    1. Stores proposal versions on IPFS (simulated)
    2. Creates immutable version history
    3. Provides content addressing via IPFS CIDs
    4. Enables decentralized access
    5. Tracks metadata (author, timestamp, etc.)
    """
    
    def __init__(self, name: str = "IPFS Provenance"):
        self.name = name
        # In production, this would connect to real IPFS node
        self.content_store: Dict[str, IPFSContent] = {}
        self.version_history: Dict[str, List[ProposalVersion]] = {}
    
    def store_proposal_version(
        self,
        proposal_id: str,
        author_did: str,
        content: str,
        content_type: str = "text/markdown"
    ) -> ProposalVersion:
        """
        Store a proposal version on IPFS.
        
        Args:
            proposal_id: ID of the proposal
            author_did: DID of the author
            content: Proposal content
            content_type: MIME type of content
            
        Returns:
            ProposalVersion object with IPFS CID
        """
        logger.info(f"IPFS Manager: Storing proposal {proposal_id} on IPFS")
        
        # Generate IPFS CID (simplified - in production, use real IPFS)
        import hashlib
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        cid = f"Qm{content_hash[:40]}"  # Simplified CID format
        
        # Store content
        ipfs_content = IPFSContent(
            cid=cid,
            content=content,
            content_type=content_type,
            stored_at=datetime.now().isoformat(),
            metadata={
                "proposal_id": proposal_id,
                "author_did": author_did,
                "content_length": len(content)
            }
        )
        
        self.content_store[cid] = ipfs_content
        
        # Track version
        if proposal_id not in self.version_history:
            self.version_history[proposal_id] = []
        
        version_number = len(self.version_history[proposal_id]) + 1
        
        version = ProposalVersion(
            version_number=version_number,
            proposal_id=proposal_id,
            ipfs_cid=cid,
            stored_at=datetime.now().isoformat(),
            author_did=author_did,
            description=f"Version {version_number} of proposal {proposal_id}",
            metadata={
                "content_type": content_type,
                "content_length": len(content)
            }
        )
        
        self.version_history[proposal_id].append(version)
        
        logger.info(f"  ✓ Stored on IPFS: {cid}")
        logger.info(f"  ✓ Version {version_number} recorded")
        
        return version
    
    def get_content_by_cid(self, cid: str) -> Optional[IPFSContent]:
        """
        Retrieve content from IPFS by CID.
        
        Args:
            cid: IPFS Content Identifier
            
        Returns:
            IPFSContent object or None if not found
        """
        logger.info(f"IPFS Manager: Retrieving content {cid}")
        return self.content_store.get(cid)
    
    def get_proposal_version_history(self, proposal_id: str) -> List[ProposalVersion]:
        """
        Get all versions of a proposal.
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            List of ProposalVersion objects in chronological order
        """
        versions = self.version_history.get(proposal_id, [])
        logger.info(f"IPFS Manager: Retrieved {len(versions)} versions of {proposal_id}")
        return versions
    
    def get_latest_version(self, proposal_id: str) -> Optional[ProposalVersion]:
        """Get the latest version of a proposal"""
        versions = self.get_proposal_version_history(proposal_id)
        return versions[-1] if versions else None
    
    def create_version_manifest(self, proposal_id: str) -> Dict:
        """
        Create a manifest of all versions for a proposal.
        Useful for transparency and audit trails.
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            Manifest dictionary
        """
        versions = self.get_proposal_version_history(proposal_id)
        
        manifest = {
            "proposal_id": proposal_id,
            "total_versions": len(versions),
            "first_version": versions[0].stored_at if versions else None,
            "last_version": versions[-1].stored_at if versions else None,
            "versions": [
                {
                    "version": v.version_number,
                    "ipfs_cid": v.ipfs_cid,
                    "stored_at": v.stored_at,
                    "author_did": v.author_did,
                    "content_length": v.metadata.get("content_length") if v.metadata else None
                }
                for v in versions
            ]
        }
        
        return manifest
    
    def create_immutable_proof(self, proposal_id: str) -> Dict:
        """
        Create an immutable proof of the proposal's history.
        Can be published on blockchain for permanent record.
        
        Args:
            proposal_id: ID of the proposal
            
        Returns:
            Proof object with versioning and integrity info
        """
        manifest = self.create_version_manifest(proposal_id)
        
        # Calculate merkle tree root (simplified)
        import hashlib
        version_hashes = []
        for version in self.version_history.get(proposal_id, []):
            h = hashlib.sha256(f"{version.ipfs_cid}:{version.stored_at}".encode()).hexdigest()
            version_hashes.append(h)
        
        # Merkle root (simplified)
        merkle_root = hashlib.sha256(
            "".join(version_hashes).encode()
        ).hexdigest() if version_hashes else ""
        
        proof = {
            "proposal_id": proposal_id,
            "manifest": manifest,
            "merkle_root": merkle_root,
            "proof_created_at": datetime.now().isoformat(),
            "status": "immutable_record_available"
        }
        
        return proof
    
    def export_version_as_json(self, proposal_id: str, version_number: int = None) -> Optional[Dict]:
        """
        Export a proposal version as JSON for sharing.
        
        Args:
            proposal_id: ID of the proposal
            version_number: Specific version (latest if not specified)
            
        Returns:
            JSON representation of the proposal version
        """
        versions = self.get_proposal_version_history(proposal_id)
        
        if not versions:
            return None
        
        if version_number is None:
            version = versions[-1]
        else:
            version = next((v for v in versions if v.version_number == version_number), None)
            if not version:
                return None
        
        content = self.get_content_by_cid(version.ipfs_cid)
        
        return {
            "proposal_id": proposal_id,
            "version": version.version_number,
            "ipfs_cid": version.ipfs_cid,
            "author_did": version.author_did,
            "stored_at": version.stored_at,
            "content": content.content if content else None,
            "content_type": content.content_type if content else None,
            "is_verified": True
        }


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)
    
    ipfs_manager = IPFSProvenanceManager()
    
    # Store multiple versions of a proposal
    print("\n=== Storing Proposal Versions on IPFS ===\n")
    
    proposal_id = "proposal_001"
    author_did = "did:key:z1234567890abcdef"
    
    # Version 1
    proposal_v1 = """
    PROPOSAL FOR: TED-style Talk on AI in Arts
    
    Alex Chen is a visual artist and creative technologist.
    """
    
    version1 = ipfs_manager.store_proposal_version(
        proposal_id, author_did, proposal_v1
    )
    
    # Version 2 (revised)
    proposal_v2 = """
    PROPOSAL FOR: TED-style Talk on AI in Arts
    
    Alex Chen is a visual artist and creative technologist with 5+ years 
    of experience at the intersection of AI and human creativity.
    
    Recent achievements:
    - Solo exhibition at MoMA PS1 (2024)
    - Residency at Eyebeam (2023)
    - Speaker at SXSW (2023)
    """
    
    version2 = ipfs_manager.store_proposal_version(
        proposal_id, author_did, proposal_v2
    )
    
    # Version 3 (final)
    proposal_v3 = proposal_v2 + """
    
    Key message:
    AI should amplify, not replace, human creativity.
    """
    
    version3 = ipfs_manager.store_proposal_version(
        proposal_id, author_did, proposal_v3
    )
    
    # Show version history
    print("\n=== Version History ===\n")
    versions = ipfs_manager.get_proposal_version_history(proposal_id)
    for v in versions:
        print(f"Version {v.version_number}: {v.ipfs_cid}")
        print(f"  Stored: {v.stored_at}")
        print()
    
    # Show manifest
    print("\n=== Version Manifest ===\n")
    manifest = ipfs_manager.create_version_manifest(proposal_id)
    print(json.dumps(manifest, indent=2))
    
    # Show immutable proof
    print("\n=== Immutable Proof ===\n")
    proof = ipfs_manager.create_immutable_proof(proposal_id)
    print(json.dumps(proof, indent=2))
    
    # Export latest version
    print("\n=== Latest Version (Exported) ===\n")
    exported = ipfs_manager.export_version_as_json(proposal_id)
    print(f"Proposal: {exported['proposal_id']}")
    print(f"Version: {exported['version']}")
    print(f"CID: {exported['ipfs_cid']}")
    print(f"Author: {exported['author_did']}")
    print(f"Content (first 100 chars): {exported['content'][:100]}...")
