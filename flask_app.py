from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
import time

app = Flask(__name__)
CORS(app, origins=["http://ssh.jan-kupke.de"], support_credentials=True)

def leere_ordner(ordnerpfad):
    for datei in os.listdir(ordnerpfad):
        dateipfad = os.path.join(ordnerpfad, datei)
        try:
            if os.path.isfile(dateipfad):
                os.unlink(dateipfad)
        except Exception as e:
            print(f"Fehler beim Löschen von {dateipfad}: {e}")

@app.route('/files/')
def file():
    with open("files.json", "r") as data_file:
        json_file = json.load(data_file)
        return jsonify({"files": list(json_file.keys())})


@app.route('/upload/', methods=['POST'])
def upload():
    datei = request.files["data"]
    datei_pfad = "./in/" + request.form['file_name']
    datei.save(datei_pfad)
    while os.path.exists(datei_pfad):
        pass

    return jsonify({"success": True})


@app.route('/download/', methods=["POST"])
def download_init():
    leere_ordner("./out/")
    print("jojo")
    print(request.data)
    print(request.content_type)
    file_name = json.loads(request.data)["file_name"]
    print(file_name)
    with open("files_to_get.txt", "a") as file:
        file.write(file_name + "\n")

    while not os.path.exists("./out/" + file_name):
        pass

    return jsonify({"succes": True})

@app.route("/download_file/")
def download_file():
    file_name = os.listdir("./out/")[0]
    response = send_file("./out/" + file_name, as_attachment=True)

    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    return response

@app.route("/remove_file", methods=["POST"])
def remove_file():
    key_to_remove = request.json.get('file_to_remove')

    if not key_to_remove:
        return jsonify({"error": "Der Parameter 'file_to_remove' fehlt im Request."}), 400

    with open("./files.json", 'r') as file:
        data = json.load(file)

    if key_to_remove in data:
        del data[key_to_remove]
        print(f"Schlüssel '{key_to_remove}' wurde erfolgreich aus der JSON-Datei entfernt.")
        with open("./files.json", 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify({"success": True})
    else:
        print(f"Der Schlüssel '{key_to_remove}' ist nicht in der JSON-Datei vorhanden.")
        return jsonify({"error": f"Der Schlüssel '{key_to_remove}' ist nicht in der JSON-Datei vorhanden."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
