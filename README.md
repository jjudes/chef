Chef
----------

A work in progress :)  
. . . . . .

### The Home Cook's Problem

As an ambitious home cook, you probably have more than a few recipes saved. 
So when when there's an occasion, you pick out a few recipes that you're going to put together. 
Maybe something like:

```
Mashed Potatoes
- 2 lbs Yukon Gold potatoes
- 50 ml heavy cream
- 4 tbsp butter
- 1 clove garlic
```

```
Oven-Roasted Turkey
- 1 Young Turkey, 3-5 lbs.
...
- 1 cup + 1 tbsp butter, room temperature
- 1 head garlic
```

Now before you go to shop for your ingredients, it'd be nice to have one consolidated grocery list.

### The Programmer's Problem

You can imagine we can automatically consolidate these lists programmatically, but we have some tricky cases:

- Which part is the quantity? Typically we have `{quantity}` `{unit}` `{ingredient}`, but recipes are unfortunately not
so straightforward! `1 cup + 1 tbsp butter` throws a wrench in things
- Obviously `butter` and `butter, room temperature` are the same ingredient, but how can we tell? 

The naive solution would be to map out a large number of parsing rules but 
this is laborious and we'll never be able to cover _all_ cases this way.

### Chef's Solution

If we were able to tag each word (token) in a recipe line as `quantity`, `unit`, `ingredient`, or `instruction` we'd 
be in pretty good shape for consolidating grocery lists!

Of course a single token won't _always_ be just one of the above. 
E.g. pound can be both a unit or and an ingredient token depending on context: `1 pound lemons`, `500g pound cake`

We can solve this problem in a generalizable way by using machine learning to predict the class of a word depending on
the context words around it.

This problem is called **Named Entity Recognition** and is exactly what chef is for!

### How It Works

1. Chef uses `recipe-scrapers` to extract recipe line listing from any supported URL domains.

2. For each recipe, Chef uses `spacy` for preprocessing/features and Conditional Random Fields to classify each token
in the sequence into `quantity`, `unit`, etc.

3. The quantity and units are converted to a standard unit (e.g. grams, millilitres) if possible

4. Consolidate recipe lines with the same `ingredient` and add together the quantities where possible
