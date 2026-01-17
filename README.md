<p align="center">
  <img src="https://www.especial.gr/wp-content/uploads/2019/03/panepisthmio-dut-attikhs.png" alt="UNIWA" width="150"/>
</p>

<p align="center">
  <strong>UNIVERSITY OF WEST ATTICA</strong><br>
  SCHOOL OF ENGINEERING<br>
  DEPARTMENT OF COMPUTER ENGINEERING AND INFORMATICS
</p>

<hr/>

<p align="center">
  <strong>Information Retrieval</strong>
</p>

<h1 align="center" style="letter-spacing: 1px;">
  Building a Search Engine for Academic Papers
</h1>

<p align="center">
  <strong>Vasileios Evangelos Athanasiou</strong><br>
  Student ID: 19390005
</p>

<p align="center">
  <a href="https://github.com/Ath21" target="_blank">GitHub</a> ·
  <a href="https://www.linkedin.com/in/vasilis-athanasiou-7036b53a4/" target="_blank">LinkedIn</a>
</p>

<p align="center">
  <strong>Pantelis Tatsis</strong><br>
  Student ID: 20390226
</p>

<p align="center">
  <a href="https://github.com/PanthegrammerPRO" target="_blank">GitHub</a> ·
  <a href="https://www.linkedin.com/in/pantelis-tatsis-8287852a2/" target="_blank">LinkedIn</a>
</p>

<p align="center">
  Supervisor: Panagiota Tselenti, Laboratory Teaching Staff
</p>
<p align="center">
  <a href="https://ice.uniwa.gr/en/emd_person/panagiota-tselenti/" target="_blank">UNIWA Profile</a> ·
  <a href="https://www.linkedin.com/in/panagiotatselenti" target="_blank">LinkedIn</a>
</p>


<p align="center">
  Athens, January 2024
</p>

---

# Project Overview

This project, developed for the **Information Retrieval** course at the University of West Attica (UNIWA), implements a local search engine that crawls, processes, and indexes academic papers from the **arXiv** repository.

---

## Table of Contents

| Section | Path / File | Description |
|--------:|-------------|-------------|
| 1 | `assign/` | Assignment specifications and project instructions |
| 1.1 | `assign/IR LabProject 2023-2024new.pdf` | Official laboratory project description |
| 1.2 | `assign/ΑΠ ΕργασίαΕργαστηρίου 2023-2024νέο.pdf` | Greek version of the assignment |
| 2 | `docs/` | Project documentation and reports |
| 2.1 | `docs/Academic-Paper-Search-Engine.pdf` | Technical documentation of the search engine |
| 2.2 | `docs/Μηχανή-Αναζήτησης-Ακαδημαϊκών-Εργασιών.pdf` | Greek documentation |
| 3 | `src/` | Source code directory |
| 3.1 | `src/main.py` | Application entry point |
| 3.2 | `src/search_engine.py` | Core search engine controller |
| 3.3 | `src/inverted_index.py` | Inverted index construction and lookup |
| 3.4 | `src/query_processing.py` | Query parsing and preprocessing |
| 3.5 | `src/ranking.py` | Document ranking algorithms |
| 3.6 | `src/text_preprocessing.py` | Text cleaning, normalization, and tokenization |
| 3.7 | `src/web_crawler.py` | Web crawling and data acquisition |
| 4 | `README.md` | Project overview and usage instructions |

---

## Features

### 1. Web Crawler
- Scrapes metadata from **arXiv** based on 2–8 random user queries (e.g., "Physics", "Statistics", "Computer").  
- **Implementation:** Python using **BeautifulSoup**.  
- **Data Collected:** Titles, authors, related courses/sub-courses, summaries, comments, publication dates, and PDF links.  
- **Storage:** Each task is assigned a unique `doc_id` and stored in a dictionary.

### 2. Text Processing
- Prepares retrieved data for indexing by implementing a text-processing pipeline (cleaning, tokenization, normalization).

### 3. Indexing
- **Inverted Index:** Efficient data structure for searching.  
- **Storage:** Index stored in a structured format accessible by the search engine.

### 4. Search Engine
- **User Interface:** Allows users to submit queries and retrieve results.  
- **Recovery Algorithms:** Retrieves relevant documents based on query terms.  
- **Filtering & Ranking:** Supports filtering by metadata (e.g., date, authors) and ranks results by relevance.

---

## Project Structure

- `main.py`: Entry point for running the local search engine and selecting random queries.  
- `web_crawler.py`: Contains the web scraping logic using BeautifulSoup.  

---

## System Evaluation

- Evaluated using datasets of **200–800 tasks**.  
- Various evaluation scenarios and metrics implemented in Python to assess search performance, precision, and recall.

---

# Installation & Setup Guide  

This guide explains how to **install, configure, and run** the Academic Paper Search Engine project.  
The project is written in **Python** and implements a local search engine that crawls, indexes, and searches academic papers from **arXiv**.

---

## Prerequisites

### 1. Operating System
- Windows, Linux, or macOS
- Python 3.11 recommended

---

### 2. Software

#### Python
- Install **Python 3.11** or later from [python.org](https://www.python.org/downloads/)
- Make sure `python` and `pip` are in your system PATH

#### Python Packages
Install required Python libraries:
```bash
pip install beautifulsoup4 requests lxml tqdm
```
Optional (for advanced ranking or evaluation):

```bash
pip install numpy pandas matplotlib
```

---

## Running the Search Engine
### 1. Clone the Repository
```bash
git clone https://github.com/Information-Retrieval-aka-Uniwa/Search-Engine.git
cd Search-Engine/src
```

### 2. Run the Application
Run the main program:
```bash
python main.py
```
- This will launch the search engine in console mode.
- A set of random queries (2–8) will be processed automatically, or you can enter custom queries interactively.

### 3. Web Crawler (Optional)
- The web crawler scrapes metadata from arXiv for indexing.
- Make sure your internet connection is active.
- The crawler stores data in a local dictionary (doc_id → document metadata).

Run crawler separately (optional):

```bash
python web_crawler.py
```

> Do not run repeatedly to avoid overwhelming the arXiv server.

### 4. Indexing
- The system automatically builds an inverted index from the crawled or preloaded dataset.
- Index is stored in memory and can be `saved/loaded` using Python’s pickle module (customize in `search_engine.py` if needed).

### 5. Searching
- Queries are processed via the `main.py` interface.
- Supports:
    - Exact keyword matching
    - Metadata filtering (authors, dates)
    - Ranked retrieval based on term frequency

Example query:
```bash
Enter your query: quantum computing
```
Results are displayed with:
- Document title
- Authors
- Publication date
- Summary snippet

---

## Open the Documentation
1. Navigate to the `docs/` directory
2. Open the report corresponding to your preferred language:
    - English: `Academic-Paper-Search-Engine.pdf`
    - Greek: `Μηχανή-Αναζήτησης-Ακαδημαϊκών-Εργασιών.pdf`