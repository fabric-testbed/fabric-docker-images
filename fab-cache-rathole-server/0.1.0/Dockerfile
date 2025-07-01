# Use an official Ubuntu base image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /workspace

# Install dependencies: wget and unzip
RUN apt update && apt install -y wget unzip

# Download and install Rathole (Linux x86_64, glibc-based)
RUN wget https://github.com/rathole-org/rathole/releases/download/v0.5.0/rathole-x86_64-unknown-linux-gnu.zip \
    && unzip rathole-x86_64-unknown-linux-gnu.zip \
    && chmod +x rathole \
    && rm rathole-x86_64-unknown-linux-gnu.zip

# Copy your config file into the container
COPY server.toml /workspace/

# Run Rathole with the config when container starts
CMD ["./rathole", "server.toml"]