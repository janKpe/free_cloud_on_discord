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


@app.route("/delete")
def delete():
    return send_file("frontend/assets/delete.svg")


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
    while os.path.exists(datei_pfad):
        pass

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

@app.route("/remove_file", methods=["POST"])
def remove_file():
    # Erhalte den Schlüssel aus den Request-Parametern
    key_to_remove = request.json.get('file_to_remove')

    if not key_to_remove:
        return jsonify({"error": "Der Parameter 'file_to_remove' fehlt im Request."}), 400

    with open("./files.json", 'r') as file:
        # Lade den JSON-Inhalt
        data = json.load(file)

    # Überprüfe, ob der Schlüssel vorhanden ist, bevor er entfernt wird
    if key_to_remove in data:
        del data[key_to_remove]
        print(f"Schlüssel '{key_to_remove}' wurde erfolgreich aus der JSON-Datei entfernt.")
        # Optional: Sende eine Bestätigung als JSON-Antwort
        with open("./files.json", 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify({"success": True})
    else:
        print(f"Der Schlüssel '{key_to_remove}' ist nicht in der JSON-Datei vorhanden.")
        # Optional: Sende eine Fehlermeldung als JSON-Antwort
        return jsonify({"error": f"Der Schlüssel '{key_to_remove}' ist nicht in der JSON-Datei vorhanden."}), 404

    # Öffne die JSON-Datei zum Schreiben und schreibe die aktualisierten Daten

if __name__ == "__main__":
    app.run(port=5000)