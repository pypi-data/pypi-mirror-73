import collections
import logging
import os
import re

import requests
from bs4 import BeautifulSoup

from xbrlassembler.enums import XBRLType, FinancialStatement, DateParser
from xbrlassembler.error import XBRLError

logger = logging.getLogger('xbrlassembler')


class XBRLElement:
    """
    An element to represent a single point on a tree.
    Specific data values are geared towards xbrl relevent information
    While relational data is close to that of an XML tree element

    Args:
        :param uri: A unique identifier for this specific point
        :type uri: str, int, float, etc.

    Kwargs:
        :param label: Printable and readable identifier
        :param value: Data that sits on a specific point, mostly used for elements at the bottem of the tree
        :param ref: Reference data that gives context to the value
    """
    def __init__(self, uri, label=None, value=None, ref=None):
        """Constructor Method"""
        self.uri = uri
        self.label = label
        self.ref = ref

        # Convert to float to remove any issues with comparing string representations of numbers
        try:
            self.value = float(value)
        except (TypeError, ValueError):
            logger.info(f"XBRLElement value convert to float failure for {value}")
            self.value = value

        self._children = {}
        self._parent = None

    def __repr__(self):
        """
        :return: Returns a string representation of various aspects of the non relational data
        """
        return f"{self.uri} (label={self.label}, ref={self.ref}, value={self.value})"

    def add_child(self, child, order=-1):
        """
        Essential function for establishing relationships between elements.
        This function ensures that the relationship is set on both parent and child
            elements without duplication or Nones

        Args:
            :param child: An XBRLElement that is going to be under this element in the tree
            :param order: An optional argument to add order to child elements
        """
        if not isinstance(child, XBRLElement):
            return

        if child in self._children:
            return

        for already_child in self._children:
            if already_child.uri == child.uri and already_child.ref == child.ref:
                self.merge(child)
                return

        try:
            order = int(float(order))
        except Exception as e:
            logger.info(f"order to float to int failed {order}, {e}")
            return

        self._children[child] = order
        child._parent = self

    def merge(self, other):
        """
        Attempts to merge one XBRLElement with another resulting in one element with more complete information
        :param other: An `XBRLElement` to be absorbed
        :return:
        """
        if not isinstance(other, XBRLElement):
            return

        if self.label is None and other.label is not None:
            self.label = other.label

        if self.value is None and other.value is not None:
            self.value = other.value

        if self._parent is None and other._parent is not None:
            self._parent = other._parent

        for new_child, order in other._children.items():
            self.add_child(new_child, order)

    def visualize(self) -> str:
        """
        A function to create a printable representation of the tree from this point
        :return: A multiline string
        """
        vis = f"\n{self.__repr__()}"
        if self._children:
            for child in self._children:
                cvis = child.visualize().replace('\n', '\n\t')
                vis += cvis
        return vis

    def references(self) -> dict:
        """
        A quick utility function to pull and parse all bottom level references in the tree
        :return: A dict mapping old references to parsed ones
        """
        refs = {}
        for atr, cells in self.to_dict().items():
            for cell in cells:
                if cell.ref not in refs.keys() and cell.ref is not None:
                    refs[cell.ref] = DateParser.parse(cell.ref)
        return refs

    def ids(self):
        """
        Recursive function to access all uri label pairs
        :return: A dictionary where keys are uri strings and values are label strings or None is there is no label
        """
        ids = {self.uri: self.label}
        for child in self._children:
            ids.update(child.ids())
        return ids

    def to_list(self) -> list:
        """
        Recursive function to return a list of all elements in the tree
        :return: A list of each XBRLElement in the tree
        """
        lst = [self]
        for child in self._children:
            lst.extend(child.to_list())
        return lst

    def to_dict(self) -> dict:
        """
        A recursive function to return a dictionary representation of the tree from this point downward
        :return: A dictionary where keys are labels and cells are bottem level xbrl elements
        """
        dic = {self.uri: []}
        if all(not child._children for child in self._children.keys()):
            dic[self.uri] = [ele for ele in self._children.keys()]
        else:
            for ele, o in sorted(self._children.items(), key=lambda item: item[1] or -1):
                dic.update(ele.to_dict())
        return dic


