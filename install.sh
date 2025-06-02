#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd coding_agent/ui/react_app
npm install