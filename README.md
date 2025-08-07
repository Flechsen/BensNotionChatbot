# Notion RAG Chatbot
**Brief Description:**

**🚀 Overview:**
- Vector Search: Uses FAISS for similarity search across Notion knowledge base
- Frontend Streamlit
- Deployment on Streamlit Cloud (free of charge)
- URL of deployed application is then embedded in Notion page as an iframe

**Before startup**
1. Re-run embedding/vectorization pipeline for new information: "python ingest.py" (locally)
2. start streamlit app: “streamlit run app.py” (locally)



## 📋 Prerequisites
- OpenAI API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Flechsen/BensNotionChatbot.git
   cd BensNotionChatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   - Create a `.streamlit` folder in your project directory
   - Create a `secrets.toml` file inside `.streamlit`
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = 'sk-your-api-key-here'
     ```

## 📁 Project Structure

```
notion-chatbot/
│
├── .streamlit/
│   └── secrets.toml          # OpenAI API key (git-ignored)
│
├── faiss_index/              # Vector database storage
│
├── notion_content/           # Your exported Notion content
│
├── app.py                    # Streamlit chat application
├── ingest.py                 # Convert Notion content to vectors
├── utils.py                  # Conversational chain utilities
├── requirements.txt          # Python dependencies
└── .gitignore               # Git ignore file
```

## 🚀 Quick Start

### Step 1: Export Your Notion Content

1. Navigate to your Notion page
2. Click the three dots (⋯) in the top-right corner
3. Select **Export**
4. Choose **Markdown & CSV** format
5. Enable **Include subpages**
6. Save as `notion_content.zip`
7. Extract the contents into the `notion_content/` folder

### Step 2: Create Vector Database

Run the ingestion script to convert your Notion content into searchable vectors:

```bash
python ingest.py
```

This will:
- Load all markdown files from `notion_content/`
- Split content into chunks based on markdown headers
- Create embeddings using OpenAI
- Store vectors in a FAISS index

### Step 3: Run the Chatbot

Launch the Streamlit application:

```bash
streamlit run app.py
```

Your chatbot will be available at `http://localhost:8501`

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub (ensure `.streamlit/secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. In **Advanced settings**, add your OpenAI API key:
   ```
   OPENAI_API_KEY = 'sk-your-api-key-here'
   ```
5. Deploy!

### Embed in Notion

1. Copy your deployed Streamlit app URL
2. In Notion, type `/embed`
3. Paste your app URL
4. Click **Embed link**

## ⚙️ Configuration

### Customize the System Prompt

Edit the template in `utils.py` to change how the chatbot responds:

```python
template = """
You are an AI assistant for answering questions about [Your Content].
...
"""
```

### Adjust Chunk Size

Modify text splitting parameters in `ingest.py`:

```python
markdown_splitter = RecursiveCharacterTextSplitter(
    separators=["#","##", "###", "\n\n","\n","."],
    chunk_size=1500,        # Adjust chunk size
    chunk_overlap=100       # Adjust overlap
)
```

### Change Number of Retrieved Documents

In `utils.py`, modify the retriever settings:

```python
retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # Change k value
```

## 🔧 Advanced Features

### Memory Configuration

The chatbot uses a sliding window memory. Adjust in `utils.py`:

```python
memory = ConversationBufferWindowMemory(k=3)  # Remember last 3 exchanges
```

### Temperature Settings

Control response creativity in `utils.py`:

```python
llm = ChatOpenAI(temperature=0)  # 0 = deterministic, 1 
