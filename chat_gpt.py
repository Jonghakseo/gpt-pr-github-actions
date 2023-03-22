from langchain.chains import ChatVectorDBChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma

if __name__ == '__main__':

    # with open('test.txt', 'r') as f:
    #     diff = f.read()

    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    diff_doc = text_splitter.split_documents([])

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(diff_doc, embeddings)
    # vectordb.persist()
    top_k = min(len(diff_doc), 4)
    diff_qa = ChatVectorDBChain.from_llm(ChatOpenAI(temperature=0.7, top_p=0.8), vectordb,
                                         return_source_documents=True, top_k_docs_for_context=top_k)


