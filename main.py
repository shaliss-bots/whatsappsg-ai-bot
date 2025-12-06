from dotenv import load_dotenv
load_dotenv()

from src.app import app  

if __name__ == "__main__":
    app.run(debug=True)
    
    





