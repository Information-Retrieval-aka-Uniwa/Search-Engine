import json
import requests

from bs4 import BeautifulSoup

def web_scrape(soup, max_limit):
    # Αναζήτηση στο HTML του URL του μαθήματος, όλων των 'div' στοιχείων που έχουν την κλάση 'meta'
    # elements = soup.find_all('div', class_='meta')
    papers = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/abs/'):
            abs_url = 'https://arxiv.org/' + href
            abs_page = requests.get(abs_url)
            abs_soup = BeautifulSoup(abs_page.text, 'html.parser')
            element = abs_soup.find('div', id='abs')
            if element:
                if len(papers) < max_limit:
                    title = element.find('h1', class_='title mathjax').text.strip().removeprefix("Title:")
                    author = element.find('div', class_='authors').text.strip().removeprefix("Authors:") 
                    subject = element.find('td', class_='tablecell subjects').text.strip()
                    hasComment = element.find('td', class_='tablecell comments mathjax')
                    if hasComment is not None:
                        comment = hasComment.text.strip()
                    else:
                        comment = ' '
                    summary = element.find('blockquote', class_='abstract mathjax').text.strip().removeprefix("Abstract:") 
                    date = element.find('div', class_='dateline').text.strip().removeprefix("[Submitted on ").removesuffix("]") 

                    data = {
                        'title': title,
                        'author': author,
                        'subject': subject,
                        'comment': comment,
                        'summary': summary,
                        'date': date
                    }

                    # Αποθήκευση του λεξικού στην λίστα papers
                    papers.append(data)
                else:
                    break
    
    return papers

def store_json(papers):

    # Εκτύπωση των μεταδεδομένων σε δομημένη μορφή JSON
    for paper in papers:
        json_data = json.dumps(paper, indent=4)
        print(f'JSON Data:\n{json_data}')
            
    return json_data