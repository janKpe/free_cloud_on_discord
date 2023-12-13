## Free Cloud on Discord

### Overview
Discord Cloud is a versatile project comprising a Discord bot developed in Python using the py-cord library and a Flask web api. The bot actively monitors a specified Discord channel for file uploads, intelligently breaks down larger files into manageable chunks, and dispatches them as messages. Meanwhile, the web application provides users with a user-friendly interface for effortless file uploading, downloading, and file management.

### How to Run

Before running the bot, make sure to create a Discord bot, invite it to your server and get its Token. 
[Tutorial](https://www.youtube.com/watch?v=4XswiJ1iUaw)

#### Using Docker (recomended)
1. Build the Docker image with `sudo docker build -t free_cloud_on_discord .`
2. Run the Docker container with `sudo docker run -p [Port]:80 -e BOT_TOKEN=[Bot token] -e WEB_DOMAIN=[Your Domain (localhost)] free_cloud_on_discord`

If you prefer not to use Docker or need to make code modifications, follow these steps:

#### Discord Bot
1. Ensure Python 3.11.7 is installed.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Replace the Discord bot token in `main.py` with your bot token.
4. Run the bot using `python3 main.py`.

#### Flask Web Application
1. Install required dependencies using `pip install -r requirements.txt`.
2. Run the Flask app with `python3 flask_app.py`.

#### React Front-End
1. Navigate to the `frontend` directory.
2. Install dependencies using `npm install`.
3. Replace the host variable in `App.js` with your Domain/Host name.
4. Compile everything with `sudo npm run build`.
5. Start the server with `sudo node main.js`.
6. Access the React app at `http://localhost:81`.

### Nginx
1. Install nginx using `sudo apt install nginx`
2. Place the `nginx.conf` in `/etc/nginx/`
3. Start nginx with `sudo systemctl start nginx`

### Contributors
- Jan Kupke

### License
This project is licensed under the [MIT License](LICENSE).

Feel free to contribute, report issues, or suggest improvements! Your involvement is highly appreciated.