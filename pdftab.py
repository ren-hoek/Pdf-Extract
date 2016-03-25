from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator

def get_horiz(extra_fields):
    return extra_fields[0]

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def convert_pdf_table(pdf_file):
    pdf_file = open(pdf_file, 'rb')
    parser = PDFParser(pdf_file)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()

    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)

    table = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page) 
        layout = device.get_result()
        page_table = tabulate_page(layout)
        header = page_table[0]
        rows = page_table[1:]
        for row in rows:
            row_dict = {}
            for item, detail in enumerate(row):
                if detail != '':
                    row_dict[header[item].lower()] =  detail
            table.append(row_dict)           
                
    return table

def tabulate_page(layout):
    a=[]
    for k in layout:
        if type(k) == LTTextBoxHorizontal:
            b=[]
            for j in k:
                c=[]
                c.append(round(j.x0, 3))
                c.append(round(j.y1, 3))
                c.append(remove_non_ascii(j.get_text().replace('\n','')))
                b.append(c)
            a.append(b)

    text_boxes = len(a)
    rows = len(a[0])

    for i in xrange(rows):
        n = []
        for j in xrange(1,text_boxes-1):
            k = len(a[j])
            for m in xrange(k):
                if a[j][m][1] == a[0][i][1]:
                    n.append([a[j][m][0],a[j][m][2]])
                extra_fields = sorted(n, key=get_horiz)

        if len(extra_fields)<3:
            a[0][i].append("")
        for field in extra_fields:
            a[0][i].append(field[1])  

    table = []
    for row in a[0]:
        table.append(row[2:])

    return table
