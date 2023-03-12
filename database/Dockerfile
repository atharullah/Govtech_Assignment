# Use the official postgres image as the parent image
FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword
ENV POSTGRES_DB mydb

# Copy the DDL scripts into the container
COPY create_tables.sql /docker-entrypoint-initdb.d/
