from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
import shutil

app = Flask(__name__)
CORS(app, support_credentials=True)

def generate_folder_tree(root_path):
    folder_tree = {'name': os.path.basename(root_path), 'children': []}
    try:
        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path):
                folder_tree['children'].append(generate_folder_tree(item_path))
    except Exception as e:
        print(f"Fehler beim Durchsuchen des Verzeichnisses {root_path}: {str(e)}")
    return folder_tree

def remove_type_key(tree):
    if 'type' in tree:
        del tree['type']
    if 'children' in tree:
        for child in tree['children']:
            remove_type_key(child)

def empty_filder(ordnerpfad):
    for datei in os.listdir(ordnerpfad):
        dateipfad = os.path.join(ordnerpfad, datei)
        try:
            if os.path.isfile(dateipfad):
                os.unlink(dateipfad)
        except Exception as e:
            print(f"Fehler beim Löschen von {dateipfad}: {e}")

@app.route("/")
def index():
    return "jojooo"


@app.route('/files/', methods=['POST'])
def file():
    path = json.loads(request.data)["path"]
    response = {}

    with open(f"./files{path}files.json", "r") as data_file:
        json_file = json.load(data_file)
        response["files"] = list(json_file.keys()) 
    
    dirs = os.listdir(f"./files{path}")
    dirs.remove("files.json")

    response["dirs"] = dirs
    
    return jsonify(response)


@app.route('/folder_tree')
def get_folder_tree():
    start_directory = "./files"  # Passe dies an den Pfad deines gewünschten Verzeichnisses an
    tree_structure = generate_folder_tree(start_directory)
    remove_type_key(tree_structure)
    return jsonify(tree_structure)

@app.route("/newFolder/", methods=['POST'])
def newFolder():
    path = json.loads(request.data)["path"]
    folder_name = json.loads(request.data)["folder_name"]
    
    new_folder_path = "./files" + path.replace("@@@", "/") + folder_name
    os.makedirs(new_folder_path)

    with open(new_folder_path + "/files.json", "w") as file:
        file.write(json.dumps({}))
    
    return jsonify({"succes": True})

@app.route('/upload/', methods=['POST'])
def upload():
    datei = request.files["data"]
    folder = request.form['path']
    datei_pfad = "./in/" + folder + request.form['file_name']
    datei.save(datei_pfad)
    while os.path.exists(datei_pfad):
        pass

    return jsonify({"success": True})


@app.route('/download/', methods=["POST"])
def download_init():
    empty_filder("./out/")
    file_name = json.loads(request.data)["file_name"]
    path = json.loads(request.data)["path"]
    print(file_name)
    with open("files_to_get.txt", "a") as file:
        file.write("./files" + path + "files.json" +"###" + file_name + "\n")

    while not os.path.exists("./out/" + file_name):
        pass
    return jsonify({"succes": True})

@app.route("/download_file/")
def download_file():
    file_name = os.listdir("./out/")[0]
    response = send_file("./out/" + file_name, as_attachment=True)

    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    return response

@app.route("/remove_file/", methods=["POST"])
def remove_file():
    print("hall jooo")
    key_to_remove = json.loads(request.data)['file_to_remove']
    path = json.loads(request.data)['path']
    print(json.loads(request.data)['file'])
    print(path)

    if not key_to_remove:
        return jsonify({"error": "Der Parameter 'file_to_remove' fehlt im Request."}), 400

    if not json.loads(request.data)['file']:
        shutil.rmtree("./files" + path + key_to_remove)
        return jsonify({"success": True})

    else:
        with open("./files" + path + "files.json", 'r') as file:
            data = json.load(file)

        if key_to_remove in data:

            del data[key_to_remove]
            print(f"Schlüssel '{key_to_remove}' wurde erfolgreich aus der JSON-Datei entfernt.")
            with open("./files" + path + "files.json", 'w') as file:
                json.dump(data, file, indent=4)

            return jsonify({"success": True})
        else:
            print(f"Der Schlüssel '{key_to_remove}' ist nicht in der JSON-Datei vorhanden.")
            return jsonify({"error": f"Der Schlüssel '{key_to_remove}' ist nicht in der JSON-Datei vorhanden."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


    
