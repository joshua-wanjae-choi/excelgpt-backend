FROM python:3.12.0

RUN useradd -m -u 1001 excelgpt
USER excelgpt

ENV PATH="/home/excelgpt/.local/bin:$PATH"

WORKDIR /home/excelgpt/app
COPY . .

CMD ["tail", "-f", ".gitignore"]
