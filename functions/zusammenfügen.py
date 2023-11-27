import os

def combine_chunks(input_directory, output_file_path):
    chunks = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
    chunks.sort(key=lambda x: int(x.split('_')[1]))

    with open(output_file_path, 'wb') as output_file:
        for chunk_file in chunks:
            chunk_path = os.path.join(input_directory, chunk_file)
            with open(chunk_path, 'rb') as input_chunk:
                output_file.write(input_chunk.read())

    dateien = os.listdir(input_directory)

    # Lösche jede Datei im Ordner
    for datei in dateien:
        datei_pfad = os.path.join(input_directory, datei)
        try:
            if os.path.isfile(datei_pfad):
                os.remove(datei_pfad)
        except Exception as e:
            print(f'Fehler beim Löschen der Datei {datei}: {str(e)}')
    print(f"Zusammenführen der Chunks abgeschlossen. Gespeichert unter '{output_file_path}'.")

if __name__ == "__main__":
    # input_directory = 'chunks/'
    # output_file_path = 'out/neue-datei.pptx'
    # combine_chunks(input_directory, output_file_path)
    combine_chunks("./chunks_to_combine", f"out/grose detei.txt")
