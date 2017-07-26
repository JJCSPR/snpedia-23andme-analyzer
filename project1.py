from bs4 import BeautifulSoup
import urllib.request
import re
import requests

def geneFinder(rsid, genotype, filename):
    """geneFinder checks if a gene is in a person's genetic code or not."""
    #project1.geneFinder('i3001931','C', 'myGenome.txt')
    with open(filename,'rt') as fin:
        return any(((rsid in line) and (genotype in line)) for line in fin)

def RSIDfinder(rsid, filename):
    """geneFinder checks if a gene is in a person's genetic code or not."""
    #project.RSIDfinder('i3001931', 'myGenome.txt')
    with open(filename,'rt') as fin:
        return any(rsid in line for line in fin)

def findChromosome(rsid, genotype, filename):
    """geneInfo returns the chromosome associated with a gene, if the gene is in a person's genetic code."""
    #project.findChromosome('i3001931','C', 'myGenome.txt')
    with open(filename, 'rt') as fin:
        for line in fin:
            if (rsid in line) and (genotype in line):
                return line.split()[1]

def findGenotype(rsid, filename):
    """geneInfo returns the genotype associated with an rsid, if the rsid is in a person's genetic code."""
    #project.findGenotype('i3001931', 'myGenome.txt')
    with open(filename, 'rt') as fin:
        for line in fin:
            if (rsid in line):
                return line.split()[3]

def position(rsid, filename):
    """geneInfo returns the chromosome associated with a gene, if the gene is in a person's genetic code."""
    #project1.position('i3001931', 'myGenome.txt')
    with open(filename, 'rt') as fin:
        for line in fin:
            if (rsid in line):
                return int(line.split()[2])
                    
def diseaseID(disease):
    """diseaseID returns the page ID that corresponds to the disease inputted by the user."""
    #diseaseID('AIDS')
    r = requests.get('http://bots.snpedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Is_a_medical_condition&cmlimit=500&format=json')
    #Connects to the pages with the diseases

    medical_categories = r.json()['query']['categorymembers']
    #Creates a list of dictionaries, each dictionary containing the disease name and pageid

    for category in medical_categories:
        if category['title'] == disease:
            return str(category['pageid'])
    #Code block above returns the pageid that corresponds to the disease
            
def diseasePage(disease):
    """diseasePage returns the page corresponding to the disease inputted by the user."""
    #diseasePage('AIDS')
    pageid = diseaseID(disease)
    disease_url = 'http://bots.snpedia.com/api.php?action=query&prop=info&pageids={}&inprop=url&format=json'.format(pageid)
    r = requests.get(disease_url)
    return r.json()['query']['pages'][pageid]['fullurl']

def diseasePageScraper(disease):
    """Scrapes a disease page for URL's to relevant SNP's. Will return a list."""
    html_page = urllib.request.urlopen(diseasePage(disease))
    soup = BeautifulSoup(html_page, "lxml")
    urls = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/index.php/Rs")}):
        urls.append("https://bots.snpedia.com" + link.get('href'))
    for link in soup.findAll('a', attrs={'href': re.compile("^/index.php/I[0-9]{1,10}")}):
        urls.append("https://bots.snpedia.com" + link.get('href'))
    return urls

def genePageScraper(disease, filename):
    # genePageScraper('Diabetes', 'myGenome.txt')
    geneLinks = diseasePageScraper(disease)
    geneInfo = []
    for link in geneLinks:
        rsid = link[35:].lower()
        if RSIDfinder(rsid, filename):
            html_page = urllib.request.urlopen(link)
            soup = BeautifulSoup(html_page, "lxml")
            table = soup.find('table' ,attrs={'class':'sortable smwtable'}).find_all("tr")
            urls=[]
            for row in table[1:]:
                cells = row.find_all("td")
                
                if position(rsid, filename)>2689575:
                    genotype = cells[0].get_text().strip()[1]
                else:
                    genotype = cells[0].get_text().strip()[1] + cells[0].get_text().strip()[3]
                if geneFinder(rsid, genotype, filename):
                    chromosome = findChromosome(rsid, genotype, filename)
                    magnitude = cells[1].get_text().strip()
                    summary = cells[2].get_text().strip()
                    geneInfo.append([rsid, genotype, chromosome, magnitude, summary])
    return geneInfo












