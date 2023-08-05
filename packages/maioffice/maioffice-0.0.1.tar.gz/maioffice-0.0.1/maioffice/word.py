import docx

def replace_text(filename, target_str, new_str):
    doc = docx.Document(filename)
    for para in doc.paragraphs:
        if target_str in para.text:
            for run in para.runs:
                if target_str in run.text:
                    text = run.text.replace(target_str, new_str)
                    run.text = text
    return doc
