<p align="center">
  <img src="https://www.especial.gr/wp-content/uploads/2019/03/panepisthmio-dut-attikhs.png" alt="UNIWA" width="150"/>
</p>

<p align="center">
  <strong>UNIVERSITY OF WEST ATTICA</strong><br>
  SCHOOL OF ENGINEERING<br>
  DEPARTMENT OF COMPUTER ENGINEERING AND INFORMATICS
</p>

<p align="center">
  <a href="https://www.uniwa.gr" target="_blank">University of West Attica</a> ·
  <a href="https://ice.uniwa.gr" target="_blank">Department of Computer Engineering and Informatics</a>
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

<hr>

<p align="center">
  <strong>Supervision</strong>
</p>

<p align="center">
  Supervisor: Panagiota Tselenti, Laboratory Teaching Staff
</p>
<p align="center">
  <a href="https://ice.uniwa.gr/en/emd_person/panagiota-tselenti/" target="_blank">UNIWA Profile</a> ·
  <a href="https://www.linkedin.com/in/panagiotatselenti" target="_blank">LinkedIn</a>
</p>

</hr>

---

<p align="center">
  Athens, January 2024
</p>

---

<p align="center">
  <img src="https://media.licdn.com/dms/image/v2/D4E12AQHWIbt3v3flAg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1674228639744?e=2147483647&v=beta&t=hxzqz31mM4-10RwYZC3WJgSo9bxQuVQzJW3qIbskdS0" width="250"/>
</p>

---

# README

## Building a Search Engine for Academic Papers

This project was developed for the Information Retrieval course at the University of West Attica.

It implements a complete Information Retrieval (IR) system that:

- Crawls academic papers from arXiv
- Preprocesses textual data
- Builds an inverted index
- Supports multiple retrieval models
- Provides ranked search results through a graphical user interface (GUI)

---

## Table of Contents

| Section | Path / File                                       | Description                                        |
| ------: | ------------------------------------------------- | -------------------------------------------------- |
|       1 | `assign/`                                         | Assignment specifications and project instructions |
|     1.1 | `assign/IR LabProject 2023-2024new.pdf`           | Official laboratory project description            |
|     1.2 | `assign/ΑΠ ΕργασίαΕργαστηρίου 2023-2024νέο.pdf`   | Greek version of the assignment                    |
|       2 | `docs/`                                           | Project documentation and reports                  |
|     2.1 | `docs/Academic-Paper-Search-Engine.pdf`           | Technical documentation of the search engine       |
|     2.2 | `docs/Μηχανή-Αναζήτησης-Ακαδημαϊκών-Εργασιών.pdf` | Greek documentation                                |
|       3 | `src/`                                            | Source code directory                              |
|     3.1 | `src/main.py`                                     | Application entry point                            |
|     3.2 | `src/search_engine.py`                            | Core search engine controller                      |
|     3.3 | `src/inverted_index.py`                           | Inverted index construction and lookup             |
|     3.4 | `src/query_processing.py`                         | Query parsing and preprocessing                    |
|     3.5 | `src/ranking.py`                                  | Document ranking algorithms                        |
|     3.6 | `src/text_preprocessing.py`                       | Text cleaning, normalization, and tokenization     |
|     3.7 | `src/web_crawler.py`                              | Web crawling and data acquisition                  |
|       4 | `README.md`                                       | Project documentation                              |
|       5 | `INSTALL.md`                                      | Usage instructions                                 |

---

## 1. Project Objective

The objective of this project is to design and implement a functional academic search engine demonstrating:

- Web Crawling
- Text Preprocessing
- Inverted Index Construction
- Boolean Retrieval
- Vector Space Model (TF-IDF + Cosine Similarity)
- Probabilistic Retrieval Model (Okapi BM25)
- Query Processing with operator precedence
- Metadata filtering (Author, Date)

---

## 2. System Architecture

```bash
Web Crawler
↓
dataset.json
↓
Text Preprocessing
↓
Inverted Index
↓
Query Processing
↓
Retrieval Model
↓
Ranking
↓
Filtering
↓
Top-20 Results (GUI Output)
```

---

## 3. Project Structure

```bash
.
├── assign/
│ ├── IR LabProject 2023-2024new.pdf
│ └── ΑΠ ΕργασίαΕργαστηρίου 2023-2024νέο.pdf
│
├── docs/
│ ├── Academic-Paper-Search-Engine.pdf
│ └── Μηχανή-Αναζήτησης-Ακαδημαϊκών-Εργασιών.pdf
│
├── src/
│ ├── main.py
│ ├── web_crawler.py
│ ├── text_preprocessing.py
│ ├── inverted_index.py
│ ├── query_processing.py
│ ├── ranking.py
│ ├── search_engine.py
│
├── dataset.json (generated at runtime)
├── README.md
└── INSTALL.md
```

---

## 4. System Modules

### 4.1 Web Crawler (`web_crawler.py`)

- Retrieves up to 100 papers per subject.
- Randomly selects between 2–8 subject categories:
  - Physics
  - Mathematics
  - Computer
  - Biology
  - Finance
  - Statistics
  - Electronics
  - Economics

### 4.2 Extracted Metadata

- Title
- Authors
- Subjects
- Abstract
- Comments
- Submission Date
- PDF URL
- Unique `doc_id`

Data is stored in `dataset.json`.

---

## 5. Text Preprocessing (`text_preprocessing.py`)

Pipeline:

- Tokenization (NLTK)
- Punctuation removal
- Special character cleaning
- Lowercasing
- Stopword removal (English)
- Porter Stemming

Applied to:

- Document abstracts
- User queries

---

## 6. Inverted Index (`inverted_index.py`)

Creates:

term → [doc_id1, doc_id2, ...]

- Alphabetically sorted terms
- Sorted posting lists
- Stored in memory

---

## 7. Query Processing (`query_processing.py`)

Supports:

- AND
- OR
- NOT
- Parentheses
- Operator precedence

Boolean evaluation is implemented using set operations.

---

## 8. Retrieval Models

Implemented in:

- `search_engine.py`
- `ranking.py`

### 8.1 Boolean Retrieval

- Logical matching
- Parentheses support
- Set-based operations

### 8.2 Vector Space Model (VSM)

- TF-IDF weighting
- Cosine Similarity
- Ranked results

### 8.3 Probabilistic Retrieval Model

- Okapi BM25
- Parameters:
  - k = 1.2
  - b = 0.75

---

## 9. Graphical User Interface

Built using:

- tkinter
- ttk

Features:

- Query input
- Retrieval model selection
- Top-20 ranked results
- Filtering by:
  - Author
  - Date

---

## 10. Technologies Used

- Python 3.11
- requests
- beautifulsoup4
- nltk
- tkinter
- math
- collections
- json
- re
- string

---

## 11. System Evaluation

The system was evaluated using datasets of 200–800 documents.

Evaluation metrics included:

- Precision
- Recall
- Comparative ranking analysis between:
  - Boolean Retrieval
  - Vector Space Model
  - BM25

---

## 12. Notes

- Internet connection is required for crawling.
- Each execution generates a new dataset (random subject selection).
- Boolean operators must be lowercase: `and`, `or`, `not`.
