# -*- coding: utf-8 -*-
"""
Web_explorer.py

Small Python utility used for scanning text content from websites
Copyright (C) 2016  Nicolas Obriot

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created on Jun 22 18:00:00 2016

@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 10/07/2016 by Nicolas Obriot
"""

#%% First section, all the different imports.
import os.path, glob, os
import shutil #Remove directories with files
import urllib2 as url #Open URLs
import re #Regex
from bs4 import BeautifulSoup #HTML parsing
import pickle #Saving Python variables
import time # calculate elapsed time or do pauses in the execution

#Extract text content from PDF files
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

#Extract text from docx documents
from docx import opendocx, getdocumenttext

#Plotting and network visualization
import networkx as nx
import matplotlib.pyplot as plt #For plotting graphs

# Class definition : webExplorer
class webExplorer:
    """ webExplorer Class. 
    This class is used to explore websites and store their 
    text content along with the list of links per page and a total amount of link
    towards external websites. This class is also used for creating text corpora
    and filtering websites displaying a Danish CVR number.
    """

    #Variable shared by all instances of webExplorer class
    # This is used to extract the URL of a website in the links (e.g. extracts google.fr from https://www.google.fr/something?query=myquery)
    base_url_regex = '^https?://.+?\..+?/|^https?://.+?\..+?\?|^https?://.+?\..+?#|^https?://.+?\..+|^//.+?\..+?/|^//.+?\..+?\?|^//.+?\..+?#|^//.+?\..+|^.+?\..+//'

    #Constructor : variable init when creating the object. Initializing variables
    def __init__(self, main_directory="", redirect_count=None, degree_depth_level=None, verbose = False):
        """ Class constructor, initialize instance variables """
        #This is the working directory, initialized with the argument given to the constructor
        self.set_main_directory(main_directory)

        # A list of websites we do not want to visit at all.
        self.url_blacklist= ".*google\..*|.*facebook\..*|.*instagram\..*|.*youtube\..*|.*twitter\..*|.*linkedin\..*|.*youtu\.be.*|.*goo\.gl.*|.*flickr\..*|.*bing\..*|.*itunes\..*|.*dropbox\..*|.*independent\.co.*" #All the websites we want to ignore

        #LIst of extension, that if we find in a URL, the URL will be discarded
        self.extensions_to_ignore = ['.*\.[pP][dD][fF].*|^.*[Pp][Dd][fF]$','^.*\.[Xx][lL][sS]$','^.*\.[Dd][oO][cC][mMxX]?$','.*\.[aA][sS][pP][xX]?.*|^.*[aA][sS][pP][xX]?$','.*\.[aA][sS][hH][xX].*|^.*[aA][sS][hH][xX]$','.*\.[pP][nN][gG].*|^.*[pP][nN][gG]$','.*\.[jJ][Pp][eE]?[gG].*|^.*[jJ][Pp][eE]?[gG]$','.*\.flv.*|^.*flv$','.*\.mp4.*|^.*mp4$','.*\.mov.*|^.*mov$']

        # Set the exploration variables
        self.set_redirect_count(redirect_count)
        self.set_exploring_depth(degree_depth_level)

        # different url list
        self.to_visit_urls = [] # Which URL are yet to visit
        self.to_visit_urls.append(set()) # We create a set for to_visit_urls[0]
        self.to_visit_urls_back_up_filename = None 

        # A verbose boolean variable : if set to True, the class prints out exec info
        self.set_verbose(verbose) # Default is false.
        self.debug = False #Debugging is disabled and can only be enabled with a function call, not with the constructor
        
        #Dictionaries :
        self.danish_dict = None
        self.english_dict = None

        # CVR number registry
        self.CVR_registry = dict() # We will store it the following way : CVR_registry['website'] = "12345343" or = None

        # Sets of base URLs (website url) 
        # NOT USED AT THE MOMENT
        self.DTU_base_urls=set() # Domain name part of DTU
        self.non_DTU_base_urls = set() # Domain name not part of DTU
        
        #Create the needed folders (if they do not exist) for our web explorer : 
        self.create_folder(self.main_directory + "web_content")
        self.create_folder(self.main_directory + "variables")
        self.create_folder(self.main_directory + "corpus")
        self.create_folder(self.main_directory + "corpus/Danish")
        self.create_folder(self.main_directory + "corpus/English")


    # Set the working directory for our object : (Where all the files will be stored)
    def set_main_directory(self,new_directory=""):
        if new_directory == "" :
            self.main_directory = os.getcwd()+'/'
        else:
            self.main_directory = new_directory
        #Ensure that where we are working is actually the directory
        os.chdir(self.main_directory)

    # Set explorer startpoints
    def set_explore_start_points(self, url_list):
        ''' This function takes a list of webpages as an argument and sets then
        into the start point for exploration'''
        if len(url_list) == 0:
            print "Please specify at least one URL/website to start from"
        else :
            # Filter what are base URLs in the arguement list and add them in the first level of the list of URL to visit.
            self.to_visit_urls[0]=self.to_visit_urls[0].union(self.filter_links(url_list))
        
        #Now filter the crap we have from User Input : 
        new_to_visit_url_set = set()
        for webpage in self.to_visit_urls[0]:
            # Find the base url and remove the actual URL.                
            base_url_webpage = self.extract_base_url(webpage)
            if base_url_webpage : #The function can return "None" if not found
                new_to_visit_url_set.add(base_url_webpage)
                if self.debug:
                    print "Filtering base URL for : "+ webpage + " - Result : " + base_url_webpage
            else : 
                new_to_visit_url_set.add(webpage)
                if self.debug:
                    print "Filtering base URL for : "+ webpage + " - Result : /!\\ None /!\\ -> URL is kept as such "
            
        #Now take the filtered set and put it into the actual set
        self.to_visit_urls[0] = new_to_visit_url_set
            

    # Set number of redirections within single websites :
    def set_redirect_count(self,redirect_count=None):
        ''' This function takes an int as an argument and sets the amount of
        redirections followed per website '''
        if redirect_count is not None and type(redirect_count) is int:
            self.redirect_count = redirect_count
        else:
            self.redirect_count = 1 #How many links we will follow (site1.page1 -> site1.page3 -> site1.page3 is 3 levels)

    # Set the depth for external websites exploration :
    def set_exploring_depth(self,degree_depth_level=None):
        ''' This function takes an int as an argument and sets the depth of
        outside links explored from the starting websites
        Example : Start_site -> site1 -> site2 is 3 levels '''
        if degree_depth_level is not None and type(degree_depth_level) is int:
            self.degree_depth_level = degree_depth_level
        else:
            self.degree_depth_level = 1 #How many links we will follow outside our start URLs (DTU -> site1 -> site2 is 3 levels)

    # Sets the verbose for the class
    def set_verbose(self,verbose=False):
         self.verbose = verbose
         
    # Sets the verbose for the class
    def set_debug(self,debug=False):
         self.debug = debug
    
    #Function to save the to_visit_url variable
    def back_up_to_visit_url(self, target_filename=None):
        if self.to_visit_urls_back_up_filename : 
            pickle.dump(self.to_visit_urls,open(self.main_directory+"variables/"+self.to_visit_urls_back_up_filename, "wb" ))
        elif target_filename: 
            pickle.dump(self.to_visit_urls,open(self.main_directory+"variables/"+target_filename, "wb" ))
        else:
            if self.debug:
                print "WARNING : Tried to save URL tree without defining a filename. The file will not be saved"
    
    # Function to save the name for saving the "to_visit_url" variable
    def set_url_tree_back_up_filename(self, new_name):
        self.to_visit_urls_back_up_filename = new_name

    # Functions
    def explore(self):
        ''' Starts from the to_visit_urls list and builds an URL tree
            - finds out what is the base url (website url)
            - Open the page
            - Store the HTML content and cleartext content in a file
            - Find all the links from the page
            Returns a list object with the list of Links found on the target_url'''
        if len(self.to_visit_urls) == 0:
            print "WARNING : You have not defined any start point for the exploration"

        # website will go as many levels as the degree_depth_level variable indicates.
        for i in range(self.degree_depth_level):
            self.to_visit_urls.append(set())
            for webpage in self.to_visit_urls[i]:

                #Prepare the variable that we add into the future URL to visit
                external_base_urls = set()

                # == The base URL has already been visited and we know the external URLs for this redirect count
                if os.path.isfile(self.main_directory+"web_content/"+webpage+"/external_urls_"+str(self.redirect_count)+"_redirect.p"):
                    if not re.match("^[\.]+$",webpage): ## TODO : This is ugly, should be removed if possible (added it because some of the external_urls(redirect_count).p contain . as a base URL and is not filtered when loaded again)
                        if self.verbose:  #Anouncement message                     
                            print webpage + " has already been visited, loading external URLs..."
                        filename = self.main_directory+"web_content/"+webpage+"/external_urls_"+str(self.redirect_count)+"_redirect.p"
                        external_base_urls=pickle.load(open(filename, "rb" ))

                # == The base URL has not been visited yet
                else:
                    # 1) Create a folder for the website in the content folder. Create sub-folders "cleartext" and "linklist"
                    if self.verbose:  #Anouncement message 
                        print "Preparing folders for " + webpage
                    self.create_folder(self.main_directory+"web_content/"+webpage)
                    self.create_folder(self.main_directory+"web_content/"+webpage+"/cleartext")
                    self.create_folder(self.main_directory+"web_content/"+webpage+"/linklist")

                    # 2) Prepare a variable which contains all the external websites found from the website
                    internal_urls = set()
                    internal_urls.add("") #We put the base URL up on the list as the first internal URL to visit

                    # 3) Explore within the website
                    for j in range(self.redirect_count): # How many times we will follow redirections within the same website
                        # Scan the URL (retrieve the content, internal links and external links)
                        print "Scanning "+webpage + " iteration " + str(j+1)
                        for internal_page in internal_urls:
                            all_links = self.URL_scan(webpage, internal_page)

                            # Find the internal links and add them to the discovery for the next iteration
                            internal_urls= internal_urls.union(self.find_internal_links(webpage,all_links))

                            # Find external base URLs and add them to the list of external URLs.
                            external_base_urls= external_base_urls.union(self.find_external_base_urls(webpage,all_links))

                    # When done for the website, we save the external base URLs
                    filename = self.main_directory+"web_content/"+webpage+"/external_urls_"+str(self.redirect_count)+"_redirect.p"
                    pickle.dump(external_base_urls,open(filename, "wb" ))

                # Add all the new found websites to the list of website to visit at the next "Web level"
                #print "Found external base URLs : "
                #print external_base_urls
                self.to_visit_urls[i+1]=self.to_visit_urls[i+1].union(external_base_urls)
                self.back_up_to_visit_url()

                if self.verbose:  #Anouncement message
                    print 'Finished webpage ' +webpage
            print 'Finished web level %d' %(i+1) #So we know how far it went on the console
    ##End of explore()

    #This is the function to load the page, save them and find child links:
    def URL_scan(self, base_url, internal_page):
        ''' Takes the base_url and internal_page performs the following actions:
            - Determine wether the URL belongs to DTU
            - Determine whether the URL has already been visited.
            - Open the page
            - Store the cleartext content in a file (cleaned from the HTML markup) if the page is not a DTU page
            - Find all the links from the page (both internal and exteral)
            Returns a list object with the list of Links found on the visited page'''
        # Prepare the file name for the corresponding website
        filename = self.main_directory+"web_content/"+base_url+"/cleartext/"+re.sub("/", '_', internal_page)+".txt"

        #Remove trailing "/"
        while internal_page[-1:] == "/" :
            internal_page = internal_page[:-1]

        # If the page has not been visited, we just visit it
        if not os.path.isfile(filename):
            #First find whether it is a DTU page and store the base URL
            url_is_DTU = re.search('.*\.dtu.*', base_url)

            try:
                # we open the URL and read the content
                if self.debug:  #Show the requested URL
                    print " - Hit http://"+base_url+"/"+internal_page
                # Make the HTTP query
                html_response= url.urlopen("http://"+base_url+"/"+internal_page)
                
                #If he status code is 404, we create a dummy file, not to try again later
                if html_response.code == 404:
                    self.create_dummy_files(base_url, internal_page)
                    raise Exception('HTTP Error 404: Not Found')
                
                #Read the text response
                html_text= html_response.read()
                
                #Initialize the list of links found on the internal page
                link_list = []
    
                #If it points at a PDF or Word, we do something different, else treat the page as HTML : 
                if not (self.is_PDF_link(internal_page) or self.is_Word_doc_link(internal_page)):
                    # We replace all empty HTML tags with a space inside:
                    html_text = html_text.replace(">", "> ")
    
                    # We use the beautiful soup to get the text from HTML :
                    soup = self.get_clean_text_from_html_content(html_text)
    
                    # If URL is DTU, just create a placeholder file in order not to revisit the same page later
                    if url_is_DTU:
                        pagefile = open(filename,'w+')
                        pagefile.close()
                    else: # We save the page text content
                        pagefile = open(filename,'w')
                        pagefile.write(soup.get_text().encode('UTF-8'))
                        pagefile.close()
    
                    #Find all the links in the webpage
                    link_list = self.find_child_links_from_html_soup(soup,base_url)
    
                elif self.is_PDF_link(internal_page) :
                    # Extract and save the PDF content
                    if self.debug:  # Debug message
                        print "Found PDF page : "+ internal_page
                    self.save_text_from_PDF(html_text, filename)
                
                elif self.is_Word_doc_link(internal_page) :
                    # Extract and save the doc content
                    if self.debug:  # Debug message
                        print "Found Word Doc page : "+ internal_page
                    self.save_text_from_Word_doc(html_text, filename)
                
                # Save the list of links in the folder                
                filename = self.main_directory+"web_content/"+base_url+"/linklist/"+re.sub("/", '_', internal_page)+".p"
                if self.debug:  #Show the filename being saved
                    print "- Saving file " + filename
                pickle.dump(link_list,open(filename, "wb" ))
    
                return link_list
            except Exception, e:
                if self.verbose:
                    print "Exception thrown in URL_scan : %s" % e  #In case the URL could not be opened, we just return nothing
                #Back off a litle when getting a HTTP error
                time.sleep(5)
                return []
        else:
            #Load the list of links from the page in the folder
            filename = self.main_directory+"web_content/"+base_url+"/linklist/"+re.sub("/", '_', internal_page)+".p"
            if self.debug:  #Show the filename being opened          
                print "- Opening file " + filename
            link_list = self.filter_links(pickle.load(open(filename, "rb" )))
            return link_list


    def create_dummy_files(self, base_url, internal_page):
        ''' Create empty files in the web content, so that broken URL are not tried several times '''
        if self.verbose:  #Anouncement message         
            print "- WARNING : Could not open the following webpage : " + base_url + "/" + internal_page
            print "-> Creating dummy placeholder files for this page"
        filename = self.main_directory+"web_content/"+base_url+"/cleartext/"+re.sub("/", '_', internal_page)+".txt"
        pagefile = open(filename,'w+')
        pagefile.close()
        filename = self.main_directory+"web_content/"+base_url+"/linklist/"+re.sub("/", '_', internal_page)+".p"
        pickle.dump([],open(filename, "wb" ))

