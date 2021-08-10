# error-spell-checker-system

It is an assignment project from Natural Language Processing (NLP) module subject

The project is to build a probabilistic model for detecting of spelling errors. 
It should correct spelling errors which result in non-words and real-words, for example correcting graffe to giraffe. 
Search and find a corpus in any sciences field, such as medical science, business, etc., consisting of at least 100,000 words, and build the system based on this corpus

a)	Your system must have an appropriate graphical user interface (GUI). There must be small editor, with a size of 500 words in the GUI to allow user to write a short piece of text. The Figure below depicts a sample of GUI needed for your application:

![image](https://user-images.githubusercontent.com/43923087/128842506-76cc849d-a464-40a5-8ee7-cc97bed09019.png)


b)	Your application must be able to find the spelling errors and suggest a few words to the user to modify the text. 

c)	The spelling errors that need to be addressed by your system are:
i.	Non-words (wrong spelling, where the word does not exist)
ii.	Real-words (wrong spelling due to wrong context, but the misspelt word does exist)

d)	The techniques used for the detection of the spelling errors must include bigram, minimum edit distance, and any other suitable popular techniques used in NLP. 

e)	Provide the following functionality in your application: 
Ability to show a sorted list of all words in the corpus with the facility of exploring the list and search for a specific word Ability to highlight the misspelled words, and right click to suggest the correct words (with their minimum edit distance from the wrong word)


Corpus was made from covid-19 research paper abstracts based on kaggle dataset link: https://www.kaggle.com/sshikamaru/cord19-covid19-open-research-dataset?select=Research_text_files.csv
