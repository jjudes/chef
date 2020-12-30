from chef.tag import tag
from chef.ingredient import Ingredient
from recipe_scrapers import scrape_me as scrape


class Recipe:
    """
    Class that scrapes a URL containing a recipe and stores structured info
    Ingredient in recipe are tagged using CRF model and stored as Ingredient
    """

    def __init__(self, url, model_path):
        """
        Arguments:
            url: Recipe URL supported by recipe_scrapers package
            model_path: Path to trained CRF model
        """

        # Try to scrape given URL using recipe_scrapers
        self.url = url
        recipe = scrape(url)

        # Extract essential info from scrape results
        self.instructions = recipe.instructions().split('\n')
        self.title = recipe.title()
        self.servings = recipe.yields()
        self.publisher = recipe.host()

        # Parse ingredients using model
        self.ingredients = []
        ingredient_tags = tag(recipe.ingredients(), model_path)

        for line, tags in zip(recipe.ingredients(), ingredient_tags):

            ingredient = None
            quantity = None
            unit = None

            for entity, start, end in tags:
                if tag == "Ingredient" and ingredient is None:
                    ingredient = line[start:end]
                if tag == "Quantity" and quantity is None:
                    quantity = line[start:end]
                if tag == "Unit" and unit is None:
                    unit = line[start:end]

            ingr = Ingredient(ingredient, quantity, unit, line)
            self.ingredients.append(ingr)

    def __repr__(self):

        sep = '-' * 20
        numbered = enumerate(self.instructions)
        instructions = [str(n + 1) + '. ' + line for n, line in numbered]

        return (self.title + '\n'
                             '(Source: ' + self.url + ')'
                                                      '\n\n' + sep + '\n\n' +
                "Ingredients:" + '\n\n' +
                '\n'.join([repr(ingr) for ingr in self.ingredients]) +
                '\n\n' + sep + '\n\n' +
                "Instructions:" + '\n\n' +
                '\n\n'.join(instructions))
