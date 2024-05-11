FROM python:latest

COPY requirements.dev.txt requirements.dev.txt
RUN pip install -r requirements.dev.txt

WORKDIR /install
COPY mongologger/ mongologger/
COPY pyproject.toml pyproject.toml
RUN pip install .

WORKDIR /
RUN rm -fr /install

WORKDIR /tests
COPY tests/ tests/

CMD ["python", "-m", "pytest"]
