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

#2) Configure various stuffs
myWebExplorer.set_main_directory("/path/where/you/want/the/files/stored/")
myWebExplorer.set_explore_start_points("mywebsite.com")
myWebExplorer.set_redirect_count(3)
myWebExplorer.set_exploring_depth(3)

#3) Get the explorer to work :
myWebExplorer.explore()
```

The saved websites content will be in "/path/where/you/want/the/files/stored/"

### License
The WebExplorer utility is open-source software distributed under the terms and conditions of the Free Software Foundation's [GNU General Public License](http://www.gnu.org/licenses/gpl.html). 

### TODO list
- [x] Make a quick reset function (which resets the url_redirect_3.p files)
- [ ] Clean-up R corpus creation
- [ ] Make more comprehensive functions to visualize the website network
- [ ] Check PDF and Word files support
- [ ] Find out why advancedbionics.com makes the program crash
