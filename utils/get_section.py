from collections import OrderedDict


def get_section(output: OrderedDict, book: str, chapter: str, verse: str = '', include_heading=False) -> str:
    if not book in output:
        raise KeyError("Invalid Book")
    if not chapter in output[book]:
        raise KeyError("Invalid Chapter")
    if verse and not verse in output[book][chapter]:
        raise KeyError("Invalid Verse")
    
    section = ""
    
    if include_heading:
        section += f"{book} {chapter}{f':{verse}' if verse else ''}\n"
    
    if verse:
        section += output[book][chapter][verse] + "\n"
    else:
        for text in output[book][chapter].values():
            section += text + " "
        section += "\n"
    return section