#==============================================================================
#     TO be revised later
#==============================================================================
    # function for finding which website belongs a URL
#    def find_base_url_and_DTU(self, target_url,find_dtu = False):
#        ''' Takes the target_url and finds out what is the base url (website url)
#        i.e. https://docs.python.org/2/library/ gives https://docs.python.org/
#        and then sorts it in a set depending on whether it contains DTU in the
#        base URL.
#        - DTU base URL are stored in the set : DTU_base_urls
#        - other URls are stored in the set : non_DTU_base_urls
#        This function will create an error if the sets are not declared before
#        returns the base_url'''
#
#        #We first find out what's the base_url (website url)
#        found_base_link = re.match('^https?://.*?/|^https?://.*?', target_url)
#
#        #We add the finding either DTU_base_urls or non_DTU_base_urls
#        if found_base_link:
#            found_base_link = found_base_link.group(0)
#            found_base_link = string.replace(found_base_link,"https:","http:")
#
#            if find_dtu:
#                url_is_DTU = re.search('.*\.dtu.*', found_base_link)
#                if url_is_DTU:
#                    DTU_base_urls.add(found_base_link)
#                else:
#                    non_DTU_base_urls.add(found_base_link)
#            return found_base_link
#        else:
#            return None

    # function for finding which links belong to the given base URL
    def find_internal_links(self, webpage, all_links):
        ''' Takes a base URL and a list of links found in the HREF tags.
        returns all the links that belong to the same webpage.'''

        #The argument should be a list, but if a string was passed, we convert it
        if type(all_links) is str:
            all_links = all_links.split()

        internal_links = []
        for link in all_links:
            #Remove leading and trailing spaces
            link = link.strip()
            #We first find out what's the base_url (website url)
            if len(link)>0 and len(link)<220: #We throw away links with more than 220 chars (255 bytes for filenames in Unix)
                if (link[0] == "/" and link[1] != "/") or (":" not in link and "//" not in link): # If it starts with a / but is not //, it is a relative path
                    #Remove eventual trailing "/"
                    if link[0] == "/" : 
                        link = link[1:]
                        
                    # Remove parameters or anchors
                    link = link.split('#')[0]
                    #link = link.split('?')[0]
                    
                    #Append to the current list
                    internal_links.append(link)

                else: # It must be an absolute path, we need to pull out the base URL
                    #Find what is the website and add the link in the list IIF it is within the same website
                    found_base_url = self.extract_base_url(link)

                    if webpage == found_base_url :
                        #Remove everything after the base url and keep everything before anchors and GET parameters
                        relative_path = link.split(found_base_url)[-1]
                        relative_path = relative_path.split('#')[0]
                        relative_path = relative_path.split('?')[0]
                        #Remove eventual trailing "/" and "//"
                        while '//' in relative_path:
                            relative_path=relative_path.replace('//','/')
                        if len(relative_path) >1 :
                            if relative_path[0] == "/": 
                                relative_path = relative_path[1:]                        
                        
                        internal_links.append(relative_path)

        #Clean up all the double / from paths : I do not know why I wrote that before
