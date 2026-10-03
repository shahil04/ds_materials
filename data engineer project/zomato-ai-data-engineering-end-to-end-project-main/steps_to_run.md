The **Business Problem & Architecture** section (3:25 - 11:09) establishes the foundation for the entire project by defining the business case and the technical roadmap.

### Business Problem
The core scenario involves a food delivery application similar to *Zomato*, *Uber Eats*, or *DoorDash*. A client requires a data pipeline to manage food delivery operations. Due to the high demand for AI capabilities, the project scope was expanded beyond simple data analytics to include an **AI-driven data pipeline** that supports advanced features like sentiment analysis on reviews and natural language querying of the data warehouse.

### Project Architecture
The architecture utilizes modern data engineering tools to process and serve data efficiently:
* **Data Sources:** Raw food delivery data (orders, users, restaurants).
* **Storage:** Data is ingested into *Amazon S3*.
* **Warehouse:** Data is loaded from *S3* into *Snowflake* for cloud data warehousing.
* **Transformation:** *dbt* (data build tool) is used to implement the **Medallion Architecture** (Bronze/Silver/Gold layers), ensuring data quality and organization.
* **Orchestration:** *Apache Airflow* automates and manages the entire pipeline workflow.
* **AI Layer:** Integration with *OpenAI* to provide:
    * **LLM Enrichment:** Analyzing review sentiments and topics.
    * **RAG (Retrieval-Augmented Generation):** Chatting with customer reviews.
    * **Text-to-SQL:** Querying the data warehouse using natural language.

This approach ensures that the pipeline is not just a standard batch processor but a modern, AI-integrated system capable of answering complex business questions.


