""""""""""""""""""""""""""""""""""""""""""""" 
 
    Step 1. Web Crawler
 
"""""""""""""""""""""""""""""""""""""""""""""
import requests

from bs4 import BeautifulSoup

def web_crawling(random_subjects):
    dataset = []
    doc_id = 0
    for sub in random_subjects:
        # ------ Step 1.a. Selection of target website ------
        url = 'https://arxiv.org/search/?query=' + sub + '&searchtype=all&source=header&size=100' # e.g. Retrieval of data from 100 papers from arXiv for the Physics subject
        page = requests.get(url)                                                                  # https://arxiv.org/search/physics?query=Physics&searchtype=all&abstracts=show&order=-announced_date_first&size=100
        page.raise_for_status()
        # ------ Step 1.b. Implementation of web crawler ------
        soup = BeautifulSoup(page.text, 'html.parser')
        for elements in soup.find_all('li', class_='arxiv-result'):
            # ------ Title ------
            title = elements.find('p', class_='title is-5 mathjax').text.strip()
            # ------ Authors ------
            authors = elements.find('p', class_='authors').text.strip().removeprefix("Authors:").split(", ")
            authors = [author.strip() for author in authors]
            # ------ Subjects ------
            subjects = []
            for subject in elements.find_all('span'):
                if subject.get('data-tooltip') is not None:
                    subjects.append(subject.get('data-tooltip')) 
            # ------ Abstract ------
            abstract = elements.find('span', class_='abstract-full has-text-grey-dark mathjax').text.strip().removeprefix("Abstract:").removesuffix("\n        \u25b3 Less")
            abstract = abstract.strip()
            # ------ Comments ------
            has_comments = elements.find('p', class_='comments is-size-7')
            if has_comments is None:
                comments = ' '
            else:
                comments = has_comments.text.strip().removeprefix("Comments:").replace("\n", "")
            # ------ Date of publication ------
            date = elements.find('p', class_='is-size-7').text.strip().removeprefix("Submitted ").split(";")[0].replace(", ", " ")
            # ------ URL for downloading the pdf of the paper ------
            for pdf_link in elements.find_all('a'):                     
                pdf_href = pdf_link.get('href')                       
                if pdf_href and pdf_href.startswith('https://arxiv.org/pdf/'):         
                    pdf_url = pdf_href
            # ------ Storage of data in a structured dictionary format ------ 
            data = {
                'doc_id'   : doc_id,
                'title'    : title,
                'authors'  : authors,
                'subjects' : subjects,
                'abstract' : abstract,
                'comments' : comments,
                'date'     : date,
                'pdf_url'  : pdf_url
            }
            doc_id = doc_id + 1
            dataset.append(data)

    return dataset    




