import re
from src.utils.constants import *

# Regex matching integers
integer_re = r'[0-9]+'
# Regex matching decimal point floats
decimal_re = r'[0-9]+\.[0-9]+'

sup = ''.join(SUPERSCRIPT)
sub = ''.join(SUBSCRIPT)
vul = ''.join(VULGAR)

# Regex matching ASCII fractions (0/0)
ascii_re = r'(\d+)[⁄/](\d+)'
# Regex matching single character unicode fractions (½)
vulgar_re = f"[{vul}]"
# Regex matching multi-character unicode fractions (¹⁄₃)
unicode_re = f"([{sup}]+)[⁄/]([{sub}]+)"
# Regex matching any fractional forms listed above
fraction_re = f"{ascii_re}|{vulgar_re}|{unicode_re}"

# Regex matching mixed fractions in purely ASCII (1 1/2)
mixed_ascii_re = fr'([0-9]+)\s+({ascii_re})'
# Regex matching mixed fractions including unicode (1½)
mixed_other_re = fr'([0-9]+)\s*({vulgar_re}|{unicode_re})'

# Regex capturing any numeric quantity defined above
numeric_re = "|".join([
    mixed_ascii_re,
    mixed_other_re,
    fraction_re,
    decimal_re,
    integer_re
])


def integer(s):
    return re.match(integer_re + '$', s)


def decimal(s):
    return re.match(decimal_re + '$', s)


def vulgarfraction(s):
    return re.match(vulgar_re + '$', s)


def asciifraction(s):
    return re.match(ascii_re + '$', s)


def unicodefraction(s):
    return re.match(unicode_re + '$', s)


def mixedfraction(s):
    a = re.match(mixed_ascii_re + '$', s)
    if a:
        return a

    u = re.match(mixed_other_re + '$', s)
    if u:
        return u


# Sensitive to overflow for high fixed precision
def asfloat(s, precision=-1):
    """
    Convert string or numeric quantity to float (rounds 0.5 up)

    Arguments:
        s: float-like string or numeric quantity
        precision: number of decimal places to keep (maximum by default)
    """

    n = 0
    mixed = mixedfraction(s)
    if mixed:
        n = int(mixed[1])
        s = mixed[2]

    if integer(s) or decimal(s):
        x = float(s)
    elif asciifraction(s) or vulgarfraction(s):
        s = VULGAR.get(s, s)
        a = asciifraction(s)
        x = int(a[1]) / int(a[2])
    elif unicodefraction(s):
        u = unicodefraction(s)
        u1 = ''.join([SUPERSCRIPT[c] for c in u[1]])
        u2 = ''.join([SUBSCRIPT[c] for c in u[2]])
        x = int(u1) / int(u2)
    else:
        raise Exception("Could not interpret string as a non-negative float")

    # Always round 0.5 up, as in NYT Cooking dataset
    if precision >= 0:
        return n + int(10 ** precision * x + 0.5) / 10 ** precision
    else:
        return n + float(x)


def isnumeric(s):
    return bool(re.match(numeric_re, s))


def find_numeric(s):
    return re.finditer(numeric_re, s)


def standardize(s):
    return STANDARDIZED.get(s, s)


def unit_type(u, standardized=True):
    """
    Return the culinary unit type of unit u (mass, volume or length)
    """

    if not standardized:
        u = standardize(u)

    if u in MASS:
        return "mass"
    elif u in VOLUME:
        return "volume"
    elif u in LENGTH:
        return "length"
    else:
        return None


def conversion(u, v, ingredient=None):
    """
    Return conversion factor for converting one specified unit into the other.
    If unit types do not match (mass, volume, length) try to find density of
    ingredient to do the conversion

    Arguments:
        u: Strings representing unit
        v: Strings representing unit
        ingredient: Name of ingredient if density conversion is to be attempted

    Returns:
        f: float of ratio u:v
    """

    u = standardize(u)
    v = standardize(v)

    ut = unit_type(u)
    vt = unit_type(v)
    assert (ut is not None and vt is not None)

    if ut == vt:
        return UNITS[ut][u] / UNITS[vt][v]

    elif ingredient in DENSITY:

        assert ({ut, vt} == {"mass", "volume"})
        density = DENSITY[ingredient]

        if ut == "mass" and vt == "volume":
            mass = UNITS[ut][u]
            volume = UNITS[vt][v]
            return mass / (volume * density)
        else:
            mass = UNITS[vt][v]
            volume = UNITS[ut][u]
            return (volume * density) / mass

    else:
        raise Exception


def is_symbol(s):
    return s in SYMBOL
