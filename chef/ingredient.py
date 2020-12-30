import chef.utils as utils


class Ingredient:
    """
    Class storing structured information about an ingredient in a recipe
    """

    def __init__(self, name, quantity=None, unit=None, text=None):
        """
        Arguments:
            name: Name of the ingredient
            quantity: Numeric quantity of ingredient
            unit: Unit quantity is specified in
            text: Raw text given in recipe, used for display if available
        """

        assert (name is not None or text is not None)

        assert (isinstance(text, (str, type(None))))
        self.text = text

        assert (isinstance(name, (str, type(None))))
        self.name = name

        assert (isinstance(unit, (str, type(None))))
        self.unit = utils.standardize(unit)
        self._unit = unit
        self.unit_type = utils.unit_type(self.unit)

        if isinstance(quantity, str):
            assert (utils.isnumeric(quantity))
            self.quantity = utils.asfloat(quantity)
            self._quantity = quantity
        elif isinstance(quantity, (int, float)):
            assert (quantity >= 0)
            self.quantity = float(quantity)
            self._quantity = str(quantity)
        else:
            assert (quantity is None)
            if self.unit is not None:
                self.quantity = 1.0
                self._quantity = "1.0"
            else:
                self.quantity = self._quantity = None

    def __repr__(self):
        """
        Returns a formatted version of the ingredient or the original recipe
        text if it is available
        """
        if self.text:
            return self.text

        else:
            s = ""
            if self._quantity:
                s += self._quantity + " "
            if self._unit:
                s += self._unit + " "

            s += self.name
            return s

    def __eq__(self, a):
        """
        Check equality of two Ingredients using name, quantity, and unit
        """

        if isinstance(a, Ingredient):
            check = [
                self.name == a.name,
                self.quantity == a.quantity,
                self.unit == a.unit
            ]

            return all(check)

        return False

    def __add__(self, a):
        """
        Add to the quantity of the Ingredient by specifying another Ingredient
        with matching name attribute or a numeric quantity
        """

        assert (self.name is not None and self.quantity is not None)

        if isinstance(a, Ingredient):

            assert (self.name == a.name and a.quantity is not None)

            if self.unit is None and a.unit is None:
                total = self.quantity + a.quantity

            else:
                factor = utils.conversion(self.unit, a.unit, self.name)

                if factor < 1:
                    total = a.quantity + factor * self.quantity
                else:
                    total = self.quantity + a.quantity / factor

            return Ingredient(self.name, total, self.unit)

        else:
            assert (isinstance(a, (int, float)) and a >= 0)
            return Ingredient(self.name, self.quantity + a, self.unit)

    def convert_to(self, unit, inplace=False):
        """
        Convert the quantity to the desired unit
        """

        try:
            factor = utils.conversion(self.unit, unit, self.name)
        except:
            print(f"{unit} incompatible with {self._unit} or unrecognized")
            return None

        if inplace:
            self.quantity = factor * self.quantity
            self._quantity = str(self.quantity)
            self.unit = utils.standardize(unit)
            self._unit = unit
            return self
        else:
            return Ingredient(self.name, factor * self.quantity, unit)
