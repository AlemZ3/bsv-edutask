import pytest
import unittest.mock as mock

#from src.util.helpers import validateHelper

#from src.controllers.usercontroller import UserController
#from src.util.dao import DAO


def test_validateAge_valid():
    #dao_obj = DATO("kitty_cat")
    #userController = UserController()
    #validationHelper = ValidationHelper(UserController)

    #Create a mock object
    mockedusercontroller = mock.MagicMock()
    mockedusercontroller.get.return_value = {"age": age}

    #Test vlidateAge with the mocked object

    ValidationHelper.validateAge()
