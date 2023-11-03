# -*- coding: utf-8 -*-
"""Копия блокнота "LLM.ipynb"

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-7bR0WfQ0NyFdNbmmWOoM2wDms6ytWKH
"""


from langchain.document_loaders import DataFrameLoader
import pandas as pd

df = pd.read_csv('data/first_five_thousand.csv', sep=';', encoding='utf-8' )
print('done')

df.head(3)

df = df.loc[:, 'Текст'].to_frame()

loader = DataFrameLoader(df, page_content_column="Текст")

from langchain.vectorstores import Chroma

df_document = loader.load()

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1600, chunk_overlap=10)
texts = text_splitter.split_documents(df_document)

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

chromadb_index = Chroma.from_documents(
    texts, embedding_function, persist_directory='./input'
)

from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline

retriever = chromadb_index.as_retriever()

# model_id = "databricks/dolly-v2-3b" #my favourite textgeneration model for testing
# task="text-generation"

# HuggingFacePipeline.from_model_id?

# pip install auto-gptq optimum

import torch
from langchain import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline

MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto"
)

# generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
# generation_config.max_new_tokens = 1024
# generation_config.temperature = 0.0001
# generation_config.top_p = 0.95
# generation_config.do_sample = True
# generation_config.repetition_penalty = 1.15

# text_pipeline = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     generation_config=generation_config,
# )

# llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
generation_config.max_new_tokens = 1024
generation_config.temperature = 0.0001
generation_config.top_p = 0.95
generation_config.do_sample = True
generation_config.repetition_penalty = 1.15

text_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    generation_config=generation_config,
)

llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})

document_qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever
)

response = document_qa.run("Инструкция: Предоставь информацию в формате одного предложения. " \
                           "Ответь на следующий вопрос: "\
                           "Что думают горожане о ситуации с уборкой снега зимой в Санкт-Петербурге?" )
display(response)

for doc in response.documents:
    print(doc.text)

# ------------------------------------------------------------------------------------------------------------------------------







llm(
    "Выдели адрес в следующем тексте: рядом с улицей Авиаторов Балтики 36 красивый парк и памятник и новый автомобиль соседа а на Гражданском нет ничего такого там Моисеев не живет"
)

llm(
    "Выдели указанный адрес в следующем тексте в формате для тренировка BERT модели: рядом с улицей Авиаторов Балтики 36 красивый парк и памятник"
)



from langchain import PromptTemplate

template = """
<s>[INST] <<SYS>>
Act as a Machine Learning engineer who is teaching high school students.
<</SYS>>

{text} [/INST]
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=template,
)

text = "Explain what are Deep Neural Networks in 2-3 sentences"
print(prompt.format(text=text))

result = llm(prompt.format(text=text))
print(result)

from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(text)
print(result)

template = "<s>[INST] Use the summary {summary} and give 3 examples of practical applications with 1 sentence explaining each [/INST]"

examples_prompt = PromptTemplate(
    input_variables=["summary"],
    template=template,
)
examples_chain = LLMChain(llm=llm, prompt=examples_prompt)

from langchain.chains import SimpleSequentialChain

multi_chain = SimpleSequentialChain(chains=[chain, examples_chain], verbose=True)
result = multi_chain.run(text)
print(result.strip())

