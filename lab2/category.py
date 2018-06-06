import urllib.request
from lxml import etree


class Category:
    # returns list of (Pages) OR (Subcategories) pageids of the given category
    # second param, mode, defaults to "page"
    # mode="page" - returns Pages
    # mode="subcat" - returns Subcategories
    @staticmethod
    def __get_pages_or_subcategories(pageid, mode="page"):
        wiki_xml = Category.__get("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers"
                                  "&cmlimit=600&format=xml&cmtype=" + mode + "&cmpageid=" + str(pageid))
        root = etree.fromstring(wiki_xml)
        categorymembers = root.findall(".//categorymembers/cm")
        return list(cm.get('pageid') for cm in categorymembers)

    @staticmethod
    def __get(url):
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Lab2/1.0'
            }
        )

        f = urllib.request.urlopen(req)
        return f.read().decode('utf-8')

    # analyzes the given category and the subcategories,
    # returns list of (Pages) pageids, affiliated with this category and the subcategories
    @staticmethod
    def analyze_category(cat_pageid):
        pages = list()
        pages.extend(Category.__get_pages_or_subcategories(cat_pageid, "page"))
        for subcat_pageid in Category.__get_pages_or_subcategories(cat_pageid, "subcat"):
            pages.extend(Category.__get_pages_or_subcategories(subcat_pageid, "page"))
        return pages