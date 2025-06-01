from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


def main():
    # 1. Load the markdown file into a single string
    with open("data/database.md", "r", encoding="utf-8") as f:
        markdown_document = f.read()

    # 2. Define which headers to split on (adjust as needed)
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    # 3. Initialize the splitter (strip_headers=False to keep header lines in each chunk)
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, strip_headers=False
    )

    # 4. Split the raw markdown text into chunks
    docs = markdown_splitter.split_text(markdown_document)

    # 5. Create embeddings using Google Generative AI
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # 6. Build a Chroma vector store directly from the list of text chunks
    vectordb = Chroma.from_documents(
        docs, embedding=embeddings, persist_directory="chroma_db"
    )
    print(f"Finished Load Chroma: {vectordb.get()['ids']}")


if __name__ == "__main__":
    main()