#        for i in range(len(internal_links)):
#            while '//' in internal_links[i]:
#                internal_links[i]=internal_links[i].replace('//','/')
#            while '..' in internal_links[i]:
#                internal_links[i]=internal_links[i].replace('..','.')

        return self.filter_links(internal_links)


    # function for finding which links belong to the given base URL
    def find_external_base_urls(self, webpage, all_links):
        ''' Takes a base URL and a list of links found in the HREF tags.
        returns all the links that belong to the same webpage.'''

        #The argument should be a list, but if a string was passed, we convert it
        if type(all_links) is str:
            all_links = all_links.split()

        external_links = []
        for link in all_links:
            #Remove leading and trailing spaces
            link = link.strip()
            #We first find out what's the base_url (website url)
            if len(link)>0 and len(link)<200: #We throw away links with more than 200 chars
                if not (link[0] == "/" and link[1] != "/") or (":" in link):  # If it starts with a /, it is a relative path, we do not want that
                    #Find what is the website for that link
                    found_base_url = self.extract_base_url(link)
                    
                    #We add it to the list if it is a different webpage
                    if webpage != found_base_url and found_base_url is not None:
                        external_links.append(found_base_url)

        #while '' in external_links:
        #    external_links.remove('')

        return self.filter_links(external_links)


    # This function remove undesirable links from a list (filenames, javascript, or blacklisted URLs)
    def filter_links(self, link_list):        
         #The argument should be a list, but if a string was passed, we convert it
        if type(link_list) is str:
            link_list = link_list.split()
            
        filtered_link_list = []

        for link in link_list:
            keep_link = True
            for extension in self.extensions_to_ignore:
                if re.match(extension,link):
                    keep_link = False
            #No poisonous extension found, so we proceed.
            if keep_link:
                if "javascript:" in link.lower() or "mailto:" in link.lower():
                    keep_link = False
                elif "ftp:" in link.lower() or "file:" in link.lower():
                    keep_link = False
                elif "mail:" in link.lower():
                    keep_link = False
                elif "unescape(" in link.lower():
                    keep_link = False
                elif "127.0.0.1" in link: #This is not correct either
                    keep_link = False
                elif re.match("^[\.]+$",link): #If it is points only, throw it away
                    keep_link = False
                elif re.match("^.+?@.+?\..+$",link): #If it is an email, throw it away
                    keep_link = False
                elif re.match(self.url_blacklist, link):
                    keep_link = False

            # Keep the link if it was not detected as a problem
            if keep_link:
                filtered_link_list.append(link)

        return filtered_link_list

    def extract_base_url(self, link):
        ''' Function returning the base url from an hyperlink '''
        found_base_url = re.match(self.base_url_regex, link)
        if found_base_url:
            found_base_url = found_base_url.group(0)
            found_base_url = found_base_url.replace('https://','')
            found_base_url = found_base_url.replace('http://','')
            found_base_url = found_base_url.replace('/','')
            found_base_url = found_base_url.split('#')[0]
            found_base_url = found_base_url.split('?')[0]
            found_base_url = found_base_url.replace('www.','')
            
            if len(found_base_url)<1: #Back-up check to prevent '' to go through.
                found_base_url = None
            
        else : 
            found_base_url = None
    
        return found_base_url


    def get_clean_text_from_html_content(self,html_text):
        ''' Takes the html_text and uses Beautiful Soup to filter out unwanted
            content and return a clean "soup" '''
        soup = BeautifulSoup(html_text, 'html.parser')

        # Removing the script/noscript/style tags
        while(soup.script is not None):
            soup.script.decompose()
        while(soup.noscript is not None):
            soup.noscript.decompose()
        while(soup.style is not None):
            soup.style.decompose()
        #We replace the <br> tags with new lines
        while(soup.br is not None):
            soup.br.replace_with(" ")

        #Returns the soup object
        return soup

    def find_child_links_from_html_soup(self,html_soup,target_url):
        ''' Takes the beautifulSoup soup and url it comes from
        returns a List of all the links (href in a <a> tag found from the
        HTML content of the soup'''
        samples = html_soup.find_all("a")

        #Here we declare two list we will be using:
        URLList = []
        samplesStr= []

        for x in samples: #We convert the bs4.ResultSet into a String
            samplesStr.append(str(x))
        #we use Regex:
        for item in samplesStr:
            links = re.findall(r'href="(.*?)"', item)
            links = links + re.findall(r"href='(.*?)'", item)
            if len(links)>0:
                link = links[0]
                if link.startswith('/'):
                    URLList.append(target_url+"/"+link)
                else :
                    URLList.append(link)

        #Remove unwanted stuffs
        URLList = list(set(URLList))
        if 'http://' in URLList:
            URLList.remove('http://')
        if None in URLList:
            URLList.remove(None)

        return URLList

    def get_child_links_from_file(self,target_url):
        ''' This function finds the child links from the HTML content of the page
        stored earlier.'''
        html_filename = self.main_directory+"web_content/html/"+re.sub("/", '_', target_url)+".html"

        html_file = open(html_filename,'r')
        html_text = html_file.read()
        html_file.close()

        #We prepare an empty list
        child_links = []

        links = re.findall(r'href="(.*?)"', html_text)
        links = links + re.findall(r"href='(.*?)'", html_text)
        for link in links:
            if link.startswith('/'):
                link = link[1:]
            if "http" in link:
                child_links.append(link)
            else :
                child_links.append(target_url+link)

        #Remove unwanted things
        child_links = list(set(child_links))
        if 'http://' in child_links:
            child_links.remove('http://')
        if ':80' in child_links:
            child_links.remove(':80')
        if ':443' in child_links:
            child_links.remove(':443')

        #When done, we mark the page as visited for the run in the temp folder
        #create_temp_file(target_url)

        #Finally return the list
        return child_links

    def is_PDF_link(self, link):
        ''' Function that returns TRUE if the URL points at a PDF file '''
        is_PDF = False
        
        pdf_link_regex = '.*\.[pP][dD][fF].*|^.*[Pp][Dd][fF]$'
        if re.match(pdf_link_regex,link):
            is_PDF = True
        
        return is_PDF
        
    def is_Word_doc_link(self, link):
        ''' Function that returns TRUE if the URL points at a Word file '''
        is_word_doc = False
        
        word_doc_regex = '.*\.[dD][oO][cC][xXmM]?.*|^.*[Dd][Oo][Cc][xXmM]?$'
        if re.match(word_doc_regex,link):
            is_word_doc = True
        
        return is_word_doc
        
    def save_text_from_PDF(self, pdfcontent, target_filename):
        #TODO : This is not working yet
        ''' Function that returns the text content from a PDF file
        Package used : https://pypi.python.org/pypi/pdfminer/
        Another page for it : http://www.unixuser.org/~euske/python/pdfminer/index.html
        Test PDF file : https://9-11commission.gov/report/911Report.pdf'''
        #First save the PDF locally :
        pdf_file = open(target_filename+".pdf",'wb')
        pdf_file.write(pdfcontent)
        pdf_file.close()
                
        #Prepare the input and destination file
        pdf_file = file(target_filename+".pdf", 'rb')
        pdf_target_file = open(target_filename,'w')
        
        #First declare a PDF manager
        rsrcmgr = PDFResourceManager()
        #Some parameter for PDF parsing
        laparams = LAParams()
        laparams.all_texts = True
        laparams.detect_vertical = True
        codec = 'utf-8'
        #Then a device
        device = TextConverter(rsrcmgr, pdf_target_file, codec=codec, laparams=laparams, imagewriter=None)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # This function taken form the PDF manager stuff will save the PDF text content in the pdf_target_file
        for page in PDFPage.get_pages(pdf_file):
            page.rotate = (page.rotate) % 360
            interpreter.process_page(page)
        
        #Finally close the files, we are done
        pdf_target_file.close() 
        pdf_file.close()
        #Erase the PDF file, we do not care : 
        os.remove(target_filename+".pdf")
        
    def save_text_from_Word_doc(self, doccontent, target_filename):
        #First save the file locally :
        doc_file = open(target_filename+".doc",'wb')
        doc_file.write(doccontent)
        doc_file.close()
                           
        # Decode the DOC from the local file
        document = opendocx(str(target_filename+".doc"))
        paratextlist = getdocumenttext(document)
        
        # Make explicit unicode version
        newparatextlist = []
        for paratext in paratextlist:
        	newparatextlist.append(paratext.encode("utf-8"))
        
        # Join the list into a long string
        docText = '\n'.join(newparatextlist)
        
        # Save the extracted text in the target file
        doc_target_file = open(target_filename,'w')
        doc_target_file.write(docText)
        doc_target_file.close()       
        
        #Erase the local DOC file, we do not care : 
        os.remove(target_filename+".doc")
        
        #Stop exec and check the result manually : 
        raise Exception('Doc file was saved! Please checked it worked at : ' + target_filename) 
        
