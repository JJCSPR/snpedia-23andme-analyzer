def geneFinder(rsid, genotype, filename):
    """geneFinder checks if a gene is in a person's genetic code or not."""
    #project.geneFinder('i6033897','II', 'myGenome.txt')
    with open(filename,'rt') as fin:
        data = fin.read()
        return True if (rsid in data) and (genotype in data) and ("\n" not in data[data.index(rsid):data.index(genotype)]) else False

def RSIDfinder(rsid, filename):
    """geneFinder checks if a gene is in a person's genetic code or not."""
    #project.RSIDfinder('i6033897','II', 'myGenome.txt')
    with open(filename,'rt') as fin:
        data = fin.read()
        return True if (rsid in data) else False

def geneInfo(rsid, genotype, filename):
    """geneInfo returns the data associated with a gene, if the gene is in a person's genetic code."""
    #project.geneInfo('i6033897','II', 'myGenome.txt')
    if geneFinder(rsid, genotype, filename):
        with open(filename, 'rt') as fin:
            for line in open(filename, 'rt').readlines()[20:]:
                if (rsid in line) and (genotype in line):
                    return line.split()
                    
def diseaseID(disease):
    """diseaseID returns the page ID that corresponds to the disease inputted by the user."""
    #diseaseID('AIDS')
    import requests

    r = requests.get('http://bots.snpedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Is_a_medical_condition&cmlimit=500&format=json')
    #Connects to the pages with the diseases

    medical_categories = r.json()['query']['categorymembers']
    #Creates a list of dictionaries, each dictionary containing the disease name and pageid

    for category in medical_categories:
        if category['title'] == disease:
            return str(category['pageid'])
    #Code block above returns the str(pageid) that corresponds to the disease
            
def diseasePage(disease):
    """diseasePage returns the page corresponding to the disease inputted by the user."""
    #diseasePage('AIDS')
    import requests
    pageid = diseaseID(disease)
    disease_url = 'http://bots.snpedia.com/api.php?action=query&prop=info&pageids={}&inprop=url&format=json'.format(pageid)
    r = requests.get(disease_url)
    return r.json()['query']['pages'][pageid]['fullurl']

def diseasePageScraper():
    """Scrapes a disease page for URL's to relevant SNP's. Will return a list."""
    from bs4 import BeautifulSoup
    import urllib.request
    import re
    html_page = urllib.request.urlopen("https://bots.snpedia.com/index.php/Intelligence")
    soup = BeautifulSoup(html_page, "lxml")
    urls = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/index.php/Rs")}):
        urls.append("https://bots.snpedia.com" + link.get('href'))
    return urls
