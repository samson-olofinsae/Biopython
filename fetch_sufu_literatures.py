################  SCRIPT
###### This script extracts a lis of papers from the PubMed database using the search Term SUFU
# SUFU is a gene that is part of a cell signaling pathway involved in the formation of tissues and organs, cell growth, and cell division during embryonic development.
# Mutations (changes) in the SUFU gene may cause cells to grow and divide too quickly or in an uncontrolled way.

# Code Description: Object Oriented Programming: Functions, class, inheritance
'''"This script demonstrates object-oriented programming (OOP) by defining:
a TextDownloader class that encapsulates the logic for querying PubMed, retrieving article details, and writing the results to a text file.
It demonstrates how to define functions (methods) that belong to a given class.
It also illustrates inheritance by creating a ChildClass that inherits from TextDownloader,
showing how a child class can reuse and extend functionality from the parent class.
By organizing PubMed logic into modular methods, the code is more maintainable and reusable."'''

# Importing the Entrez module from the Biopython library for accessing PubMed data
from Bio import Entrez

# Importing the xml.etree.ElementTree module for parsing XML data from PubMed
import xml.etree.ElementTree as ET

# Base class for downloading and extracting paper info
class TextDownloader:

    def __init__(self, email):
        Entrez.email = email

    def get_papers(self, term, db="pubmed", max_results=10):
        print("Searching for papers...")

        search_handle = Entrez.esearch(db=db, term=term, retmax=max_results, sort="pub+date")
        search_results = Entrez.read(search_handle)
        search_handle.close()

        id_list = search_results["IdList"]

        fetch_handle = Entrez.efetch(db=db, id=",".join(id_list), rettype="xml")
        xml_data = fetch_handle.read()
        fetch_handle.close()

        root = ET.fromstring(xml_data)
        records = []

        for article in root.findall(".//PubmedArticle"):
            try:
                # Extract the elements using .find() instead of .findtext()
                pmid_element = article.find(".//PMID")
                pmid = pmid_element.text if pmid_element is not None else "N/A"

                title_element = article.find(".//ArticleTitle")
                title = title_element.text if title_element is not None else "No title"

                journal_element = article.find(".//Journal/Title")
                journal = journal_element.text if journal_element is not None else "No journal"

                year_element = article.find(".//PubDate/Year")
                year = year_element.text if year_element is not None else "Unknown"

                pages_element = article.find(".//MedlinePgn")
                pages = pages_element.text if pages_element is not None else "N/A"

                authors = []
                for author in article.findall(".//Author"):
                    first_element = author.find("ForeName")
                    last_element = author.find("LastName")

                    first = first_element.text if first_element is not None else ""
                    last = last_element.text if last_element is not None else ""

                    full = f"{first} {last}".strip()
                    if full:
                        authors.append(full)

                author_line = ", ".join(authors)
                records.append((pmid, title, author_line, journal, year, pages))

            except Exception as e:
                print(f"Skipping one article due to error: {e}")
                continue

        with open("SUFU_literature.txt", "w") as f:
            for paper in records:
                f.write(f"PMID: {paper[0]}\n")
                f.write(f"Title: {paper[1]}\n")
                f.write(f"Authors: {paper[2]}\n")
                f.write(f"Journal: {paper[3]} ({paper[4]}), pp. {paper[5]}\n")
                f.write("\n" + "-"*80 + "\n")

        print("Papers saved to SUFU_literature.txt")

########### Demonstrating inheritance 


# Define the child class (ChildClass) that inherits from the parent class (TextDownloader).
# The child class inherits all functionality from the parent class and can also introduce its own unique methods.
# Inherited functionality include the __init__ and get_papers methods 

class ChildClass(TextDownloader):
    # Define a method unique to the child class (ChildClass).
    # This method is not part of the parent class and provides additional functionality specific to the child class.
    def Print(self):
        # Print a message from the method 'Print', which is unique to the child class.
        # This demonstrates behavior that is added in the child class, not inherited from the parent class.
        print("This line is printed from a method unique to the child class! De novo!")

####### Demonstrating Object Instantiation and Method Calling

# Create an instance of the child class, which inherits functionality from the parent class (TextDownloader)
# The email provided will be passed to the parent class's __init__ method, setting up Entrez.email.

inherited_class = ChildClass("youremail@youremail.com") # provide your email  

# Call the inherited method 'get_papers' from the parent class (TextDownloader)
# This method allows the child class object to search for papers related to the term "SUFU".
inherited_class.get_papers("SUFU")  # This will fetch papers related to the gene "SUFU"

# Call the method unique to the child class ('Print') that was defined in the child class (ChildClass)
# This method will print a message specific to the child class, showcasing behavior unique to it.
inherited_class.Print()  # ← This executes the method specific for the child - not inherited - de novo!
