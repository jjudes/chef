SYMBOL = {',', '.', '(', ')', ': ', ';', '/',
          '"', "'", '!', '@', '#', '$', '&', '-', 
          '+', '?'}

VULGAR = {
    '½': '1/2',
    '⅓': '1/3', '⅔': '2/3',
    '¼': '1/4', '¾': '3/4',
    '⅕': '1/5', '⅖': '2/5', '⅗': '3/5', '⅘': '4/5',
    '⅙': '1/6', '⅚': '5/6',
    '⅐': '1/7',
    '⅛': '1/8', '⅜': '3/8', '⅝': '5/8', '⅞': '7/8',
    '⅑': '1/9',
    '⅒': '1/10'
}

SUPERSCRIPT = {'¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'}
DIV = {'⁄': '/'}
SUBSCRIPT = {'₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}

UNICODE = {**VULGAR, **SUPERSCRIPT, **DIV, **SUBSCRIPT}

STANDARDIZED = {
    'tablespoon': 'tbsp',
    'teaspoon': 'tsp',
    'c': 'cup',
    'fluid': 'fl',
    'fluid ounce': 'floz',
    'pint': 'pt',
    'quart': 'qt',
    'gallon': 'gal',
    'milliliter': 'ml',
    'millilitre': 'ml',
    'liter': 'l',
    'litre': 'l',
    'gram': 'g',
    'milligram': 'mg',
    'kilogram': 'kg',
    'ounce': 'oz',
    'pound': 'lb',
    'lbs': 'lb',
    'inch': 'in',
    'centimeter': 'cm',
    'centimetre': 'cm',
    'millimeter': 'mm',
    'millimetre': 'mm'
}

# US Legal definitions

MASS = {
    'mg': 0.001,
    'g': 1,
    'oz': 28.375,
    'lb': 454,
    'kg': 1000,
    'ton': 908000
}

VOLUME = {
    'ml': 1,
    'tsp': 5,
    'tbsp': 15,
    'fl oz': 30,
    'cup': 240,
    'pt': 480,
    'qt': 960,
    'l': 1000,
    'gal': 3840
}

LENGTH = {
    'cm': 1,
    'in': 2.54
}

UNITS = {
    "mass": MASS,
    "volume": VOLUME,
    "length": LENGTH
}

# grams / ml
DENSITY = {
    'water': 1,
    
    'flour': 140/240,
    'all purpose flour': 140/240,
    'all-purpose flour': 140/240,
    'cake flour': 140/240,
    'self-raising flour': 140/240,
    
    'cornflour': 122/240,
    'cornstarch': 122/240,
    'corn starch': 122/240,
    
    'sugar': 202/240,
    'granulated sugar': 202/240,
    'white sugar': 202/240,
    'brown sugar': 202/240,
    'caster sugar': 228/240,
    'icing sugar': 126/240,
    'powdered sugar': 126/240,
    'confectioners sugar': 126/240,
    
    'honey': 345/240,
    'butter': 454/480,
    'oil': 214/240,
    'cocoa powder': 111/240
}