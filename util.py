inp = input('to regex: ')
splits = inp.split('*')
result_arrs = []
for spl in splits:
    temp = ''
    for i in range(0, len(spl), 2):
        temp += '\\x' + spl[i:i + 2]
    result_arrs.append(temp)
print('.{0,20}'.join(result_arrs))