class XBRLAssembler:
    """
    The main object to compile XBRL documents into complete sets of data by establishing a tree of information

    Args:
        :param schema: A class:`bs4.BeautifulSoup` for the xbrl schema file
        :param data: A class:`bs4.BeautifulSoup` for the xbrl data file
        :param label: A class:`bs4.BeautifulSoup` for the xbrl label file
        :param ref: A class:`bs4.BeautifulSoup` for the desired xbrl reference file (Defintion, Presetataion, Calculation)
    """
    uri_re = re.compile(r'(?:lab_)?((us-gaap|source|dei|[a-z]{3,4})[_:][A-Za-z]{5,})', re.IGNORECASE)

    def __init__(self, schema, data, label, ref):
        """Constructor Method"""
        for t, name in [(schema, "schema"),
                        (data, "data"),
                        (label, "label"),
                        (ref, "ref")]:
            if not isinstance(t, BeautifulSoup) or t is None:
                raise ValueError(f"{type(t)} is not a BeautifulSoup")

        self.schema = schema
        self.data = data
        self.label = label
        self.ref = ref

        self._docs = self.get_docs()
        self._labels = self.get_labels()
        self._cells = self.get_cells()

    @classmethod
    def from_sec_index(cls, index_url, ref_doc=XBRLType.PRE):
        """
        Alternative constructor that takes a url as a string and attempts to pull and parse all relevent documents

        :param index_url: A string for a url to an sec index
        :param ref_doc: An class:`xbrlassembler.XBRLType` to specify the type of reference document

        :return: A class:`xbrlassembler.XBRLAssembler`
        """
        if not index_url.startswith("https://www.sec.gov/Archives/edgar/data/"):
            raise XBRLError(f"{index_url} is not a url for an SEC index")

        index_soup = BeautifulSoup(requests.get(index_url).text, 'lxml')

        data_files_table = index_soup.find('table', {'summary': 'Data Files'})

        if not data_files_table:
            raise XBRLError(f"{index_url} does not appear to have any data files")

        file_map = {}
        for row in data_files_table('tr')[1:]:
            row = row.find_all('td')
            soup = BeautifulSoup(requests.get("https://www.sec.gov" + row[2].find('a')['href']).text, 'lxml')
            file_map[XBRLType.get(row[3].text)] = soup

        try:
            ref = next((ref for ref in [ref_doc, XBRLType.PRE, XBRLType.DEF, XBRLType.CALC] if ref in file_map), None)
            return cls(schema=file_map[XBRLType.SCHEMA],
                       data=file_map[XBRLType.DATA],
                       label=file_map[XBRLType.LAB],
                       ref=file_map[ref])
        except KeyError:
            raise XBRLError(f"Could not find all document from {index_url}")

    @classmethod
    def from_dir(cls, directory, ref_doc=XBRLType.PRE):
        """
        Alternative constructor that will attempt to search the specific directory for a set of xbrl documents

        :param directory: A string to a directory that will be scanned for xbrl documents
        :param ref_doc: Optional class`xbrlassembler.XBRLType` used to specify the requested reference document

        :return: A class:`xbrlassembler.XBRLAssembler`
        """
        if not os.path.isdir(directory):
            raise XBRLError(f"{directory} is not a valid directory")

        file_map = {}
        for item in os.listdir(directory):
            if re.search(r'.*\.(xml|xsd)', item):
                file_map[XBRLType.get(item)] = BeautifulSoup(open(os.path.join(directory, item), 'r'), 'lxml')

        try:
            ref = next((ref for ref in [ref_doc, XBRLType.PRE, XBRLType.DEF, XBRLType.CALC] if ref in file_map), None)
            return cls(schema=file_map[XBRLType.SCHEMA],
                       data=file_map[XBRLType.DATA],
                       label=file_map[XBRLType.LAB],
                       ref=file_map[ref])
        except KeyError:
            raise XBRLError(f"Could not find all documents from {directory}")

    def uri(self, raw):
        """
        Used to standardize uri's across mutliple documents
        :param raw: A non standard URI string

        :return:
        """
        uri_re = re.search(self.uri_re, raw)
        if uri_re:
            return uri_re.group(1)
        return raw

    def get_docs(self):
        """
        Parsing function for xbrl schema
        This establishes the access point for other documents as URI's from this
            find relevent data in the reference document
        :return: Dictionary where keys are URI's and values are top level class:`xbrlassembler.XBRLElement`
        """
        docs = {}
        for roletype in self.schema.find_all("link:roletype"):
            uri = roletype['roleuri']
            label = roletype.find("link:definition").text
            if "Parenthetical" not in label:  # "Statement" in label and
                text = label.split(" - ")
                ele = XBRLElement(uri=uri, label=text[-1], ref=text[0])
                docs[uri] = ele

        if not docs:
            raise XBRLError(f"No documents found while parsing XBRL schema")

        return docs


    def get_labels(self):
        """
        Parsing function for xbrl label file to provide readable labels to all elements
        :return: Dictionary where keys are URI's and values are strings
        """
        labels = {}
        label_link = self.label.find(re.compile('.*labellink', re.IGNORECASE))
        if not label_link:
            raise XBRLError(f"No Data found in XBRL label document")

        for lab in label_link.find_all(re.compile('label$')):
            uri = self.uri(lab['xlink:label']).lower()
            if uri == lab['xlink:label']:
                uri = self.uri(lab['id'])
            labels[uri] = lab.text

        for lab in label_link.find_all(re.compile('loc$')):
            label_uri = lab['xlink:label'].lower()
            if label_uri not in labels:
                continue

            uri = lab['xlink:href'].split('#')[1].lower()
            if uri in labels:
                continue

            labels[uri] = labels[label_uri]

        if not labels:
            raise XBRLError(f"No labels found while parsing XBRL lab")

        return labels


    def get_cells(self):
        """
        Parsing function for the base xml file that has all bottem level tree elements
        :return: A dict of low level xbrl data that is accessable through uri key
        """
        cells = collections.defaultdict(list)

        for node in self.data.find_all(attrs={"contextref": True}):
            uri = node.name.replace(':', '_')
            ele = XBRLElement(uri=uri,
                              value=node.text,
                              ref=node['contextref'])
            cells[uri].append(ele)

        if not cells:
            raise XBRLError(f"No cells found while parsing XBRL xml")

        return cells

    def find_doc(self, search_func):
        """
        A sorted search function for specific top level class:`xbrlassembler.XBRLElement` base on uri or label
        :param search_func: Function returning a bool to determine search method
        :return: Top level XBRLElement to create a tree under
        """
        for uri, ele in sorted(self._docs.items(), key=lambda item: item[1].ref):
            if search_func(uri) or search_func(ele.label):
                return ele

    def get(self, search) -> XBRLElement:
        """
        Main access function that will take a variety of search criteria and attempt to create and
            return the document tree relevent to the search

        :param search: Regex, string, or FinancialStatement enum to search with

        :return: class:`xbrlassembler.XBRLElement` for the top of a tree representing the requested document
        """
        if isinstance(search, re.Pattern):
            doc_ele = self.find_doc(lambda name: re.search(search, name))
        elif isinstance(search, str):
            doc_ele = self.find_doc(lambda name: search in name)
        elif isinstance(search, FinancialStatement):
            doc_ele = self.find_doc(lambda name: re.search(search.value, name))
        else:
            raise ValueError(f"XBRLAssembler.get() search term should be "
                             f"re.Pattern, string, or FinancialStatement not {search}")

        if doc_ele is None:
            raise XBRLError(f"No match found for {search} in names.\n\t"
                            f"Names available {[name for name in self._docs.keys()]}]")

        if not doc_ele._children:
            self.__assemble(doc_ele)

        return doc_ele

    def __assemble(self, doc_ele):
        # Find desired section in reference document
        def_link = self.ref.find(re.compile(r'link', re.IGNORECASE), attrs={'xlink:role': doc_ele.uri})
        if not def_link:
            raise XBRLError(f"Can't find document in reference doc")


        # Pull all elements and create XBRLElements out of them
        eles = {}
        cols = collections.defaultdict(int)
        for loc in def_link.find_all(re.compile(r'loc', re.IGNORECASE)):
            uri = loc['xlink:href'].split('#')[1]
            label = self._labels[uri.lower()] if uri.lower() in self._labels else None
            ele = XBRLElement(uri=uri, label=label)
            eles[loc['xlink:label']] = ele

            if ele.uri.lower() in self._cells:
                for cell in self._cells[ele.uri.lower()]:
                    cols[cell.ref] += 1

        if not cols:
            raise XBRLError(f'{doc_ele.label} could not find any columns for cells')

        # Find and create parent/child relationships between new elements
        for arc in def_link.find_all(re.compile(r'\w*arc', re.IGNORECASE)):
            parent, child, order = eles[arc['xlink:from']], eles[arc['xlink:to']], arc['order']
            parent.add_child(child=child, order=order)

        most_used = max(cols.values())
        cols = {DateParser.parse(ref): ref for ref, count in cols.items() if count == most_used}
        cols = set(cols.values())

        # Determine top and bottom level elements in the document and either fill in cells or
        #   link them to the overall document element
        for order, ele in enumerate(eles.values()):
            if ele._parent is None:
                doc_ele.add_child(child=ele, order=order)

            if ele.uri.lower() in self._cells:
                for cell in self._cells[ele.uri.lower()]:
                    if cell.ref in cols:
                        ele.add_child(cell)
