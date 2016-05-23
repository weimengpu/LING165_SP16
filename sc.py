"""LING 165 Lab 2: Spelling Correction"""

import sys, pickle, re, math, string, numpy
import kn


def edit(x):
    """List ways to that x could have been derived."""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    n = len(x)
    dd = {};
    di = {};
    ds = {};
    dr = {}
    for i in range(n):
        # reverse insertion error
        xi = x[:i] + x[i + 1:]
        di[xi] = (('#' + x)[i], x[i])
        # reverse substitution error
        for c in alphabet:
            xs = x[:i] + c + x[i + 1:]
            ds[xs] = (c, x[i])
    for i in range(n - 1):
        # reverse transposition error
        xr = x[:i] + x[i + 1] + x[i] + x[i + 2:]
        dr[xr] = (x[i + 1], x[i])
    for i in range(n + 1):
        # reverse deletion error
        for c in alphabet:
            xd = x[:i] + c + x[i:]
            dd[xd] = (('#' + x)[i], c)
    return dd, di, ds, dr


def candidates(t, v):
    """Get real-word candidates of t."""
    dd, di, ds, dr = edit(t)
    out = {}
    for x in dd:
        if x in v: out[x] = ('delete', dd[x])
    for x in di:
        if x in v: out[x] = ('insert', di[x])
    for x in ds:
        if x in v: out[x] = ('substitute', ds[x])
    for x in dr:
        if x in v: out[x] = ('transpose', dr[x])
    return out


def lm(w, lw, rw, v, d):
    """Language model"""
    seq = ' '.join([lw, w, rw])
    lp = kn.logP(False, 2, seq, d, v)
    return lp


def cm(e, (x, y), v, d):
    """Channel model"""
    p = d[e].get((x, y), 0.0)
    lp = -1e+100
    if p > 0.0: lp = math.log(p)
    return lp


def argmax(t, lw, rw, v, cmd, lmd):
    """argmax_c P(t|c)*P(c)
	where
	P(c) ~= P(lw, c, rw)
	and lw: word to the left, rw: word to the right
	"""
    cd = candidates(t, v)
    out = []
    for c in cd:
        e, (x, y) = cd[c]
        lpc = cm(e, (x, y), v, cmd)  # apply channel-model
        lpc += lm(c, lw, rw, v, lmd)  # apply language-model
        out.append((lpc, c))
    out.sort()
    if out != []:
        return out[-1][1]
    else:
        return None


def vocab():
    v = []
    for line in open('vocab'):
        w = line.strip()
        v.append(w)
    return set(v)

def cmd():
    cmd = {'delete': {}, 'insert': {},'substitute': {}, 'transpose': {}}

    d = numpy.zeros(27,27)

    i = numpy.zeros(27,27)

    s = numpy.zeros(27,27)

    t = numpy.zeros(27,27)

    c = numpy.zeros(27)

    f = open('spelling_error.edits').readlines()
    s = f.split()
    s1 = s[::3]
    s3 = s[2::3]
    for sss in s1:
            for ss in sss.strip():
                c[string.lowercase.index(ss) + 1] += 1.0
    for line in s3:
        c[0] += 1.0
        e = line.split(',')
        if e[0] == 'delete':
            d[string.lowercase.index(e[1]),string.lowercase.index(e[2])] += 1.0
        elif e[0] == 'insert':
            i[string.lowercase.index(e[1]),string.lowercase.index(e[2])] += 1.0
        elif e[0] == 'substitute':
            s[string.lowercase.index(e[1]),string.lowercase.index(e[2])] += 1.0
        elif e[0] == 'transpose':
            t[string.lowercase.index(e[1]),string.lowercase.index(e[2])] += 1.0

    for dd in d:
        for ddd in d:
            prob = (d[dd,ddd]) / (c[string.lowercase.index(dd)])
            dict = {(string.ascii_lowercase[dd], string.ascii_lowercase[ddd]): prob}
            cmd.update({'delete': dict})
    for ii in i:
        for iii in i:
            prob = (i[ii,iii]) / (c[string.lowercase.index(ii)])
            dict = {(string.ascii_lowercase[ii], string.ascii_lowercase[iii]): prob}
            cmd.update({'insert': dict})
    for ss in s:
        for sss in s:
            prob = (s[ss,sss]) / (c[string.lowercase.index(ss)])
            dict = {(string.ascii_lowercase[ss], string.ascii_lowercase[sss]): prob}
            cmd.update({'substitute': dict})
    for tt in t:
        for ttt in t:
            prob = (t[tt,ttt]) / (c[string.lowercase.index(tt)])
            dict = {(string.ascii_lowercase[tt], string.ascii_lowercase[ttt]): prob}
            cmd.update({'transpose': dict})

    return cmd

if __name__ == '__main__':
    v = vocab()
    lmd = pickle.load(open('2gram.kn'))

    ## TODO:
    ## Provide a probability dictionary for the channel model:
    ## I. Call the dictionary cmd.
    ## II. The dictionary should have the following structure:
    ## (1) Four keys: 'delete', 'insert', 'substitute', 'transpose'
    ## (2) Each key maps to another dictionary of the form (x, y) : prob(x, y)
    ##     where x and y are (lower-case) letters of the alphabet.
    ## (2-1) (x, y) in 'delete' means delete y after x (i.e. xy -> x);
    ## (2-2) (x, y) in 'insert' means insert y after x (i.e. x -> xy);
    ## (2-3) (x, y) in 'substitute' means change x to  y (i.e. x -> y);
    ## (2-4) (x, y) in 'transpose' means swap x and y (i.e. xy -> yx).
    ## (3) Estimate prob(x, y) using spelling_error.edits
    ##     and the formula for Pr(t|c) in p.206 of Kernighan et al (1990)'s paper.
    ##
    ## Here's a very simple example:
    ## cmd = {
    ##        'delete' : {('a', 'b') : 0.3, ('c', 'd') : 0.01},
    ##        'insert' : {('a', 'c') : 0.02},
    ##        'substitute' : {('b', 'd') : 0.001, ('a', 'e') : 0.07},
    ##        'transpose' : {('a', 'e') : 0.000009}
    ##       }
    ##
    ## You can create this in several ways. To give two examples,
    ## (1) Write a function that creates the dictionary
    ##     somewhere above (preferably above if __name__ == '__main__')
    ##     or in another python program
    ##     and simply call that function here.
    ## (2) Create the dictionary using another program,
    ##     save it as a (pickle) file,
    ##     and load the file into a dictionary here.
    ##

    ## Provide the cmd dictionary in the line below:
	cmd  = cmd()

    ## Don't mess with the lines below:
    f = open('correct_me.txt')
    c = 0.0
    acc = 0.0
    for line in f:
        lc, e, rc = line.strip().split('\t')
        t = re.findall('>(.+?)<', e)[0].strip()
        c = re.findall('targ=(.+?)>', e)[0].strip()
        lw = lc.split()[-1]
        rw = rc.split()[0]
        pred = argmax(t, lw, rw, v, cmd, lmd)
        label = '0'
        c += 1.0
        if c == pred:
            label = '1'
            acc += 1.0
        print '\t'.join([label, pred, line.strip()])

    print "Accuracy: " + (acc/c)*100 + "%"

    f.close()