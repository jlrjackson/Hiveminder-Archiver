import html.parser
import sys
import xml.etree.ElementTree as ET

class hiveHTMLToXMLAsTextParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.xmllist = []
    def handle_starttag(self, tag, attrs):
        if tag == "html":
           self.xmllist.append("<root>")
           self.xmllist.append("<task>")
        elif tag == "title":
           self.xmllist.append("</task>")
           self.xmllist.append("<task>")
        elif tag == "dt":
           self.xmllist.append("<pair>")
           self.xmllist.append("<key>")
        elif tag == "dd":
           self.xmllist.append("<value>")
    def handle_endtag(self, tag):
        if tag == "dt":
           self.xmllist.append("</key>")
        elif tag == "dd":
           self.xmllist.append("</value>")
           self.xmllist.append("</pair>")
        elif tag == "html":
            self.xmllist.append("</task>")
            self.xmllist.append("</root>")
    def handle_data(self, data):
        self.xmllist.append(data)
    def return_parsed_data(self):
        # Collapse the list into text.
        xmlfilteredlist = [l for l in self.xmllist if l != 'Hiveminder - REST API' and l.strip() != ""]
        xmltext = "".join(xmlfilteredlist)
        return xmltext

################################################################################################

def hiveCollapseXML(xmltext):
    # Parse the XML data from text into a more shallow XML structure.
    root = ET.fromstring(xmltext)
    newRoot = ET.Element('root')
    tasks = root.findall('task')
    for task in tasks:
        xmlTask = ET.Element('task')
        pairs = task.findall('pair')
        for pair in pairs:
            key = pair.find('key').text
            value = pair.find('value').text
            xmlTask.set(key, value)
        newRoot.append(xmlTask)
    return newRoot
 

# Get all the file names of the Hiveminder saved files.
path = sys.argv[0]
files = []
for i in range(1, 27):
    files.append("Hiveminder - REST API - page " + str(i) + ".html")

# Open the first one and put all the text into a string.
f = open(path + "/" + files[0], 'r')
lines = f.readlines()
f.close()
text = "".join(lines)

# Parse the relevant task data into a strict XML format.
p = hiveHTMLToXMLAsTextParser()
p.feed(text)
xmltext = p.return_parsed_data()

# Parse into shallow XML.
xmlroot = hiveCollapseXML(xmltext)




