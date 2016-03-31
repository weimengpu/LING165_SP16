import random


# (Aux) Pad sentences. -> DONE!
# (1) Store n-gram tokens.
# (2) Randomly generates a sentence.

def pad(n, line):
    # e.g.
    # n = 3, the coffee is good
    # -> <s> <s> the coffee is good </s>
    out = '<s> ' * (n - 1)
    out += line.strip()
    out += ' </s>'

    return out


def update_ngram_dictionary(n, line, d):
    # Incorporate ngrams from line into d.
    # 1. Pad the line.
    line = pad(n, line)
    # 2. Extract and store n-grams.
    words = line.split()

    for i in range(0, len(words) - (n - 1)):

        ngram = words[i: i + n]
        prefix = ' '.join(ngram[:-1])  # a string made of first n-1 words
        word = ngram[-1]  # the last word

        if not prefix in d: d[prefix] = []
        d[prefix].append(word)

    return d


def gen(n, d):
    # Generate a random sentence.
    sent = []
    prefix = '<s> ' * (n - 1)
    prefix = prefix.strip()
    last_word = ''

    while last_word != '</s>':

        word_list = d[prefix]
        last_word = random.choice(word_list)
        sent.append(last_word)
        ngram = prefix + ' ' + last_word
        suffix = ngram.split()[1:]
        prefix = ' '.join(suffix)

    sent = ' '.join(sent[:-1])

    return sent


if __name__ == '__main__':

    n = input('N-gram: ')
    d = {}
    f = open('bullshit.txt', 'r')

    for line in f:

        d = update_ngram_dictionary(n, line, d)

    f.close()

    for i in range(10):

        print str(i) + ') ' + gen(n, d)
