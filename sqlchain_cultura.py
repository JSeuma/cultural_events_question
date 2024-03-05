from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
import sqlite3
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

def cultura_es_vida(query):
    # Load your CSV file
    csv_file = "https://analisi.transparenciacatalunya.cat/resource/rhpv-yr4f.csv"
    df = pd.read_csv(csv_file)

    # Create a SQLite database and save the dataframe to it
    conn = sqlite3.connect('my_database.db')
    df.to_sql('my_table', conn, if_exists='replace', index=False)
    conn.close()

    uri_mysql = "sqlite:///my_database.db"

    _mysql_prompt = """You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use date('now') function to get the current date, if the question involves "today" or "tomorrow".

    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here in Catalan

    SQLQuery

    """
    PROMPT_SUFFIX = """Only use the following tables:
    {table_info}
    Question: {input}"""

    MYSQL_PROMPT = PromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        template=_mysql_prompt + PROMPT_SUFFIX,
    )

    OPENAI_API_KEY="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"

    streaming_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True, openai_api_key=OPENAI_API_KEY)

    db = SQLDatabase.from_uri(uri_mysql)

    chain = SQLDatabaseChain(llm=streaming_llm,
                            database=db,
                            verbose=False,
                            top_k=8,
                            prompt = MYSQL_PROMPT
                            )

    output =  chain.invoke(
                    {
                        "query": query,
                        # "input": user_msg,
                        "table_info": db.get_table_info(),
                        "top_k": 10
                    }
                    )
    
    #answer = output['Answer']
    return output['result']
