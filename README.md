# Property Intelligence (Australia Liveability)

An engaging Australia-first address intelligence app inspired by realestate-style exploration.

## What this app now includes
- Address assessment for Australian locations
- Three liveability dimensions: Social, Environment, Economy
- Interactive dimension tabs with metric score bars
- Market signals panel (median price, monthly/annual trend, rental yield)
- Nearby amenities snapshot (schools, transport, health, lifestyle)
- Key highlights summary for quick decision-making

## Stack
- Frontend: React + Vite
- Backend: Python + Flask

## Run locally

### 1) Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Backend: `http://localhost:5000`

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend: `http://localhost:5173`

## API
- `GET /api/health`
- `POST /api/assess`

Example request:
```json
{ "address": "11 Collins St, Melbourne VIC 3000, Australia" }
```

Example response includes:
- `overallScore`
- `cityContext`
- `assessmentTypes`
- `dimensions` (with metric-level scores)
- `marketSignals`
- `nearby`
- `highlights`

## Next recommended upgrade
Integrate real Australian open data (ABS, transport GTFS feeds, school performance, healthcare accessibility, crime and climate risk layers) and replace deterministic mock values with computed geospatial scoring.
