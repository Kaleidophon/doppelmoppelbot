import codecs
import re


def main():
    """
    Main function
    """
    dict_entries = filter_dict("../rsc/dict_cut.txt")
    write_cleaned_entries(dict_entries, "../rsc/entries_cleaned.txt")


def filter_dict(dict_inpath):
    """
    Filters first column entries of dict.cc export file.

    @param dict_inpath: Path to input file
    @type dict_inpath: str
    @return Set of dictionary entries
    @rtype set
    """
    dict_entries = set()

    with codecs.open(dict_inpath, 'rb', 'utf-8') as dict_infile:
        line = dict_infile.readline()
        while line:
            for entry in line.strip().split("/"):
                dict_entries.add(clean_dict_entry(entry.strip()))
            line = dict_infile.readline()

    return dict_entries


def write_cleaned_entries(dict_entries, dict_outpath):
    """
    Write cleaned dictionary entries into a file.

    @param dict_entries: Set of dictionary entries.
    @type dict_entries: set
    @param dict_outpath: Path to output file
    @type dict_outpath: str
    """
    with codecs.open(dict_outpath, 'wb', 'utf-8') as dict_outfile:
        for dict_entry in dict_entries:
            dict_outfile.write("%s\n" % dict_entry)


def clean_dict_entry(line):
    """
    Removes all kinds of parenthesis from dictionary entry.

    @param line: Entry to be cleaned.
    @type line: str
    @return Cleaned entry
    @rtype str
    """
    line = re.sub(r'\([^)]*\)', '', line)
    line = re.sub(r'\{[^}]*\}', '', line)
    line = re.sub(r'\[[^]]*\]', '', line)
    line = re.sub(r'<[^>]*>', '', line)
    return line.strip()


if __name__ == "__main__":
    main()
