import pytest

def test_equal_or_not_equal():
    assert 3 == 3


def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)


def test_boolean():
    validated = True
    assert validated is True
    assert ("hello" == 'world') is False


def test_type():
    assert type("Hello" is str)
    assert type("World" is not int)

def test_gerather_than():
    assert 7 > 3
    assert 4 < 20

def test_list():
    nums_list = [1,2,3,4]
    any_list = [False, False]

    assert 1 in nums_list
    assert 7 not in nums_list
    assert all(nums_list)

class Student:
    def __init__(self, first_name:str, last_name:str, major:str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major =  major
        self.years = years

@pytest.fixture
def default_student():
    return Student('Sahachel', 'Flores', 'CS', 3)

def test_person_init(default_student):
    #p = Student('Sahachel', 'Flores', 'CS', 3)

    assert default_student.first_name == 'Sahachel', 'first name should be sahachel'
    assert default_student.last_name == 'Flores', 'last name should be flores'
    assert default_student.major == 'CS'
    assert default_student.years == 3

