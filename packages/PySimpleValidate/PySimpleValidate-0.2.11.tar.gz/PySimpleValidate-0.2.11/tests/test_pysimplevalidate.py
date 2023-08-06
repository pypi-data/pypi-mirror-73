import datetime

import pytest
# NOTE: PySimpleValidate tests using PyTest 3.6.3. Doesn't support versions before 3.0.

import pysimplevalidate as pysv


# TODO - These tests don't cover non-English strings.

# TODO - Test _prevalidationCheck

def test__errstr():
    pysv.MAX_ERROR_STR_LEN == 50 # Make sure this constant hasn't changed.

    pysv.MAX_ERROR_STR_LEN = 50 # Set it to 50 for the purposes of this test.

    # Test that it doesn't truncate short messages.
    assert pysv._errstr('ABC') == 'ABC'
    assert pysv._errstr('X' * 50) == 'X' * 50

    # Test that it truncates long messages.
    assert pysv._errstr('X' * 51) == 'X' * 50 + '...'


def test__validateGenericParameters():
    # Test typical allowlist arguments.
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=None) is None
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=[], blockRegexes=None) is None
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=['valid'], blockRegexes=None) is None

    # Test typical blocklist arguments.
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=None) is None
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=[]) is None
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=['x']) is None
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=[('x', 'x')]) is None
    assert pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=[('x', 'x'), ('x', 'x')]) is None

    # Test invalid blank argument.
    with pytest.raises(pysv.PySimpleValidateException):
        pysv._validateGenericParameters(blank=None, strip=None, allowRegexes=None, blockRegexes=[])

    # Test invalid blocklist arguments.
    with pytest.raises(pysv.PySimpleValidateException):
        pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=42)
    with pytest.raises(pysv.PySimpleValidateException):
        pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=[('x', 42)])
    with pytest.raises(pysv.PySimpleValidateException):
        pysv._validateGenericParameters(blank=True, strip=None, allowRegexes=None, blockRegexes=[(42, 'x')])


def test_blocklist():
    # Test typical usage.
    with pytest.raises(pysv.ValidationException):
        pysv.validateStr('cat', blockRegexes=[r'c'])
    with pytest.raises(pysv.ValidationException):
        pysv.validateStr('cat', blockRegexes=[r'\w'])
    with pytest.raises(pysv.ValidationException):
        pysv.validateStr('cat', blockRegexes=[r't$'])
    with pytest.raises(pysv.ValidationException):
        pysv.validateStr('cat', blockRegexes=[r'x', r'y', r'c'])

    # Test that these do not raise an exception:
    assert pysv.validateStr('cat', blockRegexes=[r'xyz']) == 'cat'
    assert pysv.validateStr('cat', blockRegexes=[r'x', r'y', r'z']) == 'cat'
    assert pysv.validateStr('cat', blockRegexes=[r'caterpillar']) == 'cat'
    assert pysv.validateStr('cat', blockRegexes=[r'\d']) == 'cat'
    assert pysv.validateStr('cat', blockRegexes=[r'\W']) == 'cat'



def test_validateNum():
    # Test typical usage.
    assert pysv.validateNum('42')
    assert pysv.validateNum('3.14')
    assert pysv.validateNum(42)  # Non-strings should be fine.
    assert pysv.validateNum(3.14)

    # Test typical validation failure cases.
    with pytest.raises(pysv.ValidationException, match="'ABC' is not a number."):
        pysv.validateNum('ABC')
    with pytest.raises(pysv.ValidationException, match='Blank values are not allowed.'):
        pysv.validateNum('')

    # Test for when blanks are allowed.
    assert pysv.validateNum('', blank=True) == ''

    # Test for when blanks are allowed and value strips to a blank value.
    assert pysv.validateNum('XXX', blank=True, strip='X') == ''

    # Test for when blanks aren't allowed and value strips to a blank value.
    with pytest.raises(pysv.ValidationException, match="' ' is not a number."):
        pysv.validateNum(' ', blank=True, strip=False)

    # Duplicate tests as above, but setting _numType explicitly.
    assert pysv.validateNum('42', _numType='num')
    assert pysv.validateNum('3.14', _numType='num')
    assert pysv.validateNum(42, _numType='num')  # Non-strings should be fine.
    assert pysv.validateNum(3.14, _numType='num')
    with pytest.raises(pysv.ValidationException, match="'ABC' is not a number."):
        pysv.validateNum('ABC', _numType='num')
    with pytest.raises(pysv.ValidationException, match='Blank values are not allowed.'):
        pysv.validateNum('', _numType='num')
    assert pysv.validateNum('', blank=True, _numType='num') == ''
    with pytest.raises(pysv.ValidationException, match="' ' is not a number."):
        pysv.validateNum(' ', blank=True, strip=False, _numType='num')

    # TODO - need to test strip, blocklistRegexes

