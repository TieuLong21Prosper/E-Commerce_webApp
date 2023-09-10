# D = {'a': 1, 'b': 2, 'c': 3}
# for key in D:
#     print(key, '=>', D[key])


# for (key, value) in D.items():
#     print(key, '=>', value)


# for (a, c, _) in [(1, 2, 3, 4), (5, 6, 7, 8)]:
#     print(a,c)


# list = [11, 22, 13, 14, 15, 16, 17, 18, 19, 20]
# for i in range(1, len(list), 3):
#     print(list[i])

# L = [1, 2, 3, 4, 5]
# for i in range(len(L)):
#     L[i] = L[i] + 1
# print(L)
# # >>> L ???


# L = [1, 2, 3, 4, 5]
# for x in L:
#     x += 1
# print(L)

# L1 = [1,3,5,7] # 4
# L2 = [2,4,6,8] # 4
# for (x, y) in zip(L1, L2):
#     print(x, y, '--', x+y)

for line in open('script2.py').readlines():
    print(line.upper(), end='')

f = open('script2.py')
while True:
    line = f.readline()
    if not line:
        break
    print(line.upper(), end='')