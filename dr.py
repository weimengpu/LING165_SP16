import numpy
import glob

vocab = (open('/Users/puweimeng/Downloads/vocab').read().splitlines())
C = []
r = []

for text in sorted(glob.glob('/Users/puweimeng/Downloads/wsj100/WSJ_****')):
    r.append(text)
    words = open(text).readline().split(' ')
    num = []
    for w in vocab:
        num.append(words.count(w))
    C.append(num)

C = numpy.matrix(C).transpose()
U, s, VT = numpy.linalg.svd(C, full_matrices=False)
S_50 = numpy.matrix(numpy.diag(s[:50]))
U_50 = U[:, :50]
VT_50 = VT[:50, :]
C = U_50 * S_50 * VT_50

query = ['oil', 'industry']
q = []
for ww in vocab:
    q.append(query.count(ww))
q = numpy.matrix([q]).transpose()
q_50 = S_50.getI() * U_50.transpose() * q

D_50 = S_50 * VT_50

score = []
for i in range(100):
    score.append((float(q_50.transpose() * D_50[:, i])) / (numpy.linalg.norm(q_50) * numpy.linalg.norm(D_50[:, i])))
    
for j in reversed(sorted(range(len(score)), key=lambda x: score[x])[-5:]):
    print r[j].split("/")[-1]
