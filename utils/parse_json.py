import os
import json
from collections import OrderedDict

def parse_books(filename: str='old-testament.json') -> OrderedDict:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)

    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
    data = json.loads(data)

    output = OrderedDict()


    if 'books' in data:
        for b in data['books']:
            book = b['book']
            if(book == 'Joshua'):
                break
            output[book] = OrderedDict()
            if 'heading' in b:
                output[book]['heading'] = b['heading']

            for c in b['chapters']:
                chapter = str(c['chapter'])

                if chapter not in output[book]:
                    output[book][chapter] = OrderedDict()

                if 'heading' in c:
                    output[book][chapter]['heading'] = c['heading']

                for v in c['verses']:
                    output[book][chapter][str(v['verse'])] = v['text']
    return output