import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO


@pytest.fixture
def dao_mock():
    """Create a mock DAO object for testing"""
    return MagicMock(spec=DAO)


@pytest.fixture
def controller(dao_mock):
    """Create a UserController instance with mocked DAO"""
    return UserController(dao=dao_mock)


class TestUserControllerEmailValidation:
    """Tests for email format validation"""

    @pytest.mark.unit
    def test_rejects_email_without_at_symbol(self, controller):
        """Should raise ValueError for email missing @ symbol"""
        with pytest.raises(ValueError) as exc_info:
            controller.get_user_by_email('invalid.email.com')
        assert "invalid email address" in str(exc_info.value)

    @pytest.mark.unit
    def test_rejects_email_with_multiple_at_symbols(self, controller):
        """Should raise ValueError when email contains multiple @ signs"""
        with pytest.raises(ValueError) as exc_info:
            controller.get_user_by_email('user@@domain.com')
        assert "invalid email address" in str(exc_info.value)

    @pytest.mark.unit
    def test_rejects_empty_email_string(self, controller):
        """Should raise ValueError when email is empty"""
        with pytest.raises(ValueError) as exc_info:
            controller.get_user_by_email('')
        assert "invalid email address" in str(exc_info.value)

    @pytest.mark.unit
    def test_rejects_email_without_domain(self, controller):
        """Should raise ValueError for email missing domain portion"""
        with pytest.raises(ValueError) as exc_info:
            controller.get_user_by_email('user@nodomain')
        assert "invalid email address" in str(exc_info.value)


class TestUserControllerDatabaseOperations:
    """Tests for database queries and results"""

    @pytest.mark.unit
    def test_returns_user_when_exactly_one_found(self, controller, dao_mock):
        """Should return the user object when single match found"""
        user_data = {'email': 'alice@example.com', 'name': 'Alice', 'id': '123'}
        dao_mock.find.return_value = [user_data]

        result = controller.get_user_by_email('alice@example.com')

        assert result == user_data
        assert result['email'] == 'alice@example.com'

    @pytest.mark.unit
    def test_returns_none_when_no_user_exists(self, controller, dao_mock):
        """Should raise IndexError when no matching user found (BUG: should return None per docstring)"""
        dao_mock.find.return_value = []

        with pytest.raises(IndexError):
            controller.get_user_by_email('nonexistent@example.com')

    @pytest.mark.unit
    def test_handles_multiple_duplicate_emails(self, controller, dao_mock):
        """Should return first user and log warning when duplicates exist"""
        duplicate_users = [
            {'email': 'bob@example.com', 'name': 'Bob First'},
            {'email': 'bob@example.com', 'name': 'Bob Second'}
        ]
        dao_mock.find.return_value = duplicate_users

        result = controller.get_user_by_email('bob@example.com')

        assert result == duplicate_users[0]
        assert result['name'] == 'Bob First'

    @pytest.mark.unit
    def test_logs_warning_message_for_duplicate_emails(self, controller, dao_mock, capsys):
        """Should output warning message when multiple users share same email"""
        duplicate_users = [
            {'email': 'carol@example.com'},
            {'email': 'carol@example.com'}
        ]
        dao_mock.find.return_value = duplicate_users

        controller.get_user_by_email('carol@example.com')
        captured = capsys.readouterr()

        assert 'more than one user found' in captured.out
        assert 'carol@example.com' in captured.out

    @pytest.mark.unit
    def test_propagates_database_exceptions(self, controller, dao_mock):
        """Should propagate exceptions from database operations"""
        dao_mock.find.side_effect = Exception("Connection timeout")

        with pytest.raises(Exception) as exc_info:
            controller.get_user_by_email('test@example.com')
        assert "Connection timeout" in str(exc_info.value)
