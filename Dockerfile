FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

COPY . .

COPY justfile .

# create ~/bin
RUN mkdir -p /root/bin

# download and extract just to ~/bin/just
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /root/bin

# add `/root/bin` to the paths that your shell searches for executables
ENV PATH="/root/bin:${PATH}"

# just should now be executable
RUN just --help

EXPOSE 8000


CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000 & python manage.py run_bot"]
