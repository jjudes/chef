import argparse
from recipe import Recipe


def new_list(name, recipe_urls, model_path="model.crfsuite"):

    recipes = []
    for url in recipe_urls:
        try:
            recipe = Recipe(url, model_path)
            recipes.append(recipe)
        except:
            print("Could not parse " + url)

    grocery_list = {}

    for recipe in recipes:
        for ingredient in recipe.ingredients:
            if ingredient.name not in grocery_list:
                grocery_list[ingredient.name] = ingredient
            else:
                try:
                    combined = grocery_list[ingredient.name] + ingredient
                    grocery_list[ingredient.name] = combined
                except:
                    grocery_list[str(ingredient.name)+"*"] = ingredient

    with open(name+".txt", "w") as file:
        ingredients = [repr(ingr) for ingr in grocery_list.values()]
        file.write("\n".join(ingredients))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs=1, type=str, action='store')
    parser.add_argument('urls', nargs='+', type=str, action='store', default='model.crfsuite')
    parser.add_argument('--model', nargs='?', type=str, action='store', default='model.crfsuite')

    args = parser.parse_args()
    if args.filename[0].endswith(".txt"):
        filename = args.filename[0][:-4]
    else:
        filename = args.filename[0]

    new_list(filename, args.urls, args.model)
