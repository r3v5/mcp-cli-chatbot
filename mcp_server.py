from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field
from typing import List

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc",
    description="Read the contents of a document and return is as a string"
)
def read_document(
    doc_name: str = Field(description="Name of the document")
    ) -> str:
    return docs.get(doc_name, "")


@mcp.tool(
    name="edit_doc",
    description="Edit a document by replacing a string in the documents content with a new string"
)
def edit_document(
    doc_name: str = Field(description="Name of the document that will be edited"), 
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
    ) -> None:
    if doc_name not in docs:
        raise ValueError(f"Document {doc_name} wasn't found")
    
    docs[doc_name] = docs[doc_name].replace(old_str, new_str)


@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_documents() -> List[str]:
    return list(docs.keys())


@mcp.resource(
    "docs://documents/{doc_name}",
    mime_type="text/plain"   
)
def fetch_content_from_document(doc_name: str) -> str:
    if doc_name not in docs:
        raise ValueError(f"Document {doc_name} wasn't found")

    return docs[doc_name]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_name: str = Field(description="Name of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The name of the document you need to reformat is:
<document_name>
{doc_name}
</document_name>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""
    
    return [
        base.UserMessage(prompt)
    ]


@mcp.prompt(
    name="summarize",
    description="Summarized the contents of the document."
)
def format_document(
    doc_name: str = Field(description="Name of the document to summarize")
) -> list[base.Message]:
    prompt = f"""
Your goal is to summarize a document.

The name of the document you need to summarize is:
<document_name>
{doc_name}
</document_name>


Use the 'fetch_content_from_document' resource to fetch the content from the document.
"""
    
    return [
        base.UserMessage(prompt)
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
