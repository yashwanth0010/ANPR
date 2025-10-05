# A tiny test image to verify Jenkins → DockerHub push
FROM alpine:latest

# Add a simple test file
RUN echo "Hello from Jenkins CI/CD pipeline!" > /hello.txt

# Default command
CMD cat /hello.txt
