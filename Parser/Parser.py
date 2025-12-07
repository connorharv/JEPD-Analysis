import numpy as np
from WordUtils.functionwords import functions_words
from WordUtils.punctuation import punctuation
from WordUtils.n_grams import n_grams_3_raw, n_grams_4_raw
import string



from nltk import word_tokenize, pos_tag

class Parser:
    def __init__(self, chapter: str, chunk: str):
        self.chapter = chapter
        self.chunk = chunk.lower()
        self.unmodified = str(chunk.lower())
        # While these aren't typically included, I want to sanatize inputs
        self.chunk = self.chunk.strip("\n")
        self.chunk = self.chunk.strip("\t")
        # Remove punctuation
        self.chunk = self.chunk.translate(str.maketrans('', '', string.punctuation))
        self.words = self.chunk.split(" ")
        self.chunk_size = len(self.words)

    def add_identifier(self) -> list[dict]:
        return {'identifier' : self.chapter}

    # 1. Function Words
    def function_frequency(self) -> list[dict]:
        # Add identifier
        keys = functions_words.keys()
        counts = {k: 0 for k in keys}
        for word in self.words:
            for key in keys:
                if word in functions_words[key]:
                    counts[key] += 1
        # Reduce counts to be frequencies
        for k, v in counts.items():
            counts[k] = v / self.chunk_size
        return counts

    # 2. Overall Word Frequency
    def word_frequency(self) -> dict:
        counts = {}
        for word in self.words:
            if not word in counts:
                counts[word] = 1
            else:
                counts[word] += 1
        # Reduce to get frequency
        for k, v in counts.items():
            counts[k] = v / self.chunk_size
        return counts

    # 3. TTR / Unique Words
    def type_token_ratio(self) -> dict:
        unique_words = []
        for word in self.words:
            if not word in unique_words:
                unique_words.append(word)
        ratio_dict = {'TTR' : len(unique_words) / self.chunk_size}
        return ratio_dict

    # 4. Average Word Length
    def word_length(self) -> dict:
        total_words_length = 0
        total_words_length = sum([len(word) for word in self.words])
        word_length_dict = {'word_length': total_words_length / self.chunk_size}
        return word_length_dict
    
    # 5. Word Length Distribution
    def word_length_distribtuion(self) -> dict:
        percentage_dict = {
            '1-4%': 0,
            '5-8%': 0,
            '9+%' : 0
        }
        for word in self.words:
            if len(word) < 5:
                percentage_dict["1-4%"] += 1
            elif len(word) < 9:
                percentage_dict["5-8%"] += 1
            else:
                percentage_dict["9+%"] += 1
        for k, v in percentage_dict.items():
            percentage_dict[k] = v / len(self.words)
        return percentage_dict

    # 6. Sentence Length
    def sentence_length(self) -> dict:
        sentence_len = 0
        sentences = []
        for i in range(len(self.unmodified)):
            if self.unmodified[i] == '.':
                sentences.append(i-sentence_len)
                sentence_len = i
        sentence_len_dict = {'sentence_len' : sum(sentences) / len(sentences)}
        return sentence_len_dict

    # 7. Punctutation
    def punctuation_frequency(self) -> dict:
        counts = {k: 0 for k in punctuation}
        for char in self.unmodified:
            if char in counts:
                counts[char] += 1
        return counts

    # 8. Character level patterns -- N gram
    def n_grams(self, n: int = 3) -> dict:
        n_grams = n_grams_3_raw if n == 3 else n_grams_4_raw
        output = {}
        for i in range(len(self.unmodified)-n+1):
            word = self.unmodified[i:i+n]
            if word in n_grams:
                output[word] = output.get(word, 0) + 1
        return output
    
    # 9. POS-Tag ratios
    def pos_tag_ratios(self) -> dict:
        tokens = word_tokenize(self.unmodified)
        tagged = pos_tag(tokens)

        total = len(tagged)
        if total == 0:
            return {
                "noun_ratio": 0,
                "verb_ratio": 0,
                "adj_ratio": 0,
                "adv_ratio": 0,
                "pron_ratio": 0
            }
        
        # Tag groups
        noun_tags = {"NN", "NNS", "NNP", "NNPS"}
        verb_tags = {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"}
        adj_tags  = {"JJ", "JJR", "JJS"}
        adv_tags  = {"RB", "RBR", "RBS"}
        pron_tags = {"PRP", "PRP$", "WP", "WP$"}
        counts = {
            "noun_ratio": 0,
            "verb_ratio": 0,
            "adj_ratio": 0,
            "adv_ratio": 0,
            "pron_ratio": 0
        }
        for _, tag in tagged:
            if tag in noun_tags: counts["noun_ratio"] += 1
            if tag in verb_tags: counts["verb_ratio"] += 1
            if tag in adj_tags:  counts["adj_ratio"] += 1
            if tag in adv_tags:  counts["adv_ratio"] += 1
            if tag in pron_tags: counts["pron_ratio"] += 1
        for k in counts:
            counts[k] /= total
        return counts
    
    # 10. MTLD Lexical Richness
    def lexical_richness(self) -> dict:
        def mtld(tokens, threshold=0.72):
            def mtld_calc(direction_tokens):
                factor_count = 0
                token_count = 0
                types = set()
                current_ttr = 1.0

                for token in direction_tokens:
                    token_count += 1
                    types.add(token)
                    current_ttr = len(types) / token_count

                    if current_ttr <= threshold:
                        factor_count += 1
                        token_count = 0
                        types = set()

                if token_count > 0:
                    factor_count += (1 - (current_ttr / threshold))

                return len(direction_tokens) / factor_count if factor_count > 0 else 0

            if len(tokens) == 0:
                return 0.0

            return (mtld_calc(tokens) + mtld_calc(tokens[::-1])) / 2.0
        tokens = word_tokenize(self.unmodified.lower())
        mtld_score = mtld(tokens)
        return {'mtld': mtld_score} 



