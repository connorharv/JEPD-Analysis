import numpy as np
from FunctionWords.functionwords import functions_words

class Parser:
    def __init__(self, chapter: str, chunk: str):
        self.chapter = chapter
        self.chunk = chunk.lower()
        # While these aren't typically included, I want to sanatize inputs
        self.chunk = self.chunk.strip("\n")
        self.chunk = self.chunk.strip("\t")
        self.words = self.chunk.split(" ")
        self.chunk_size = len(self.words)

    # 1. Function Words
    def function_frequency(self) -> list[dict]:
        keys = functions_words.keys()
        counts = {k: 0 for k in keys}
        for word in self.words:
            for key in keys:
                if word in functions_words[key]:
                    counts[key] += 1
        # Reduce counts to be frequencies
        for k, v in counts.items():
            counts[k] = v / self.chunk_size
        # Add identifier
        counts['identifier'] = self.chapter
        return counts

    # 2. Overall Word Frequency
    def word_frequency(self) -> dict:
        raise NotImplementedError()

    # 3. TTR / Unique Words
    def type_token_ratio(self) -> dict:
        raise NotImplementedError()

    # 4. Average/mean word length
    def word_length(self) -> dict:
        raise NotImplementedError()

    # 5. Distribution of word lengths
    def sentence_word_length_distribution(self) -> dict:
        raise NotImplementedError()

    # 6. Sentence Length
    def sentence_length(self) -> dict:
        raise NotImplementedError()

    # 7. Punctutation
    def punctuation_frequency(self) -> dict:
        raise NotImplementedError()

    # 8. Syntatic Pattern Repetition
    def syntatic_pattern_repetition(self) -> dict:
        raise NotImplementedError()

    # 9. Character-level patterns
    def character_patterns(self) -> dict:
        raise NotImplementedError()

    # 10. Relative Entropy between WANs
    def relative_entropy(self) -> dict:
        raise NotImplementedError()