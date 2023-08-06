from decimal import Decimal

from bitfield import BitHandler, Bit

from isc_common import setAttr


def DecimalToStr(value):
    if value == None:
        return ''

    try:
        res = str(value)
        res.split('.')
        cel = res.split('.')[0]
        float = StrToNumber(res.split('.')[1:][0])
        if float > 0:
            return f'{cel}.{float}'
        return cel
    except IndexError:
        return value


def StrToNumber(s1):
    if s1 == None:
        return None

    if not isinstance(s1, str):
        raise Exception(f'{s1} is not str type.')

    s = s1.replace(',', '.')

    if not isinstance(s, str):
        raise Exception(f'{s} is not str type.')
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError as ex:
            return None


def IntToNumber(s):
    if s == None:
        return None

    if not isinstance(s, int):
        raise Exception(f'{s} is not int type.')

    return float(s)

def ToNumber(s):
    if s == None:
        return 0

    if isinstance(s, int):
        return IntToNumber(s)
    elif isinstance(s, str):
        return StrToNumber(s)
    elif isinstance(s, float):
        return s
    elif isinstance(s, Decimal):
        return float(s)
    else:
        raise Exception(f'{s} unknown type.')

def ToDecimal(s):
    if s == None:
        return 0

    if isinstance(s, int):
        return Decimal(s)
    elif isinstance(s, str):
        return Decimal(s)
    elif isinstance(s, float):
        return Decimal(s)
    elif isinstance(s, Decimal):
        return s
    else:
        raise Exception(f'{s} unknown type.')


def IntToDecimal(s):
    if s == None:
        return None

    if not isinstance(s, int):
        raise Exception(f'{s} is not int type.')

    return Decimal(s)


def StrToInt(s):
    if s == None:
        return None
    try:
        return int(s)
    except ValueError as ex:
        return None


def DelProps(value):
    if isinstance(value, dict):
        for key, _value in value.items():
            if isinstance(_value, BitHandler):
                setAttr(value, key, _value._value)
            elif isinstance(_value, Bit):
                setAttr(value, key, _value.is_set)
        return value
    else:
        value


def GetPropsInt(value):
    if isinstance(value, BitHandler):
        return value._value
    else:
        value
