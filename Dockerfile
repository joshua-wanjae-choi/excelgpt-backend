FROM python:3.12.0

# Create User
RUN useradd -m -u 1001 excelgpt
USER excelgpt

WORKDIR /home/excelgpt/app
COPY . .

ENV PATH="/home/excelgpt/.local/bin:$PATH"

USER root

# Install mariadb client
RUN apt install wget apt-transport-https -y
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN echo "935944a2ab2b2a48a47f68711b43ad2d698c97f1c3a7d074b34058060c2ad21b  mariadb_repo_setup" \
       | sha256sum -c -
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup

RUN apt install mariadb-client -y


# Install dependencies
RUN apt-get update
RUN apt-get install libffi-dev -y
RUN apt-get install cmake -y
RUN pip install --upgrade pip

RUN cp -R /home/excelgpt/app/dependency /dependency

WORKDIR /dependency
RUN tar -xvzf mariadb-connector-c-3.3.5-src.tar.gz

WORKDIR /dependency/mariadb-connector-c-3.3.5-src
RUN cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local
RUN cmake --build . --config Release
RUN make install

WORKDIR /dependency
RUN tar -xvzf mariadb-connector-python-1.1.6.tar.gz

WORKDIR /dependency/mariadb-connector-python-1.1.6
RUN python -m pip install .

RUN cp /usr/local/lib/mariadb/libmariadb.so.3 /usr/local/lib/

RUN chown -R excelgpt:excelgpt /home/excelgpt


# Select User
USER excelgpt

# Install dependency
WORKDIR /home/excelgpt/app
RUN bash dependency_commands

# Run
WORKDIR /home/excelgpt/app/api

# # DEV Command
# CMD ["tail", "-f", "main.py"]

# # PRODUCT command
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000", "--lifespan", "on"]
