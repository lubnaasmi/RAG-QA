
# ------------------------- api key setup-----------------------
import os
from dotenv import load_dotenv
load_dotenv() # Load variables from .env into os.environ

api_key = os.getenv("OPENAI_API_KEY") # Get the key
if not api_key:
    raise ValueError("OPENAI_API_KEY not found")




def answer(query, pdf_paths=None):
    """
    query: str
    returns: (answer_text, primary_page, title, sources)
    - answer_text: str
    - primary_page: int (page number of the top source)
    - title: str (filename of the top source)
    - sources: list[dict] = [{"title": filename, "page": Y}, ...]
    """

    import os
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_community.vectorstores import FAISS
    from langchain.chains import RetrievalQA

    # Load Pdf
    pdf_folder = "data"
    lecture_slides = []
    for file in os.listdir(pdf_folder):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(pdf_folder, file)
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            lecture_slides.extend(docs)

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(lecture_slides)

    # Embed and Store
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    retriever = db.as_retriever()

    # Build RetrievalQA+llm chain
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=True
    )

    res = qa.invoke({"query": query})
    answer_text = res.get("result", "")

    # Extract info
    primary_page, title = None, None
    sources = []

    if res.get("source_documents"):
        first_doc = res["source_documents"][0]

        # 
        primary_page = first_doc.metadata.get("page")

        # Filename only
        raw_title = (
            first_doc.metadata.get("title")
            or first_doc.metadata.get("source")
            or first_doc.metadata.get("file_path")
        )
        title = os.path.basename(raw_title) if raw_title else None

        # Build list of sources (only page)
        sources = [
            {
                "title": os.path.basename(
                    d.metadata.get("title") or d.metadata.get("source") or d.metadata.get("file_path") or ""
                ),
                "page": d.metadata.get("page_label"),
            }
            for d in res["source_documents"]
        ]

    return answer_text, primary_page, title, sources

