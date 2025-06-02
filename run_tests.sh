#!/bin/bash

# Run Python tests
echo "Running Python tests..."
python -m pytest coding_agent/tests/ -v

# Run React tests
echo "Running React tests..."
cd coding_agent/ui/react_app
npm test -- --watchAll=false
cd ../../..

echo "All tests completed."