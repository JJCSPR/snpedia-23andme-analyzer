import requests

def geneFinder(rsid, genotype, filename):
    """geneFinder checks if a gene is in a person's genetic code or not."""
    #project.geneFinder('i6033897','II', 'myGenome.txt')
    with open(filename,'rt') as fin:
        data = fin.read()
        return True if (rsid in data) and (genotype in data) and ("\n" not in data[data.index(rsid):data.index(genotype)]) else False

def geneInfo(rsid, genotype, filename):
    """geneInfo returns the data associated with a gene, if the gene is in a person's genetic code."""
    #project.geneInfo('i6033897','II', 'myGenome.txt')
    if geneFinder(rsid, genotype, filename):
        with open(filename, 'rt') as fin:
            for line in open(filename, 'rt').readlines()[20:]:
                if (rsid in line) and (genotype in line):
                    return line.split()
                    
def accessingStuff(disease):
    r = requests.get('http://bots.snpedia.com/api.php?action=query&list=categorymembers&cmtitle=Category:Is_a_medical_condition&cmlimit=500&format=json')
    medical_categories = r.json()['query']['categorymembers']
    for category in medical_categories:
        if category['title'] == disease:
            return category['pageid']
            
def diseasePageGenes(disease):
    pageid = '{}'.format(accessingStuff(disease))
    print(pageid)
    disease_url = 'http://bots.snpedia.com/api.php?action=query&prop=info&pageids={}&inprop=url&format=json'.format(pageid)
    r = requests.get(disease_url)
    url = r['query']['pages'][pageid]['fullurl']