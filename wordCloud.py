import pandas

removeCommonWords = True  ## (True or False)
removeCommonSymbols = True  ## (True or False)

commonWords = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.', '&', 'A', 'ABLE', 'ABOUT', 'ABSOLUTELY', 'AFTER',
               'AGAIN', 'ALL', 'ALONG', 'ALSO', 'ALWAYS', 'AM', 'AN', 'AND', 'ANOTHER', 'ANY', 'ANYONE', 'ANYTHING',
               'ANYWHERE', 'ARE', 'AROUND', 'AS', 'ASKED', 'AT', 'AWAY', 'BACK', 'BE', 'BECAUSE', 'BECOME', 'BEEN',
               'BEFORE', 'BEST', 'BETTER', 'BETWEEN', 'BIGGEST', 'BOTH', 'BRING', 'BUT', 'BY', 'CAME', 'CAN', 'CAN''T',
               'CANNOT', 'CANT', 'CHANCE', 'COME', 'COMES', 'COULD', 'COULDN''T', 'DEFINITELY', 'DID', 'DIDN''T', 'DO',
               'DOES', 'DOESN''T', 'DOING', 'DON''T', 'DONE', 'DURING', 'EACH', 'ELSE', 'ENOUGH', 'ENTIRE',
               'ESPECIALLY', 'EVEN', 'EVER', 'EVERY', 'EVERYDAY', 'EVERYONE', 'EVERYTHING', 'FELT', 'FEW', 'FIRST',
               'FOR', 'FROM', 'FRONT', 'GET', 'GETS', 'GETTING', 'GIVE', 'GIVEN', 'GIVES', 'GO', 'GOES', 'GOING',
               'GOOD', 'GOT', 'GREAT', 'HAD', 'HAS', 'HASN''T', 'HAVE', 'HAVEN''T', 'HAVING', 'HE', 'HE''S', 'HELPED',
               'HER', 'HER.', 'HERE', 'HERSELF', 'HERSELF.', 'HI', 'HIM', 'HIS', 'HOW', 'I', 'I''D', 'I''LL', 'I''M',
               'I''VE', 'IF', 'IM', 'IN', 'INTO', 'IS', 'IT', 'IT.', 'IT''S', 'ITS', 'JUST', 'KEEP', 'KEEPS', 'KNOW',
               'LAST', 'LET', 'LIKE', 'LOOKS', 'LOT', 'MADE', 'MAKE', 'MAKES', 'MAKING', 'MANY', 'MATTER', 'MAY', 'ME',
               'ME.', 'MEANS', 'MORE', 'MORE.', 'MOST', 'MUCH', 'MY', 'MYSELF', 'NEARLY', 'NEED', 'NEEDS', 'NEVER',
               'NEXT', 'NO', 'NOT', 'NOTHING', 'NOW', 'OF', 'ON', 'ONE', 'ONLY', 'OR', 'OTHER', 'OTHERS', 'OUR', 'OUT',
               'OVER', 'OWN', 'PLEASE', 'PROBABLY', 'PUT', 'PUTS', 'REALLY', 'RECENTLY', 'SAID', 'SAME', 'SAW', 'SAY',
               'SEE', 'SEEN', 'SHE', 'SHE''S', 'SHOULD', 'SIMPLE', 'SINCE', 'SO', 'SOME', 'SOMEONE', 'SOMETHING',
               'SOMEWHERE', 'SPECIAL', 'STILL', 'SUCH', 'SURE', 'SURELY', 'TAKE', 'TAKES', 'TELL', 'TH', 'THAN', 'THAT',
               'THAT''S', 'THE', 'THEIR', 'THEM', 'THEN', 'THERE', 'THESE', 'THEY', 'THING', 'THINGS', 'THINK',
               'THINKING', 'THIS', 'THOSE', 'THOUGH', 'THOUGHT', 'THREE', 'THROUGH', 'TILL', 'TO', 'TOGETHER', 'TOLD',
               'TOO', 'TOOK', 'TOWARDS', 'TRULY', 'TRYING', 'U', 'UNTIL', 'UP', 'UR', 'US', 'US.', 'USE', 'VERY', 'VIA',
               'WANT', 'WANTED', 'WANTS', 'WAS', 'WAY', 'WE', 'WE''RE', 'WENT', 'WERE', 'WHAT', 'WHATEVER', 'WHEN',
               'WHENEVER', 'WHERE', 'WHICH', 'WHILE', 'WHO', 'WHOM', 'WHY', 'WILL', 'WITH', 'WITHIN', 'WITHOUT',
               'WOULD', 'YET', 'YOU', 'YOU.', 'YOU''D', 'YOU''RE', 'YOUR']

commonSymbols = ['~', '`', '!', '@', '#', '£', '€', '$', '¢', '¥', '§', '%', '°', '^', '&', '*', '(', ')', '-', '_',
                 '+', '=', '{', '}', '[', ']', '|', '\\', '/', ':', ';', "'", ',', '<', '>', '.', '?', '“', '”', '-',
                 '–', '’', '"', '\n', ' ', '\r', '\t']

from pandas import *
# Import the domomagic package into the script
# from domomagic import *

# read data from inputs into a data frame
input1 = read_csv('cases_description.csv')  ## SET TO YOUR TABLE NAME
# print(input1.info())
# write your script here
tempOutput = []
valueColumn = input1["description"].dropna() ## SET TO YOUR COLUMN TO SPLIT
for i, row in enumerate(valueColumn):
    values = row.split(" ")
    for value in values:
        if removeCommonSymbols:
            for symbol in commonSymbols:
                value = value.replace(symbol, "")
        if removeCommonWords and value.upper() not in commonWords:
            newData = {"id": input1['id'][i], "word": value.lower()}
            tempOutput.append(newData)
        elif not removeCommonWords:
            newData = {"id": input1['id'][i], "word": value.lower()}
            tempOutput.append(newData)

output = pandas.DataFrame(tempOutput)

# output = output.drop('description', axis=1)
# output['occurances'] = 1
wordcount = output.groupby('word').nunique().sort_values(by='id', ascending=False).rename(columns={'word': 'word','id': 'occurrence'})

# print(output.head(100))
print(wordcount.head(100))
# print(type(output))

# wordcount.to_csv('output.csv')