with open('data.txt', 'r') as f:
    data = f.read().split('\n')

while '' in data:
    data.remove('')

SUBJECTS = {}

i = 0
while i < len(data):
    if data[i][0] == '#':
        data.pop(i)
        continue
    data[i] = data[i].split(' - ')
    data[i][1] = ' - '.join(data[i][1:])
    i += 1

data.sort(key=lambda x:int(x[0]))

for num, name in data:
    if '/' in name:
        name = name.replace('/', '-')
    SUBJECTS[num] = name

for i in SUBJECTS:
    print(i, SUBJECTS[i])
