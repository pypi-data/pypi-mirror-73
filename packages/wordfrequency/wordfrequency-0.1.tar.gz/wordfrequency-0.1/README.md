# wordfreq
A small python script to count frequencies of words including tokenization, stemming/lemming, removal of stop words++

Accepts path to a text file as an input and will then count frequencies in text using nltk and prior to that perform cleansing on words


## Requires that 

NLTK is installed



## Running

### Run options

**inputfile** -> path to file with input text to process
**resultfile** -> path to file to write results to as a csv file
**additional_stopwords** -> path to a file containing additional stopwords (in addition to default english ones from NLTK). Each stop word should be on a new line
**logfile** -> path to logfile
**lemmetize** -> if specified runs lemmitization on words
**stem** -> if specified runs stemming of words
**numerics** -> if specified tries to remove numerics e.g. 1250
**uoms** -> if specified tries to remove uoms in the form of e.g. 1m, 1m3 
**singlechars** -> if specified tries to remove single chars
**decimals** -> if specified tries to remove decimals e.g. 10.35

### Examples

With the sample text below are an example of different outputs

*I have a dog which is 30cm high and 12.5cm long. My dog likes barking all of the day. He also likes pizza. He also likes to take 1hr walks in very rainy and cold weather.*

### Running just counting words and lowercasing text

**python3 -m categorize categorizetext --inputfile=./sample/input.txt --logfile=./log.txt --resultfile=./results.csv**

Gives the result

Word      | Frequency
--------- | ---------
dog | 2
30cm | 1
high | 1
12.5cm | 1
long | 1
. | 4
likes | 3
barking | 1
day | 1
also | 2
pizza  | 1
take | 1
1hr | 1
walks | 1
rainy| 1
cold | 1
weather | 1

### Running removing numerics, singlechars, decimals and uoms

**python3 -m categorize categorizetext --inputfile=./sample/input.txt --logfile=./log.txt --resultfile=./results.csv --uoms --numerics --singlechars --decimals** 

Gives the result

Word | Frequency
----- | --------
dog | 2
high | 1
long | 1
likes | 3
barking | 1
day | 1
also | 2
pizza | 1
take | 1
walks | 1
rainy | 1
cold | 1
weather | 1


### Running removing numerics, singlechars, decimals, uoms and lemmitization

**python3 -m categorize categorizetext --inputfile=./sample/input.txt --logfile=./log.txt --resultfile=./results.csv --uoms --numerics --singlechars --decimals --lemmetize** 

Gives the result


Word | Frequency
----- | --------
dog | 2
high | 1
long | 1
like | 3
barking | 1
day | 1
also | 2
pizza | 1
take | 1
walk | 1
rainy | 1
cold | 1
weather | 1

### Running removing numerics, singlechars, decimals, uoms and stemming

**python3 -m categorize categorizetext --inputfile=./sample/input.txt --logfile=./log.txt --resultfile=./results.csv --uoms --numerics --singlechars --decimals --stem** 

Gives the result


Word | Frequency
----- | --------
dog | 2
high | 1
long | 1
like | 3
bark | 1
day | 1
also | 2
pizza | 1
take | 1
walk | 1
raini | 1
cold | 1
weather | 1