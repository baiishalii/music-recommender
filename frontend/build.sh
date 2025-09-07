#!/bin/bash

# Build the frontend
cd frontend
npm install
npm run build
cd ..

# Make sure the backend requirements are installed
pip install -r requirements.txt
