users = [
    {'firstname' : 'kristen', 'lastname': 'moreland'},
    {'firstname' : 'khalil', 'lastname': 'sanmartin'},
]

for x in users:
    print('<tr>')
    for val in x.values():
        print(f'<td> {val} </td>')
    print('<td>')
    for val in x.values():   
        print(f'{val}')
    print('</td>')
    print('</tr>')
