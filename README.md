# StudyBetter
An AI-Powered Study Assistant

StudyBetter is designed to transform user-uploaded documents into useful study materials using a local LLM. The goal is to reduce student workload by automating the creation of summaries, definitions, quizzes, and simplified explanations. 

To run the application: 

1) Have Python 3.8+ installed
2) Install Ollama from https://ollama.com
3) Pull the llama3.18B (the LLM we’re using) with the following terminal command: ollama pull llama3.1:8b
4) Make sure Ollama is running
5) Create a folder with the following structure:
ai-project/
app.py
input.txt
static/
  index.html
  styles.css
7) Make sure each file has the appropriate code/text
8) In a terminal, cd to the project folder (ai-project) and run the following command:
pip install flask requests
9) start the application by running the following command from within the same terminal: python app.py
10) open a browser and go to http://127.0.0.1:8000
11) The application should now be running
