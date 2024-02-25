
import pandas as pd

AAA = pd.read_csv('AAA.csv')
BBB = pd.read_csv('BBB.csv')

update = pd.merge(AAA, BBB, left_on='col1', right_on='col4', how='left')
update['col4'].fillna(-1, inplace=True)

update = update[['col4', 'col2', 'col3']]

update.to_csv('update.csv', index=False)
