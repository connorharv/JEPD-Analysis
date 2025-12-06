# Analysis of the Documentary Source Hypothesis

The following project will use extensively the following github as JSON for the Old Testament.

[GitHub](https://github.com/bcbooks/scriptures-json)

# Stylometry

Defined to be the statistical analysis of variations in literary style between one writer or genre and another.

For this project, I will use it to determine the current status on the JEPD or Documentary Source hypothesis, which states that the 5 books of Moses were actually written by 4 different authors. Currently its validity is questioned, and I will do research using the tactics of stylometry to determine the veracity of the Documentary Source Hypothesis (appreviated JEPD).

This will be done in two ways.

1. Traditional programming with my own program using specific characteristics that will be listed below.
2. An unsupervised machine learning model will be trained on numerous articles/books/authors, then be tested to categorize the data.

## 1. Traditional Programming

The following metrics will be used to determine authorship. In style with the Old Testament, I will grade each chapter (and perhaps larger sections as well) according to the following 10 characteristics. Instead of the Ten Commandments, it will be the

### Ten Characteristics of Authorship

1. Function words (the, and, of, in, etc.)
2. Word frequency distributions
3. Type-Token Ratio (TTR) -- Unique words in a chunk
4. Average/mean word length
5. Distribution of word lengths (where in sentences)
6. Sentence length
7. Punctuation / Punctuation frequency
8. Syntatic Pattern repetition (POS tag distributions)
9. Character-level patterns (pairs/triples of characters)
10. Relative entropy between word adjaceny networks (WANs).

## 2. Unsupervised Model

This will be far more exciting. I will create a completely unsupervised model to determine where the authors (and how many) were present. The following tactics will be used.

1. Feature Extraction
2. PCA -- Principal Component Analysis (dimensional reduction)
3. Clustering (probably K-means)

### Feature Extraction

### PCA

### Clustering

I'd prefer to use `K-means` since I have the most experience with it. However, `Hierarchical Clustering`, `DBSCAN` or `Gaussian Mixture Models` could provide useful if I don't want to specify a `k` for `K-means`, although I probably will.
