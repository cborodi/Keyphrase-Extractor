# Keyphrase-Extractor

*Application for Keyphrase Extraction in Romanian Language*

The main objective of the application is to evaluate two keyphrase extraction methods (TextRank and RAKE) on a target dataset. Apart from that, the application provides a graphical user interface for quick testing.

The dataset used is created specifically for this application. It was collected from both online news articles and academic papers.

There are a total of 200 texts, split in two halves, one for text extracted from various research papers (named from 1.txt to 100.txt), and online articles (from 1a.txt to 100a.txt). All the texts are in the Romanian Language, which is less studied in this domain, and it makes it harder to achieve good results, due to the fact that it is a romance language. The length of texts is between 200 to 1000 words.

The extraction of keywords for the annotation part is done manually by students from the Applied Computational Intelligence Masters, each text being studied and annotated by at least two and at most four students, in order to demonstrate that even human extraction yields different results from one person to another as this task has a certain degree of subjectivity. The number of extracted keyphrases is between 4 and 10.

All the texts go through a preprocessing step, which firstly implies tokenization, normalization by switching to lowercase letters and standardization through removal of punctuation marks. Next preprocessing step is removing stop words, using a list of about 500 predefined Romanian stop words. After that, a particularly important lemmatization step follows, that is used to reduce a word to its base or root form, known as the lemma. For example, lemmatization would convert "running" to "run" and "better" to "good". This last step is done with the use of SpaCy.

The best results are obtained by TextRank, by not using lemmas, and mixing adjacent keywords to form the final keyphrase > **Performance: 68.01%**, which is different from the results obtained in English. The performance was chosen as the number of correctly identified keyphrases / the number of total keyphrases extracted by the agorithm.
