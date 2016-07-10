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
import argparse

#%%  Main execution : We call the functions we want
if __name__ == '__main__':
    print "Hello, I am the main"

    #1) Declare a webExplorer instance, using 3 redirect per website and 3 depths levels
    myWebExplorer = web_explorer.webExplorer(3,3)

    # 2) Change the working directory
    myWebExplorer.set_main_directory("/home/shared/Scripts/web_explorer/")
    print "1) Changing working directory: "+ myWebExplorer.main_directory

    # 3) Add DTU url as start point
    DTU_url = "www.dtu.dk"
    print "2) Adding startpoint URLs : " + DTU_url
    myWebExplorer.set_explore_start_points(DTU_url)

    #myWebExplorer.set_redirect_count(3)
    #myWebExplorer.set_exploring_depth(3)

    # 4) Continue to explore the webpages until we reached degree_depth_level
    print "3) Exploring web links: this will take VERY long (weeks)"
    myWebExplorer.explore()

    # 5) Create a R corpus for a certain language - Stored in "main_directory"/web_content/corpus/"Language"
    if 0 :
        print "4) Creating a corpus"
        #create_R_corpus("English") #Remember to erase the previous corpus if you want to update the existing pages
        #create_R_corpus("Danish")

    # 6) Find the CVR numbers we can from the corpuses.
    # It is advised to have a Danish corpus for finding CVR numbers, as they usually are not mentionned in English.
    if 0:
        print "5) Look up the CVR numbers"
        #update_CVR_registry()
