import pickle, math, logfunc

if __name__ == '__main__':

    pick, n = raw_input("Enter the pickle dictionary and n (separated by space): ").split()
    f = open('sent.100').readlines()
    x = []
    for lines in f:
            for www in lines.split("\t", 1)[1]:
                x.append(www)
    theta = pickle.load(open(pick))

    for i in range(int(n)):
        z = []
        for x1 in x:
            logprobzero = math.log(0.5)
            logprobone = math.log(0.5)
            for w in x1.strip().split():
                if w in theta['0']:
                    logprobzero += math.log(theta['0'][w])
                elif w not in theta['0']:
                    logprobzero += math.log(theta['0']['<UNK>'])
                if w in theta['1']:
                    logprobone += math.log(theta['1'][w])
                elif w not in theta['1']:
                    logprobone += math.log(theta['1']['<UNK>'])

            logjoint = [logprobzero, logprobone]
            for l in logfunc.posterior(logjoint):
                z.append(l)

        sumlogzero = 0
        sumlogone = 0
        for j in z[::2]:
            sumlogzero += j
        for k in z[1::2]:
            sumlogone += k

        for x2 in x:
            for w in x2.strip().split():
                if w in theta['0']:
                    theta['0'][w] = sumlogzero * x2.count(w) + 0.1
                    theta['0'][w] = theta['0'][w] / (sum(theta['0'].get(s1) for s1 in theta['0']))
                elif w not in theta['0']:
                    theta['0']['<UNK>'] = 0.1 / (sum(theta['0'].get(s1) for s1 in theta['0']))
                if w in theta['1']:
                    theta['1'][w] = sumlogone * x2.count(w) + 0.1
                    theta['1'][w] = theta['1'][w] / (sum(theta['1'].get(s2) for s2 in theta['1']))
                elif w not in theta['1']:
                    theta['1']['<UNK>'] = 0.1 / (sum(theta['1'].get(s2) for s2 in theta['1']))

    count = 0.0
    acc = 0.0
    for a in range(len(f)):
        count += 1.0
        final = 1
        pos = 0
        neg = 0
        for w in x[a].strip().split():
            if w in theta['0']:
                neg += theta['0'][w]
            elif w not in theta['0']:
                neg += theta['0']['<UNK>']
            if w in theta['1']:
                pos += theta['1'][w]
            elif w not in theta['1']:
                pos += theta['1']['<UNK>']

        if pos >= neg:
            final = 1
        else:
            final = 0

        if f[a].split("\t", 1)[0].strip() == str(final):
            acc += 1.0
        else:
            acc += 0.0

    print "Accuracy: " + str((acc / count) * 100) + "%"