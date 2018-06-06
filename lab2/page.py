import urllib.request
from lxml import etree
import os
import wikitextparser as wtp


class Page:
    def __init__(self, pageid):
        self.pageid = pageid
        self.filename = os.path.join(os.path.dirname(__file__), "xml", str(self.pageid) + ".xml")

    # creates .xml file with fields of page
    def __create_blank_page(self):
        # if "name" file exists, it will overwrite it
        root = etree.Element('page')
        etree.SubElement(root, 'title')
        etree.SubElement(root, 'pageid')
        etree.SubElement(root, 'category')
        etree.SubElement(root, 'sections')
        tree = etree.ElementTree(root)

        tree.write(self.filename, xml_declaration=True, encoding='UTF-8', method='xml')

    # fills fields of blank .xml file with contents
    def __fill_page_with_contents(self, contents):
        tree = etree.parse(self.filename)
        root = tree.getroot()

        # fill title
        root.find(".//title").text = contents['title']
        # fill title
        root.find(".//pageid").text = contents['pageid']
        # fill category
        category = root.find(".//category")
        for cont_category in contents['categories']:
            category.text = cont_category.strip()
            # take only first category
            break
        # fill sections
        sections = root.find(".//sections")
        undesired_sections = ["See also", "Notes", "External links", "References"]
        for wtp_sect in contents['wtp_sections']:
            # level == >=3 are subsections
            # Sections "See also", "References", "Notes" and "External links" are not needed
            if wtp_sect.level < 3 and not (wtp_sect.title.strip() in undesired_sections):
                section = etree.SubElement(sections, 'section')
                section.set('title', wtp_sect.title.strip())
                section.text = wtp_sect.contents

        tree.write(self.filename)

    # method, that returns dict() with contents of the page,
    # received from wiki REST API in xml format
    @staticmethod
    def __parse_wiki_xml(wiki_xml):
        parsed = dict()
        root = etree.fromstring(wiki_xml)

        page = root.find(".//page")
        # categories of the page
        cats = page.findall(".//categories/cl")
        # cat.get('title')[9:] - slices the first 9 symbols of the category name (it's "Category:")
        parsed['categories'] = list(cat.get('title')[9:] for cat in cats)
        # title of the page
        parsed['title'] = page.get('title')
        # pageid of the page
        parsed['pageid'] = page.get('pageid')
        # text of the page
        parsed['text'] = page.find(".//extract").text
        return parsed

    # GET method
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

    # creates .xml document with the info of the given page from Wikipedia
    def xml_page_create(self):
        try:
            wiki_xml = self.__get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts|categories&clshow=!hidden"
                                  "&explaintext=&exsectionformat=wiki&format=xml&pageids=" + str(self.pageid))
            page_contents = self.__parse_wiki_xml(wiki_xml)
            self.__create_blank_page()

            # wtp
            wtp_text = wtp.parse(page_contents['text'])

            page_contents['wtp_sections'] = wtp_text.sections
            self.__fill_page_with_contents(page_contents)
        # If the original given page is wrong (i. e. redirects somewhere)
        except Exception:
            print("Error occured while trying to parse the Page with pageid: " + str(self.pageid))
            os.remove(self.filename)