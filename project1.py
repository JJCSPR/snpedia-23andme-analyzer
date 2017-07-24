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

def findChromosome(rsid, genotype, filename):
    """geneInfo returns the chromosome associated with a gene, if the gene is in a person's genetic code."""
    #project.chromosome('i6033897','II', 'myGenome.txt')
    if geneFinder(rsid, genotype, filename):
        with open(filename, 'rt') as fin:
            for line in open(filename, 'rt').readlines()[20:]:
                if (rsid in line) and (genotype in line):
                    return line.split()[1]

def position(rsid, filename):
    """geneInfo returns the chromosome associated with a gene, if the gene is in a person's genetic code."""
    #project.chromosome('i6033897','II', 'myGenome.txt')
    if RSIDfinder(rsid, filename):
        with open(filename, 'rt') as fin:
            for line in open(filename, 'rt').readlines()[20:]:
                if (rsid in line):
                    return int(line.split()[2])
                    
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

def diseasePageScraper(disease):
    """Scrapes a disease page for URL's to relevant SNP's. Will return a list."""
    from bs4 import BeautifulSoup
    import urllib.request
    import re
    html_page = urllib.request.urlopen(diseasePage(disease))
    soup = BeautifulSoup(html_page, "lxml")
    urls = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/index.php/Rs")}):
        urls.append("https://bots.snpedia.com" + link.get('href'))
    for link in soup.findAll('a', attrs={'href': re.compile("^/index.php/I[0-9]{1,10}")}):
        urls.append("https://bots.snpedia.com" + link.get('href'))
    return urls

def genePageScraper(disease, filename):
    from bs4 import BeautifulSoup
    import urllib.request
    import re
    geneLinks = diseasePageScraper(disease)
    geneInfo = []
    for link in geneLinks:
        rsid = link[35:]
        if RSIDfinder(rsid.lower(), filename):
            html_page = urllib.request.urlopen(link)
            soup = BeautifulSoup(html_page, "lxml")
            table = soup.find('table' ,attrs={'class':'sortable smwtable'}).find_all("tr")
            urls=[]
            for row in table[1:]:
                cells = row.find_all("td")

                
                if position(rsid.lower(), filename)>2700157:
                    genotype = cells[0].get_text().strip()[1]
                else:
                    genotype = cells[0].get_text().strip()[1] + cells[0].get_text().strip()[3]
                #code block above is correct
                if geneFinder(rsid.lower(), genotype, filename):
                    chromosome = findChromosome(rsid.lower(), genotype, filename)
                    magnitude = cells[1].get_text().strip()
                    summary = cells[2].get_text().strip()
                    geneInfo.append([rsid.lower(), genotype, chromosome, magnitude, summary])
    return geneInfo












