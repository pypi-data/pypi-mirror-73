import docx

def load(filename):
    """return python-docx.Document object by filename
    """
    return docx.Document(filename)

def replace(doc, target_str, new_str):
    """replace all text in an MS word document from target_str to new_str.

    Arguments:
    doc -- python-docx.Document
    target_str -- origin text
    new_str -- new text
    """
    for para in doc.paragraphs:
        if target_str in para.text:
            for run in para.runs:
                if target_str in run.text:
                    text = run.text.replace(target_str, new_str)
                    run.text = text
