import pandas as pd
import os
import csv

with open('DataBase_prueba.xlsx', 'rb') as file :
    players = pd.read_excel(file, sheet_name='players', index_col=0, header=0)

with open('test.csv') as doc:
    reader = csv.reader(doc)
    discord_ids = {}
    for idx, row in enumerate(reader):
        if idx == 0:
            cols = row
        else:
            ID = row[0].lower()
            discord_ids[ID] = row[1]
for i in discord_ids:
    print(discord_ids[i])
#print(discord_ids)
#for i in players.index:
#    print(players.loc[i])
#discord_id = int(players.loc[1069808]['prueba'])
#print(players.dtypes)
#print(1069808 in players.index)
