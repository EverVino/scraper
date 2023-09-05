import math
import os
import string
import sys

import nltk

nltk.download("punkt")

FILE_MATCHES = 1
SENTENCE_MATCHES = 2


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dirs = os.listdir(directory)
    lista = dict()

    for file in dirs:
        file_path = os.path.join(directory, file)
        with open(file_path, "r", encoding="utf-8") as f:
            lista[file] = f.read()

    return lista


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    ndoc = nltk.word_tokenize(document.lower())
    # ndoc=nltk.tokenize.WhitespaceTokenizer().tokenize(document.lower()) #rev
    for word in ndoc.copy():
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            ndoc.remove(word)

    return ndoc


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    one_words = set()
    set_wordoc = []
    for key in documents:
        one_words |= set(documents[key])
        set_wordoc.append(set(documents[key]))

    nn = len(documents)
    nlistdic = dict.fromkeys(one_words, 0)
    for word in one_words:
        for docs in set_wordoc:
            if word in docs:
                nlistdic[word] += 1

    for w, v in nlistdic.items():
        nlistdic[w] = math.log(nn / v)

    return nlistdic


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    rank = dict.fromkeys(files, 0)

    for word in query:
        for file in files:
            c = list(files[file]).count(word)
            if c > 0:
                rank[file] += c * idfs[word]

    ord_ranks = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))

    return list(ord_ranks.keys())[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rank_sentences = {sentence: [0, 0] for sentence in sentences}

    for sentence, words in sentences.items():
        for word in query:
            if word in words:
                rank_sentences[sentence][0] += idfs[word]
                c = words.count(word)
                rank_sentences[sentence][1] += c
        nn = len(words)
        rank_sentences[sentence][1] = rank_sentences[sentence][1] / nn

    ord_rank = dict(sorted(rank_sentences.items(), key=lambda x: (-x[1][0], -x[1][1])))

    return list(ord_rank.keys())[:n]


if __name__ == "__main__":
    main()
