import spacy
import chef.utils as utils
import argparse
import pycrfsuite as crf
from recipe_scrapers import scrape_me as scrape


def tag(ingredients, model_path, keep_biluo=False):
    """
    Use specified model to tag components for given list of ingredients

    Arguments:
        ingredients: list of strings containing lines of recips
        model_path: trained CRF model
        keep_biluo: flag indicating whether to keep BILUO tags in labels

    Returns:
        List of tags (label, start index, end index, <BILUO>) for each line
    """

    nlp = spacy.load('en_core_web_sm')
    tagger = crf.Tagger()
    tagger.open(model_path)

    results = []

    for line in ingredients:

        tokens = nlp(line)
        features = utils.create_features(tokens)
        prediction = tagger.tag(features)

        tags = []
        for token, pred in zip(tokens, prediction):
            if pred != 'O':
                biluo, label = pred.split('-')
                t = (label, token.idx, token.idx + len(token), biluo)
                tags.append(t)

        if not keep_biluo:
            tags = _join_tags(tags)

        results.append(tags)

    tagger.close()

    return results


def _join_tags(tags):
    """
    Join multiple labels tags with BILUO into one (helper for tag function)
    e.g. Maps (Unit, 1, 4, B), (Unit, 4, 6, L) to (Unit, 1, 6)
    """

    joined = []

    current = None
    idx = None

    for entity, start, end, biluo in tags:
        if biluo == "U":
            joined.append((entity, start, end))
            current = None
        elif biluo == "B":
            current = entity
            idx = start
        elif biluo == "I" and entity == current:
            continue
        elif biluo == "L" and entity == current:
            joined.append((current, idx, end))
            current = None
        else:
            current = None

    return joined

def display(ingredients, model_path):

    tags = tag(ingredients, model_path)

    for line, labels in zip(ingredients, tags):
        print('-' * 40)
        print(line)
        print('-' * 40)
        for label in labels:
            print(f"{line[label[1]:label[2]]}: {label[0]}")
        print('\n')


if __name__ == "__main__":
    """
    Accept a URL and model path via Command Line, scrape recipe and print tagged components
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs=1, type=str, action='store')
    parser.add_argument('model', nargs='?', type=str, action='store', default='spacymodel.crfsuite')
    args = parser.parse_args()

    try:
        ingredients = scrape(args.url[0]).ingredients()
    except:
        print("Could not retrieve recipe from provided URL")
        ingredients = None

    if ingredients is not None:
        try:
            display(ingredients, args.model)
        except:
            raise print("Specified model does not exist or is corrupt")
