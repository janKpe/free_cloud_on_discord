from os import system, mkdir, listdir, environ
from subprocess import Popen
from json import dumps

mkdir("files")
with open("files/files.json", "w") as file:
    file.write(dumps({}))

system("service nginx start")

files = listdir("/free_cloud_on_discord/build/static/js/")

for file in files:
    if file.endswith(".js") and ".chunk.js" not in file:
        with open(f"/free_cloud_on_discord/build/static/js/{file}", "r") as js_file:
            file_text = js_file.read()
        
        file_text = file_text.replace("https://example.com", f"http://{environ.get('WEB_DOMAIN')}")
        with open(f"/free_cloud_on_discord/build/static/js/{file}", "w") as js_file:
            js_file.write(file_text)

Popen("node main.js", shell=True)
Popen("/opt/venv/bin/python main.py", shell=True)
Popen("/opt/venv/bin/python flask_app.py", shell=True)

with open("App.js", "a") as file:
    file.write("// jajsjdfkasjdf")
while True:
	pass
