import os 
import evadb
from dotenv.main import load_dotenv

load_dotenv()

if os.path.exists(".env") and os.environ.get("OPENAI_KEY") is not None:
    user_api_key = os.environ["OPENAI_KEY"]
else:
    user_api_key = "KEY"
os.environ["OPENAI_KEY"] = user_api_key
open_ai_key = os.environ.get('OPENAI_KEY')

cursor = evadb.connect().cursor()
cursor.drop_table("MyPDF").execute()
cursor.load(file_regex="./layout-parser-paper.pdf",
            format="pdf", table_name="MyPDF").execute()
df = cursor.table("MyPDF").df()
print(df)
cursor.drop_udf("ChatGPT").df()
cursor.create_udf("ChatGPT",True,"./chatgpt.py").df()
text_noise = "noise text"
data = (
    cursor.table("MyPDF")
    .filter("page < 2")
    .cross_apply(f"ChatGPT('Act as a classifier. Classify this text as noise:',{text_noise})","objs(response)")
).df()
print(data)
