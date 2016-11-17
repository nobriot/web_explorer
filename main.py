# -*- coding: utf-8 -*-
"""
main.py

Short tool for using the web_explorer python utility.
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
Created on Mon Feb 22 20:50:06 2016

@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 10/07/2016 by Nicolas Obriot
"""

#%% First section, all the different imports.
import web_explorer

#%%  Main execution : We call the functions we want
if __name__ == '__main__':
    print "Hello, I am the main"

    #1) Declare a webExplorer instance, using 3 redirect per website and 3 depths levels
    myWebExplorer = web_explorer.webExplorer("/home/shared/Scripts/web_explorer/",3,3)

    # 2) Add DTU url as start point
    DTU_url = "dtu.dk"
    print "1) Adding startpoint URLs : " + DTU_url
    myWebExplorer.set_explore_start_points(DTU_url)

    #Exploring configuration
    myWebExplorer.set_redirect_count(3)
    myWebExplorer.set_exploring_depth(3)
    
    #Reset previous result : 
    #myWebExplorer.clear_all_link_lists()
    #myWebExplorer.remove_www_for_websites()
    
    # Verbose/debug configuration : 
    myWebExplorer.set_verbose(True)
    myWebExplorer.set_debug(True)

    # 3) Continue to explore the webpages until we reached degree_depth_level
    #print "2) Exploring web links: this will take VERY long (weeks)"
    #myWebExplorer.explore()

    # 4) Find the CVR numbers we can from the corpuses.
    #print "4) Look up the CVR numbers"
    #myWebExplorer.clear_all_CVR_numbers()
    #myWebExplorer.find_CVR_numbers()

    # 5) Create a R corpus for a certain language - Stored in "main_directory"/web_content/corpus/"Language"
    print "5) Creating a corpus"
    #myWebExplorer.reset_R_corpus("English")    
    #myWebExplorer.create_R_corpuses("English") #Remember to erase the previous corpus if you want to update the existing pages
    #myWebExplorer.create_R_corpus("Danish")
    
    # 6) Play with the resust : 
    #myWebExplorer.list_danish_companies()
    
    #7) Create a network graph
    #myWebExplorer.create_web_network_graph()