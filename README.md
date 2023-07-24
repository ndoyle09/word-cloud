# word-cloud
# Purpose
Domo has a [Word Cloud Chart](https://domo-support.domo.com/s/article/360042925094?language=en_US) but is difficult to use out-of-the-box for two reasons:
1. to power the chart, the data must be given to Domo directly instead of calculating individual words natively for its users.  For example, per its own documentation linked above, the chart requires the data from a typical column-based spreadsheet to be converted into a Word Cloud chart:

| Word     | Occurence |
|----------|-----------|
| america  | 11        |
| american | 19        |
| change   | 6         |
| etc.     | etc.      |

When I connect Domo to Salesforce, my data, particularly Salesforce's 'Description' field, is not formatted this way. It _would_ be possible to simply export data out of Salesforce into a CSV file and perform the same aggregation as what this code does within Excel, for example.  However, we're dealing with hundreds of thousands of Support cases, each with a widely variable number of words within the 'Description' column. There was not enough oomph behind my laptop to handle this necessary amount of processing power sift through that large of a data set.

2. Domo _does_ have a Python Scripting tile built into its Magic ETL Dataflow utility however it is not included within my company's subscription. 

The Knowledge Base article provides a script intended to be copy-pasted by end-users into the Python Scripting tile to produce a dataset usable by the Word Cloud Chart but, since it's off-limits to me, I decided to repurpose it to fit my needs.

For demonstration purposes, I have included a fake dataset based on what someone might export out of Salesforce: `mock salesforce data.csv`. This file contains extra fields that one might expect in a Salesforce report, but we only really care about one: 'Description'. For the purposes of demonstration, the fake data has been _Lorem Ipsum_-ified and reduced to 1000 rows.

# Step-by-step explanation
The code reads data from a CSV file, processes the 'description' column by splitting it into words and filtering out common words and symbols based on the boolean variables. The result is aggregated to count the occurrences of each word and displayed as the first 100 rows. Finally, the aggregated data is saved to a CSV file.  The CSV file can be uploaded into any BI/visualization tool to create a Word Cloud, for example. 

## 1. Importing pandas module
```python
import pandas as pd
```

This line imports the pandas library and aliases it as 'pd'. The pandas library is used for data manipulation and analysis, especially for working with tabular data.

## 2. Defining boolean variables

```python
removeCommonWords = True  ## (True or False)
removeCommonSymbols = True  ## (True or False)
```

These lines define two boolean variables: `removeCommonWords` and `removeCommonSymbols`. These variables can be adjusted to fit the needs of the user. Setting one or both of these variables to 'True' will remove the words (`commonWords` variable)/symbols (`commonSymbols` variable) contained therein later in the code. 'False', on the other hand, will not remove the words/symbols.

## 3. Defining sets of common words and symbols
```python
commonWords = { ... }
commonSymbols = { ... }
```

These lines define two lists: `commonWords` and `commonSymbols`. The lists contain strings that represent common words and symbols that will be used for filtering later in the code.

Additional lists can be defined here for company-, product-, or industry-specific buzzwords.

## 4. Reading data from a CSV file into a DataFrame
```python
cases = pd.read_csv('mock salesforce data.csv')
```

This line reads data from a CSV file named 'mock salesforce data.csv' into a DataFrame named `cases`. The file should be located in the same directory as the Python script, or you can specify the full path to the file.

## 5. Initializing variables and looping through descriptions
```python
tempOutput = []
descriptions = cases["description"].dropna() ## SET TO YOUR COLUMN TO SPLIT

for i, row in enumerate(descriptions):
    ...
```

These lines initialize an empty list `tempOutput` and extract the 'description' column from the DataFrame `cases` into the `descriptions` variable.

'Description' is a standard field within the Case object of Salesforce. It is intended to be a customer question or feedback, however, depending on the use-case, it can be blank.  As such, the `.dropna()` method removes any rows with missing values from the 'description' DataFrame because there's nothing to count.

## 6. Splitting words and filtering

```python
for i, row in enumerate(descriptions):
    words = row.split(" ")
    for word in words:
        if removeCommonSymbols:
            for symbol in commonSymbols:
                word = word.replace(symbol, "")
        if removeCommonWords and word.upper() not in commonWords:
            newData = {"id": cases['case number'][i],
                       "word": word.lower()}
            tempOutput.append(newData)
        elif not removeCommonWords:
            newData = {"id": cases['case number'][i],
                       "word": word.lower()}
            tempOutput.append(newData)
```

These lines iterate through each row in the `descriptions` variable. For each row, it splits the text into `words` using the space character as the delimiter. It then processes each `word` based on the boolean flags set for the `removeCommonSymbols` and `removeCommonWords` variables. If `removeCommonSymbols` is `True`, it replaces common symbols from the commonSymbols set with an empty string for each word. 

If `removeCommonWords` is `True` and the row's word in uppercase form is not already present in the `commonWords` list (which is also capitalized words), it creates a new dictionary `newData` with the 'id' from the 'case number' column of the `cases` DataFrame and the lowercase version of the word. This `newData` dictionary is appended to the `tempOutput` list.

## 7. Creating a DataFrame and performing aggregation

```python
output = pd.DataFrame(tempOutput)

wordcount = output.groupby('word').nunique().sort_values(by='id', ascending=False).rename(columns={'word': 'word', 'id': 'occurrence'})
```

These lines create a DataFrame `output` from the `tempOutput` list. The `.groupby()` method groups the data by `'word'`, and the `.nunique()` method counts the unique occurrences of each word. The result is then sorted in descending order based on the count of 'id' (case number). The columns 'word' and 'id' are renamed to 'word' and 'occurrence', respectively.

## 8. Displaying the result and saving to a CSV file

```python
print(wordcount.head(100))
wordcount.to_csv('output.csv')
```

This code prints the first 100 rows of the `wordcount` DataFrame using `.head(100)`. I like to do this just to get a quick glimpse at the data to ensure it performed as expected.  This print statement can be removed entirely to no effect.

It then saves the `wordcount` DataFrame to a CSV file named 'output.csv' to the directory.
