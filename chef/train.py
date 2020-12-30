import csv
import pickle
import spacy
import pycrfsuite as crf
import utils as utils


def match_labels(entry, nlp):
    """
    Tokenize recipe line using spacy and label tokens

    Arguments:
        entry: dictionary-like map containing the following
               - "input": <full recipe line> (string)
               - "name": <the ingredient> (string)
               - "qty": <the amount of the ingredient, or 0> (float-like)
               - "range_end": <the upper limit if range, or 0> (float-like)
               - "comment": <other specifications> (string)
        nlp: instance of spacy nlp model

    Sample Input:
        entry: {"input": "1/2 cup oranges, freshly squeezed"
               "name": "orange"
               "qty": 0.5
               "range_end": 0
               "comment": ""}
        nlp: spacy.load('en_core_web_sm')

    Sample Output:
        tokens: ["1/2", "cup", "oranges", ",", "freshly", "squeezed"] (spacy Token objects)
        labels: ["Quantity", "Unit", "Ingredient", "", "Comment", "Comment"] (strings)
    """

    # Raw tokens in line
    tokens = nlp(entry["input"])
    labels = []

    # Labelled parts
    ingr = [token.lemma_ for token in nlp(entry["name"])]
    unit = [utils.standardize(token.lemma_) for token in nlp(entry["unit"])]
    #     comment = [token.lower_ for token in nlp(entry["comment"])]

    try:
        qty = float(entry["qty"])
    except ValueError:
        qty = 0.0

    try:
        upr = float(entry["range_end"])
    except ValueError:
        upr = 0.0

    # Numeric components in line
    numeric = utils.find_numeric(entry["input"])

    # Find numeric component matching qty/upr
    qty_match = upr_match = None

    for match in numeric:
        if qty != 0 and not qty_match and qty == utils.asfloat(match[0]):
            qty_match = match
        if upr != 0 and not upr_match and upr == utils.asfloat(match[0]):
            upr_match = match

    for token in tokens:

        # Check if token corresponds to quantity
        if (qty_match and
                qty_match.start() <= token.idx and
                token.idx + len(token) <= qty_match.end()):
            labels.append("Quantity")

        # Check if token corresponds to upper range
        elif (upr_match and
              upr_match.start() <= token.idx and
              token.idx + len(token) <= upr_match.end()):
            labels.append("Upper Range")

        # Check for other labels
        elif utils.standardize(token.lemma_) in unit:
            labels.append("Unit")
            unit.remove(utils.standardize(token.lemma_))

        elif token.lemma_ in ingr:
            labels.append("Ingredient")
            ingr.remove(token.lemma_)

        #         elif token.lower_ in comment:
        #             labels.append("Comment")
        #             comment.remove(token.lower_)

        # If not a labelled token, tag as ""
        else:
            labels.append("")

    return tokens, labels


def create_sequence(entry, nlp):
    """
    Tokenize and create features to pass crfsuite
    Label each token and tab using BILUO scheme

    Arguments:
        entry: dictionary-like map to pass into match_labels
        nlp: instance of spacy nlp model

    Returns:
        xseq: list of dictionaries containing features
        yseq: list of corresponding BILUO-tagged labels
    """

    tokens, labels = match_labels(entry, nlp)

    yseq = utils.biluo_tag(labels)
    xseq = utils.create_features(tokens)

    return xseq, yseq


def build_dataset(data_path,
                  features_path="features.pkl",
                  labels_path="labels.pkl",
                  save=True):
    """
    Accepts CSV dataset with columns matching keys for match_labels
    Returns (and saves) sequences of features and labels to pass into crf-suite

    Arguments:
        data_path: path to CSV dataset
        features_path: path to save features to
        labels_path: path to save labels to
        save: flag indicating whether or not to save the resulting dataset
    """

    features = []
    labels = []

    nlp = spacy.load('en_core_web_sm')

    with open(data_path) as f:
        reader = csv.DictReader(f)
        for entry in reader:
            x, y = create_sequence(entry, nlp)
            features.append(x)
            labels.append(y)

    if save:
        pickle.dump(features, open(features_path, 'wb'))
        pickle.dump(labels, open(labels_path, 'wb'))

    return features, labels


def train_crf(features_path,
              labels_path,
              model_path,
              params=None,
              algorithm=None):
    """
    Train a CRF using python-crfsuite and return resulting model

    Arguments:
        features_path: path to pickled feature data
        labels_path: path to pickled labels data
        model_path: path to save resulting CRF model to
        params: optional dictionary containing parameters for CRF model
        algorithm: optional specification for optimization algorithm used to train
    """

    model = crf.Trainer()
    if params is not None:
        model.set_params(params)
    if algorithm is not None:
        model.select(algorithm)

    with open(features_path, "rb") as f:
        features = pickle.load(f)

    with open(labels_path, "rb") as f:
        labels = pickle.load(f)

    for xseq, yseq in zip(features, labels):
        model.append(xseq, yseq)

    model.train(model_path)

    return model