def test_validateInt():
    # Test typical usage.
    assert pysv.validateInt('42')
    assert pysv.validateInt(42)  # Non-strings should be fine.

    # Test typical validation failures.
    with pytest.raises(pysv.ValidationException, match="'3.14' is not an integer."):
        pysv.validateInt('3.14')
    with pytest.raises(pysv.ValidationException, match="'3.14' is not an integer."):
        pysv.validateInt(3.14)
    with pytest.raises(pysv.ValidationException, match="'ABC' is not an integer."):
        pysv.validateInt('ABC')

    # Test blank settings.
    with pytest.raises(pysv.ValidationException, match='Blank values are not allowed.'):
        pysv.validateInt('')
    assert pysv.validateInt('', blank=True) == ''
    with pytest.raises(pysv.ValidationException, match="' ' is not an integer."):
        pysv.validateInt(' ', blank=True, strip=False)

    # Duplicate the above tests, but setting _numType explicitly:
    assert pysv.validateNum('42', _numType='int')
    with pytest.raises(pysv.ValidationException, match="'3.14' is not an integer."):
        pysv.validateNum('3.14', _numType='int')
    assert pysv.validateNum(42, _numType='int')  # Non-strings should be fine.
    with pytest.raises(pysv.ValidationException, match="'3.14' is not an integer."):
        pysv.validateNum(3.14, _numType='int')
    with pytest.raises(pysv.ValidationException, match="'ABC' is not an integer."):
        pysv.validateNum('ABC', _numType='int')
    with pytest.raises(pysv.ValidationException, match='Blank values are not allowed.'):
        pysv.validateNum('', _numType='int')
    assert pysv.validateNum('', blank=True, _numType='int') == ''
    with pytest.raises(pysv.ValidationException, match="' ' is not an integer."):
        pysv.validateNum(' ', blank=True, strip=False, _numType='int')


def test_validateChoice():
    # Test typical usage.
    assert pysv.validateChoice('42', ('42', 'cat', 'dog'))
    assert pysv.validateChoice('42', ['42', 'cat', 'dog'])

    # Test lettered=True
    assert pysv.validateChoice('a', ['42', 'cat', 'dog'], lettered=True)
    assert pysv.validateChoice('A', ['42', 'cat', 'dog'], lettered=True)
    assert pysv.validateChoice('c', ['42', 'cat', 'dog'], lettered=True)
    assert pysv.validateChoice('C', ['42', 'cat', 'dog'], lettered=True)
    assert pysv.validateChoice('cat', ['42', 'cat', 'dog'], lettered=True)
    assert pysv.validateChoice('CAT', ['42', 'cat', 'dog'], lettered=True)

    # Test that caseSensitive doesn't affect the lettered options, only typing the exact option.
    assert pysv.validateChoice('a', ['42', 'cat', 'dog'], lettered=True, caseSensitive=True)
    assert pysv.validateChoice('A', ['42', 'cat', 'dog'], lettered=True, caseSensitive=True)
    assert pysv.validateChoice('cat', ['42', 'cat', 'dog'], lettered=True, caseSensitive=True)

    # Test numbered=True
    assert pysv.validateChoice('1', ['42', 'cat', 'dog'], numbered=True)
    assert pysv.validateChoice('3', ['42', 'cat', 'dog'], numbered=True)

    # Test for failure when a choice beyond the range of choices is selected
    with pytest.raises(pysv.ValidationException):
        assert pysv.validateChoice('z', ['42', 'cat', 'dog'], lettered=True)
    with pytest.raises(pysv.ValidationException):
        assert pysv.validateChoice('9', ['42', 'cat', 'dog'], numbered=True)

    # Test that zero is never an allowed numbered option.
    with pytest.raises(pysv.ValidationException):
        assert pysv.validateChoice('0', ['42', 'cat', 'dog'], numbered=True)

    # Test that lettered and numbered can't both be True.
    with pytest.raises(pysv.PySimpleValidateException):
        pysv.validateChoice('42', ['42', 'cat', 'dog'], lettered=True, numbered=True)

    # Test that lettered options are limited to 26 options.
    with pytest.raises(pysv.PySimpleValidateException):
        pysv.validateChoice('a', [str(i) for i in range(27)], lettered=True)

    # Test for typical validation failure.
    with pytest.raises(pysv.ValidationException, match="'XXX' is not a valid choice."):
        pysv.validateChoice('XXX', ['42', 'cat', 'dog'])


