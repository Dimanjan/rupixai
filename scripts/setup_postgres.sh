#!/bin/bash

# RupixAI PostgreSQL Setup Script
# This script sets up PostgreSQL database for RupixAI

set -e

echo "🚀 Setting up PostgreSQL for RupixAI..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL is not installed. Please install PostgreSQL first."
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -q; then
    print_warning "PostgreSQL is not running. Starting PostgreSQL..."
    if command -v brew &> /dev/null; then
        brew services start postgresql@14
    else
        print_error "Please start PostgreSQL manually."
        exit 1
    fi
fi

# Database configuration
DB_NAME="rupixai_db"
DB_USER="rupixai_user"
DB_PASSWORD="rupixai_password"

print_status "Creating database and user..."

# Create database
if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    print_warning "Database $DB_NAME already exists."
else
    createdb $DB_NAME
    print_status "Database $DB_NAME created."
fi

# Create user
if psql -d $DB_NAME -c "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    print_warning "User $DB_USER already exists."
else
    psql -d $DB_NAME -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    print_status "User $DB_USER created."
fi

# Grant privileges
psql -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
psql -d $DB_NAME -c "ALTER USER $DB_USER CREATEDB;"
print_status "Privileges granted to $DB_USER."

print_status "PostgreSQL setup completed successfully!"
print_status "Database: $DB_NAME"
print_status "User: $DB_USER"
print_status "Host: localhost"
print_status "Port: 5432"

echo ""
print_status "Next steps:"
echo "1. Update your .env file with actual API keys"
echo "2. Run: python manage.py migrate"
echo "3. Run: python manage.py runserver"
echo "4. Create a superuser: python manage.py createsuperuser"
