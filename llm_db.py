from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

def get_env_vars(*args):
    return [os.getenv(arg) for arg in args]

OPENAI_API_KEY, DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT = get_env_vars('OPENAI_API_KEY', 'DB_HOST', 'DB_NAME', 'DB_USERNAME', 'DB_PASSWORD', 'DB_PORT')

from langchain.sql_database import SQLDatabase
import psycopg2
from langchain_openai import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
import json;

# Establish database connection
LOCALDB_URL_STRING = (
"postgresql+psycopg2://"
+ DB_USERNAME
+ ":"
+ DB_PASSWORD
+ "@"
+ DB_HOST
+ ":"
+ DB_PORT
+ "/"
+ DB_NAME
)

def custom_prompt(input_text):
    prompt = f"""
    Query the database using PostgreSQL syntax.

    Use the shoe_color enum to query the color. Do not query this column with any values not found in the shoe_color enum.
    Use the shoe_width enum to query the width. Do not query this column with any values not found in the shoe_width enum.

    The color and width columns are array types. The name column is of type VARCHAR.
    An example query using an array columns would be:
    SELECT * FROM products, unnest(color) as col WHERE col::text % SOME_COLOR;
    or
    SELECT * FROM products, unnest(width) as wid WHERE wid::text % SOME_WIDTH;

    An example query using the name column would be:
    select * from products where name ILIKE '%input_text%';

    It is not necessary to search on all columns, only those necessary for a query. 
    
    Generate a PostgreSQL query using the input: {input_text}. 
    
    Answer should be in the format of a JSON object. This object should have the key "query" with the SQL query and "query_response" as a JSON array of the query response.
    """

    return prompt

def query_database(user_prompt):
    prompt = custom_prompt(user_prompt)

    sql_database = SQLDatabase.from_uri(LOCALDB_URL_STRING, include_tables=["products", "users", "purchases", "product_inventory"])

    llm = OpenAI(temperature=0, max_tokens=-1)
    db_chain = SQLDatabaseChain(llm=llm, database=sql_database, verbose=True, use_query_checker=True,return_intermediate_steps=True)

    try:
        nw_ans = db_chain.invoke(prompt)
        result = nw_ans["result"]
        result_json = json.loads(result)

        # query = nw_ans["query"]
        # print(f"prompt query: {query}")
        # print(f"prompt result: {result}")
        # print(result_json);

        return result_json["query_response"]
    except (Exception, psycopg2.Error) as error:
        print("this is an error")
        print(error)
    finally: 
        print("finished.")