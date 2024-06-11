# Origin image
FROM ubuntu:16.04

# update
RUN apt update

# Install necessary packages
RUN apt install -y \
    make \
    gcc \
    socat \
    passwd

# Add new user 'ctf' with password 'ctf'
RUN useradd -d /home/test/ -m -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

# Add new user 'test' with password 'test'
RUN useradd -m -s /bin/bash test
RUN echo "test:test" | chpasswd

# Change work directory
WORKDIR /home/test

# Setup the vulnerability environment
COPY sources .

# Compile binary
RUN make clean; make

# Change user
USER test

# Entry point
ENTRYPOINT socat tcp-l:8080,fork,reuseaddr exec:./pwn && /bin/bash
