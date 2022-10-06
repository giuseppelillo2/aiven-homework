#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing packages...${NC}"
pip install -e .
echo -e "${BLUE}Running migrations...${NC}"
dbmate up
echo -e "${BLUE}Starting application...${NC}"
python -m aiven.main "$1"