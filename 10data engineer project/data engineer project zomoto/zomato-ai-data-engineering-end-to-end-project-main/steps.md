This end-to-end AI data engineering project follows a structured pipeline to process *Zomato* food delivery data. Here are the step-by-step phases:

1. **Data Ingestion (16:42 - 1:00:34):** The raw dataset is loaded from local storage into an *Amazon S3* bucket. Afterward, a *Snowflake* database is configured with secure storage integration to connect and ingest this raw data.

2. **Data Modeling with dbt (1:11:17 - 2:10:21):** Using *dbt*, the data is transformed through the **Medallion Architecture**:
   * **Staging Layer:** Initial cleaning of raw data.
   * **Gold Layer:** Creation of fact tables, dimension tables, and data marts for business analytics.
   * **Quality Assurance:** Implementation of dbt tests and documentation to ensure data lineage and integrity.

3. **Orchestration (2:10:21 - 2:28:14):** *Apache Airflow* is used to manage the automated scheduling and execution of the entire data pipeline.

4. **AI/LLM Integration (2:59:36 - 4:16:48):** Three distinct AI layers are implemented using *OpenAI* and *Streamlit*:
   * **LLM Enrichment:** Using GPT-4o-mini to classify sentiment, extract topics, and identify key issues from customer reviews.
   * **RAG (Retrieval-Augmented Generation):** A chatbot interface allowing users to query and chat with the enriched review data using vector embeddings.
   * **Text-to-SQL:** A mechanism that converts natural language questions into SQL queries to chat directly with the data warehouse.

5. **Final Orchestration (4:16:48 - 4:25:03):** The final step involves integrating these AI processes into the main Airflow DAG to ensure the full pipeline runs automatically.