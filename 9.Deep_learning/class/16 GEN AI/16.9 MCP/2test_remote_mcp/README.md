
Steps
0. create a project folder(test rempte mcp and open the folder in vscode and also open the terminal for run)
1. uv init ((IN CMD))
2. uv add fastmcp (IN CMD)
3. add the code in main.py (in vscode file)
4. activate env (IN CMD)-->  .\.venv\Scripts\activate
5. (IN CMD) --> uv run main.py or ( fastmcp run main.py --transport http --host 0.0.0.0 --port 8000)
6. (IN CMD) check our mcpserver run or not --> uv run fastmcp dev inspector main.py --> or  uv run fastmcp dev main.py

6. now create a github repo and push the  code 
    - git init
       - git add *
       - git commit -m "first commit"
       - git branch -M main
       - git remote add origin https://github.com/shahil04/test-remote-mcp-server-1.git
       - git push -u origin main
7. NOw host this mcp server in cloud --> https://horizon.prefect.io/ 

