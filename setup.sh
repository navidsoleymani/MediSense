#!/bin/bash

# --------------------------------------------------------------------
# setup.sh - Initial Setup Script for Django + Docker Environment
# --------------------------------------------------------------------
# This script:
# 1. Creates a .env file from SAMPLE_ENV.txt if it doesn't exist
# 2. Ensures entrypoint.sh is executable
# 3. Builds and starts the Docker containers using docker-compose
# --------------------------------------------------------------------

set -e  # Exit on any error

# Colors for pretty output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Ensure Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
  echo -e "${RED}❌ Docker is not installed! Please install Docker first.${NC}"
  exit 1
fi

if ! command -v docker-compose &> /dev/null; then
  echo -e "${RED}❌ Docker Compose is not installed! Please install Docker Compose first.${NC}"
  exit 1
fi

# Step 2: Generate .env file if missing
if [ ! -f ".env" ]; then
  echo -e "${GREEN}Creating .env file from SAMPLE_ENV.txt...${NC}"
  cp SAMPLE_ENV.txt .env
else
  echo -e "${GREEN}.env file already exists. Skipping copy.${NC}"
fi

# Step 3: Ensure entrypoint.sh is executable
if [ -f "entrypoint.sh" ]; then
  echo -e "${GREEN}Making entrypoint.sh executable...${NC}"
  chmod +x entrypoint.sh
else
  echo -e "${RED}❌ entrypoint.sh not found in project root!${NC}"
  exit 1
fi

# Optional Cleanup (uncomment to use)
echo -e "${GREEN}Cleaning up Docker system...${NC}"
docker-compose down --volumes --remove-orphans
docker system prune -f

# Step 4: Start Docker containers
echo -e "${GREEN}Starting Docker containers...${NC}"
docker-compose up --build
