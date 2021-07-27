import requests 
import json

response = requests.get('https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow')
# print(response.json()['items'])
new_list = []
fil_list = []
for data in response.json()['items']:
    
    # if len(data['tags'])== 4:
    #      print((data['tags']))      
    # else:
    #     print('skipped')
    # print(list(value for value in (data['tags']) if value == 'javascript'))
    new_list.append(data['tags'])
    res =    any(value in  (data['tags']) for value in  ['python', 'pandas'])
    if res :
        print(data['tags'])
        fil_list.append(data['tags'])
    # else:
    #     print('not present')
print('--------------------')
print(new_list)
print('--------------------')
fin = all(values in fil_list for values in (fil_list))
if fin:
    print(f'Yes, there are {len(fil_list)} matches, here are the matches', fil_list)