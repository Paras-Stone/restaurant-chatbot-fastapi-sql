# restaurant-chatbot-fastapi-sql
AI-powered restaurant chatbot using Dialogflow, FastAPI, and MySQL to handle orders, reservations, and menu queries.
This project features a conversational AI chatbot built for a restaurant, integrating Dialogflow for intent detection, FastAPI for backend logic, and MySQL for managing orders, reservations, and menu data.

restaurant-chatbot-fastapi-sql/
main.py               # FastAPI routes and app setup
db_helper.py          # MySQL connection and database functions
generic_helper.py     # Utility functions for intent handling
database/
 restaurant_db.sql # MySQL schema with sample data
 dialogflow_agent/
     # Exported Dialogflow agent files
The main logic is split across three Python modules: main.py (FastAPI app and webhook setup), db_helper.py (MySQL connection and queries), and generic_helper.py (intent routing and response formatting). The backend connects to a Dialogflow agent exported as a ZIP file, located in the dialogflow_agent/ folder, which includes predefined intents and entities like OrderFood and BookTable. The MySQL schema and sample data are available in the database/restaurant_db.sql file. To run the project, users must set up a local MySQL instance, import the schema, install dependencies (FastAPI, Uvicorn, mysql-connector-python), and start the server via uvicorn main:app --reload. The FastAPI docs are accessible at /docs, and the chatbot logic handles real-time webhook communication from Dialogflow to return dynamic, database-driven responses. This project demonstrates end-to-end integration of a conversational AI interface with a live backend and database, suitable for scalable restaurant automation systems.

## Database Setup

To load the database schema and sample data:

1. Ensure MySQL is installed and running.
2. Create a new database:
   ```sql
   CREATE DATABASE restaurant_db;


## 🤖 Dialogflow Agent

The `dialogflow_agent/` folder contains the exported Dialogflow ES agent used in this project.

To import it:

1. Open [Dialogflow Console](https://dialogflow.cloud.google.com/)
2. Go to **Settings ⚙️ → Export and Import**
3. Click **Restore from ZIP** and upload the `dialogflow-agent.zip` file

This will restore all intents, entities, and responses required for the chatbot to work.
