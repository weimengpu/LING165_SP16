import glob
import math
import operator

idf = {}
counter = 0.0

for text in glob.glob('wsj/**'):
    text = '/Users/puweimeng/Downloads/l6/' + text
    counter += 1.0
    words = list(set(open(text).readline().split(' ')))
    for word in words:
        if word in idf:
            idf[word] += 1.0
        else:
            idf[word] = 1.0

tf = {}
line = open('WSJ_2325').readline().split(' ')
for ww in line:
    if ww in tf:
        tf[ww] += 1.0
    else:
        tf[ww] = 1.0

score = {}
for key, value in tf.items():
    score[key] = value * math.log10(counter / idf[key])

score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

for result in range(0, 10):
    print score[result][0] + "  " + str(score[result][1]) + "\n"
