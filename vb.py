import math  # We'll use math.log(x)
import pickle

# Part 1. Build trellis.

def create_column(pd, A, B, word):
    # Create a column of states to add to our trellis.
    # What are those states?
    # (1) Reachable states (from previous column)
    # (2) Generating states (can spit out this word)
    cd = {}  # current column
    for prev_state in pd:  # from each prev-state in previous column
        reachables = A[prev_state].keys()  # list reachable states
        for reachable in reachables:  # for each reachable state
            if word in B[reachable].keys():  # can this reachable gen word?
                if not reachable in cd:  # is this reachable new?
                    cd[reachable] = [None, None]  # initialize with dummies
                score = pd[prev_state][0]  # log-delta from prev-state
                score += math.log(A[prev_state][reachable])  # A
                score += math.log(B[reachable][word])  # B
                if cd[reachable][0] < score:  # is new score better?
                    cd[reachable] = [score, prev_state]
    return cd


def build(A, B, words):
    # Build a trellis as a list of dictionaries:
    # (1) one dictionary per column
    # (2) one key per state in column
    # (3) d[key] = [log-delta, crumb]
    # (3-1) log-delta(state) = max [ log-delta(prev-state) + log(A[prev-state][state]) + log(B[state][word]) ]
    # (3-2) crumb = argmax log-delta(state)
    # Build the trellis in following procedure:
    # Step 1. First column
    # Step 2. Use previous column to create next column.
    # Step 3. Repeat step 2 until we run out of words.
    # Yay!
    t = []  # trellis
    # Step 1. The first column
    first_column = {'<s>': [0.0, None]}
    t.append(first_column)
    # Step 2. Add column based on previous column.
    for i in range(1, len(words)):
        word = words[i]  # latest word
        pd = t[-1]  # previous column (last entry in trellis)
        t.append(create_column(pd, A, B, word))  # add new column
    return t


# Part 2. Trace-back: follow the bread-crumbs.


def best(t):
    # Find the best path in the trellis.
    crumbs = ['</s>']  # store crumbs here
    for i in range(len(t) - 1, 0, -1):
        crumb = t[i][crumbs[-1]][1]
        crumbs.append(crumb)
    crumbs.reverse()
    return crumbs


def tag(A, B, sent):
    words = ['<s>'] + sent.split() + ['</s>']
    t = build(A, B, words)
    return best(t)


if __name__ == '__main__':
    A = pickle.load(open('A.pickle'))
    B = pickle.load(open('B.pickle'))
    lines = open('brown.test').readlines()
    answers = open('brown.test.answers')
    num = 0.0
    den = 0.0
    for line in lines:
        sent = line.strip()
        tags = tag(A, B, sent)[1:-1]
        out = ''
        words = sent.split()
        for i in range(len(words)):
            out += words[i] + '_#_' + tags[i] + ' '
        answer = answers.readline().strip()
        acc = answer.split()
        comp = out.split()
        for k in range(len(comp)):
            if comp[k].split('_#_')[1] == acc[k].split('_#_')[1]:
                num += 1.0
            den += 1.0
        
    print num / den