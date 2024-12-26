from kiwipiepy import Kiwi
import csv
# print(reader[0])
kiwi = Kiwi()
nouns = []
input_csv = "C:/work/news_crawler/test.csv"
with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        print(row)
        tokens = kiwi.tokenize(row[0], normalize_coda=False)
        print(tokens)
        temp = []
        for a in range(len(tokens)):
            if tokens[a][1] == 'NNG' or tokens[a][1] == 'NNP':
                temp.append(tokens[a][0])
        nouns.append(temp)
print(nouns)
