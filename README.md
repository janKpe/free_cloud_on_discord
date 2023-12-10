## Discord Cloud

### Overview
This project consists of a Discord bot written in Python using the py-cord library and a Flask web application written in Python for file transfer. The bot monitors a designated Discord channel for file uploads, splits large files into chunks, and sends them as messages. The web application provides a user interface for uploading, downloading, and managing files.

### How to Run

#### Discord Bot
1. Ensure Python is installed.
2. Install required dependencies using `pip install -r requirements.txt`.
3. Replace the Discord bot token in `main.py` with your bot token.
4. Run the bot using `python main.py`.

#### Flask Web Application
1. Install required dependencies using `pip install -r requirements.txt`.
2. Run the Flask app using `python flask_app.py`.

#### React Front-End
1. Navigate to the `frontend` directory.
2. Install dependencies using `npm install`.
3. Replace the host var in App.js with your Domain/Host name
4. Compile everything with `sudo npm run build`
5. Start the server with `sudo node main.js`.
6. The React app will be accessible at `http://localhost:80`.

### Usage
1. Upload files to Discord channel designated for the bot to trigger file processing.
2. Use the web interface to manage and download files.
3. Files are stored in the `./in/`, `./out/`, `./chunks/`, and `./chunks_to_combine/` directories.

### Contributors
- Jan Kupke

### License
This project is licensed under the [MIT License](LICENSE).

Feel free to contribute, report issues, or suggest improvements!
