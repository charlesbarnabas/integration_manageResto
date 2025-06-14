#!/bin/bash

echo "🍽️ Integration ManageResto — Microservice Restaurant Management System"
echo "-----------------------------------------------------------------------"
echo ""
echo "This is a microservice-based restaurant management platform using Flask + GraphQL + Docker."
echo ""
echo "📦 Project Structure:"
echo "
integration_manageResto/
├── user_service/
├── menu_service/
├── inventory_service/
├── procurement_service/
├── transaction_service/
├── docker-compose.yml
└── README.md
"
echo ""
echo "🚀 Getting Started"
echo "------------------"

echo ""
echo "🐳 Option 1: Run with Docker"
echo "----------------------------"
echo "1. cd integration_manageResto"
echo "2. docker compose build && docker compose up -d"
echo "3. docker compose restart nginx (optional)"
echo ""
echo "🖥️ Option 2: Run Locally via Python Virtual Environment"
echo "--------------------------------------------------------"

SERVICES=(user_service menu_service inventory_service procurement_service transaction_service)

for SERVICE in "${SERVICES[@]}"; do
    echo ""
    echo "📦 Setting up: $SERVICE"
    cd "$SERVICE" || exit
    echo "Creating virtual environment for $SERVICE..."
    python -m venv venv
    source venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo "Running service..."
    python run.py &
    deactivate
    cd ..
done

echo ""
echo "✅ All services initialized in background"
echo ""
echo "🧪 Open browser and visit: http://localhost:5000 to register and login"
echo ""
echo "📡 API Endpoints:"
echo "-----------------"
echo "👤 User         : http://localhost:5000"
echo "📋 Menu         : http://localhost:5001"
echo "📦 Inventory    : http://localhost:5002"
echo "🛒 Procurement  : http://localhost:5003"
echo "💳 Transaction  : http://localhost:5004"
echo ""
echo "🎉 Done!"