def test_validateDate():
    # Test typical usage.
    assert pysv.validateDate('2018/7/10')
    assert pysv.validateDate('18/7/10')
    assert pysv.validateDate('7/10/2018')
    assert pysv.validateDate('7/10/18')

    # Test for typical validation failure.
    with pytest.raises(pysv.ValidationException): #, match="'2018/13/10' is not a valid date."):
        pysv.validateDate('2018/13/10')

    # TODO - finish


def test_validateTime():
    # Test typical usage.
    assert pysv.validateTime('00:00') == datetime.time(0, 0)
    assert pysv.validateTime('12:00') == datetime.time(12, 0)
    assert pysv.validateTime('7:00') == datetime.time(7, 0)
    assert pysv.validateTime('00:00:00') == datetime.time(0, 0, 0)
    assert pysv.validateTime('12:00:00') == datetime.time(12, 0, 0)
    assert pysv.validateTime('7:00:00') == datetime.time(7, 0, 0)

    # Test for typical validation failure.
    with pytest.raises(pysv.ValidationException): #, match="'25:00' is not a valid time."):
        pysv.validateTime('25:00')
    with pytest.raises(pysv.ValidationException): #, match="'25:0:00' is not a valid time."):
        pysv.validateTime('25:0:00')
    with pytest.raises(pysv.ValidationException): #, match="'7:61' is not a valid time."):
        pysv.validateTime('7:61')
    with pytest.raises(pysv.ValidationException): #, match="'7:61:00' is not a valid time."):
        pysv.validateTime('7:61:00')
    with pytest.raises(pysv.ValidationException): #, match="'7:30:62' is not a valid time."):
        pysv.validateTime('7:30:62')
    with pytest.raises(pysv.ValidationException): #, match="'XXX' is not a valid time."):
        pysv.validateTime('XXX')

    # TODO - finish


def test_validateDatetime():
    # Test typical usage.
    assert pysv.validateDatetime('2018/7/10 12:30:00')
    assert pysv.validateDatetime('2018/7/10 12:30')
    assert pysv.validateDatetime('2018/7/1 23:00')

    # TODO - finish


def test_validateURL():
    # Test typical usage.
    assert pysv.validateURL('https://www.metafilter.com/')
    assert pysv.validateURL('www.metafilter.com')
    assert pysv.validateURL('https://www.metafilter.com/175250/Have-you-ever-questioned-the-nature-of-your-streaming-content')

    # TODO - finish


def test_validateRegex():
    # Test typical usage.
    assert pysv.validateRegex('cat', 'cat')
    assert pysv.validateRegex('cat', r'\w+')
    assert pysv.validateRegex('cat 123', r'\d+')


def test_validateRegexStr():
    # Test typical usage.
    pysv.validateRegexStr(r'\w+')


    with pytest.raises(pysv.ValidationException):
        pysv.validateRegexStr(r'(')


def test_validateIP():
    # Test typical usage.
    assert pysv.validateIP('127.0.0.1')
    assert pysv.validateIP('255.255.255.255')
    assert pysv.validateIP('300.255.255.255')


