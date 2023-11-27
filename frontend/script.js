// Führe einen GET-Request durch
fetch('http://127.0.0.1:5000/files')
    .then(response => response.json())
    .then(data => {
        // 'data' ist das Ergebnis der Anfrage, wandele es in eine Liste um
        console.log(data);

        // Gib die Liste aus


        data.files.forEach((element) => {
            document.getElementById("files").innerHTML += `<li onclick='downloadFile("${element}")' >${element}</li>`
        })
    })


    function uploadDatei() {
        const dateiInput = document.getElementById('dateiInput');
        const datei = dateiInput.files[0];
    
        if (datei) {
            const formData = new FormData();
            formData.append('file_name', datei.name);
            formData.append('data', datei);
    
            fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Fehler:', error));
        } else {
            console.log('Bitte eine Datei auswählen.');
        }
    }


    function downloadFile(fileName) {
        const data = { file_name: fileName };
    
        fetch('http://localhost:5000/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(response)
            return response.json();
        })
        .then(data => {
            // Erstelle einen Blob-URL und erstelle ein unsichtbares a-Element für den Download
            
            if (data.succes === true) {
                let download = document.createElement('a');
                download.href = "http://127.0.0.1:5000/download_file";
                download.innerHTML = "download"
                download.id = "huhn"
                download.download = fileName;
                document.body.appendChild(download);
                download.click();
            }
        })
        .catch(error => {
            console.error('Fehler beim Herunterladen der Datei:', error);
        });

    }
    
    
    