# -*- coding: utf-8 -*-
"""
webExplore.py

Small command line tool for using the web_explorer python utility.
Copyright (C) 2016  Nicolas Obriot - Sabrina Woltmann

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
Created on Sun Jul 10 19:50:46 2016

@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 08/12/2016 by Nicolas Obriot
"""

#%% First section, all the different imports.
import web_explorer
import argparse

#%%  Main execution : We call the functions we want
if __name__ == '__main__':

    # First using the arg parsing
    parser = argparse.ArgumentParser(prog='webExplore.py', description='Command line utility for using the Web_explorer Program. Specify a starting point URL and various script parameters, and the script will scan the websites and store the content in the current directory or the directory that has been passed as argument.')
    parser.add_argument('start_website', nargs='+', help='Defines a starting website for the exploration. Several websites can be specified')
    parser.add_argument('-d','--directory', type=str, dest='working_directory', metavar='WorkingDirectory', help='Defines a directory to use for storing file content. Uses the current directory if this argument is not specified')
    parser.add_argument('-r', '--redirect-count', type=int, dest='redirect_count', metavar='RedirectCount', help='Defines how many redirections are followed within a website when scanning it')
    parser.add_argument('-l', '--depth-level', type=int, dest='depth_level', metavar='DepthLevel', help='Defines the level depth of the web exploration.')
    parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-n','--name', type=str, dest='exploration_name', metavar='ExplorationName', help='Defines a name for this exploration run. The same name can subsequently be used to "resume" a previously aborted exploration')
    parser.add_argument('--debug', action='store_true', help='Print out debugging messages')
    args = parser.parse_args()

    #1) Declare a webExplorer instance
    myWebExplorer = web_explorer.webExplorer()

    # 2) Change the working directory if specified
    if args.working_directory is not None:
        myWebExplorer.set_main_directory(args.working_directory)

    print "Working directory: "+ myWebExplorer.main_directory

    # 3) Add url as start point
    print "Startpoint URLs : " +  "".join(args.start_website)
    myWebExplorer.set_explore_start_points(args.start_website)

    if args.redirect_count is not None :
        print "Redirect count: " +  str(args.redirect_count)
        myWebExplorer.set_redirect_count(args.redirect_count)

    if args.depth_level is not None :
        print "Exploration depth: " +  str(args.depth_level)
        myWebExplorer.set_exploring_depth(args.depth_level)
        
    if args.exploration_name is not None :
        print "Exploration run name: " +  str(args.exploration_name)
        myWebExplorer.set_url_tree_back_up_filename(args.exploration_name)

    #Set the verbose and debugging modes
    myWebExplorer.set_verbose(args.verbose)
    myWebExplorer.set_debug(args.debug)

    # Explore the web pages :
    myWebExplorer.explore()
