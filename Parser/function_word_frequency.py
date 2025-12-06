# Used for importing
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.parse_json import parse_books
from utils.get_section import get_section
from utils.values import book_boundaries, book_names
from Parser import Parser

import matplotlib.pyplot as plt
import pandas as pd

def get_data_from_books() -> list[dict]:
    books = parse_books()
    data = []
    for book_name, book_value in books.items():
        for chapter in book_value.keys():
            identifier = f"{book_name}_{chapter}"
            chapter_str = get_section(books, book_name, chapter, include_heading=False)
            parser = Parser(identifier, chapter_str)
            freq = parser.function_frequency()
            data.append(freq)
    return data


def main():
    data = get_data_from_books()
    df = pd.DataFrame(data)

    ax_array = df.plot(subplots=True, layout=(4,2), xticks=[])
    
    for ax_row in ax_array:
        for ax in ax_row:
            for idx, boundary in enumerate(book_boundaries):
                ax.axvline(boundary, color="black", linestyle="--")
                ax.text(boundary, ax.get_ylim()[1], book_names[idx], 
                        verticalalignment='bottom', fontsize=12)

    plt.tight_layout()
    plt.show()  


if __name__ == '__main__':
    main()




