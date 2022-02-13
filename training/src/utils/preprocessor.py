import src.utils.parser as parser


def create_features(tokens):
    """
    Create crfsuite features for list of tokens using token attributes

    Arguments:
        tokens: List of spacy Tokens

    Return:
        seq: List of dictionaries containing feature name and value
    """

    seq = []
    is_parenthetical = False

    for token in tokens:

        features = {
            "token": token.lower_,
            "length": len(token),
            "is_numeric": parser.isnumeric(token.text),
            "is_punctuation": token.is_punct,
            "is_title": token.is_title,
            "is_parenthetical": is_parenthetical,
            "entity": token.ent_type_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dependency": token.dep_
        }

        seq.append(features)

        if token.text == "(":
            is_parenthetical = True
        if token.text == ")":
            is_parenthetical = False

    return seq


def biluo_tag(y):
    """
    Append BILUO tags to the beginning of each label

    Arguments:
        y: List of labels

    BILUO is specified as follows:
        BEGIN - The first token of a multi-token entity.
        IN ---- An inner token of a multi-token entity.
        LAST -- The final token of a multi-token entity.
        UNIT -- A single-token entity.
        OUT --- A non-entity token.
    """

    n = len(y)

    # Trivial cases of empty or unit sequence
    if n == 0:
        return []
    if n == 1:
        if not y[0]:
            return ["O"]
        else:
            return ["U-" + y[0]]

    tagged = []

    # First label can only be B, U, or O
    if not y[0]:
        tagged.append("O")
    elif y[0] == y[1]:
        tagged.append("B-" + y[0])
    else:
        tagged.append("U-" + y[0])

    # Intermediary labels
    for i in range(1, n - 1):

        prv = y[i] == y[i - 1]
        nxt = y[i] == y[i + 1]

        if not y[i]:
            tagged.append("O")
        elif not prv and nxt:
            tagged.append("B-" + y[i])
        elif prv and nxt:
            tagged.append("I-" + y[i])
        elif prv and not nxt:
            tagged.append("L-" + y[i])
        else:
            tagged.append("U-" + y[i])

    # Last label can only be L, U, or O
    if not y[n - 1]:
        tagged.append("O")
    elif y[n - 1] == y[n - 2]:
        tagged.append("L-" + y[n - 1])
    else:
        tagged.append("U-" + y[n - 1])

    return tagged
