# run.sh

# Start the backend
echo "Starting backend..."
uvicorn coding_agent.api.routes:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start the frontend
echo "Starting frontend..."
cd coding_agent/ui/react_app
npm start &
FRONTEND_PID=$!

# Wait for both processes to finish
wait $BACKEND_PID
wait $FRONTEND_PID