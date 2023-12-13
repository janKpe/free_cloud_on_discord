FROM nginx:latest

# Kopiere die lokale Nginx-Konfigurationsdatei in das Image
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /free_cloud_on_discord

# copy files

COPY requiremnts.txt requirements.txt 
COPY /frontend/main.js main.js
COPY ./frontend/build/ build/
COPY flask_app.py flask_app.py
COPY main.py main.py
COPY functions/ functions/
COPY startup.py startup.py

# get packages in cache
RUN apt-get update


# install python3 and pip
RUN apt install -y python3.11
RUN apt install -y python3.11-venv
RUN apt install -y python3-pip

RUN python3 -m venv /opt/venv


# install python dependencies
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
    

# install node js and npm
ENV NODE_VERSION=16.13.0
RUN apt-get install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version


RUN npm install express


EXPOSE 8080

CMD ["python3", "startup.py"]
