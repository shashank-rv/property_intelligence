# Property Intelligence Explorer

Property Intelligence Explorer is an open-source web application that analyzes
any property listing or address and instantly generates a detailed **Property
Intelligence Card**. It aggregates multiple open data sources — including
zoning, flood risk, noise exposure, broadband availability, nearby council
development approvals, and local rental yields — to provide a comprehensive
snapshot of a property's risks and opportunities.

## 🚀 How it works

1. Users enter a property URL or address.
2. The system automatically geocodes the input and retrieves spatial layers
   from PostGIS.
3. Analytics evaluate contextual factors such as environmental risk,
   infrastructure access, and development activity.
4. An AI summary engine translates the raw data into clear, human-readable
   insights.

## 🔑 Key features

- 🔍 Analyze any property in seconds using open data.
- 🗺️ Interactive map with zoning, flood, and infrastructure layers.
- 🧠 AI-generated Property Intelligence Card summarizing risks & opportunities.
- 📊 Local market signals: rental yield, vacancy rate, nearby development
  approvals.
- 🧾 Export shareable PDF reports for investors or developers.
- 💬 Open-source stack, deployable on a single VM.

## 🛠️ Technology stack

- **Frontend:** Next.js, MapLibre GL JS
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL + PostGIS
- **Data processing:** GeoPandas, GDAL, DuckDB
- **AI summaries:** Ollama (Llama-3 or Mixtral)
- **Map tiles:** Tippecanoe + Tileserver-GL

## 🧭 Goal

Empower buyers, developers, and analysts with instant due-diligence insights —
no subscriptions, no paywalls, and no need to navigate multiple government
portals.
