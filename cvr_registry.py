# -*- coding: utf-8 -*-
"""
cvr_registry.py

Small Python utility used for CVR (Company civil registration in Denmark) number
detection within a text.
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

Created on Jul 10 19:40:00 2016

@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 10/07/2016 by Nicolas Obriot
"""

# Class definition : CVRRegistry
class CVRRegistry:

    #Constructor : variable init when creating the object. Initializing variables
    def __init__(self):
        self.registry = dict()

    def find_CVR_number(self,target_base_url):
        ''' Takes a base URL and find all the files that have been scanned
    	for finding the CVR number. Returns the CVR when found, else None.'''
        #We declare our variables.
        found_CVR = None
        html_filename_mask = self.main_directory+"web_content/corpus/*/"+re.sub("/", '_', target_base_url)+"*"

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


    def update_registry(self):
        ''' Uses the find_CVR_number for each of the Base_URL in the url_tree and
        update the CVR_registry dict with the found CVRs.'''

        for base_url in url_tree:
            found_CVR = self.find_CVR_number(base_url)
            if found_CVR:
                self.CVR_registry[base_url] = found_CVR.replace(" ","")
            else:
                self.CVR_registry[base_url] = "Not found"
