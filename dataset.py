import random

from web_crawler import store_json, web_crawling


subjects = ['Physics', 'Mathematics', 'Computer Science', 'Quantitative Biology', 'Quantitative Finance', 'Statistics', 'Electrical Engineering and Systems Science', 'Economics']

num_subjects = random.randint(1, len(subjects))
random_subjects = random.sample(subjects, num_subjects)
print(random_subjects)

random_subject = ['Statistics']
documents = web_crawling(random_subject)

store_json(documents, 'dataset.json')