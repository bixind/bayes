f = open('test.txt', 'r', encoding='windows-1251')
o = open('test1.txt', 'w', encoding='utf-8')
for s in f:
    b = s.encode()
    print(b.decode(), file = o)
f.close()
o.close()
