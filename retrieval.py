import os
from pinecone import Pinecone
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from azure.identity import DefaultAzureCredential
#from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


def retrieve():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("cis-benchmark")



    question = "Can you tell me how an Azure VM running linux achieves a certain CIS score?"

    # embedding_response = client.embeddings.create(
    #     model="text-embedding-3-small",
    #     input=question
    # )
    #pinecone_embeddings = PineconeEmbeddings(model="llama-text-embed-v2")
    


    # results = index.search(
    #     namespace="default",
    #     query={
    #         "top_k": 5,
    #         "inputs": {
    #             "text": question
    #         }
    #     },
    #     fields=["text", "source"]
    # )
    results = index.search(
        namespace="default",
        top_k=5,
        inputs={
            "text": question
        },
        fields=["text", "source"]
    )
    context = "\n\n".join(
    hit["fields"]["text"]
    for hit in results["result"]["hits"]
    )

    prompt = f"""
        Use the provided context to answer the question.

        Context:
        {context}

        Question:
        {question}
    """
    
    azure_llm = AzureAIOpenAIApiChatModel(
        project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model="gpt-4.1-mini",  # e.g., "gpt-4o" or "mistral-large"
        credential=DefaultAzureCredential(),
    )
    
     
    response = azure_llm.invoke(prompt)
    print(response)
    # 3. Connect to your Pinecone Vector Store using the model
    # index_name = "cis-benchmark"
    # vector_store = PineconeVectorStore(
    #     index_name=index_name,
    #     embedding=pinecone_embeddings
    # )

    # 4. Pull the relevant vectors for RAG
    
    #retrieved_docs = vector_store.similarity_search(query, k=3)

    # 5. Look at the retrieved documents
    # for doc in retrieved_docs:
    #     print(f"Content: {doc.page_content}")
    #     print(f"Metadata: {doc.metadata}")