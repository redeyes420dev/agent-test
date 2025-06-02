#!/bin/bash

# Run Python tests
echo "Running Python tests..."
pytest coding_agent/tests

# Run React tests
echo "Running React tests..."
cd coding_agent/ui/react_app
npm test