import os

def split_large_file(input_file_path, output_directory, chunk_size=20):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    chunk_size_bytes = chunk_size * 1024 * 1024

    with open(input_file_path, 'rb') as input_file:
        chunk_number = 1
        while True:
            chunk = input_file.read(chunk_size_bytes)

            if not chunk:
                break

            output_file_path = os.path.join(output_directory, f"chunk_{chunk_number}")
            with open(output_file_path, 'wb') as output_file:
                output_file.write(chunk)

            chunk_number += 1

    print(f"Aufteilung der Datei '{input_file_path}' abgeschlossen.")

if __name__ == "__main__":
    # Beispielaufruf
    input_file_path = 'files/Der-Bosco-Verticale-in-Mailand-Italien.pptx'
    output_directory = 'chunks/'
    split_large_file(input_file_path, output_directory, 1)


