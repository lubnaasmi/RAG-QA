# Ask Your PDFs (RAG + Streamlit)


An interactive Q&A application that allows you to ask questions about your PDF documents and get answers based on their content. Built with Streamlit and LangChain, this tool uses a  Retrieval-Augmented Generation (RAG) pipeline to provide accurate answers grounded in the PDFs’ text. It integrates OpenAI’s language models with a FAISS vector store to search relevant content chunks, enabling a chatbot-like experience over your PDF files.

## Features
• **Multi-PDF Support**:  Include multiple documents at once (the app comes with four sample PDFs) and ask questions across all of them ￼. The retrieval system will find relevant information from any of the PDFs to answer your query.<br>

• **Retrieval-Augmented QA**:  Implements a RAG pipeline – PDFs are automatically parsed and split into chunks, embeddings are created with OpenAI, and similar chunks are retrieved via FAISS for each query. This ensures answers stay factual and specific to your documents.<br>

• **Streamlit Web Interface**:  Easy-to-use interface built with Streamlit. Simply run the app and interact through a browser UI in real time – type your questions and receive answers with cited context from the PDFs.<br>

• **OpenAI & LangChain Powered**: Utilizes OpenAI’s GPT-4 API for generating answers from the retrieved text, orchestrated by LangChain. The app uses LangChain’s integration with FAISS for efficient similarity search on document embeddings.(PyPDF2 is used under the hood for PDF text extraction.)<br>

• **Local Knowledge Base**: All processing is done locally – your PDF content is converted to embeddings and stored in a FAISS vector index on the fly. No external storage of data; simply add or remove PDFs in the data/ folder to change the knowledge base.


 ### Usage
- **Asking Questions**: In the Streamlit app, you’ll be able to enter a question in a text box. Upon submission, the app will process your query against the PDFs. It will retrieve relevant snippets from the documents and then use the OpenAI LLM to generate an answer based on those snippets ￼. The answer will be displayed, often with references or source text from the PDFs to provide context.<br>
- **Sample PDFs**: The repository includes four sample PDFs in the data/ folder covering topics like data processing, feature engineering, NLP embeddings, and Naive Bayes. Feel free to ask questions about their content (e.g., “What is a naive Bayes classifier?” or “Explain vector embeddings.”). The app will pull the answer from the relevant PDF.<br>

- **Viewing Sources**:The app show you which document or section provided the information for the answer. This helps verify the answer against the original text.


## Keeping Your API Key Secure

- This project uses a .env file to store your OpenAI API key (and any other secret keys).
	
- Used .env.example: The repository provides a .env.example file with the necessary variable names . Use this as a template for your own .env. 

### How It Works (Brief Overview)

When you ask a question, here’s what happens behind the scenes:

	1.	Document Ingestion: Each PDF in data/ is read and split into smaller text chunks (to fit into the model’s context window). 

	2.	Embedding Generation: The app uses OpenAI’s embedding model to convert each text chunk into a numeric vector representation.These embeddings are stored in a FAISS vector index for fast similarity search.

	3.	Retrieval: Upon receiving your query, the app also embeds the question and searches the vector index for the most relevant chunks of text. It fetches the top matching snippets from your PDFs that are semantically related to your question.

	4.	Generation: The retrieved text snippets are passed to the OpenAI LLM (via LangChain’s RetrievalQA chain) as context. The LLM then generates a answer to the question, using the provided document context to ground the response.

	5.	Response: The answer is returned and displayed in the Streamlit interface. Because the answer was generated with knowledge from your PDFs, it should directly address your query using the content of your documents (and not rely on any outside data).

This RAG approach ensures that the AI’s responses remain tied to your source material, making it especially useful for Q&A on custom documents.



## Final Thoughts

This project provides a solid foundation for experimenting with Retrieval-Augmented Generation on your own documents. You can extend it, refine it, and adapt it to fit your needs. Most importantly, enjoy exploring and asking meaningful questions to your PDFs! 🚀



