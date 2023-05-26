FROM python:3.11-alpine

RUN pip install --upgrade pip

RUN pip install poetry

WORKDIR /rapid_crawler

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --only main --no-root --no-interaction

COPY rapid_crawler ./rapid_crawler

COPY ./main.py ./main.py

CMD ["poetry", "run", "python", "main.py"]