#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building image...${NC}"
docker build --target base -t aiven:latest .
echo -e "${BLUE}Running migrations...${NC}"
docker run -v $(pwd)/db:/db --env-file .env amacneil/dbmate up
echo -e "${BLUE}Starting application...${NC}"
docker run --env-file .env aiven "$1"