FROM python:3.12.0

WORKDIR /home/excelgpt/app

# Create User
RUN useradd -m -u 1001 excelgpt
USER excelgpt

COPY . .

ENV PATH="/home/excelgpt/.local/bin:$PATH"

USER root

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
WORKDIR /home/excelgpt/app

# Command
CMD ["tail", "-f", ".gitignore"]
