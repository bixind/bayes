from math import *
from random import *

wordlen = 3

def filter(s):
    ns = []
    s = s.lower()
    for c in s:
        if c.isalpha():
            ns.append(c)
    return "".join(ns)

def part(s):
    f1 = open(s, "r", encoding='utf-8')
    lyrics = []
    cur = ""
    for s in f1:
        # print(s)
        if len(s) <= 1:
            continue
        if ord(s[0]) == 9 or s[0] == ' ':
            cur += s
        else:
            if (len(cur) > 0):
                lyrics.append(cur)
            cur = ""
    if (len(cur) > 0):
        lyrics.append(cur)
    f1.close()
    return lyrics

def appl(lyr):
    pr = []
    for l in lyr:
        buf = list(i for i in map(filter, l.split()) if len(i) > wordlen)
        if len(buf) > 0:
            pr.append(buf)
    return pr

def read(f):
    return appl(part(f))

class Bayescl:
    pc = 1
    def __init__(self, proc, allcnt):
        self.baseprob = len(proc) / allcnt
        self.count = dict()
        self.allcount = dict()
        self.words = 0
        for l in proc:
            for s in l:
                self.allcount[s] = self.allcount.get(s, 0) + 1
                self.words += 1
            for s in set(l):
                if len(s) > 0:
                    self.count[s] = self.count.get(s, 0) + 1
        self.all = len(proc)
        print(len(self.count))

    def getprob(self, text):
        sum = log(self.baseprob)
        zc = 0
        for word in text:
            cnt = self.count.get(word, 0)
            # print(cnt, end =' ')
            if cnt != 0:
                sum += log(cnt / self.all)
            else:
                zc+=1
                sum += log(1/(self.pc * self.all))
        return sum

    def getprob2(self, text):
        sum = log(self.baseprob)
        zc = 0
        for word in text:
            cnt = self.allcount.get(word, 0)
            # print(cnt, end =' ')
            if cnt != 0:
                sum += log(cnt / self.words)
            else:
                zc+=1
                sum += log(1/(self.pc * self.words))
        return sum




# lyrics = part('push.txt')

# print(lyrics[0])


push = read('push.txt')
lerm = read("lerm.txt")

# for i in push:
#     print(i)

shuffle(push)
shuffle(lerm)

p1 = push[:len(push) // 2]
p2 = push[len(push) // 2:]

l1 = lerm[:(len(lerm) // 2)]
l2 = lerm[(len(lerm) // 2):]

all = len(p1) + len(l1)

# p1 = push
# l1 = lerm

d = open('output.txt', 'w')
for i in lerm:
    print(' '.join(i), file = d)
d.close()

bp = Bayescl(p1, all)
bl = Bayescl(l1, all)

# p2 = push
# l2 = lerm

lg = 0
pg = 0
lg2 = 0
pg2 = 0

for s in p2:
    prp = bp.getprob(s)
    prl = bl.getprob(s)
    if prp < prl:
        pg += 1
    prp = bp.getprob2(s)
    prl = bl.getprob2(s)
    if prp < prl:
        pg2 += 1

for s in l2:
    prp = bp.getprob(s)
    prl = bl.getprob(s)
    if prp > prl:
        lg += 1
    prp = bp.getprob2(s)
    prl = bl.getprob2(s)
    if prp > prl:
        lg2 += 1

print('Pushkin:', pg, 'out of', len(p2), ':' , pg / len(p2))
print('Lermontov:', lg, 'out of', len(l2), ':' , lg / len(l2))
print('Pushkin2:', pg2, 'out of', len(p2), ':' , pg2 / len(p2))
print('Lermontov2:', lg2, 'out of', len(l2), ':' , lg2 / len(l2))


testpr = read('esen.txt')

# testpr = appl(testlr)

print(len(testpr))
# for i in testpr:
#     print(i)

t = sum(testpr, [])

p1 = bp.getprob(t)
print('\n------------------')
p2 = bl.getprob(t)
print()
print(p1, p2)

if (p1 > p2):
    print('Pushkin')
else:
    print('Lermontov')

