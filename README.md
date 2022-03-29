# Amerikan and British swear word counting on Twitter corpus
In this GitHub you can find the code to find the frequency of curse words in a corpora. The following steps will help you to get the data. 

# Install required libraries
Run the following commands to install the required libraries for the python files:

```
pip install -U spacy
```
```
python -m spacy download en
```
```
pip install pandas
```

# Clone repository to you computer
Command to clone the files to you repository:

```
git clone https://github.com/Marijn03/Final-report.git
```

# Get the paths to the gz files in a text file from the Karora Twitter corpus to local server:
Note: access to the corpus is required. If you do not have access, then you the file gz_files.txt. 

## Put the paths of the gz files in a text file
Use the following command to geth the paths to the gz files in the english twitter corpus:

```
find /net/corpora/twitter2_en/Tweets -name \*.out.gz > gz_files.txt
```

## Get the gz_text file from the Karora server to the local server
First go to the place on the local server where you want to put the file. You can do this with the command:

```
cd PATH
```

PATH is the path you take to get to the place on the local server, where you want to put the text file. 

Run the following command to get the text file from the server to your local server and replace 123456 with your own student number: 

```  
scp -r s123456@karora.let.rug.nl:/home/s4850998/gz_files.txt .
```

Now you have to put your password.

# Get 10 randomly selected files to your local server
## Get 10 random files
To get random files from the gz_files.txt you have to run the python file random_files_selector.py with the following command:

```
python3 random_files_selector.py gz_files.txt
```

The result will show you ten random selected files. The files used in the research are stored in the folder "en". 

## Get the randomly selected files to you local server
Put each path of the random selected file from the Karora server to your local server with the following command, place each path at PATH and replace 123456 with your own student number: 

```
scp -r s123456@karora.let.rug.nl:PATH .
```

You have to put your password for each path. 

# Get the all the csv files of the curse words 
The python file swear_word_freq.py should be stored at the same place as the folder "en". 

Run the following command to get all the csv files: 

```
python3 abbreviation_frequency_detector.py
```

# Specifications
- Python version: 3.9.10
- Laptop: macbook pro 2021 M1