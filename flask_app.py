from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os


app = Flask(__name__)
CORS(app)


def leere_ordner(ordnerpfad):
    for datei in os.listdir(ordnerpfad):
        dateipfad = os.path.join(ordnerpfad, datei)
        try:
            if os.path.isfile(dateipfad):
                os.unlink(dateipfad)
        except Exception as e:
            print(f"Fehler beim Löschen von {dateipfad}: {e}")

@app.route("/")
def index():
    return send_file("frontend\index.html")


@app.route("/script.js")
def scriptjs():
    return send_file("frontend\script.js")

@app.route('/files')
def file():
    with open("files.json", "r") as data_file:
        json_file = json.load(data_file)
        return jsonify({"files": list(json_file.keys())})



@app.route('/upload', methods=['POST'])
def upload():
    datei = request.files["data"]

    datei_pfad = "./in/" + request.form['file_name']
    datei.save(datei_pfad)
    return jsonify({"success": True})


@app.route('/download', methods=['POST'])
def download_init():
    leere_ordner("./out/")
    file_name = request.json.get('file_name')

    with open("files_to_get.txt", "a") as file:
        file.write(file_name + "\n")

    while not os.path.exists("./out/" + file_name):
        pass

    return jsonify({"succes": True})

@app.route("/download_file")
def download_file():
    file_name = os.listdir("./out/")[0]
    response = send_file("./out/" + file_name, as_attachment=True)

    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    return response


if __name__ == "__main__":
    app.run(port=5000)