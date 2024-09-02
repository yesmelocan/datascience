import os

script_path = "c:/Users/melih/Documents/GitHub/datascience/project/project 2/webscraping_working_doc.py"
with open(script_path, 'r') as f:
    script_code = f.read()

exec(script_code)
