import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {"name": "Jane Doe"}


@pytest.mark.unit
def test_hasAttribute_True(obj):
    result = hasAttribute(obj, "name")
    #print(result)
    assert result == True

@pytest.mark.unit
def test_hasAttribute_False(obj):
    result = hasAttribute(obj, "age")
    #print(result)
    assert result == False

#@pytest.mark.unit
#def test_hasAttribute_None():
#    result = hasAttribute(None, "age")
    #print(result)
#    assert result == False


