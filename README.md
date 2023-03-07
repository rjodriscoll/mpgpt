Youtube Summarizer

A Python project that uses OpenAI's GPT-3.5 and whisper models to summarise the content of a YouTube video as you request.


To interact with the summariser notebook you will need to add your openai API key to a `src/config.py` file:

```python
API_KEY = 'my key'
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate    # For Unix-based systems
venv\Scripts\activate.bat   # For Windows
```

Install the required packages using pip:
```bash
pip install -r requirements.txt
```


Use the url and output_format to get a youtube video and decribe how you want it summarised: 

```python
r = Responder(url = 'youtube.com/something', output_format= '10 bullet points')
Markdown(r.get_response())
```
