from io import BytesIO
from docx import Document

def generate_content_from_doc(
        doc_file: BytesIO
):
    document = Document(doc_file)
    content = []

    for para in document.paragraphs:
        style = para.style.name
        if style.startswith("Heading"):
            content.append({
                "type": "heading",
                "attrs": {
                    "level": int(style[-1])
                },
                "content": [
                    {
                        "type": "text",
                        "text": para.text
                    }
                ]
            })
        elif style.startswith("Normal"):
            content.append({
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": para.text
                    }
                ]
            })
        elif style.startswith("List"):
            list_item = {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": para.text
                            }
                        ]
                    }
                ]
            }
            if content[-1].get("type") == "bulletList":
                content[-1]["content"].append(list_item)
            else:
                content.append({
                    "type": "bulletList",
                    "attrs": {
                        "tight": True
                    },
                    "content": [list_item]
                })

    full_json = {
        "type": "doc",
        "content": content
    }

    return full_json
