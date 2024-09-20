FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry install

COPY . /app

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "app/app.py"]
