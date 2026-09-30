#!/usr/bin/env bash
echo "========================================================"
echo "  ATELIER TERRA - Artisanal Ceramics & Cozy Home Living"
echo "========================================================"
echo ""

echo "[1/3] Checking dependencies..."
pip install -r requirements.txt

echo ""
echo "[2/3] Applying migrations and verifying seed data..."
python3 manage.py migrate
python3 manage.py seed_shop

echo ""
echo "[3/3] Starting Atelier Terra Development Server..."
echo "Server running at: http://127.0.0.1:8000/"
echo "Admin portal:     http://127.0.0.1:8000/admin/"
echo "(Press CTRL+C to stop the server)"
echo ""
python3 manage.py runserver
