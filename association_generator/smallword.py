import requests

base_url = 'https://smallworldofwords.org/search/en/dictionary/all/'


def get_synonyms(concept, degree=1, min_backward=-1, min_forward=-1, min_freq=-1):
    """

    :param concept: String
    :param degree: Int degree for association exploration
    :param min_backward: Int
    :param min_forward: Int
    :param min_freq: Float minimum frequency to be considered as
    :return syms: List of String

    """

    syms = list()

    # replace underscore with whitespace
    if '_' in concept:
        concept = concept.replace('_', ' ')

    # request the result
    link = base_url + concept

    try:
        sym_list = eval(requests.get(url=link).text)
    except:
        return []

    if len(sym_list):
        # association_types: 'forward', 'backward', 'synonyms'

        if min_forward == -1 or len(sym_list['forward']) <= 5:
            syms += [item['word'] for item in sym_list['forward']]
        else:
            for words in sym_list['forward']:
                if words['freq'] > min_forward:
                    syms.append(words['word'])

        if min_backward == -1 or len(sym_list['backward']) <= 5:
            syms += [item['word'] for item in sym_list['backward']]
        else:
            for words in sym_list['backward']:
                if words['freq'] > min_backward:
                    syms.append(words['word'])

        related = sym_list['synonyms']

        if len(related) > 5 and min_freq != -1:
            for i in range(5):
                syms.append(related[str(i + 1)]['word'])
            for i in range(5, len(related)):
                if related[str(i + 1)]["S"] > min_freq:
                    syms.append(related[str(i + 1)]['word'])
        else:
            for item in related:
                syms.append(related[item]['word'])

    syms_all = syms
    if degree > 1:
        syms = list(set(syms))
        for item in syms:
            syms_all += get_synonyms(item, degree-1, min_backward, min_forward, min_freq)
    return list(set(syms_all))


def get_synonyms_smallword(concept, degree=1, args=None):
    """

    :param concept: String
    :param degree: Int degree for association exploration
    :param args: Dictionary arguments for SWOW association
    :return syms: List of String

    """
    if args and 'min_freq' in args and args['min_freq']:
        min_freq = float(args['min_freq'])
    else:
        min_freq = -1
    if args and 'min_backward' in args and args['min_backward']:
        min_backward = int(args['min_backward'])
    else:
        min_backward = -1
    if args and 'min_forward' in args and args['min_forward']:
        min_forward = int(args['min_forward'])
    else:
        min_forward = -1

    return get_synonyms(concept, degree, min_backward, min_forward, min_freq)
