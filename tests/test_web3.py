"""
Unit tests for Web3 components
"""

import unittest
from src.web3.did_manager import DIDManager
from src.web3.ipfs_provenance import IPFSProvenanceManager


class TestDIDManager(unittest.TestCase):
    """Tests for DID Manager"""
    
    def setUp(self):
        self.did_manager = DIDManager()
    
    def test_create_did(self):
        """Test DID creation"""
        did = self.did_manager.create_did("user_001", {"name": "Test User"})
        self.assertIsNotNone(did)
        self.assertTrue(did.did.startswith("did:key:z"))
        self.assertEqual(did.user_id, "user_001")
    
    def test_sign_document(self):
        """Test document signing"""
        content = "Test proposal content"
        signature = self.did_manager.sign_document("user_001", content)
        self.assertIsNotNone(signature)
        self.assertIsNotNone(signature.signature)
    
    def test_verify_signature(self):
        """Test signature verification"""
        content = "Test proposal content"
        signature = self.did_manager.sign_document("user_001", content)
        is_valid = self.did_manager.verify_signature(signature, content)
        self.assertTrue(is_valid)
    
    def test_signature_fails_with_modified_content(self):
        """Test signature verification fails with modified content"""
        content = "Original content"
        signature = self.did_manager.sign_document("user_001", content)
        
        modified = "Modified content"
        is_valid = self.did_manager.verify_signature(signature, modified)
        self.assertFalse(is_valid)


class TestIPFSProvenanceManager(unittest.TestCase):
    """Tests for IPFS Provenance Manager"""
    
    def setUp(self):
        self.ipfs_manager = IPFSProvenanceManager()
    
    def test_store_proposal_version(self):
        """Test storing a proposal version"""
        version = self.ipfs_manager.store_proposal_version(
            proposal_id="prop_001",
            author_did="did:key:test",
            content="Test proposal"
        )
        self.assertIsNotNone(version)
        self.assertEqual(version.version_number, 1)
    
    def test_get_version_history(self):
        """Test retrieving version history"""
        prop_id = "prop_001"
        
        self.ipfs_manager.store_proposal_version(prop_id, "did:key:test", "Version 1")
        self.ipfs_manager.store_proposal_version(prop_id, "did:key:test", "Version 2")
        
        history = self.ipfs_manager.get_proposal_version_history(prop_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].version_number, 1)
        self.assertEqual(history[1].version_number, 2)
    
    def test_create_version_manifest(self):
        """Test creating version manifest"""
        prop_id = "prop_test"
        self.ipfs_manager.store_proposal_version(prop_id, "did:key:test", "Content")
        
        manifest = self.ipfs_manager.create_version_manifest(prop_id)
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest["proposal_id"], prop_id)
        self.assertEqual(manifest["total_versions"], 1)


if __name__ == "__main__":
    unittest.main()
