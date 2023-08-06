from kindlelamp.kindle import Kindle
from kindlelamp.kindle_collection import KindleCollection
from lxml.etree import parse
import os


RESPONSE = 'response'


def read(filepath=None) -> KindleCollection:
    if filepath is None:
        filepath = os.environ['HOME'] + \
            '/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml'
    tree = parse(filepath)
    root = tree.getroot()
    books = {}
    for meta_data in root.iter('meta_data'):
        asin = ''
        res = {}
        for child in meta_data:
            if child.tag == 'ASIN':
                asin = child.text
            elif child.tag == 'title':
                res[child.tag] = child.text
                title_pronunciation = child.attrib['pronunciation']
                res['title_pronunciation'] = title_pronunciation
            elif child.tag == 'authors':
                res[child.tag] = _generate_authors(child.iter('author'))
            elif child.tag == 'publishers':
                res[child.tag] = _generate_publishers(child.iter('publisher'))
            else:
                res[child.tag] = child.text
        kindle = Kindle(res)
        books[asin] = kindle
    return KindleCollection(books)


def _generate_publishers(element):
    array = []
    for child in element:
        array.append(child.text)
    return array


def _generate_authors(element):
    array = []
    for child in element:
        el = {}
        el['author'] = child.text
        pronunciation = child.attrib['pronunciation']
        el['pronunciation'] = pronunciation
        array.append(el)
    return array
