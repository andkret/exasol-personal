# High-Performance Data Analysis with Exasol

Learn how to run machine learning and AI directly inside [Exasol](https://www.exasol.com/personal/), the massively parallel processing (MPP) analytical database, keeping your data and compute on your own infrastructure instead of external cloud ML platforms. This hands-on lab covers MPP architecture, deploying Exasol on AWS, query optimization with distribution and partition keys, running Python scripts directly in the database with UDFs, in-database scikit-learn and Hugging Face models, and building a conversational interface with the Model Context Protocol (MCP) and local LLMs.

Built for data engineers, data scientists, and AI engineers. No prior Exasol experience required.

👉 **Take the free course:** [High-Performance Data Analysis with Exasol](https://learndataengineering.com/p/high-performance-data-analysis-with-exasol)

## Lessons

| # | Lesson | Description |
|---|--------|-------------|
| 1.1 | [MPP Basics and Exasol](Lessons/1_1-MPP-basics-and-exasol.md) | MPP data store fundamentals, horizontal scaling, and Exasol use cases |
| 1.2 | [Installation Steps](Lessons/1_2-installation-steps.md) | Setting up AWS IAM, CLI, and installing Exasol Personal on EC2 |
| 1.3 | [Getting to Know Exasol](Lessons/1_3-getting-to-know-exasol.md) | Connecting via DbVisualizer, the Admin UI, and importing data |
| 2.1 | [How Exasol Achieves Performance](Lessons/2_1-how-Exasol-achieves-performamce.md) | Distribution keys, partition keys, indexes, joins and query best practices |
| 2.2 | [Query Optimization](Lessons/2_2-Querying-optimization.md) | TPC-H dataset setup, distribution key demo with bad vs good distribution |
| 2.3 | [Use a UDF](Lessons/2_3-use-a-udf.md) | Creating and running a Python UDF to query a stock symbol API |
| 3.1 | [AI Lab](Lessons/3_1-ai-lab.md) | Exasol AI Lab with Hugging Face integration |
| 3.2 | [Credit Back Payments Prediction](Lessons/3_2-credit_back_payments_prediction.ipynb) | Notebook predicting credit back payments |
| 3.3 | [Text Classification](Lessons/3_3-text_classification-3.ipynb) | Notebook for text classification |
| 4.1 | [MCP Use Case](Lessons/4_1-mcp-use-case.md) | MCP process overview |
