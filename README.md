# zepto-data-AI-platform-capstone-project
End-to-end AI/ML platform for Zepto featuring data engineering pipelines, predictive analytics, and a grounded GenAI support assistant.

                              ZEPTO DATA AI PLATFORM

This repository contains three modules covering web scraping, data analysis, machine learning, RAG, API development, and Docker.

Project Modules Module 1 — Book Scraping & SQLite Database

This module scrapes book information from Books to Scrape, cleans the collected data, converts GBP prices to INR, stores the data in a SQLite database, and performs SQL and Pandas analysis.

Main tasks:

Web scraping using Requests and BeautifulSoup Extract book title, price, rating, availability, and category Data cleaning and transformation GBP to INR price conversion SQLite database creation SQL queries using JOIN, GROUP BY, COUNT, AVG, WHERE, ORDER BY, LIMIT, BETWEEN, and IN Compare SQL JOIN results with Pandas merge()

Main output:

zepto_catalog.db Module 2 — Titanic Survival Prediction

This module performs exploratory data analysis and builds machine learning models to predict Titanic passenger survival.

Main tasks:

Load and profile the Titanic dataset Handle missing values Detect outliers using IQR Perform univariate, bivariate, and multivariate analysis Create data visualizations Analyze correlations Train classification models Handle class imbalance using SMOTE Perform Random Forest hyperparameter tuning Predict fare using Linear Regression Export the final machine learning pipeline

Models used:

Logistic Regression Decision Tree Random Forest Linear Regression

Main output:

best_titanic_pipeline.joblib Module 3 — RAG Support Assistant API & Docker

This module builds a small RAG-based support assistant for Zepto policies.

The application uses document embeddings, ChromaDB for retrieval, LangGraph for workflow routing, Pydantic for structured responses, and FastAPI for the API.

Main tasks:

Load 8 Zepto policy documents Generate embeddings using all-MiniLM-L6-v2 Store embeddings in ChromaDB Classify user questions Retrieve relevant policy documents Generate structured responses Build a LangGraph workflow Create a FastAPI /ask endpoint Run the application locally Containerize the application using Docker.
