#!/bin/bash

# Database Migration Script for Urban Copilot
# This script helps migrate data from local PostgreSQL to Azure PostgreSQL

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Azure PostgreSQL connection details
AZURE_DB_HOST="your-azure-postgres-server.postgres.database.azure.com"
AZURE_DB_USER="$DB_USER@your-azure-postgres-server"
AZURE_DB_PASSWORD="$DB_PASSWORD"  # Should be your secure production password

# Backup local database
echo "Creating backup of local database..."
PGPASSWORD=$DB_PASSWORD pg_dump -U $DB_USER -h db -p $DB_PORT $DB_NAME > urban_copilot_backup.sql

if [ $? -ne 0 ]; then
    echo "Error: Database backup failed!"
    exit 1
fi

echo "Local database backup created successfully: urban_copilot_backup.sql"

# Restore to Azure PostgreSQL
echo "Would you like to restore the database to Azure PostgreSQL? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Restoring database to Azure PostgreSQL..."
    PGPASSWORD=$AZURE_DB_PASSWORD psql -U $AZURE_DB_USER -h $AZURE_DB_HOST -p $DB_PORT $DB_NAME < urban_copilot_backup.sql
    
    if [ $? -ne 0 ]; then
        echo "Error: Database restore to Azure failed!"
        exit 1
    fi
    
    echo "Database successfully migrated to Azure PostgreSQL!"
else
    echo "Skipping database restore to Azure. You can manually import the backup later."
fi

echo "Database migration process completed!"
