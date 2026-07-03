from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv



def retrieve_context(pdf_url,query):

    load_dotenv()

    llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.8,convert_system_message_to_human=True)

    loader = PyPDFLoader(pdf_url)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents([page.page_content for page in pages])

    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",task_type="retrieval_document")

    db = Chroma.from_documents(texts, embeddings_model)

    retriever = db.as_retriever(search_type="mmr")
    
    docs = retriever.get_relevant_documents(query)

    context = ""
    for doc in docs:
        context = context + doc.page_content
    
    return context

def query(pdf_url,system_prompt,query):

    context=""

    if(pdf_url):
        context=retrieve_context(pdf_url,query)

    llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.8,convert_system_message_to_human=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "the context is  :{context}, the input is : {input}")
    ])

    chain = prompt | llm

    return chain.invoke({"input" : query,"context":  context }).content

