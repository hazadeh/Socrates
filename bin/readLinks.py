from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

document = Document('test.docx')
rels = document.part.rels


def iter_hyperlink_rels(rels):
    for rel in rels.values():
        print(rel._target)


iter_hyperlink_rels(rels)
