import math

def process_line(line):

    label, subject_line = line.strip().split('\t')
    bow = subject_line.split()
    return label, bow

def update_counts(label, bow, dc, ds, dh, dd1, dd0):

    if not label in dc:
        dc[label] = 0.0
    dc[label] += 1.0

    if label == '1':
        for word in bow:
            if not word in ds:
                ds[word] = 1.0
            elif word in ds:
                ds[word] += 1.0
            dd1 += 1
    elif label == '0':
        for word in bow:
            if not word in dh:
                dh[word] = 1.0
            elif word in dh:
                dh[word] += 1.0
            dd0 += 1

    return dc, ds, dh, dd1, dd0

if __name__ == '__main__':

    lines = open('spam_assassin.train')
    dc = {}
    ds = {}
    dh = {}
    dd1 = 0
    dd0 = 0

    for line in lines:
        label, bow = process_line(line)
        dc, ds, dh, dd1, dd0 = update_counts(label, bow, dc, ds, dh, dd1, dd0)

    #Priors
    pprobSpam = dc['1'] / (dc['1'] + dc['0'])
    pprobHam = dc['0'] / (dc['1'] + dc['0'])

    #TrainedDictionary
    vocab = []
    for c1 in ds:
        if not c1 in vocab:
            vocab.append(c1)
    for c0 in dh:
        if not c0 in vocab:
            vocab.append(c0)

    #TEST
    test = open('spam_assassin.test')
    TP = 0.0
    TN = 0.0
    FP = 0.0
    FN = 0.0

    for l in test:
        la, b = process_line(l)
        listProbSpam = []
        listProbHam = []
        for w in b:
            #if not w in ds:
               # ds[w] = 0.0
            #if not w in dh:
                #dh[w] = 0.0

            sc = ds.get(w, 0.0)
            hc = dh.get(w, 0.0)

            listProbSpam.append((sc + 1.0) / (dd1 + 1.0 + len(ds))) #listProbSpam.append((ds[w] + 1.0) / (dd1 + len(ds)))
            listProbHam.append((hc + 1.0) / (dd0 + 1.0 + len(dh))) #listProbHam.append((dh[w] + 1.0) / (dd0 + len(dh)))

        finalProbSpam = math.log(pprobSpam) #finalProbSpam = pprobSpam
        finalProbHam = math.log(pprobHam) #finalProbHam = pprobHam

        for final1 in listProbSpam:
            finalProbSpam += math.log(final1)#finalProbSpam *= math.pow(final1, l.count(w))
        for final0 in listProbHam:
            finalProbHam += math.log(final0) #finalProbHam *= math.pow(final0, l.count(w))

        predictedLabel = 2
        if finalProbSpam >= finalProbHam:
            predictedLabel = 1
        else:
            predictedLabel = 0

        if predictedLabel == 1 and int(la) == 1:
            TP += 1.0
        elif predictedLabel == 1 and int(la) == 0:
            FP += 1.0
        elif predictedLabel == 0 and int(la) == 0:
            TN += 1.0
        elif predictedLabel == 0 and int(la) == 1:
            FN += 1.0

    #Evaluation...Exciting!
    accuracy = (TP + TN) / (TP + FP + TN + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    fScore = 2 * precision / (precision + recall)

    print ("")
    print 'Accuracy: ', accuracy
    print 'Precision: ', precision
    print 'Recall: ', recall
    print 'FScore: ', fScore