#==============================================================================
#    THIS will be revised later
#==============================================================================
#    def update_url_tree(webpage,child_links):
#        ''' Update the URL tree by adding all the base URLs in a list at the
#        webpage index. Ich bin Sabi moin moin!'''
#        global url_tree
#
#        #Now update the URL tree, only with baselinks
#        webpage_base_url = self.find_base_url_and_DTU(webpage)
#
#        if webpage_base_url not in url_tree.keys(): #fisrt time we find a base URL, start with an emptpy list in the dict
#            url_tree[webpage_base_url] = []
#
#        for child_url in child_links:
#            url_tree[webpage_base_url].append(find_base_url_and_DTU(child_url))
#
#        #Clean up the URL tree of doubles and None objects
#        url_tree[webpage_base_url] = list(set(url_tree[webpage_base_url]))
#        if None in url_tree[webpage_base_url]:
#            url_tree[webpage_base_url].remove(None)


    def find_language(self,text):
        ''' Find whether the text is in English, Danish or unknown by looking up
        the percentage of words belonging to Enlish and Danish.
        Returns "English", "Danish" or None'''

        #If the dicts variables are not loaded from the files, we do.
        #As they are global variables, it will load the dicts only once
        if self.english_dict is None:
            self.english_dict = set(word.strip().lower() for word in open(self.main_directory+"dictionaries/US.dic"))
        if self.danish_dict is None:
            self.danish_dict = set(word.strip().lower() for word in open(self.main_directory+"dictionaries/dk.dic"))

        #We protect from errors with a Try block
        try :
            #First need to convert the text into a list of words (tokenize)
            word_list_tmp = re.sub("[^\wøæå]", " ",  text).split() #<-Does not deal good with Danish special characters
            #word_list_tmp = word_tokenize(text)
            word_list = []

            #Filter out everything that is not a word :
            for word in word_list_tmp:
                if word.isalpha()==True:
                    word_list.append(word)

            #Prepare variables for counting words
            english_word_count = 0
            danish_word_count = 0

            #Now we do a count :
            for word in word_list:
                if word.lower() in self.english_dict:
                    english_word_count +=1
                if word.lower() in self.danish_dict:
                    danish_word_count +=1

            #Look at the returns when we are done
            total_words = len(word_list)

            if self.debug:  #Debug : Set word count details
                print "Danish word percentage : "+str(float(danish_word_count)/total_words*100)
                print "English word percentage : "+str(float(english_word_count)/total_words*100)

            #Now we decide what we return: 50 for danish as all the words with å æ ø are not counted
            if float(danish_word_count)/total_words*100 > 45 and danish_word_count>english_word_count:
                return "Danish"
            elif float(english_word_count)/total_words*100 > 65:
                return "English"
            else:
                return None
        except:
            return None


    def create_R_corpus(self,language):
        ''' Create a corpus of files for R from the working directory.
        - language parameter has to a supported language by returned by the find_language() function. 
        Currently it is either "Danish" or "English"
        The corpus is placed in the corpus/ folder, followed by the language'''

        #Check whether the language is supported :
        if language not in ['English','Danish']:
            print 'ERROR : Input language is incorrect : ' + language
            print 'The corpus will not be created. Exiting...'
            return

        #For each website, the corpus file corresponding will be a concatenation of all the content
        for base_url in os.listdir(self.main_directory+"web_content/"):
            # Now small test to see whether the website should be part of the corpus or not
            should_take_url = False
        
            # Could do another kind of test
            if self.is_danish_company(base_url):
                should_take_url = True

            if should_take_url:
                if self.verbose:
                    print "Adding "+base_url+" to the R corpus"
                
                # Prepare the destination file
                base_url_filename = self.main_directory+"/corpus/"+language+"/"+base_url+".txt"
    
                # We save the cleartext file (only if it is not already there)
                if not os.path.isfile(base_url_filename):
                    # Then find all the urls belonging to the site :
                    for filename in glob.glob(self.main_directory+"web_content/"+base_url+"/cleartext/*.txt"):
                        #Remove the file if it is a JPEG or PDF or whatever else                        
                        keep_file=True
                        for extension in self.extensions_to_ignore:
                            if re.match(extension,filename):
                                keep_file = False
                                
                        if keep_file:
                            #First open the page :
                            page_content="" #Re-init the page content
                            file_object = open(filename,'r')
                            page_content = file_object.read()
                            file_object.close()
            
                            #We check the language for that very page (a website can have several languages)
                            if self.find_language(page_content) == language:
                                #if self.debug:
                                #    print "Adding "+filename+" to the corpus"
                                #We add the content to the total content (with a space between in case)
                                page_content = self.clean_up_double_line_returns_and_spaces(page_content)
                                base_url_file = open(base_url_filename,'a')
                                base_url_file.write(page_content)
                                base_url_file.close()
                
        #I guess that's it.
                
                
    def create_R_corpuses(self,language):
        ''' Create a corpus of files for R from the working directory.
        - Each site is a folder with its own corpora 
        Language :  Currently it is either "Danish" or "English"
        The corpuses are placed in the corpus/ folder, followed by the language'''

        #Check whether the language is supported :
        if language not in ['English','Danish']:
            print 'ERROR : Input language is incorrect : ' + language
            print 'The corpus will not be created. Exiting...'
            return

        #For each website, the corpus file corresponding will be a concatenation of all the content
        for base_url in os.listdir(self.main_directory+"web_content/"):
            # Now small test to see whether the website should be part of the corpus or not
            should_take_url = False
        
            # Could do another kind of test
            if self.is_danish_company(base_url):
                should_take_url = True

            if should_take_url:
                if self.verbose:
                    print "Adding "+base_url+" to the R corpus"
                
                # Prepare the destination file
                base_url_foldername = self.main_directory+"/corpus/"+language+"/"+base_url
    
                # We do it only if it is not already here
                if not os.path.exists(base_url_foldername):
                    #First create the folder for the website : 
                    self.create_folder(base_url_foldername)
                    # Then find all the urls belonging to the site :
                    for filename in glob.glob(self.main_directory+"web_content/"+base_url+"/cleartext/*.txt"):
                        #Remove the file if it is a JPEG or PDF or whatever else                        
                        keep_file=True
                        for extension in self.extensions_to_ignore:
                            if re.match(extension,filename):
                                keep_file = False
                                
                        if keep_file:
                            #First open the page :
                            page_content="" #Re-init the page content
                            file_object = open(filename,'r')
                            page_content = file_object.read()
                            file_object.close()
            
                            #We check the language for that very page (a website can have several languages)
                            if self.find_language(page_content) == language:
                                #We add the content to the total content (with a space between in case)
                                page_content = self.clean_up_double_line_returns_and_spaces(page_content)
                                destination_filename = filename.split("/")[-1]
                                base_url_file = open(base_url_foldername+"/"+destination_filename,'w')
                                base_url_file.write(page_content)
                                base_url_file.close()
                
        #I guess that's it.
                    
    def reset_R_corpus(self,language) :
        ''' Functiont that resets the R corpus by erasing the files for a clean
        re-creation of the corpus '''
        
        #Check whether the language is supported :
        if language not in ['English','Danish']:
            print 'ERROR : Input language is incorrect : ' + language
            print 'The corpus will not be created. Exiting...'
            return
        
        folder = self.main_directory+"corpus/"+language+"/"
        for filename in os.listdir(folder):
             os.remove(folder+ filename)
            

    def clean_up_double_line_returns_and_spaces(self,text):
        ''' Quick function for rough cleanup of the double tabs, spaces and line
        returns. Returns the clean text'''
        while '\t' in text:
             text = re.sub("\t", ' ', text)
        while '\r' in text:
             text = re.sub("\r", ' ', text)
        while '\n' in text:
             text = re.sub("\n", ' ', text)
        while "\xc2\xa0" in text:
            text = re.sub("\xc2\xa0", ' ', text)
        while '  ' in text:
            text = re.sub("  ", ' ', text)
            
