import codecs
from collections import defaultdict


def main():
    freqs = read_dewiki_freqs_file("../rsc/dewiki_freqs.txt")
    stopwords = read_stopwords("../rsc/stopwords_de.txt")
    filter_freqs(freqs, stopwords=stopwords)


def read_dewiki_freqs_file(dewiki_inpath):
    print "Reading wikipedia frequencies..."
    freqs = defaultdict(int)

    with codecs.open(dewiki_inpath, 'rb', 'utf-8') as dewiki_infile:
        line = dewiki_infile.readline().strip()
        while line:
            parts = line.split("\t")
            freqs[parts[0]] = int(parts[1])
            line = dewiki_infile.readline().strip()

    return freqs


def read_stopwords(sw_inpath):
    print "Reading stopwords..."
    stopwords = set()

    with codecs.open(sw_inpath, 'rb', 'utf-8') as sw_infile:
        line = sw_infile.readline().strip()
        while line:
            stopwords.add(line)
            line = sw_infile.readline().strip()

    return stopwords


def filter_freqs(freqs, constraint=100, stopwords=set()):
    print "Deleting stopwords from Wikipedia vocabulary ..."
    freq_keys = set(freqs.keys())
    for stopword in stopwords:
        if stopword in freq_keys:
            freqs.pop(stopword, None)

    print "Sorting words in vocab by frequency..."
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1])
    sorted_freqs.reverse()
    for pair in sorted_freqs:
        word, word_freq = pair
        if word_freq >= constraint:
            print word


if __name__ == "__main__":
    main()