def test_validateYesNo():
    # Test typical usage.
    assert pysv.validateYesNo('yes')
    assert pysv.validateYesNo('y')
    assert pysv.validateYesNo('no')
    assert pysv.validateYesNo('n')

    assert pysv.validateYesNo('YES')
    assert pysv.validateYesNo('Y')
    assert pysv.validateYesNo('NO')
    assert pysv.validateYesNo('N')

    assert pysv.validateYesNo('si', yesVal='si')
    assert pysv.validateYesNo('SI', yesVal='si')
    assert pysv.validateYesNo('n', yesVal='oui', noVal='no')

    # Test typical failure cases.
    with pytest.raises(pysv.ValidationException):
        pysv.validateYesNo('dog')

    # Test case sensitive.
    assert pysv.validateYesNo('yes', caseSensitive=True)
    assert pysv.validateYesNo('y', caseSensitive=True)
    assert pysv.validateYesNo('no', caseSensitive=True)
    assert pysv.validateYesNo('n', caseSensitive=True)

    # Test typical failures when case sensitive.
    with pytest.raises(pysv.ValidationException):
        pysv.validateYesNo('YES', caseSensitive=True)
    with pytest.raises(pysv.ValidationException):
        pysv.validateYesNo('Y', caseSensitive=True)
    with pytest.raises(pysv.ValidationException):
        pysv.validateYesNo('NO', caseSensitive=True)
    with pytest.raises(pysv.ValidationException):
        pysv.validateYesNo('N', caseSensitive=True)


def test_validateUSState():
    # Test typical usage.
    assert pysv.validateUSState('CA') == 'CA'
    assert pysv.validateUSState('California') == 'CA'
    assert pysv.validateUSState('CA', returnStateName=True) == 'California'

    # Test typical failure cases.
    with pytest.raises(pysv.ValidationException):
        pysv.validateUSState('gaseous')


def test__validateParamsFor_validateChoice():
    # Note that these calls raise PySimpleValidateException, not
    # ValidationException, because they are problems with the call itself,
    # not with the value being validated.

    # Test typical usage.
    pysv._validateParamsFor_validateChoice(['dog', 'cat'])

    # Test typical failure cases.
    with pytest.raises(pysv.PySimpleValidateException, match='choices arg must be a sequence'):
        pysv._validateParamsFor_validateChoice(42)

    with pytest.raises(pysv.PySimpleValidateException, match='choices must have at least two items if blank is False'):
        pysv._validateParamsFor_validateChoice([])

    with pytest.raises(pysv.PySimpleValidateException, match='choices must have at least one item'):
        pysv._validateParamsFor_validateChoice([], blank=True)

    with pytest.raises(pysv.PySimpleValidateException, match='choices must have at least one item'):
        pysv._validateParamsFor_validateChoice([], blank=True)

    with pytest.raises(pysv.PySimpleValidateException, match='duplicate entries in choices argument'):
        pysv._validateParamsFor_validateChoice(['dog', 'dog'], caseSensitive=False)

    with pytest.raises(pysv.PySimpleValidateException, match='duplicate case-insensitive entries in choices argument'):
        pysv._validateParamsFor_validateChoice(['dog', 'DOG'], caseSensitive=False)

    # "Duplicates" are fine if they have different cases:
    pysv._validateParamsFor_validateChoice(['dog', 'DOG'], caseSensitive=True)



def test__validateParamsFor_validateNum():
    # Test typical usage.
    pysv._validateParamsFor_validateNum()

    # Test typical failure cases.
    with pytest.raises(pysv.PySimpleValidateException, match='min argument must be int, float, or NoneType'):
        pysv._validateParamsFor_validateNum(min='invalid')

    with pytest.raises(pysv.PySimpleValidateException, match='max argument must be int, float, or NoneType'):
        pysv._validateParamsFor_validateNum(max='invalid')

    with pytest.raises(pysv.PySimpleValidateException, match='lessThan argument must be int, float, or NoneType'):
        pysv._validateParamsFor_validateNum(lessThan='invalid')

    with pytest.raises(pysv.PySimpleValidateException, match='greaterThan argument must be int, float, or NoneType'):
        pysv._validateParamsFor_validateNum(greaterThan='invalid')

def test_validateFilename():
    # Test typical usage.
    assert pysv.validateFilename('foobar.txt') == 'foobar.txt'

    # Test typical failure cases.
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('\\')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('/')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename(':')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('*')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('?')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('"')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('<')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('>')
    with pytest.raises(pysv.ValidationException, match='is not a valid filename'):
        pysv.validateFilename('|')

if __name__ == '__main__':
    pytest.main()


