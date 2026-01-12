# v.1
## Use the official Python runtime image
#FROM python:3.13-slim
#
## Set the working directory inside the container
#WORKDIR /app/www/cozyshop
#
## Create Group and User
#RUN groupadd -r groupdj && \
#    useradd -r -g groupdj userdj
#
## Set environment variables
## Prevents Python from writing pyc files to disk
#ENV PYTHONDONTWRITEBYTECODE=1
##Prevents Python from buffering stdout and stderr
#ENV PYTHONUNBUFFERED=1
#
## Upgrade pip
#RUN pip install --upgrade pip
#
## Copy the Django project  and install dependencies
#COPY requirements.txt .
#
## run this command to install all dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the Django project to the container
#COPY . .
#
#USER userdj

# v. 2
# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Set the working directory
WORKDIR /app/www/cozyshop

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app/www/cozyshop

# Create Group and User
RUN groupadd -r groupdj && \
    useradd -r -g groupdj userdj && \
    chown -R userdj:groupdj . && \
    chown -R userdj:groupdj /usr/local/lib/python3.13/site-packages/

# Copy application code
COPY --chown=userdj:userdj . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy entrypoint.sh to a system path NOT overridden by the volume mount
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Fix Windows line endings (CRLF) and ensure execution permissions
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER userdj

# Set the new path as the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]