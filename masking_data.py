from faker.providers.person.en import Provider
import pandas as pd
import numpy as np

def random_names(name_type, size):
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)
'''
print(f'Name: {faker.name()}')
print(f'First name: {faker.first_name()}')
print(f'Last name: {faker.last_name()}')

print('--------------------------')

print(f'Male name: {faker.name_male()}')
print(f'Female name: {faker.name_female()}')
'''
size = 150000
df = pd.DataFrame(columns=['FN','LN'])

df['FN'] = random_names('first_names', size)
df['LN'] = random_names('last_names', size)
df.to_csv('C:\\Users\\ajkim\\Links\\OneDrive - Sony Tenant\\Desktop\\fake-file.csv')
