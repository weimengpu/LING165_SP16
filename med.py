def minEditDist(target, source):

    if len(target) < len(source):

        return minEditDist(source, target)

    if len(source) == 0:

        return len(target)

    m = len(target) + 1
    n = len(source) + 1

    pRow = range(n)

    for i, l1 in enumerate(target):

       cRow = [i + 1]

       for j, l2 in enumerate(source):

            if l2 == l1:
                cRow.append(pRow[j])

            else:
                deletion = cRow[-1]
                insertion = pRow[j + 1]
                substitution = pRow[j]

                cRow.append(1 + min(deletion, insertion, substitution))

       pRow = cRow

    return pRow[-1]

if __name__ == '__main__':

    lines = open('spelling_error.pairs')

    count = 0.0
    dd1 = 0.0
    dd2 = 0.0

    for line in lines:

        count += 1.0

        target, source = line.strip().split()

        result = minEditDist(target, source)

        if result == 1:

            dd1 += 1.0

        elif result == 2:

            dd2 += 1.0

    print("")
    print 'Percentage of pairs with distance of 1: ', dd1 / count
    print("")
    print 'Percentage of pairs with distance of 2: ', dd2 / count



