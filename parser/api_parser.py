from bs4 import BeautifulSoup
from base_parser import BaseParser
import requests
import os

class LTIResearchPapersParser(BaseParser):
    def __init__(self, urls, year=2023):
        super().__init__(url='https://api.semanticscholar.org/graph/v1/paper/search')
        # self.url = 'https://api.semanticscholar.org/graph/v1/paper/search'
        self.urls_faulty = urls
        self.year = year
        self.S2_API_KEY = 'scv8zP7sDUao0gvaUt1aN7iUttJdx4hwfjP0UtK0'
        self.result_limit = 100

    def scrape_faculty_names(self):
        all_faculty_names = []
        for url in self.urls_faulty:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            faculty_names = [name_tag.text.strip() for name_tag in soup.select('.views-field.views-field-nothing h2')]
            all_faculty_names.extend(faculty_names)
        return all_faculty_names

    def fetch_papers_for_faculty(self, faculty_name):
        print(f"Searching for papers by: {faculty_name}")
        rsp = requests.get('https://api.semanticscholar.org/graph/v1/paper/search',
                           headers={'X-API-KEY': self.S2_API_KEY},
                           params={'query': faculty_name, 'year': self.year,
                                   'limit': self.result_limit, 'fields': 'title,authors,year,venue,citationCount'})
        rsp.raise_for_status()
        results = rsp.json()
        if results["total"] == 0:
            print(f"No papers found for {faculty_name}.")
            return []
        print(f"Found {results['total']} papers for {faculty_name}.")
        return results['data']

    def parse(self):
        faculty_names = self.scrape_faculty_names()
        for name in faculty_names:
            papers = self.fetch_papers_for_faculty(name)
            doc = "\n".join([f"{paper['title']} - {', '.join([author['name'] for author in paper['authors']])}, Year: {paper['year']}" for paper in papers])
            self._write_doc(doc)
            self._save_file()

if __name__ == '__main__':
    lti_urls = ['https://lti.cs.cmu.edu/directory/all/154/1',
                'https://lti.cs.cmu.edu/directory/all/154/1?page=1']
    parser = LTIResearchPapersParser(urls=lti_urls, year=2023)
    parser.parse()
