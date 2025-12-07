# Used for importing
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Parser.Parser import Parser
from utils.get_section import get_section
from utils.parse_json import parse_books
from utils.values import book_boundaries, book_names

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from WordUtils.n_grams import n_grams_3_raw, n_grams_4_raw

def char_ngrams(input, n):
    output = {}
    for i in range(len(input)-n+1):
        if not input[i:i+n] in output:
            output[input[i:i+n]] = 1
        else:
            output[input[i:i+n]] += 1
    return output

def get_trigrams() -> list:
    books = parse_books()
    total_str = ""
    for book_name, book_value in books.items():
        for chapter in book_value.keys():
            total_str += get_section(books, book_name, chapter, include_heading=False)
    n_grams = char_ngrams(total_str, 4)
    
    N = 100
    most_common = sorted(n_grams.items(), key=lambda item: item[1], reverse=True)[:N]
    print([common[0] for common in most_common])

    

def get_data_from_books() -> list[list]:
    books = parse_books()
    data = []
    for book_name, book_value in books.items():
        for chapter in book_value.keys():
            identifier = f"{book_name}_{chapter}"
            chapter_str = get_section(books, book_name, chapter, include_heading=False)
            parser = Parser(identifier, chapter_str)
            chunk_data = {}
            chunk_data |= parser.add_identifier()
            chunk_data |= parser.function_frequency()
            chunk_data |= parser.word_length()
            chunk_data |= parser.type_token_ratio()
            chunk_data |= parser.sentence_length()
            chunk_data |= parser.lexical_richness()
            chunk_data |= parser.pos_tag_ratios()
            chunk_data |= parser.word_length_distribtuion()
            chunk_data |= parser.punctuation_frequency()
            chunk_data |= parser.n_grams()
            data.append(chunk_data)
    return data

def smooth_savgol(x, window=15, poly=3, dtype=float):
    x = np.array(x, dtype=dtype)
    return savgol_filter(x, window_length=window, polyorder=poly)


def create_plots(attributes: list, csv: str = "datasets/strict_data.csv"):
    columns = ['index'] + attributes
    if os.path.isfile(csv):
        try:
            df = pd.read_csv(csv, usecols=columns)
        except ValueError:
            print("One or more of the columns does not exist")
            return
    else:
        all_data = get_data_from_books()
        df = pd.DataFrame(all_data)
        df.to_csv(csv)

    total_plots = len(columns)-1
    x_column = df.columns[0]

    df = df.fillna(0)

    # Dynamically allocate
    if total_plots % 2 == 0:
        ncols = nrows = total_plots // 2
    else:
        ncols = (total_plots // 2) + 1
        nrows = (total_plots // 2) + 1

    ax_array = df.plot(x=x_column, subplots=True, layout=(nrows,ncols), xticks=[], alpha=0.3)
    all_axes = [ax for ax_row in ax_array for ax in ax_row]

    for ax, col in zip(all_axes, columns[1:]):
        # Raw data
        y_raw = df[col].values
        x_vals = df[x_column].values

        # Smooth data
        y_savgol = smooth_savgol(y_raw, window=15, poly=3, dtype=type(y_raw[0]))

        ax.plot(x_vals, y_savgol, label=f"{col} (SavGol)", alpha=1, color="black")

        # Add book boundaries
        for idx, boundary in enumerate(book_boundaries):
            ax.axvline(boundary, color="black", linestyle="--")
            ax.text(boundary, ax.get_ylim()[1], book_names[idx], 
                    verticalalignment='bottom', fontsize=9)

    plt.show()
        

if __name__ == '__main__':
    create_plots(['1-4%', '5-8%', '9+%'])