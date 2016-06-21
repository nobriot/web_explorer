# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 20:50:06 2016

@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 20/06/2016 by Nicolas Obriot
"""

#%% First section, all the different imports.
import os.path, glob, os
import string
import urllib2 as url
import re
from bs4 import BeautifulSoup
import pickle

#%% Here we assign all variables for our code execution

main_directory = "/home/shared/Scripts/web_explorer/" #Working directory
DTU_url = "www.dtu.dk" # The URL we will be starting from
degree_depth_level = 3 #How many links we will follow (DTU -> site1 -> site2 is 3 levels)
redirect_count = 3 #How many links we will follow (site1.page1 -> site1.page3 -> site1.page3 is 3 levels)

# A list of websites we do not want to visit at all.
url_blacklist= ".*google\..*|.*facebook\..*|.*instagram\..*|.*youtube\..*|.*twitter\..*|.*linkedin\..*|.*youtu\.be.*|.*goo\.gl.*|.*flickr\..*" #All the websites we want to ignore

# Sets of base URLs (website url) 
DTU_base_urls=set() # Domain name part of DTU
non_DTU_base_urls = set() # Domain name not part of DTU

# different url list
to_visit_urls = [] # Which URL are yet to visit
to_visit_urls.append(set())

# Keep a dictionary making a tree of the URL discovery for us.
url_tree = dict()
url_tree_last_key_count = 0

#Dictionaries : 
danish_dict = None
english_dict = None

# CVR number registry
CVR_registry = dict()

#%% Functions
def web_explore():
    ''' Starts from DTU_url and builds an URL tree
        - finds out what is the base url (website url)
        - Open the page
        - Store the HTML content and cleartext content in a file
        - Find all the links from the page
        Returns a list object with the list of Links found on the target_url'''
    #We re declare our variables as they will get modified
    global url_tree
    global to_visit_urls
    global url_tree_last_key_count
    
    # We now look what is visited, the range is 5 as trials suggest this should be extensive enough.
    for i in range(degree_depth_level):
        for webpage in to_visit_urls[i]:
            to_visit_urls.append(set())
            found_black_listed = re.match(url_blacklist, webpage)
            if not found_black_listed:
                #Prepare the variable that we add into the future URL to visit
                external_base_urls = set()
                
                if os.path.isfile(main_directory+"web_content/"+webpage): # == The base URL has already been visited
                    filename = main_directory+"web_content/"+webpage+"/external_urls.p" 
                    external_base_urls=pickle.load(open(filename, "rb" ))
                
                
                else: # == The base URL has not been visited yet
                    
                    # 1) Create a folder for the website in the content folder. Create sub-folders "cleartext" and "linklist"
                    print "Creating folders for " + webpage
                    create_folder(main_directory+"web_content/"+webpage)
                    create_folder(main_directory+"web_content/"+webpage+"/cleartext")
                    create_folder(main_directory+"web_content/"+webpage+"/linklist") 
                    
                    # 2) Prepare a variable which contains all the external websites found from the website
                    internal_urls = set()
                    internal_urls.add("") #We put the base URL up on the list as the first internal URL to visit
                    
                    # 3) Explore within the website
                    for j in range(redirect_count): # How many times we will follow redirections within the same website
                        # Scan the URL (retrieve the content, internal links and external links)
                        print "Scanning "+webpage + " iteration " + str(j+1)
                        for internal_page in internal_urls:
                            all_links = URL_scan(webpage, internal_page)
                            
                            # Find the internal links and add them to the discovery for the next iteration
                            internal_urls=internal_urls.union(find_internal_links(webpage,all_links))
                            
                            # Find external base URLs and add them to the list of external URLs.
                            external_base_urls=external_base_urls.union(find_external_base_urls(webpage,all_links))
                            
                    # When done for the website, we save the external base URLs
                    filename = main_directory+"web_content/"+webpage+"/external_urls.p" 
                    pickle.dump(external_base_urls,open(filename, "wb" ))
                    
                to_visit_urls[i+1]=to_visit_urls[i+1].union(external_base_urls)

            print 'Finished webpage ' +webpage 
        print 'Finished web level %d' %(i) #So we know how far it went
        #save_variables(url_tree,broken_urls,url_tree_last_key_count,DTU_base_urls,non_DTU_base_urls) #Save them each time we finish


#This is the function to load the page, save them and find child links:
def URL_scan(base_url, internal_page): 
    ''' Takes the base_url and internal_page performs the following actions:
        - Determine wether the URL belongs to DTU    
        - Determine whether the URL has already been visited.
        - Open the page
        - Store the cleartext content in a file (cleaned from the HTML markup) if the page is not a DTU page
        - Find all the links from the page (both internal and exteral)
        Returns a list object with the list of Links found on the visited page'''
    # Prepare the file name for the corresponding website
    filename = main_directory+"web_content/"+base_url+"/cleartext/"+re.sub("/", '_', internal_page)+".txt"
     
    # If the page has not been visited, we just visit it
    if not os.path.isfile(filename):
        #First find whether it is a DTU page and store the base URL
        url_is_DTU = re.search('.*\.dtu.*', base_url)
        
        #Remove trailing "/"    
        while internal_page[-1:] == "/" :
            internal_page = internal_page[:-1]

        try:
            # we open the URL and read the content
            #print " - Hit http://"+base_url+"/"+internal_page
            html_response= url.urlopen("http://"+base_url+"/"+internal_page)
            html_text= html_response.read()
            
            # We replace all empty HTML tags with a space inside:
            html_text = html_text.replace(">", "> ")

            # We use the beautiful soup to get the text from HTML : 
            soup = get_clean_text_from_html_content(html_text)
            
            # If URL is DTU, just create a placeholder file in order not to revisit the same page later
            if url_is_DTU:
                pagefile = open(filename,'w+')
                pagefile.close()
            else: # We save the page text content
                pagefile = open(filename,'w')
                pagefile.write(soup.get_text().encode('UTF-8'))
                pagefile.close()

            #Find all the links in the webpage
            link_list = find_child_links_from_html_soup(soup,base_url)
            
            # Save the list of links in the folder 
            #print "- Saving file " + filename
            filename = main_directory+"web_content/"+base_url+"/linklist/"+re.sub("/", '_', internal_page)+".p"   
            pickle.dump(link_list,open(filename, "wb" ))

            return link_list     
        except: #In case the URL could not be opened, we just return nothing
            create_dummy_files(base_url, internal_page)
            return []
    else:
        #Load the list of links from the page in the folder
        filename = main_directory+"web_content/"+base_url+"/linklist/"+re.sub("/", '_', internal_page)+".p"   
        print "- Opening file " + filename
        link_list = pickle.load(open(filename, "rb" ))
        return link_list

def create_dummy_files(base_url, internal_page):
    ''' Create empty files in the web content, so that broken URL are not tried several times '''
    filename = main_directory+"web_content/"+base_url+"/cleartext/"+re.sub("/", '_', internal_page)+".txt"
    pagefile = open(filename,'w+')
    pagefile.close()
    filename = main_directory+"web_content/"+base_url+"/linklist/"+re.sub("/", '_', internal_page)+".p" 
    pagefile = open(filename,'w+')
    pagefile.close()


# function to save the variables, so it can load them after interruption 
def save_variables(url_tree,broken_urls,url_tree_last_key_count,DTU_base_urls,non_DTU_base_urls,number=None):
    ''' This function saves the 3 given variables into the variable folder.
    if number is specified, it will save the variables appending the number 
    at the end'''
    if not number:
        #we store them all                
        pickle.dump(url_tree,open(main_directory+"/variables/url_tree.p", "wb" ))
        pickle.dump(broken_urls,open (main_directory+'/variables/broken_urls.p', 'wb'))
        pickle.dump(DTU_base_urls,open (main_directory+'/variables/DTU_base_urls.p', 'wb'))
        pickle.dump(non_DTU_base_urls,open (main_directory+'/variables/non_DTU_base_urls.p', 'wb'))
        pickle.dump(url_tree_last_key_count,open (main_directory+'/variables/url_tree_last_key_count.p', 'wb'))
    else:
        #we store a special backup
        pickle.dump(url_tree,open(main_directory+"/variables/backup/url_tree"+str(number)+".p", "wb" ))
        pickle.dump(broken_urls,open (main_directory+"/variables/backup/broken_urls"+str(number)+".p", 'wb'))
        pickle.dump(DTU_base_urls,open (main_directory+"/variables/backup/DTU_base_urls"+str(number)+".p", 'wb'))
        pickle.dump(non_DTU_base_urls,open (main_directory+"/variables/backup/non_DTU_base_urls"+str(number)+".p", 'wb'))
        pickle.dump(url_tree_last_key_count,open (main_directory+"/variables/backup/url_tree_last_key_count"+str(number)+".p", 'wb'))

# function to save the variables, so it can load them after interruption 
def restore_variables():
    ''' This function restore the 3 variables: 
    - url_tree
    - broken_urls
    - url_tree_last_key_count
    from the variable folder.'''
    global url_tree
    global broken_urls
    global non_DTU_base_urls    
    global DTU_base_urls
    global url_tree_last_key_count
    
    #we restore the latest saving of them 
    if os.path.isfile(main_directory+"/variables/url_tree.p"):
        url_tree=pickle.load(open(main_directory+"/variables/url_tree.p", "rb" ))
    if os.path.isfile(main_directory+"/variables/broken_urls.p"):
        broken_urls=pickle.load(open(main_directory+"/variables/broken_urls.p", "rb" ))
    if os.path.isfile(main_directory+"/variables/DTU_base_urls.p"):
        DTU_base_urls=pickle.load(open(main_directory+"/variables/DTU_base_urls.p", "rb" ))
    if os.path.isfile(main_directory+"/variables/non_DTU_base_urls.p"):
        non_DTU_base_urls=pickle.load(open(main_directory+"/variables/non_DTU_base_urls.p", "rb" ))
    if os.path.isfile(main_directory+"/variables/url_tree_last_key_count.p"):
        url_tree_last_key_count=pickle.load(open(main_directory+"/variables/url_tree_last_key_count.p", "rb" ))

# function for finding which website belongs a URL
def find_base_url_and_DTU(target_url,find_dtu = False):
    ''' Takes the target_url and finds out what is the base url (website url)
    i.e. https://docs.python.org/2/library/ gives https://docs.python.org/
    and then sorts it in a set depending on whether it contains DTU in the 
    base URL. 
    - DTU base URL are stored in the set : DTU_base_urls
    - other URls are stored in the set : non_DTU_base_urls 
    This function will create an error if the sets are not declared before
    returns the base_url'''
    #We will modify some global variable here : 
    global DTU_base_urls
    global non_DTU_base_urls
   
    #We first find out what's the base_url (website url)
    found_base_link = re.match('^https?://.*?/|^https?://.*?', target_url)
 
    #We add the finding either DTU_base_urls or non_DTU_base_urls
    if found_base_link:
        found_base_link = found_base_link.group(0)
        found_base_link = string.replace(found_base_link,"https:","http:")

        if find_dtu:
            url_is_DTU = re.search('.*\.dtu.*', found_base_link)
            if url_is_DTU:
                DTU_base_urls.add(found_base_link)
            else:
                non_DTU_base_urls.add(found_base_link)
        return found_base_link
    else:
        return None
        
# function for finding which links belong to the given base URL
def find_internal_links(webpage,all_links):
    ''' Takes a base URL and a list of links found in the HREF tags.
    returns all the links that belong to the same webpage.'''
    
    internal_links = []    
    for link in all_links:
        #We first find out what's the base_url (website url)
        if len(link)>0 and len(link)<200: #We throw away links with more than 200 chars
            if link[0] == "/" : # If it starts with a /, it is a relative path
                #Remove trailing "/"    
                while link[0] == "/" :
                    link = link[1:]
                internal_links.append(link) 
                
            else: # It must be an absolute path, we need to pull out the base URL
                #Find what is the website and add the link in the list IIF it is within the same website
                found_base_url = re.match('^https?://.*?/|^https?://.*?|^https?://.*?\?|^.*?/|^.*?\?|^.*?', link)
                if found_base_url:
                    found_base_url = found_base_url.group(0)
                    found_base_url = found_base_url.replace('https://','')
                    found_base_url = found_base_url.replace('http://','')
                    found_base_url = found_base_url.replace(':80','')
                    found_base_url = found_base_url.replace(':443','')
                    found_base_url = found_base_url.replace('/','')
                    found_base_url = found_base_url.replace('?','')
                    
                    if webpage == found_base_url :
                        relative_path = link.replace(webpage,'')
                        relative_path = relative_path.replace('https://','')
                        relative_path = relative_path.replace('http://','')
                        relative_path = relative_path.replace(':80','')
                        relative_path = relative_path.replace(':443','')
                        internal_links.append(relative_path)

    #Clean up all the double / from paths
    for i in range(len(internal_links)):
        while '//' in internal_links[i]:
            internal_links[i]=internal_links[i].replace('//','/')
            
    return internal_links


# function for finding which links belong to the given base URL
def find_external_base_urls(webpage,all_links):
    ''' Takes a base URL and a list of links found in the HREF tags.
    returns all the links that belong to the same webpage.'''
    
    external_links = []    
    for link in all_links:
        #We first find out what's the base_url (website url)
        if len(link)>0 and len(link)<200: #We throw away links with more than 200 chars
            if link[0] != "/" : # If it starts with a /, it is a relative path, we do not want that
                #Find what is the website for that link
                found_base_url = re.match('^https?://.*?/|^https?://.*?|^https?://.*?\?|^.*?/|^.*?\?|^.*?', link)
                if found_base_url:
                    found_base_url = found_base_url.group(0)
                    found_base_url = found_base_url.replace('https://','')
                    found_base_url = found_base_url.replace('http://','')
                    found_base_url = found_base_url.replace(':80','')
                    found_base_url = found_base_url.replace(':443','')
                    found_base_url = found_base_url.replace('/','')
                    found_base_url = found_base_url.replace('?','')
                    
                    #We add it to the list if it is a different webpage
                    if webpage != found_base_url :
                        external_links.append(found_base_url)
    
    while '' in external_links:
        external_links.remove('')
            
    return external_links

        
def get_clean_text_from_html_content(html_text):
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

def find_child_links_from_html_soup(html_soup,target_url):
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


def has_been_visited(target_url):
    ''' Checks whether there is a file the web_content folder and returns true
    returns false if not.'''
    html_filename = main_directory+"web_content/cleartext/"+re.sub("/", '_', target_url)+".txt"
    if os.path.isfile(html_filename):
        return True
    else:
        return False

def get_child_links_from_file(target_url):
    ''' This function finds the child links from the HTML content of the page
    stored earlier.'''
    html_filename = main_directory+"web_content/html/"+re.sub("/", '_', target_url)+".html"

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
    create_temp_file(target_url)
    
    #Finally return the list
    return child_links
    

def update_url_tree(webpage,child_links):
    ''' Update the URL tree by adding all the base URLs in a list at the 
    webpage index. Ich bin Sabi moin moin!'''
    global url_tree
    
    #Now update the URL tree, only with baselinks
    webpage_base_url = find_base_url_and_DTU(webpage)
    
    if webpage_base_url not in url_tree.keys(): #fisrt time we find a base URL, start with an emptpy list in the dict
        url_tree[webpage_base_url] = []
    
    for child_url in child_links:          
        url_tree[webpage_base_url].append(find_base_url_and_DTU(child_url))
    
    #Clean up the URL tree of doubles and None objects                
    url_tree[webpage_base_url] = list(set(url_tree[webpage_base_url]))
    if None in url_tree[webpage_base_url]:
        url_tree[webpage_base_url].remove(None)


def find_language(text):
    ''' Find whether the text is in English, Danish or unknown by looking up 
    the percentage of words belonging to Enlish and Danish. A language is 
    matched when more than 70% of the words are identified belonging to a 
    language.
    Returns "English", "Danish" or None'''
    #Prepare the dictionaries.
    global english_dict   
    global danish_dict
    
    #If the dicts variables are not loaded from the files, we do. 
    #As they are global variables, it will load the dicts only once
    if english_dict is None:
        english_dict = set(word.strip().lower() for word in open(main_directory+"dictionaries/US.dic"))
    if danish_dict is None:
        danish_dict = set(word.strip().lower() for word in open(main_directory+"dictionaries/dk.dic"))
    
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
            if word.lower() in english_dict:
                english_word_count +=1
            if word.lower() in danish_dict:
                danish_word_count +=1
                
        #Look at the returns when we are done
        total_words = len(word_list)
        
        if 0: #Debug : Set 1 for seeing the details when calling the function 
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


def create_R_corpus(language):
    ''' Create a corpus of files for R from the url_tree variable.
    - language parameter has to a supported language by find_language(). Currently it is
    either "Danish" or "English"
    The corpus is placed in the corpus/ folder, followed by the language'''
    
    #Check whether the language is supported : 
    if language not in ['English','Danish']:
        print('Input language is incorrect')
        return
    
    #We make the process for each Base URL : 
    for base_url in url_tree.keys():
        should_take_url = True
        #if CVR_registry[base_url] == '30060946' or 'dtu' in base_url:
        #if 'dtu' in base_url:
        #     should_take_url = False
        
        if should_take_url:
            print "Base URL is : "+base_url
            #First we create a master text in which we will add all the content for the website
            base_url_total_content = ""
            
            # Then find all the urls belonging to the site :
            for filename in glob.glob(main_directory+"web_content/cleartext/"+re.sub("/", '_', base_url)+"*"):
                #First open the page :             
                file_object = open(filename,'r')
                page_content = file_object.read()
                file_object.close()
                
                #We check the language
                if find_language(page_content) == language:
                    #We add the content to the total content (with a space between in case)
                    base_url_total_content = base_url_total_content +" "+ page_content
    
            #When we saw all the pages, we save the text file for the base URL.
            base_url = base_url.replace('http://www.','')
            base_url = base_url.replace('https://www.','')
            base_url = base_url.replace('http://','')
            base_url = base_url.replace('https://','')
            base_url_filename = main_directory+"web_content/corpus/"+language+"/"+re.sub("/", '', base_url)+".txt"
    
            # We save the cleartext file (only if it is not already there)
            if not os.path.isfile(base_url_filename) and base_url_total_content != "":
                base_url_total_content = clean_up_double_line_returns_and_spaces(base_url_total_content)
                base_url_file = open(base_url_filename,'w')
                base_url_file.write(base_url_total_content)
                base_url_file.close()
    #I guess that's it.

def clean_up_double_line_returns_and_spaces(text):
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
    
    #Now we tokenize the text in order to clean it up: 
    word_list = text.split()
    filtered_text = ""
    for word in word_list:
        # isalpha() returns true if it is neither punctuation nor a number, so just words
        if(word.isalpha()==True):
            # In case it is an actual word, we keep it and store it to lowercase.
            filtered_text = filtered_text + word.lower() + " "
    
    return filtered_text


def should_take_children_from_file(webpage):
    ''' Returns True if the page has been visited in the past and the 
    content is stored in the webpages files but has not been taken yet in the 
    run for checking on the children URL.
    Returns False if the URL children have already been added to 
    the "to_visit_urls" list'''
    html_filename = main_directory+"web_content/temp/"+re.sub("/", '_', webpage)+".txt"
    if os.path.isfile(html_filename):
        return False
    else:
        return True


def find_CVR_number(target_base_url):
    ''' Takes a base URL and find all the files that have been scanned
	for finding the CVR number. Returns the CVR when found, else None.'''
    #We declare our variables.
    found_CVR = None
    html_filename_mask = main_directory+"web_content/corpus/*/"+re.sub("/", '_', target_base_url)+"*"
    
    #We repeat for each file starting with the base URL.
    for filename in glob.glob(html_filename_mask):#Load the file cleartext content
        html_page_file = open(filename,'r')
        html_page_cleartext = html_page_file.read()
        html_page_file.close()
        
        #We first find out what's the base_url (website url)
        CVR_regex_result = re.findall("((CVR|VAT)\D{0,12}(\d{2}\D{0,2}\d{2}\D{0,2}\d{2}\D{0,2}\d{2})(\D{0,2}\d{2}\D{0,2}\d{2})?)",html_page_cleartext)
            
        if CVR_regex_result:
    		#First results matches the whole stuff, 2nd matches the letters and 3rd matches the numbers
    		# Example : CVR_regex_result = [('CVR number 05 5048 54','CVR','05 5048 54')]
    		found_CVR = CVR_regex_result[0][2]
    		print "Found CVR number : " + found_CVR + " for " + target_base_url
    		break #Exit the for loop, no need to browse more of the base website pages.
    
    if not found_CVR :  #Did not find CVR, but maybe we have a chance with ApS or A/S
        for filename in glob.glob(html_filename_mask):#Load the file cleartext content
            html_page_file = open(filename,'r')
            html_page_cleartext = html_page_file.read()
            html_page_file.close()#Did not find CVR, but maybe we have a chance with ApS or A/S
            APS_regex_result = re.findall("(ApS|A/S)",html_page_cleartext)
            if APS_regex_result:
                found_CVR = "ApS"
                print "Found ApS for website : " + target_base_url
                break
               
    #Return the found CVR number.
    return found_CVR


def update_CVR_registry():
    ''' Uses the find_CVR_number for each of the Base_URL in the url_tree and
    update the CVR_registry dict with the found CVRs.'''
    global CVR_registry
    global url_tree
    
    for base_url in url_tree:
        found_CVR = find_CVR_number(base_url)
        if found_CVR:
            CVR_registry[base_url] = found_CVR.replace(" ","")
        else:
            CVR_registry[base_url] = "Not found"


def create_folder(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except:
        print "Could not create folder '"+folder_name+"'. Expect the script to experience problems."

#%%  Main execution : We call the functions we want
# 1) Change the working directory
print "1) changing working directory: "+main_directory
os.chdir(main_directory)

# 2) Resume where we were by restoring the variables
#print "2) restoring variables"
#restore_variables()

# 3) Add DTU url as start point
print "3) Adding startpoint URLs :" + DTU_url
to_visit_urls[0].add(DTU_url)

# 4) Continue to explore the webpages until we reached degree_depth_level
print "4) Exploring web links: this will take VERY long (weeks)"
web_explore()

# 6) Create a R corpus for a certain language - Stored in "main_directory"/web_content/corpus/"Language"
if 0 :
    print "6) Creating a corpus"
    create_R_corpus("English") #Remember to erase the previous corpus if you want to update the existing pages
    create_R_corpus("Danish")

# 7) Find the CVR numbers we can from the corpuses.
# It is advised to have a Danish corpus for finding CVR numbers, as they usually are not mentionned in English.
if 0:
    print "7) Look up the CVR numbers"
    update_CVR_registry() 

