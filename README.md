<!-- markdownlint-disable MD033 MD013 MD022 -->
<h1 align="center"><img src="https://raw.githubusercontent.com/yyoel/yyoel/main/asset/gif/wave.gif" width="30px"> Hi, I'm Yulius!</h1>
<h3 align="center">Data Engineer | ETL, CDC &amp; Big Data Pipelines | Python, SQL, PySpark | Financial Services</h3>

<p align="center">
  <a href="https://www.linkedin.com/in/yulius-yoel/" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
  <a href="mailto:yoelyulius@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  <a href="https://twitter.com/yyoel97" target="_blank"><img alt="Twitter" src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" /></a>
</p>

<p align="center"><i>I move data from "where it lives" to "where it's useful", and try to keep it correct on the way. 🚚📊</i></p>

## 👋 About

Data engineer working in financial services (insurance, fintech and multi-finance). I build ETL/ELT and Change Data Capture (CDC) pipelines, tune Spark workloads, and turn raw enterprise data into datasets for analytics and reporting.

- 🏢 Currently a Data Engineer at **Manulife Indonesia**
- 📍 Jakarta, Indonesia
- 💼 Open to Data Engineer and ETL Developer roles
- 🎓 Studying Information Systems at Universitas Terbuka
- 🌱 Learning: DataOps, data quality automation and modern data engineering tooling

## 💼 Experience

| Period | Role | Company |
| --- | --- | --- |
| Jan 2024 – Present | Data Engineer | Manulife Indonesia |
| Jan 2023 – Dec 2023 | ETL Developer | Prudential Indonesia |
| Sep 2022 – Nov 2022 | Senior Data Engineer | KoinWorks |
| Jun 2022 – Jul 2022 | Data Engineer (freelance) | Datawan.io |
| Apr 2020 – Aug 2022 | Data Engineer → Big Data Engineer → Data Innovation Engineer | BFI Finance Indonesia |
| Sep 2017 – Mar 2020 | Backend Developer → DevOps Engineer | Andal Software |

## 🧭 How my pipelines flow

```text
 Oracle / APIs / files
        │  CDC · event-driven ingestion
        ▼
 Azure Data Factory ──▶ ADLS + Delta (Unity Catalog)
                              │  PySpark · validation
                              ▼
                  CosmosDB APIs · BI dashboards
```

## 🔧 What I work on

- **Ingestion on Azure:** Azure Data Factory pipelines that load 20+ Oracle source tables into ADLS with event-driven triggers, registered in Databricks Unity Catalog as external tables
- **Change Data Capture:** CDC pipelines (Debezium) that land change data in Delta managed tables in Unity Catalog for near real-time analytics
- **Serving layer:** 12+ Azure CosmosDB containers designed for low-latency access by downstream APIs
- **Data quality:** automated validation in Azure Databricks to keep Oracle and CosmosDB data consistent
- **Analytics products:** co-developed an agent performance monitoring application (achievements, policy submissions, claims, potential APE and commissions)
- **Spark performance:** PySpark partitioning, broadcast joins, and cluster/executor tuning
- **Earlier work:** web scraping and ML model REST APIs with Docker at BFI Finance; CI/CD for 20+ applications in Azure DevOps at Andal Software

## 💬 Ask me about

- 🔄 CDC with Debezium and Delta tables
- ⚡ Making slow Spark jobs fast (partitioning, broadcast joins, OOM hunting)
- 🧱 Ingesting Oracle into the Azure lake, the event-driven way
- 🧹 Catching bad data before it reaches a dashboard

## 🛠 Tech Stack

<p align="center">
  <img alt="Azure" src="https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoftazure&logoColor=white" />
  <img alt="Databricks" src="https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white" />
  <img alt="Apache Spark" src="https://img.shields.io/badge/PySpark-E25A1C?style=flat&logo=apachespark&logoColor=white" />
  <img alt="Hadoop" src="https://img.shields.io/badge/Hadoop-66CCFF?style=flat&logo=apachehadoop&logoColor=black" />
  <img alt="Debezium" src="https://img.shields.io/badge/Debezium-FF6A00?style=flat&logo=debezium&logoColor=white" />
  <img alt="Hive" src="https://img.shields.io/badge/Hive-FDEE21?style=flat&logo=apachehive&logoColor=black" />
  <img alt="Airflow" src="https://img.shields.io/badge/Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white" />
  <img alt="Alibaba Cloud" src="https://img.shields.io/badge/Alibaba_Cloud-FF6A00?style=flat&logo=alibabacloud&logoColor=white" />
  <img alt="GCP" src="https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
  <img alt="SQL" src="https://img.shields.io/badge/SQL-4479A1?style=flat&logo=postgresql&logoColor=white" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" />
  <img alt="Oracle" src="https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white" />
  <img alt="MSSQL" src="https://img.shields.io/badge/MSSQL-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white" />
  <img alt="CosmosDB" src="https://img.shields.io/badge/CosmosDB-0078D4?style=flat&logo=microsoftazure&logoColor=white" />
  <img alt="Bash" src="https://img.shields.io/badge/Bash-4EAA25?style=flat&logo=gnubash&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" />
  <img alt="Kubernetes" src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white" />
  <img alt="Azure DevOps" src="https://img.shields.io/badge/Azure_DevOps-0078D7?style=flat&logo=azuredevops&logoColor=white" />
  <img alt="Git" src="https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white" />
  <img alt="Linux" src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" />
  <img alt="VS Code" src="https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white" />
  <img alt="PyCharm" src="https://img.shields.io/badge/PyCharm-000000?style=flat&logo=pycharm&logoColor=white" />
</p>

## 📜 Certifications

- Google Data Analytics: Coursera (2022)
- Alibaba Cloud Associate, Cloud Computing: Alibaba Cloud (2021, expired 2023)
- Python and SQL courses: Progate (2021)

## 🚀 Fresh from the workshop

<!--START_PROJECTS-->
| Project | What it is | Stack | Last push |
| --- | --- | --- | --- |
| [**ulauncher-pomodoro**](https://github.com/yyoel/ulauncher-pomodoro) | A full-featured Pomodoro timer extension for Ulauncher with focus and break cycles, desktop notifications, and audio alerts. | Python | 2026-08-21 |
<!--END_PROJECTS-->

## 🤝 Let's connect

Always happy to talk data engineering, pipelines or Spark war stories. Reach me on [LinkedIn](https://www.linkedin.com/in/yulius-yoel/) or [email](mailto:yoelyulius@gmail.com).

<!-- markdownlint-enable MD033 MD013 MD022 -->
<!--
Badges: https://shields.io
-->
