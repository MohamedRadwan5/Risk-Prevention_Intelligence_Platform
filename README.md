 <div align="center">

# 🌍 Global Diabetes — Risk & Prevention Intelligence Platform

### 🩺 Diabetes Risk & Prevention Intelligence System

**A Data Intelligence Platform for Understanding Diabetes Trends Worldwide and in Egypt**

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)

<br/>

**📊 Data Analysis | 🤖 Machine Learning | 🏥 Healthcare Analytics | 📈 Business Intelligence**

</div>

---

## 👥 Team Members

| Role | Name |
|:---:|:---|
| 👑 Team Leader | Mohammed Saber Salama Radwan |
| 👨‍💻 Team Member | Ziad Amr Abdelmageed |
| 👨‍💻 Team Member | Elsayed Ibrahem Elbdwy |
| 👨‍💻 Team Member | Islam Mohammed Hassan |
| 👨‍💻 Team Member | Ali Ahmed AbdelAziz |

### 🎓 Instructor

**Dr. Amal Mahmoud**

---

## 📌 Project Overview

The **Diabetes Risk & Prevention Intelligence System** is a data analysis platform that studies how diabetes has spread across more than **200 countries from 1990 to 2025**, and what drives the differences between them.

The project links diabetes prevalence and treatment coverage with obesity, diet composition, income, health spending, and population ageing, then uses global patterns as a benchmark for Egypt.

Using **Python and SQL**, the team will clean, validate, and organize multi-source historical data, analyze trends and risk factors, and build statistical and machine learning models to explore future scenarios.

The results will be presented through interactive **Power BI and Tableau dashboards** and a research report.

> 🎯 **Project Mission:** Support public health analysis and prevention planning through data-driven insights.

*Country-level findings describe populations, not individual patients, and the project distinguishes correlation from causation throughout.*

---

## ❓ Research Questions

### 🔍 Main Research Question

**Where should Egypt focus its diabetes prevention and diagnosis resources (early screening, food policy, specific age groups) to prevent the largest number of cases at the lowest cost?**

### 📊 Supporting Questions

| Category | Research Question |
|:---|:---|
| 🌍 Scale | How have diabetes prevalence and the number of people with diabetes changed in each country since 1990, and which countries are rising fastest? |
| 👥 Who Is Affected? | Which age groups and which sex carry the highest burden, and is diabetes appearing at younger ages? |
| 🇪🇬 Egypt | Where does Egypt rank globally and within the Middle East and North Africa? |
| 💊 Treatment Gap | What share of people with diabetes are not receiving treatment, and how does this gap relate to income and health spending? |
| ⚖️ Risk Factors | How strongly is diabetes associated with obesity, income, urbanization, and population ageing? |
| 🍎 Diet | Do countries whose diets rely more on sugar, refined starches, and processed foods have higher diabetes prevalence, after controlling for income, age, and obesity? Do changes in diet precede changes in diabetes by 5–10 years? |
| 🏥 Health Spending | Does higher health spending reduce prevalence or deaths, or does it mainly treat cases after they appear? |
| 🔮 Future Outlook | How have diabetes deaths changed, and what could prevalence look like over the next 10–20 years? |

---

## 🎯 Project Objectives

- 📥 Collect, merge, and document diabetes, risk-factor, diet, and socioeconomic data for 200+ countries from 1990 to 2025, keeping the source of every indicator.
- 🌍 Explore global and regional trends, age and sex patterns, the treatment gap, and Egypt’s position relative to other countries.
- 📊 Measure the relationship between diabetes and obesity, diet composition, income, and health spending using correlation and regression analysis, with clear limits on causal claims.
- 🤖 Develop and compare baseline and machine learning models to explain and project diabetes prevalence, evaluated with chronological testing and metrics such as MAE and RMSE.
- 📈 Communicate findings, priorities for Egypt, data limitations, and uncertainty through interactive dashboards and a documented research report.

---

## 🧭 Project Scope & Methodology

### 1️⃣ 📥 Data Acquisition

Gather country-year data on:

- Diabetes prevalence and treatment coverage (by age and sex).
- Diabetes deaths.
- Obesity and BMI.
- Blood pressure.
- Tobacco and alcohol use.
- Food supply by food group.
- Economic and health-system indicators.

### 2️⃣ 🗄️ Data Engineering & Database

- Standardize country codes, years, and units.
- Handle missing values and duplicates.
- Ensure that compared figures measure the same age group, definition, and period.
- Store processed data in SQL/PostgreSQL using related tables:
  - Prevalence
  - Health Indicators
  - Economic Indicators
  - Projections

### 3️⃣ 📊 Exploratory & Risk-Factor Analysis

- Examine trends since 1990.
- Identify the fastest-rising countries.
- Analyze age and sex patterns.
- Evaluate the treatment gap.
- Investigate Egypt's global ranking.
- Study relationships between diabetes and obesity, diet, income, and health spending.
- Distinguish correlation from causation.

### 4️⃣ 🤖 Modeling & Scenarios

