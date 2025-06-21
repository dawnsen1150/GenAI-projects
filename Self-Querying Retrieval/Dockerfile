FROM node:20-alpine AS frontend  
WORKDIR /home/node/app 
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

COPY --chown=node:node ./frontend/package*.json ./
#USER node
RUN npm ci  
COPY --chown=node:node ./frontend/ ./frontend
WORKDIR /home/node/app/frontend
RUN npm run build
  
FROM python:3.11.9-bookworm

# Install necessary packages
RUN apt update && \
    apt install -y build-essential libffi-dev libssl-dev curl wget gnupg

COPY --chown=node:node ./backend/.env /app/backend/.env
COPY ./backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir --verbose -r /app/backend/requirements.txt \
    && rm -rf /root/.cache
    
COPY . /app

COPY --from=frontend /home/node/app/frontend/build  /app/frontend/build/

RUN ls /app/frontend/build/

RUN ls /app/frontend/build/static

WORKDIR /app/backend

EXPOSE 80  

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
