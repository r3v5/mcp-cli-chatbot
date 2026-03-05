from mcp.server.fastmcp import FastMCP
from pydantic import Field

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


# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
