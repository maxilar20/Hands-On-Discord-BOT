import json, csv, os, glob


items = {}
for infile in glob.glob("./discordid/*.json"):
        print(infile)
        with open(infile, 'r') as f:
            data = tuple(json.load(f).items())
            print(data[0][0])
            items[data[0][0]] = data[0][1]
with open('test.csv', 'w') as f:
    for key in items.keys():
        f.write('{},"{}"\n'.format(key,items[key]))
print(items)
