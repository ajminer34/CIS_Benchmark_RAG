from pinecone import Pinecone
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import traceback

def ingest():
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index("cis-benchmark")

        files = os.listdir("/Users/aidenminer/repos/CIS_Benchmark_RAG/ingestion/CIS_benchmarks")
       

        for file in files:
           
            if ".pdf" not in file:
                continue
            loader = PyPDFLoader(f"/Users/aidenminer/repos/CIS_Benchmark_RAG/ingestion/CIS_benchmarks/{file}")
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=150
            )

            chunks = splitter.split_documents(documents)

            records = []

            for chunk in chunks:
                
                records.append(
                    {
                        "id": f"{file}:{os.path.getmtime(f"/Users/aidenminer/repos/CIS_Benchmark_RAG/ingestion/CIS_benchmarks/{file}")}",
                        "text": chunk.page_content,
                        "source": chunk.metadata.get("source"),
                        "page": chunk.metadata.get("page"),
                    }
                )

                if len(records) == 95:

                    index.upsert_records(
                        namespace="__default__",
                        records=records
                    )
                    records = []

            index.upsert_records(
                        namespace="__default__",
                        records=records
                    )
    except Exception as e:
        print(e)
        traceback.print_exc()
   