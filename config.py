import os

CAZE_ICON_PATH = os.path.join(os.getcwd(), 'assets', 'whi_logo.png')
PNG_LOGO = os.path.join(os.getcwd(), 'assets', 'col_logo.png')

# These must match the models listed from Ollama
LOCAL_MODEL = "llama2" 
LOCAL_EMBED_MODEL = "nomic-embed-text"
BASE_URL = "http://localhost:11434"  # ✅ Important: localhost instead of IP

FILE_PATH = os.path.join(os.getcwd(), 'docs')
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)

PERSISTAND_PATH = os.path.join(os.getcwd(), "persistent_dir")
if not os.path.exists(PERSISTAND_PATH):
    os.makedirs(PERSISTAND_PATH)

