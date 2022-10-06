#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Building image...${NC}"
docker build --target testing -t aiven-test:latest .
echo -e "${BLUE}Running migrations...${NC}"
docker run -v $(pwd)/db:/db --env-file tests/.env amacneil/dbmate up
echo -e "${BLUE}Starting application...${NC}"
docker run --env-file tests/.env aiven-test