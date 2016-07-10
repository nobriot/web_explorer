## web_explorer

Web_explorer is a small Python web crawler, retrieving text content from the
websites it visits in order to analyze it afterwards.

* TODO : Nice description

* Tests
* Contributors


### webExplorer() Class
This class allows to specify a list of URL to start from as a first level. It explores the content the starting website, following a certain amount of hyperlinks within the same website.

Afterwards, it stores all the hyperlinks pointing to external website.

On the next discovery level, it will take the list of external websites.

This program starts from a list of start URLs. Based on that, it explores the first URLs following a certain amount of links within the same website. it collects the text content and also all the external URLs.

### Installation
No installation is required, simply run the program with Python :
```
python main.py
```

### Example
See the file `main.py`
It takes www.dtu.dk as a starting point. Adjust the following variables in `web_explorer.py` :
```python
self.degree_depth_level = 3
self.redirect_count = 3
```

### License
The WebExplorer utility is open-source software distributed under the terms and conditions of the Free Software Foundation's [GNU General Public License](http://www.gnu.org/licenses/gpl.html).  

### TODO list
* Make possible to run the program from the terminal with arguments
* Creating R corpus from the stored website content
* Find out website text containing CVR numbers.
