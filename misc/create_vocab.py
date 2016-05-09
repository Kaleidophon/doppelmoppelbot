import cPickle as pckl
import codecs
import argparse


vocab_path = "../rsc/vocab.pickle"


def main():
    argparser = init_argparse()
    args = argparser.parse_args()
    print args
    total_vocab = merge_vocabularies(args.input)
    save_vocab(total_vocab)


def merge_vocabularies(paths):
    assert len(paths) > 0
    total_vocab = set()

    for path in paths:
        total_vocab.union(read_vocabular(path))

    return total_vocab


def save_vocab(vocab):
    global vocab_path
    encoded_vocab = set()

    for entry in vocab:
        encoded_vocab.add(entry.decode('latin-1'))

    with open(vocab_path, 'wb') as vocab_file:
        pckl.dump(encoded_vocab, vocab_file)


def read_vocabular(vocab_inpath):
    vocab = set()

    with codecs.open(vocab_inpath, 'rb', 'utf-8') as vocab_infile:
        line = vocab_infile.readline()
        while line:
            vocab.add(line.strip())
            line = vocab_infile.readline()

    return vocab


def init_argparse():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input',
                            nargs='+',
                            required=True,
                            help='Paths to vocabulary files.')
    return argparser

if __name__ == "__main__":
    main()
