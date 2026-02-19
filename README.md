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

This project, developed for the **Information Retrieval** course at the University of West Attica (UNIWA), implements a local search engine that crawls, processes, and indexes academic papers from the **arXiv** repository.

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

## 1. Web Crawler

- Scrapes metadata from **arXiv** based on 2–8 random user queries (e.g., "Physics", "Statistics", "Computer").
- **Implementation:** Python using **BeautifulSoup**.
- **Data Collected:** Titles, authors, related courses/sub-courses, summaries, comments, publication dates, and PDF links.
- **Storage:** Each task is assigned a unique `doc_id` and stored in a dictionary.

---

## 2. Text Processing

- Prepares retrieved data for indexing by implementing a text-processing pipeline (cleaning, tokenization, normalization).

---

## 3. Indexing

- **Inverted Index:** Efficient data structure for searching.
- **Storage:** Index stored in a structured format accessible by the search engine.

---

## 4. Search Engine

- **User Interface:** Allows users to submit queries and retrieve results.
- **Recovery Algorithms:** Retrieves relevant documents based on query terms.
- **Filtering & Ranking:** Supports filtering by metadata (e.g., date, authors) and ranks results by relevance.

---

## 5. Project Structure

- `main.py`: Entry point for running the local search engine and selecting random queries.
- `web_crawler.py`: Contains the web scraping logic using BeautifulSoup.

---

## 6. System Evaluation

- Evaluated using datasets of **200–800 tasks**.
- Various evaluation scenarios and metrics implemented in Python to assess search performance, precision, and recall.
