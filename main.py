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

    ## 1) Declare a webExplorer instance, using 3 redirect per website and 3 depths levels
    myWebExplorer = web_explorer.webExplorer("/home/shared/Scripts/web_explorer/",3,3)
    
    ## 2) Add DTU url as start point
    #url_start_list = "dtu.dk"
    url_start_list = ["dtu.dk","http://www.glycom.com/","https://www.ibm.com/dk-da/","https://www.siemens.com/dk/da/home.html", "http://www.oestkraft.dk/", "http://www.emd.dk/","http://www.omicia.com/","http://www.itu-bd.dk/","http://www.centerforlys.dk/index2.php","http://dk.madebydelta.com/", "http://isc-konstanz.de/" , "https://alexandra.dk/dk", "http://www.agrotech.dk/", "http://www.finansraadet.dk/en/Pages/mainpage.aspx", "http://www.bila.dk/", "http://www.globalcastings.com/", "http://www.largestcompanies.com/company/Damrc-FMBA-2576623/ranking", "http://en.cnconsite.dk/","http://www.globalfoundries.com/", "http://www.systra.co.uk/", "http://www.xellia.com/", "https://www.beiresources.org/About/BEIResources.aspx", "http://www.femern.info/en/", "http://startvaekst.dk/vhsjaelland.dk","http://www.novozymes.com","http://www.metricorr.com/","http://www.cowi.dk/menu/home/", "https://deas.dk/", "http://livingstrategy.dk/","http://ekolab.dk/", "http://www.teknologisk.dk/", "http://www.sony.com/", "http://www.cmcbio.com/", "http://windpower.org/","http://www.ge.com/dk/","http://www.hotswap.eu/","http://www.topsoe.com/","http://www.rockwool.com/","http://www.borregaard.no/", "http://www.arla.com/","http://www.kmc.dk/", "http://hamletprotein.com/en/", "https://forcetechnology.com", "http://www.agropark.dk/","http://www.teknologisk.dk/","http://www.agnion.net", "http://www.dgc.eu", "http://aquaporin.dk/", "http://energinet.dk/EN/Sider/default.aspx", "http://www.dongenergy.com", "http://energinet.dk/EN/Sider/default.aspx","http://www.dfm.dtu.dk/", "http://www.powercurve.dk/", "https://www.terma.com/", "http://www.dfm.dtu.dk/", "http://nordicpowerconverters.com/Frontpage", "http://www.dovista.com", "http://simplight.co/", "http://www.3xn.dk/#/","http://www.vestas.com/","http://littlesmartthings.com/", "https://www.catie.ac.cr/en/", "http://www.freightfarms.com/#leafygreenmachine", "http://www.agrimetis.com/","http://jomitek.dk/en/","http://www.amadix.com/", "http://daposy.com/", "http://novonordiskfonden.dk/da", "http://www.inomega3.dk/", "http://www.danforel.com/", "http://hesalight.com/about-us/" , "http://www.bosch.nl/en/nl/startpage_13/country-landingpage.php","http://www.moveinnovation.dk/", "http://www.lonza.com/", "http://nordicinnovation.org/", "http://www.white.dk/","http://www.helenhard.no/","http://codland.is/", "http://vandkunsten.com/","http://www.ramboll.com/", "www.spesohealth.com", "https://www.omicsonline.org/","http://rencat.net/index.html","http://www.kopenhagenfur.com/", "http://www.nikon.com/", "http://www.ramboll.dk/om-os/ramboll-fonden", "http://www.bms.com/pages/default.aspx", "http://www.twincore.de/en/home/", "https://www.thermofisher.com/dk/en/home/life-science/lab-plasticware-supplies/nalgene-labware.html", "http://www.maerskoil.com/Pages/default.aspx", "http://www.elplatek.dk/","http://greenhydrogen.dk/","http://www.widex.dk", "http://bio-aqua.dk/","http://www.lmwindpower.com/", "http://www.metal-supply.dk/company/view/21702/eltronic_as", "https://fiberline.com/","https://www.nestecinc.com/", "http://www.metal-supply.dk/company/view/21702/eltronic_as", "http://www.danaseals.dk/","http://www.meabco.com/", "http://www.inra-transfert.fr/fr/", "http://www.pharmacosmos.com/", "https://catalog.coriell.org/1/CoriellCourses","https://www.accenture.com/","http://nordicpowerconverters.com", "http://www.codejudge.net/", "http://www.geoteric.com/", "http://www.eldor.no/", "http://www.eliis.fr/content/contact-0", "http://www.biolinscientific.com/", "http://www.cobham.com/communications-and-connectivity/satcom/", "http://www.kosancrisplant.com/en/home/", "http://www.movingenergy.dk/","http://www.analogic.com/", "http://bkultrasound.com/","http://www.cobham.com/communications-and-connectivity/satcom/","http://mekoprint.dk/forside.aspx", "http://cleancluster.dk/", "http://di.dk/Pages/Forsiden.aspx","http://www.danfoss.dk/home/#/", "http://www.grundfos.com/", "http://www.topsoe.com/", "http://www.siemens.com/global/en/home/markets/wind.html","https://www.qualiware.com/","http://biosintel.com/","http://dgih.dk/", "http://www.babcock.com/Pages/default.aspx","http://www.sintef.no/Fiskeri-og-havbruk-AS/","http://www.cidetec.es/cas/index.aspx", "http://www.cerpotech.com/","http://www.sintef.no/Fiskeri-og-havbruk-AS/","http://www.pfizer.dk/", "https://sbtaqua.com/","http://www.medtronic.dk/", "http://www.gsk.com/en-gb/research/", "http://www.tennet.eu/de/","http://www.kl.dk/Menu---fallback/Energiklyngecenter-Sjalland-id180611/","http://www.reka.com/en/","http://www.1stmile.dk/","http://www.statoil.com/no/Pages/default.aspx","http://www.optosecurity.com/", "http://nordicpowerconverters.com/Frontpage","http://copenhageneventcompany.com/default.aspx","http://www.danskenergi.dk/", "http://www.chr-hansen.com/en","https://www.cpkelco.com/", "http://www.smithinnovation.dk/","http://www.plh.dk/", "http://www.brplast.dk/", "http://www.sustainair.dk/", "http://greenday.ebmpapst.com/denmark/", "https://www.healthcare.siemens.com/","http://www.caltech.edu/","https://www.ikonscience.com/", "http://www.cgg.com/en/What-We-Do/GeoSoftware/Solutions/HampsonRussell", "http://jgi.doe.gov/","https://www.nimblestorage.com/", "http://www.nykredit.dk/#!/","https://www.signicat.com/", "http://www.dfds.com/","http://riemann.io/", "http://dcum.dk/","http://www.harptechnologies.com/", "http://dieselturbo-north-america.man.eu/", "http://www.lyngsoe.com/About-us.aspx", "http://www.mellanox.com/","https://www.ashrae.org/", "http://www.roche.com/research_and_development.htm", "http://aditechcorp.com/?lang=en","http://cemitec.com/en/home/", "http://www.danisco.com/food-beverages/", "http://www.mcmelectronics.com/", "http://fertin.com/", "http://www.nuvve.com/","http://www.bygdeforskning.no/en","http://www.rdas.dk/en/","http://www.hitachi.com/","http://www.nssmc.com/en/","http://www.ntt.co.jp/index_e.html", "http://www.fujikura.com/", "http://www.coriant.com/" ,"http://www.alfalaval.com/","https://www.convatec.dk/", "http://www.nissan-global.com/EN/index.html", "http://www.wavepiston.dk/", "https://www.avantium.com/", "http://www.magneto.nl/en/", "http://www.gensoric.com/","http://www.wavepiston.dk/", "http://www.fsenergy.dk/", "https://www.lokalebasen.dk/","http://www.epinionglobal.com/da/forside","http://en.dbi-net.dk/", "http://www.datatransparencylab.org/", "http://www.unisense.com/","https://fracturecode.com/","http://www.slb.com/","http://www.cancer.dk/", "http://hh-intellitech.dk/en/", "http://www.danishfarmdesign.dk/", "http://www.comfil.biz/", "https://configit.com/", "https://www.lf.dk/", "https://www.moviatrafik.dk/","http://glaucus.dk/", "http://www.teradata.dk/?LangType=1030&LangSelect=true", "https://www.evalueserve.com/", "http://www.simtech.de/index.php/de/", "http://www.n-o-s.eu/", "http://prozyme.com/","http://www.wormdevelopment.com/", "http://delawarecompanysearch.com/sira-pharmaceuticals-inc", "http://www.leo-pharma.dk/","http://www.f-star.com/", "http://www.wormdevelopment.com/", "http://www.msystem.dk/", "http://csr.astrium.eads.net/", "https://www.dovregroup.com/", "https://www.dnvgl.com/energy/index.html", "http://www.steno.dk/", "http://www.dendanskemaritimefond.dk/", "http://www.ecophon.com/dk", "http://acornprojects.dk/", "http://www.landia.dk/", "http://www.interacoustics.com/", "http://vildlaks.dk/velkommen/", "http://acornprojects.dk/","http://www.landia.dk/", "http://www.mercator-ocean.fr/", "http://www.unibio.dk/","http://www.symbiosecenter.dk/", "http://www.forwind.net/","https://www.mellanox.com/", "https://idt-biologika.com/", "http://www.gram-equipment.com/", "http://neontherapeutics.com/", "https://tegvirginia.com/", "https://www.suragus.com/en/", "http://www.aixtron.com/en/home/","http://polycsp.com/", "http://www.arosteknik.dk", "http://www.cenergia.dk/da/","http://www.cenergia.dk/da/", "http://www.energyxxi.com/", "http://www.inqpharm.com/","http://hpnow.dk/", "http://biosyntia.com/", "http://www.uptime.dk/2-om-uptime-it-aps.html","http://www.tekno.dk/","http://www.daposy.com/", "http://www.e4sma.com/en/home/","http://www.alk-abello.com/DK/Pages/AffWelcome.aspx", "http://www.dgc.dk/", "http://customercarecontacts.com/microsoft-denmark-office-contact-phone-address/", "http://www.elcogen.com/en/", "http://www.bluegen.de/de/start/","http://www.dallenergy.com/","http://www.elster-instromet.dk/da/index", "http://www.dinex.dk/en/", "http://ctr.dk/", "http://www.veks.dk/da ","http://www.hofor.dk/om-os/organisation/net/hofor-fjernvarme-ps/","https://www.dhi.org/","http://po3.dk/", "http://www.bioceval.dk/bc/sonderseiten/hjem/",  "http://nordsoenforskerpark.dk/" ]
    
    print "1) Adding startpoint URLs ... "# + url_start_list
    myWebExplorer.set_explore_start_points(url_start_list)

    ## Exploring configuration
    myWebExplorer.set_redirect_count(3)
    myWebExplorer.set_exploring_depth(3)
    myWebExplorer.set_exploring_depth(2) #Use this one for suggested websites
    
    ## Reset previous result : 
    #myWebExplorer.clear_all_link_lists()
    #myWebExplorer.remove_www_for_websites()
    
    ## Verbose/debug configuration : 
    myWebExplorer.set_verbose(True)
    myWebExplorer.set_debug(True)
    
    ## Setting a filename for saving the URL tree
    #myWebExplorer.set_url_tree_back_up_filename("web_crawler_dtu.p")
    myWebExplorer.set_url_tree_back_up_filename("suggested_url_dicovery_tree.p")

    ## 3) Continue to explore the webpages until we reached degree_depth_level
    print "2) Exploring web links: this will take VERY long (weeks)"
    myWebExplorer.explore()

    ## 4) Find the CVR numbers we can from the corpuses.
    #print "4) Look up the CVR numbers"
    #myWebExplorer.clear_all_CVR_numbers()
    #myWebExplorer.find_CVR_numbers()

    ## 5) Create a R corpus for a certain language - Stored in "main_directory"/web_content/corpus/"Language"
    #print "5) Creating a corpus"
    #myWebExplorer.reset_R_corpus("English")    
    #myWebExplorer.create_R_corpuses("English") #Remember to erase the previous corpus if you want to update the existing pages
    #myWebExplorer.create_R_corpus("Danish")
    
    ## 6) Play with the resust : 
    #myWebExplorer.list_danish_companies()
    
    ## 7) Create a network graph
    #myWebExplorer.create_web_network_graph()
    
    ## 8) Create a GEPHI csv 
    myWebExplorer.load_previous_to_visit_url()
    myWebExplorer.export_csv_dataset_for_GEPHI(True)
    
    
    
#Couple of notes :
#myWebExplorer = webExplorer("/home/shared/Scripts/web_explorer/",1,1)
#myWebExplorer.set_verbose(True)
#myWebExplorer.set_debug(True)
#myWebExplorer.URL_scan("kom.aau.dk","group/12gr1010/Report.pdf")
