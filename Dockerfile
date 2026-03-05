FROM python:3.11-slim

WORKDIR /app

RUN apt-get update

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "app.py", "--server.address=0.0.0.0"]