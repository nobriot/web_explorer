## web_explorer

Web_explorer is a small Python web crawler, retrieving text content from the
websites it visits in order to analyze it afterwards.

This software is still a beta version under development, use at your own risk :stuck_out_tongue:

This module allows to specify a list of URLs to start from as a first level. It explores the content the starting website, following a certain amount of hyperlinks within the start website (redirect_count) and subsequently visits the links to other websites found in the previous level.

### Installation
No installation is required, simply run the program with Python :
```
python main.py
```
Or the Command line tool can be used  :
```
python webExplore.py -h
```

### Example
See the file `main.py`
The script can be configured using class functions. An example is given here :
```python
#1) Declare a webExplorer instance, using 3 redirect per website and 3 depths levels
myWebExplorer = web_explorer.webExplorer()
#Alternatively, you can specify main_directory, redirect_count and exploring depth in the constructor : 
myWebExplorer = web_explorer.webExplorer("/path/where/you/want/the/files/stored/",2,3)

#2) Configure various stuffs
myWebExplorer.set_main_directory("/path/where/you/want/the/files/stored/") #If not done in the constructor
myWebExplorer.set_explore_start_points("mywebsite.com") # Here can be 1 or more websites
myWebExplorer.set_redirect_count(3) #If not done in the constructor
myWebExplorer.set_exploring_depth(3) #If not done in the constructor

#3) If stopping and resuming is intended, it is adviced to give a name to the session :
myWebExplorer.set_url_tree_back_up_filename("2017_03_my_session.p") #Assigns a name to the session
myWebExplorer.load_previous_to_visit_url() #Reloads any previous exploring infomation having the same name, if any
myWebExplorer.print_progress() #Small print for seeing where we stand in the exploration

#4) Get the explorer to work :
myWebExplorer.explore()
```

The saved websites content will be in "/path/where/you/want/the/files/stored/"

### License
The WebExplorer utility is open-source software distributed under the terms and conditions of the Free Software Foundation's [GNU General Public License](http://www.gnu.org/licenses/gpl.html). 

### TODO list
- [ ] Make the program respect /robots.txt
- [ ] Make more comprehensive functions to visualize the website network
- [ ] Find out why advancedbionics.com makes the program crash
