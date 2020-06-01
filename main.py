from bs4 import BeautifulSoup
from os import path

from bs_processors import join, flatten_factory, local_modify_factory
from bs_processors import has_name_pf

def path_resolver(*args):
    return path.abspath(path.join(*args))


flatten_children = has_name_pf(["div", "p"])
is_internal_tag = has_name_pf(["span", "a"])
flatten = flatten_factory(flatten_children=flatten_children, is_internal=is_internal_tag)


def save_elm(doc, file_name):
    html = doc.prettify("utf-8")
    path = _to_full_name("../processed/out-" + file_name)
    with open(path, "wb") as f:
        f.write(html)

def process(file_name):
    path = _to_full_name(file_name)

    with open(path, 'r') as f:
        doc = BeautifulSoup(f, features='html.parser')

    processor = join([
        flatten
    ])

    # TODO do *NOT* pass the Soup in ... I fixed it to work but it is an ugly hack.
    # Check if the soup has a top level child called <html> and if not create one and
    # add everything else under html... then pass the html tag .
    result = processor([doc])
    assert len(result) == 1
    result = result[0]
    save_elm(result, file_name)


def _to_full_name(file_name):
    return path_resolver(__name__, '..', "samples", file_name)


if __name__ == '__main__':
    # process('1.html')
    # process('2.html')
    process('embedded-div.html')


