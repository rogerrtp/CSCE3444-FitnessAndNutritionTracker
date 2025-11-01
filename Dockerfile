FROM python:3.13-trixie

RUN apt-get update
RUN apt-get upgrade
RUN pip install uv

COPY . .

RUN uv sync --no-dev
RUN uv run python3 ./initialize_db.py

ENTRYPOINT [ "uv", "run", "flask", "--app", "app",  "run", "--host=0.0.0.0"]
