import cPickle as pckl
import codecs
import argparse

VOCAB_PATH = "../rsc/vocab.pickle"


def main():
    """ Main method. """
    argument_parser = init_argument_parser()
    args = argument_parser.parse_args()
    print args

    # Save vocabulary to a pickle file
    if args.write:
        args_dict = vars(args)
        viable_options = {"min_length", "max_length", "mwes"}
        options = {
            option: args_dict[option] for option in args_dict
            if option in viable_options
        }

        total_vocab = merge_vocabularies(args.input)
        print len(total_vocab)
        save_vocab(total_vocab, options=options)

    # Load vocabulary from a pickle file
    elif args.read:
        total_vocab = load_vocab()
        print total_vocab, len(total_vocab)


def merge_vocabularies(paths):
    """
    Merges multiple files containing vocabulary.

    Args:
        paths (list): List of path to input files.

    Returns:
        set: Set of all words in vocabulary.
    """
    assert len(paths) > 0
    total_vocab = set()

    for path in paths:
        total_vocab = total_vocab.union(read_vocabulary(path))

    return total_vocab


def save_vocab(vocab, options={}):
    """
    Saves vocabulary to a pickle file.

    Args:
        vocab (set): Set of all words in vocabulary.
        options (dict): Filtering options.
    """
    global VOCAB_PATH
    encoded_vocab = set()

    for entry in vocab:
        try:
            if False not in check_constraints(entry, options):
                print entry
                encoded_vocab.add(entry.decode('latin-1'))
        except UnicodeEncodeError:
            continue

    with open(VOCAB_PATH, 'wb') as vocab_file:
        pckl.dump(encoded_vocab, vocab_file)


def check_constraints(word, options):
    """
    Enforce filtering constraints on the vocabulary.

    Args:
        word (str): Current vocabulary to be checked.
        options (dict): Filtering options.

    Returns:
        list: List of filtering results with booleans for each check.
    """
    # Defining checks
    def _min_length_check(_word, min_length):
        if len(_word) < min_length:
            return False
        return True

    def _max_length_check(_word, max_length):
        if len(_word) > max_length:
            return False
        return True

    def _multi_word_check(_word, mwes):
        return True if mwes else (' ' not in _word)

    # Enforcing constraints
    checks = {
        "min_length": _min_length_check,
        "max_length": _max_length_check,
        "mwes": _multi_word_check
    }

    results = []

    for option in options:
        arg = options[option]
        results.append(checks[option](word, arg))

    return results


def load_vocab():
    """
    Load vocabulary from pickle file.

    Returns:
        set: Set of all words in vocabulary.
    """
    global VOCAB_PATH

    with open(VOCAB_PATH, 'rb') as vocab_file:
        vocab = pckl.load(vocab_file)
        print vocab

        decoded_vocab = set()

        for entry in vocab:
            decoded_vocab.add(entry.encode('latin-1'))

        return decoded_vocab


def read_vocabulary(vocab_inpath):
    """
    Read a vocabulary file with one word per line.

    Args:
        vocab_inpath (str): Path to vocabulary file.

    Returns:
       set: Set of all words in vocabulary.
    """
    vocab = set()

    with codecs.open(vocab_inpath, 'rb', 'utf-8') as vocab_infile:
        line = vocab_infile.readline()
        while line:
            vocab.add(line.strip())
            line = vocab_infile.readline()

    return vocab


def init_argument_parser():
    """
    Initialize the argument parser for this script.

    Returns:
        argparse.ArgumentParser: ArguementParser object
    """
    argument_parser = argparse.ArgumentParser()

    # Basic arguments
    argument_parser.add_argument(
        '--input',
        nargs='+',
        help='Paths to vocabulary files.'
    )

    argument_parser.add_argument(
        '-r',
        '--read',
        action='store_true',
        help='Enable reading mode.'
    )

    argument_parser.add_argument(
        '-w',
        '--write',
        action='store_true',
        help='Enable writing mode.'
    )

    # Filtering options
    argument_parser.add_argument(
        '--min',
        type=int,
        help='Minimum length of a word.'
    )

    argument_parser.add_argument(
        '--max',
        type=int,
        help='Maximum length of a word.'
    )

    argument_parser.add_argument(
        '--mwes',
        action='store_true',
        default=False,
        help="Are multi-word entries allowed or not?"
    )

    return argument_parser

if __name__ == "__main__":
    main()
