# StudyBetter
An AI-Powered Study Assistant

StudyBetter is designed to transform user-uploaded documents into useful study materials using a local LLM. The goal is to reduce student workload by automating the creation of summaries, definitions, quizzes, and simplified explanations. 

To run the application: 

1) Have Python 3.8+ installed
2) Install Ollama from https://ollama.com
3) Pull the llama3.18B (the LLM we’re using) with the following terminal command: ollama pull llama3.1:8b
4) Make sure Ollama is running
5) Create a folder with the following structure:
app.py
input.txt
static/
  index.html
  styles.css
6) Make sure each file has the appropriate code/text
7) In a terminal, cd to the project folder and run the following command: pip install flask requests
8) start the application by running the following command from within the same terminal: python app.py
9) open a browser and go to http://127.0.0.1:8000
10) The application should now be running
