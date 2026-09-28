import docx

doc = docx.Document('Thông tin sản phẩm chay.docx')
with open('output.txt', 'w', encoding='utf-8') as f:
    for p in doc.paragraphs:
        f.write(f'PARAGRAPH: {p.text}\n')
    
    for rel in doc.part.rels.values():
        if 'hyperlink' in rel.reltype:
            f.write(f'LINK: {rel.target_ref}\n')
