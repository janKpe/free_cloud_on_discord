// Führe einen GET-Request durch
fetch('http://127.0.0.1:5000/files')
    .then(response => response.json())
    .then(data => {
        // 'data' ist das Ergebnis der Anfrage, wandele es in eine Liste um
        console.log(data);

        // Gib die Liste aus


        data.files.forEach((element) => {
            document.getElementById("files").innerHTML += `<li>${element}</li>`
        })
    })
    // .catch(error => console.error('Fehler bei der Anfrage:', error));