- Create features such as growth rates, lagged diet indicators, and rolling averages.
- Establish baseline models.
- Compare regression, Random Forest, or gradient-boosting approaches where supported by the data.
- Evaluate models through chronological out-of-sample testing.

### 5️⃣ 📈 Business Intelligence & Reporting

Build interactive dashboards using:

- **Power BI**
- **Tableau**

Dashboards will cover global trends, Egypt's profile, risk factors, diet, treatment gaps, and model results, with findings and technical decisions documented.

---

## 🗂️ Data Sources

| Data Source | Dataset / Indicators | Coverage |
|:---|:---|:---:|
| 🔬 NCD-RisC (Lancet 2024) | Diabetes prevalence and treatment coverage by country, sex, and age group | 200 countries, 1990–2022 |
| 🩺 IDF Diabetes Atlas (via World Bank) | Diabetes prevalence, adults aged 20–79 | 2000, 2011, 2021, 2024 |
| 🌐 WHO Global Health Estimates | Diabetes deaths and death rates | 2000–2021 |
| ⚖️ WHO / NCD-RisC | Obesity, overweight, mean BMI, hypertension | 1990–2024 |
| 🍎 FAO Food Balance Sheets | Daily calories by food group (sugar, cereals, oils, meat, etc.), carbohydrates, fat, protein | 1990–2023 |
| 💰 World Bank WDI | Population, ageing, urbanization, GDP per capita, health spending, physicians | 1990–2025 |

### 📦 Prepared Dataset

The project includes the following prepared datasets:

| Dataset | Size |
|:---|---:|
| Country-Year Dataset | ~8,000 rows × 93 indicators |
| Age & Sex Dataset | ~198,000 rows |
| Long-Format Dataset | ~517,000 rows |

**Data Readiness:** Prepared datasets are ready for SQL integration and Power BI analysis.

### ⚠️ Known Data Gaps & Limitations

- Detailed diabetes prevalence data ends in 2022.
- Country-level undiagnosed rates are not available as open data.
- The share of people with diabetes not receiving treatment is used as a proxy for the treatment gap, not as a direct measure of undiagnosed cases.
- Physical activity data is still to be added.

---

## 📦 Final Deliverables

The project will deliver a documented public health intelligence platform containing:

| Deliverable | Description |
|:---|:---|
| 🐍 Python Data Workflow | Reproducible data cleaning, validation, integration, and analysis pipeline. |
| 🗄️ SQL Database | Structured and organized database for diabetes and related indicators. |
| 📊 Statistical Analysis | Evidence-based analysis of diabetes trends and risk factors, including diet. |
| 🤖 Predictive Models | Baseline and machine learning models for diabetes prevalence projection. |
| 📈 Interactive Dashboards | Power BI and Tableau dashboards for global and Egypt-focused insights. |
| 📄 Research Report | Findings, prevention priorities for Egypt, methodology, and limitations. |
| 📚 Technical Documentation | Data dictionary, data sources, processing decisions, and model evaluation. |

> **Expected Outcome:** An evidence-based platform that transforms global health data into actionable insights for diabetes prevention and public health planning in Egypt.

---

## 🗓️ Project Timeline — 5 Weeks

### 🔹 Week 1 — Research, Data Sources & Project Setup

- Finalize research questions.
- Review the methods behind each data source (age groups, definitions, estimation models).
- Assess data coverage and limitations.
- Set up the Python environment and project structure.
- Create an inventory of collected files.

### 🔹 Week 2 — Data Cleaning, Database & Exploratory Analysis

- Validate and clean the merged data.
- Document every indicator in the data dictionary.
- Load structured tables into SQL/PostgreSQL.
- Perform exploratory analysis of:
  - Global diabetes trends.
  - Age and sex patterns.
  - Treatment gaps.
  - Egypt's ranking.
  - Data gaps.

### 🔹 Week 3 — Risk-Factor Analysis & Feature Engineering

- Analyze the relationship between diabetes and obesity, diet composition, income, and health spending.
- Apply correlation and regression with appropriate controls.
- Create features such as:
  - Lagged diet indicators.
  - Growth rates.
  - Rolling statistics.
- Avoid information leakage from future periods.

### 🔹 Week 4 — Modeling, Comparison & Interpretation

- Build baseline and machine learning models.
- Compare models using chronological training and testing periods.
- Evaluate performance using MAE and RMSE.
- Interpret important factors.
- Test the robustness of results.
- Translate findings into prevention priorities for Egypt.

### 🔹 Week 5 — Dashboards, Reporting & Final Presentation

- Build and refine Power BI and Tableau dashboards.
- Cover global trends, Egypt, risk factors, diet, treatment gaps, and model performance.
- Complete the research report.
- Finalize technical documentation.
- Prepare the final presentation.
- Clearly communicate findings, uncertainty, and limitations.

---

<div align="center">

## 🌍 Turning Data Into Better Health Decisions

**Global Insights. Local Impact. A Healthier Future.**

<br/>

🩺 Healthcare Analytics • 📊 Data Intelligence • 🤖 Predictive Modeling

**Made with ❤️ by the Diabetes Risk & Prevention Intelligence Team**

</div>