#        #Now we tokenize the text in order to clean it up:
#        word_list = text.split()
#        filtered_text = ""
#        for word in word_list:
#            # isalpha() returns true if it is neither punctuation nor a number, so just words
#            if(word.isalpha()==True):
#                # In case it is an actual word, we keep it and store it to lowercase.
#                filtered_text = filtered_text + word.lower() + " "
#
#        return filtered_text

        return text
        
    

    def create_folder(self,folder_name):
        ''' Simple function taking a folder name and create it into the current working directory.'''
        try:
            if not os.path.exists(folder_name):
                if self.debug:  #Print out that we create a folder
                    print " - Creating folder : " + folder_name
                os.makedirs(folder_name)
        except:
            print "ERROR : Could not create folder '"+folder_name+"'. Expect the script to experience problems."
            
    
    
    def find_CVR_numbers(self):
        ''' Function scanning the content of text files (with .txt extension) 
        in a folder and finds out whether it contains a CVR number.
        When found, it saves a cvr.p variable in the website folder
        Returns : 
        - None if nothing found, 
        - ApS if no CVR is found but ApS is present in the site
        - A string with the CVR number if CVR is found'''

        #We try to find CVR for each scanned website : 
        for base_url in os.listdir(self.main_directory+"web_content/"):
            # Variable which remembers when we find the CVR number
            found_CVR = False
            # If CVR has been previously found, we have saved it in the file            
            if os.path.isfile(self.main_directory+"web_content/"+base_url+"/cvr.p"):
                found_CVR = True
            
            #Mask for the files that will be investigated 
            html_filename_mask = self.main_directory+"web_content/"+base_url+"/cleartext/*.txt"
            
            if not found_CVR : #CVR has never been found :             
                for filename in glob.glob(html_filename_mask):
                    #Load the file cleartext content
                    html_page_file = open(filename,'r')
                    html_page_cleartext = html_page_file.read()
                    html_page_file.close()

                    #We first find out what's the base_url (website url)
                    CVR_regex_result = re.findall("((CVR|VAT)\D{0,12}(\d{2}\D{0,2}\d{2}\D{0,2}\d{2}\D{0,2}\d{2})(\D{0,2}\d{2}\D{0,2}\d{2})?)",html_page_cleartext)
            
                    if CVR_regex_result:
                        #First results matches the whole stuff, 2nd matches the letters and 3rd matches the numbers
                        # Example : CVR_regex_result = [('CVR number 05 5048 54','CVR','05 5048 54')]
                        found_CVR_text = CVR_regex_result[0][2]
                        found_CVR = True
                        if self.verbose:  #Anouncement message 
                            print "Found CVR number : " + found_CVR_text + " for " + base_url
                        
                        #Save the cvr.p file containing the CVR number
                        filename= self.main_directory+"web_content/"+base_url+"/cvr.p"
                        pickle.dump(found_CVR_text,open(filename, "wb" ))
                        
                        break #Exit the for loop, no need to browse more of the base website pages.

            if not found_CVR :  #Did not find CVR, but maybe we have a chance with ApS or A/S
                for filename in glob.glob(html_filename_mask):#Load the file cleartext content
                    #Load the file cleartext content
                    html_page_file = open(filename,'r')
                    html_page_cleartext = html_page_file.read()
                    html_page_file.close()#Did not find CVR, but maybe we have a chance with ApS or A/S
                    
                    APS_regex_result = re.findall("(ApS|A/S)",html_page_cleartext)
                    
                    if APS_regex_result:
                        found_CVR = True
                        if self.verbose:  #Anouncement message                         
                            print "Found 'ApS' for website : " + base_url
                            
                        #create an empty aps.p file
                        open(self.main_directory+"web_content/"+base_url+"/aps.p", 'a').close()
                        break #Exit the for loop, no need to browse more of the base website pages.

        if self.verbose:  #Anouncement message 
            print "Finished finding CVR number for all websites "
        
    def has_cvr_number(self, base_url):
        '''Function that returns True is a CVR number has been found in the 
        website scan
        '''
        if os.path.isfile(self.main_directory+"web_content/"+base_url+"/cvr.p"):
            return True
        else:
            return False
            
    def is_danish_company(self, base_url):
        '''Function that returns True is a ApS or A/S or a CVR number has been 
        found on the website scan
        '''
        if os.path.isfile(self.main_directory+"web_content/"+base_url+"/cvr.p"):
            return True
        elif os.path.isfile(self.main_directory+"web_content/"+base_url+"/aps.p"):
            return True
        else:
            return False
            
    def get_CVR_number(self,base_url) :
        '''Return the CVR number of a company, else returns None'''
        if self.has_cvr_number(base_url) : 
            return pickle.load(open(self.main_directory+"web_content/"+base_url+"/cvr.p", "rb"))
        else :
            return None
            
    def clear_all_CVR_numbers(self) :
        ''' Function going around and erasing the files containing the CVR data
        in order to do a fresh re-discovery'''
        for base_url in os.listdir(self.main_directory+"web_content/"):
            # If CVR or ApS has been previously found, remove it for a fresh start
            if os.path.isfile(self.main_directory+"web_content/"+base_url+"/cvr.p"):
                if self.verbose:  #Anouncement message 
                    print "Removing CVR number for " + base_url + "..."
                os.remove(self.main_directory+"web_content/"+base_url+"/cvr.p")
            if os.path.isfile(self.main_directory+"web_content/"+base_url+"/aps.p"):
                if self.verbose:  #Anouncement message 
                    print "Removing ApS mark for " + base_url + "..."
                os.remove(self.main_directory+"web_content/"+base_url+"/aps.p")
                
    def clear_all_link_lists(self, redirect_count=None):
        ''' Function going around and erasing the files containing the list of 
        links for each website in order to do a fresh re-discovery'''
        #Redirect_count argument is optional, if not given we take the current setting
        if redirect_count is None:
            redirect_count = self.redirect_count
            
        #Do the job for every website
        for base_url in os.listdir(self.main_directory+"web_content/"):
            # If CVR or ApS has been previously found, remove it for a fresh start
            if os.path.isfile(self.main_directory+"web_content/"+base_url+"/external_urls_"+str(redirect_count)+"_redirect.p"):
                if self.verbose:  #Anouncement message 
                    print "Removing external URL list for " + base_url + "..."
                os.remove(self.main_directory+"web_content/"+base_url+"/external_urls_"+str(redirect_count)+"_redirect.p")
            
            if self.verbose:  #Anouncement message 
                    print "Removing external URL list for " + base_url + "..."
            for filename in glob.glob(self.main_directory+"web_content/"+base_url+"/linklist/*.p"):                
                os.remove(filename)
            if os.path.isfile(self.main_directory+"web_content/"+base_url+"/linklist/.p"):
                os.remove(self.main_directory+"web_content/"+base_url+"/linklist/.p")
                
    def remove_www_for_websites(self):
        ''' Function going around and renaming folders to remove www. in front 
        if there is any '''            
        #Do the job for every website
        for base_url in os.listdir(self.main_directory+"web_content/"):
            if base_url.startswith('www.'):                 
                #Rename the website iwthout the www.
                #Just remove the file if the destination already exists
                if os.path.exists(self.main_directory+"web_content/"+base_url[4:]):
                    shutil.rmtree(self.main_directory+"web_content/"+base_url)
                else:
                    os.rename(self.main_directory+"web_content/"+base_url ,self.main_directory+"web_content/"+base_url[4:])
                
    def list_danish_companies(self):
        ''' Function that returns a list object of danish companies '''
        danish_companies = []
        
        for base_url in os.listdir(self.main_directory+"web_content/"):
            if self.is_danish_company(base_url):
                danish_companies.append(base_url)
        
        return danish_companies
        
    def create_web_network_graph(self):
        ''' Functions that creates a NetworkX network visualization from the 
        explored pages '''
        #Create a directed graph
        web_graph=nx.DiGraph()
        # Add our start nodes first to the graph, as the center.
        web_graph.add_nodes_from(self.to_visit_urls[0])
        
        #Now we explore our results to add the relevant websites to the graph
        for base_url in os.listdir(self.main_directory+"web_content/"):
            if self.is_danish_company(base_url): #Only Danish companies are added : 
                web_graph.add_node(base_url)
        
        #Explore again to fill up all the edges (connections/links) between websites
        for base_url in os.listdir(self.main_directory+"web_content/"):
            if self.is_danish_company(base_url): # Same as before only Danish companies
                #Load up the links from this Danish company to other websites
                filename = self.main_directory+"web_content/"+base_url+"/external_urls_"+str(self.redirect_count)+"_redirect.p"
                external_base_urls=pickle.load(open(filename, "rb" ))
                
                #Now we also filter the list of external links
                for external_link in external_base_urls:
                    if web_graph.has_node(external_link) : # The link is also in the graph, so the connection is added
                        web_graph.add_edge(base_url,external_link)
        
        #Finally draw the network 
        #plt.figure(figsize=(120, 90))
        plt.figure(figsize=(40, 40))
        pos = nx.random_layout(web_graph)
        nx.draw_networkx_nodes(web_graph,pos,node_size=2500)
        nx.draw_networkx_nodes(web_graph,nodelist=self.to_visit_urls[0],pos=pos,node_size=3000,node_color='b')
        #nx.draw_networkx_labels(web_graph,pos,fontsize=12)
        nx.draw_networkx_edges(web_graph,pos,alpha=0.5)
        plt.savefig(self.main_directory+"DTU network.png",dpi=40)
        plt.show()
        