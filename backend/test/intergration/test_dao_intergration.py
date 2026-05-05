import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError
from src.util.dao import DAO
from src.util.validators import getValidator


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def user_repo():
    """
    Sets up an isolated MongoDB test repository with proper schema enforcement.
    Initializes a fresh collection and cleans up after each test execution.
    """
    mongo_conn = MongoClient('mongodb://root:root@localhost:27017')
    test_database = mongo_conn['edutask_test']

    collection_name = 'user'

    # Ensure fresh state
    if collection_name in test_database.list_collection_names():
        test_database[collection_name].drop()

    # Build collection with schema
    schema_validator = getValidator(collection_name)
    test_database.create_collection(collection_name, validator=schema_validator)


    # Initialize data access layer
    accessor = DAO(collection_name)
    accessor.collection = test_database[collection_name]

    yield accessor

    # Teardown
    test_database[collection_name].drop()
    mongo_conn.close()


# ============================================================================
# Mock Data
# ============================================================================

VALID_USER_ALICE = {
    'firstName': 'Alem',
    'lastName': 'Zvirkic',
    'email': 'alemzvirkic@gmail.com'
}

VALID_USER_BOB = {
    'firstName': 'Gabriel',
    'lastName': 'Axegart',
    'email': 'gabriel.axegart@gmail.com'
}

INVALID_USER_MISSING_FIRST = {
    'lastName': 'Zxe',
    'email': 'zzz@gmail.com'
}

INVALID_USER_MISSING_LAST = {
    'firstName': 'Gabe',
    'email': 'gabe@gmail.com'
}

INVALID_USER_MISSING_EMAIL = {
    'firstName': 'Alex',
    'lastName': 'Guess'
}

INVALID_USER_BAD_FIRST_TYPE = {
    'firstName': 999,
    'lastName': 'Jhonson',
    'email': 'j@gmail.com'
}

INVALID_USER_BAD_LAST_TYPE = {
    'firstName': 'John',
    'lastName': 777,
    'email': 'jo@gmail.com'
}

INVALID_USER_BAD_EMAIL_TYPE = {
    'firstName': 'Crhis',
    'lastName': 'Brown',
    'email': 555
}


# ============================================================================
# Test Suite
# ============================================================================

class TestUserPersistence:
    """Integration tests validating DAO.create with MongoDB schema validation."""

    def test_single_valid_user_insert(self, user_repo):
        """TC-01: Successfully persist a valid user record with all required attributes."""
        inserted = user_repo.create(VALID_USER_ALICE)
        assert '_id' in inserted

    def test_multiple_distinct_users(self, user_repo):
        """TC-02: Successfully persist multiple users with unique email addresses."""
        user_repo.create(VALID_USER_ALICE)

        second_insert = user_repo.create(VALID_USER_BOB)
        assert '_id' in second_insert

    def test_duplicate_email_rejected(self, user_repo):
        """TC-03: Reject insertion when email uniqueness constraint violated."""
        user_repo.create(VALID_USER_ALICE)

        duplicate_payload = {
            'firstName': 'Different',
            'lastName': 'Name',
            'email': 'alemzvirkic@gmail.com'
        }

        with pytest.raises(WriteError):
            user_repo.create(duplicate_payload)

    def test_missing_given_name_rejected(self, user_repo):
        """TC-04: Reject insertion when firstName field absent."""
        with pytest.raises(WriteError):
            user_repo.create(INVALID_USER_MISSING_FIRST)

    def test_missing_family_name_rejected(self, user_repo):
        """TC-05: Reject insertion when lastName field absent."""
        with pytest.raises(WriteError):
            user_repo.create(INVALID_USER_MISSING_LAST)

    def test_missing_contact_email_rejected(self, user_repo):
        """TC-06: Reject insertion when email field absent."""
        with pytest.raises(WriteError):
            user_repo.create(INVALID_USER_MISSING_EMAIL)

    def test_given_name_type_validation(self, user_repo):
        """TC-07: Reject insertion when firstName has incorrect data type."""
        with pytest.raises(WriteError):
            user_repo.create(INVALID_USER_BAD_FIRST_TYPE)

    def test_family_name_type_validation(self, user_repo):
        """TC-08: Reject insertion when lastName has incorrect data type."""
        with pytest.raises(WriteError):
            user_repo.create(INVALID_USER_BAD_LAST_TYPE)

    def test_email_type_validation(self, user_repo):
        """TC-09: Reject insertion when email has incorrect data type."""
        with pytest.raises(WriteError):
            user_repo.create(INVALID_USER_BAD_EMAIL_TYPE)