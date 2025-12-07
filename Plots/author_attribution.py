from matplotlib import pyplot as plt
from utils.values import book_boundaries, book_names
import numpy as np


author_colors = {
    0: "#999999", 
    1: "#009E73", 
    2: "#56B4E9", 
    3: "#E69F00",
}

author_to_name = {
    0: "Yahwist? (J)",
    1: "Elohist? (E)",
    2: "Deuteronimist? (D)",
    3: "Priestly? (P)",
}

def plot_discrete_authors(labels):
    n_chunks = len(labels)
    x = np.arange(n_chunks)
    colors = [author_colors[l] for l in labels] 

    plt.bar(
        x,
        np.ones(n_chunks),
        color=colors,
        width=1.0,
        align="edge",
        linewidth=0
    )
    plt.ylabel("Author Label")

    plt.xticks([], [])

    for i, b in enumerate(book_boundaries):
        plt.axvline(b, color="black", linestyle="--")
        plt.text(
            b,
            1.05,
            book_names[i],
            ha="left",
            va="bottom",
            fontsize=18,
        )
        
    handles = [plt.Rectangle((0,0),1,1, color=author_colors[a]) for a in author_colors]
    labels_leg = [f"{author_to_name[a]}" for a in author_colors]
    plt.legend(handles, labels_leg, loc="upper right")

    plt.suptitle("Predicted Author per Chapter", y=0.04, fontsize=20)

    plt.tight_layout()
    plt.show()

def plot_probability_bars(probas):
    n_chunks, n_authors = probas.shape
    x = np.arange(n_chunks)

    bottom = np.zeros(n_chunks)

    plt.xticks([], [])

    for author_id in range(n_authors):
        plt.bar(
            x,
            probas[:, author_id],
            bottom=bottom,
            color=author_colors[author_id],  
            edgecolor="none",
            label=f"{author_to_name[author_id]}",
            width=1.0,
            align="edge",
            linewidth=0
        )
        bottom += probas[:, author_id]

    plt.ylabel("Probability")
    plt.ylim(0, 1)

    for i, b in enumerate(book_boundaries):
        plt.axvline(b, color="black", linestyle="--")
        plt.text(b, 1.02, book_names[i], fontsize=18)

    plt.suptitle("Predicted Author per Chapter", y=0.04, fontsize=20)
    
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

def plot_author_probabilities_vertical_width(probas):
    n_chunks, n_authors = probas.shape


    for i in range(n_chunks):
        bottom = 0 
        left = i 

        for author_idx in range(n_authors):
            width = probas[i, author_idx]
            if width > 0:
                plt.bar(
                    left,
                    1,
                    width=width,
                    bottom=bottom,
                    align='edge',
                    color=author_colors[author_idx],
                    edgecolor='none'
                )
            left += width
    
    for i, b in enumerate(book_boundaries):
        plt.axvline(b, color="black", linestyle="--")
        plt.text(
            b,
            1.05,
            book_names[i],
            ha="left",
            va="bottom",
            fontsize=18,
        )

    plt.ylabel("Author Label")
    plt.xticks([], [])

    # Legend
    handles = [plt.Rectangle((0,0),1,1,color=author_colors[a]) for a in author_colors]
    labels_leg = [f"{author_to_name[a]}" for a in author_colors]
    plt.legend(handles, labels_leg, loc="upper right")

    plt.suptitle("Predicted Author per Chapter", y=0.04, fontsize=20)
    plt.tight_layout()
    plt.show()