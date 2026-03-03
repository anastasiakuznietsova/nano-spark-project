# Big Data Mining Project: Apache Spark Analysis

This project is a collaborative effort focused on processing and analyzing large-scale datasets using the **Apache Spark** framework.The project demonstrates skills in SQL queries for distributed data, Docker containerization, and team-based development using Git Flow.

## Team Roles & Responsibilities

Based on our internal team agreement, the following roles have been assigned for each technical phase.

### Phase 1: Preparation stage
* **Repository Management (Anastasiia Kuznietsova):** Setting up the Git repository and establishing the branch structure (Main/Develop).
* **Initial Configuration (Ania Savchuk):** Creating the foundational `.gitignore` and `README.md` files.
* **Reporting (Olena Novosad):** Initializing the project report and tracking development progress.
* **Data Sourcing (Anastasiia Zhmud):** Selecting and downloading the dataset to an external project folder.

### Phase 2: Environment Setup stage
* **Docker Configuration (Anastasiia Zhmud):** Creating the `Dockerfile` for the Spark environment setup.
* **Documentation Update (Olena Novosad):** Updating configuration files and technical documentation.
* **System Entry Point (Anastasiia Kuznietsova):** Developing the `main.py` file as the primary application entry point.
* **Verification (Ania Savchuk):** Testing the environment and documenting setup results.

### Phase 3: Extraction stage
* **Schema Design (Anastasiia Kuznietsova):** Defining explicit data schemas for the selected dataset.
* **Data Ingestion (Anastasiia Zhmud):** Implementing functions to read raw data into Spark DataFrames.
* **Data Validation (Ania Savchuk):** Verifying the accuracy and integrity of the ingestion process.
* **Module Development (Olena Novosad):** Organizing operations into a reusable Python module.

### Phase 4: Data Preprocessing stage
* **Statistical Analysis (Olena Novosad):** Generating descriptive statistics for numerical features.
* **Data Typing (Ania Savchuk):** Parsing and converting data into required formats.
* **Feature Engineering (Anastasiia Kuznietsova):** Analyzing and selecting informative features for the analytical models.
* **Data Cleaning (Anastasiia Zhmud):** Handling missing values, duplicates, and noise in the dataset.

### Phase 5: Data Preprocessing stage
* Each member implements 6 unique business questions using filter, join, group by, and window functions

### Phase 6: Recording results stage
* All members participate in exporting their query results into .csv files.

### Phase 7: Presentation stage
* As a team, we provide a holistic demonstration of the data processing pipeline and showcase the specific contribution of each member to the project's success.

---

## Tech Stack
* **Framework:** Apache Spark (PySpark).
* **Database:** Spark SQL.
* **Containerization:** Docker.
* **Version Control:** Git.


---

## PySpark Installation & Setup Guide

To ensure the project runs smoothly without version conflicts, we use **Java 17** and **Python 3.11** as the most stable combination for PySpark.

### 1. Environment Configuration (Conda)
Run these commands in your terminal to create a clean, isolated environment:

```bash
# Create a new environment with Python 3.11 to avoid 3.12 bugs
conda create -n spark_env python=3.11 -y

# Activate the environment
conda activate spark_env

# Install PySpark
pip install pyspark

# Install compatible Java 17 (overrides problematic system Java versions)
conda install -c conda-forge openjdk=17 -y
```

### 2. PyCharm Interpreter Setup
To make the **Run (▶︎)** button work correctly, link PyCharm to your new environment:

* In PyCharm, click on the **Python version** in the bottom right corner.
* Select **Add New Interpreter** -> **Add Local Interpreter**.
* Choose **Conda Environment** on the left.
* If it asks for the **Conda executable path**, point it to: **D:\anaconda\Scripts\conda.exe** (or **condabin\conda.bat**).
* Click **Load Environments**, select **spark_env** from the list, and hit **OK**.

---

### 3. Windows Compatibility (Hadoop)

### Why do we need this?
Apache Spark was originally built for Linux. On Windows, it needs **"translators"** (**winutils.exe** and **hadoop.dll**) to translate Linux-style requests into Windows-friendly commands. Without these, the code will crash during I/O operations.

### Configuration Steps:
* **Download binaries:** Download **hadoop.dll** and **winutils.exe** from the trusted repository (https://github.com/kontext-tech/winutils/blob/ff8e529a72bde2ec95b06ab76e797bdcbade9685/hadoop-3.4.0-win10-x64/bin/hadoop.dll
https://github.com/kontext-tech/winutils/blob/ff8e529a72bde2ec95b06ab76e797bdcbade9685/hadoop-3.4.0-win10-x64/bin/winutils.exe).
* **File Placement:** Create the directory **C:\hadoop\bin** and move both downloaded files into the bin folder.
* **System Environment Variables:** Add **C:\hadoop\bin** to your **System Path**.

> **IMPORTANT:** DO NOT download the standalone Spark application. We use the version installed via **pip**.

---

### 4. Running the Project
Once the environment is active and Hadoop binaries are in place:

* Open **main.py**.
* Ensure **spark_env** is selected as the interpreter in PyCharm.
* Click the **Run** button.


---

## Docker Installation & Usage

This project is configured to run within a Docker container to ensure a consistent environment (Python, Spark, Java) across all machines.

### 1. Preparation
* **Download Docker:** Install Docker Desktop from the official site: **https://docs.docker.com/get-docker/**
* **Launch:** After installation, run Docker Desktop and wait until the status says **Docker is running**.
* **Verification:** Open your terminal and run the following commands to check the setup:

```bash
docker --version
docker run hello-world
```

* If you see the message **"Hello from Docker!"**, you are ready to go.

### 2. Local Check
> **IMPORTANT:** First, ensure the project runs locally without Docker. If it doesn't work locally, it won't work in a container!

### 3. Build Docker Image (One-time setup)
To create your Spark environment inside Docker, run this command in the project root:

```bash
docker build -t my-spark-img .
```

*Note: The first build may take 5–15 minutes as Docker downloads Linux and Spark dependencies.*

### 4. Running the Program
To execute the analysis, use the following command:

```bash
docker run --rm my-spark-img
```

When you run this, the system will automatically:
* Initialize the Spark session.
* Execute the **main.py** script.
* Display the analytical results directly in your console.
* Clean up the container after execution (thanks to the **--rm** flag).