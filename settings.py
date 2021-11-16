from dotenv import load_dotenv, find_dotenv
import os 

load_dotenv(find_dotenv("./Env/.env"))

API = os.environ.get("API_token")

print(API)
