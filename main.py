# -*- coding: utf-8 -*-
"""
main.py

Short tool for using the web_explorer python utility.
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
Created on Mon Feb 22 20:50:06 2016

@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 08/12/2016 by Nicolas Obriot
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
    #TODO: Add the option to take a CSV file for input
    url_start_list = ["http://www.glycom.com","https://www.ibm.com","https://www.siemens.com/dk/da/home.html","http://www.emd.dk/","http://www.omicia.com/","http://www.itu-bd.dk/","http://www.centerforlys.dk/index2.php","http://isc-konstanz.de/","http://www.agrotech.dk/","https://alexandra.dk","http://www.bila.dk/","http://www.globalfoundries.com/","http://www.systra.co.uk/","http://www.xellia.com/","https://www.beiresources.org/About/BEIResources.aspx","http://www.femern.info/en/","http://www.novozymes.com","http://www.metricorr.com/","https://deas.dk/","http://www.sony.com/","http://www.cmcbio.com/","http://windpower.org/","http://www.ge.com/dk/","http://www.hotswap.eu/","http://www.topsoe.com/","https://forcetechnology.com","http://www.dongenergy.com","http://www.powercurve.dk/","https://www.terma.com/","http://www.dovista.com/","http://www.vestas.com","http://littlesmartthings.com/","https://www.catie.ac.cr/en/","http://www.slaatto-sag.no/??","http://www.freightfarms.com/#leafygreenmachine","http://www.agrimetis.com/","http://jomitek.dk/en/","http://www.amadix.com/","http://daposy.com/","http://novonordiskfonden.dk","http://www.inomega3.dk/","http://hesalight.com/about-us/","http://www.huahonggrace.com/html/about_structure.php","http://www.moveinnovation.dk/","http://www.bosch.com/en/com/home/index.php","http://www.lonza.com/","http://nordicinnovation.org/","http://codland.is/","http://vandkunsten.com/","www.spesohealth.com","https://www.omicsonline.org/","http://www.interreg-oks.eu/","http://rencat.net/index.html","http://www.nikon.com/","http://www.kopenhagenfur.com/","http://www.ramboll.dk/om-os/ramboll-fonden ","http://www.bms.com/pages/default.aspx","http://www.twincore.de/en/home/","http://www.gentherm.com/","http://www.graftontechnology.co.uk/","https://www.thermofisher.com/dk/en/home/life-science/lab-plasticware-supplies/nalgene-labware.html","http://www.maerskoil.com/Pages/default.aspx","http://www.elplatek.dk/","http://www.widex.dk","http://www.rakolax.com/","http://www.lmwindpower.com/","https://fiberline.com/","https://www.nestecinc.com/","http://www.danaseals.dk/","http://www.meabco.com/","http://www.inra-transfert.fr/fr/","http://www.pharmacosmos.com/","https://catalog.coriell.org/1/CoriellCourses ","https://www.fairchildsemi.com/","https://www.accenture.com/","http://www.codejudge.net/","http://www.eldor.no/","http://www.geoteric.com/","http://www.eliis.fr/content/contact-0 ","http://www.biolinscientific.com/","http://www.cobham.com/communications-and-connectivity/satcom/","http://www.kosancrisplant.com/en/home/","http://www.analogic.com/","http://www.cobham.com/communications-and-connectivity/satcom/","http://mekoprint.dk/forside.aspx","http://cleancluster.dk/","http://www.danfoss.dk/home/#/","http://biosintel.com/","http://dgih.dk/","http://www.fstg.dk/dk/","http://www.interoute.it/","http://www.babcock.com/Pages/default.aspx","http://www.cidetec.es/cas/index.aspx","http://www.pfizer.dk/","https://sbtaqua.com/","http://www.medtronic.dk/","http://www.gsk.com/en-gb/research/","http://www.tennet.eu/de/","https://ruc.dk/","http://www.1stmile.dk/","http://www.statoil.com/no/Pages/default.aspx","http://www.optosecurity.com/","http://nordicpowerconverters.com/Frontpage ","http://copenhageneventcompany.com/default.aspx","http://www.danskenergi.dk/","http://www.chr-hansen.com/en","https://www.cpkelco.com/","http://www.smithinnovation.dk/","https://www.healthcare.siemens.com/","http://www.caltech.edu/","https://www.ikonscience.com/","http://www.cgg.com/en/What-We-Do/GeoSoftware/Solutions/HampsonRussell ","http://jgi.doe.gov/","https://www.nimblestorage.com/","http://www.nykredit.dk/#!/","http://www.dfds.com/","http://riemann.io/","http://dcum.dk/","http://www.harptechnologies.com/","http://www.lyngsoe.com/About-us.aspx","http://dieselturbo-north-america.man.eu/","http://www.mellanox.com/","https://www.ashrae.org/","http://www.roche.com/research_and_development.htm","http://aditechcorp.com/?lang=en","http://www.danisco.com/food-beverages/","http://www.cochlear.com/wps/wcm/connect/intl/home ","http://fertin.com/","http://www.nuvve.com/","http://www.bygdeforskning.no","http://www.rdas.dk/en/","http://www.hitachi.com/","http://www.nssmc.com/en/","http://www.alstom.com/US/","http://www.ntt.co.jp/index_e.html","http://www.bayer.com/","https://www.convatec.dk/","http://www.nissan-global.com/EN/index.html","https://www.avantium.com/","http://www.wavepiston.dk/","http://www.fsenergy.dk/","https://www.lokalebasen.dk/","http://www.epinionglobal.com/da/forside ","http://en.dbi-net.dk/","http://www.datatransparencylab.org/","http://www.unisense.com/","https://fracturecode.com/","http://www.slb.com/","http://www.cancer.dk/","http://hh-intellitech.dk/en/","http://www.danishfarmdesign.dk/","http://www.comfil.biz/","http://www.eneco.nl/","https://configit.com/","https://www.lf.dk/","https://www.moviatrafik.dk/","http://glaucus.dk/","http://www.teradata.dk/?LangType=1030&LangSelect=true","http://www.hedegaard-foods.dk/","http://www.simtech.de/index.php/de/","http://www.n-o-s.eu/","http://prozyme.com/","http://delawarecompanysearch.com/sira-pharmaceuticals-inc","http://www.leo-pharma.dk/","http://www.wormdevelopment.com/","http://www.f-star.com/","http://csr.astrium.eads.net/","http://www.msystem.dk/","https://www.dovregroup.com/","https://www.dnvgl.com/energy/index.html","http://www.steno.dk/","http://www.dendanskemaritimefond.dk/","http://www.ecophon.com/dk ","http://www.interacoustics.com/","http://www.landia.dk/","http://acornprojects.dk/","http://vildlaks.dk/velkommen/","http://www.mercator-ocean.fr/","http://www.unibio.dk/","http://www.symbiosecenter.dk/","http://www.forwind.net/","https://www.mellanox.com/","https://idt-biologika.com/","http://www.gram-equipment.com/","http://neontherapeutics.com/","https://tegvirginia.com/","http://www.aixtron.com/en/home/","http://polycsp.com/","http://www.solarventi.dk/","http://www.inqpharm.com/","http://hpnow.dk/","http://solarkey.dk/solasure-tender/logo.htm","http://biosyntia.com/","http://www.uptime.dk/2-om-uptime-it-aps.html","http://www.tekno.dk/","http://www.daposy.com/","http://www.alk-abello.com/DK/Pages/AffWelcome.aspx","http://www.bluegen.de/de/start/","http://www.elcogen.com/en/","http://customercarecontacts.com/microsoft-denmark-office-contact-phone-address/","http://www.dgc.dk/","http://www.dallenergy.com/","http://www.elster-instromet.dk/da/index ","http://www.topsoe.com/","http://www.veks.dk/da ","http://www.dinex.dk/en/","https://www.dhi.org/","http://www.bioceval.dk/bc/sonderseiten/hjem/","http://cotes.com/","http://www.advansor.dk/","http://www.avia-gis.com/","http://www.siemens.com/global/en/home/markets/wind.html","http://www.dongenergy.com/en ","http://www.upm.com/Pages/default.aspx","http://liqtech.com/","http://www.gea.com/en/index.jsp","http://bregentved.dk/index.php/bregentved-home ","https://issuu.com/","http://www.cowi.com/","http://lithiumbalance.com/en/","https://nnepharmaplan.com/","http://www.lockheedmartin.com/us.html","http://www4.syngenta.com/","http://www.akpdesign.dk/","https://www2.sahlgrenska.se/en/SU/In-English/","http://www.amadix.com/","http://www.ea-energianalyse.dk/uk/","http://www.hellokaleido.com/","http://www.amarcon.com.au/","http://www.bar-sosu.dk/","http://www.hydrogenics.com/","http://www.vectorcommand.com","http://www.mediscan.at/","http://www.kaist.edu/html/en/index.html","https://www.terma.com/","http://www.epri.com/Pages/Default.aspx","http://www.rockwool.com/","http://www.hempel.com/","http://www.torm.com/","http://www.ipu.org/english/home.htm","http://www.grundfos.com/","http://www.allianceforsustainableenergy.org/","http://www.niras.com/","http://www.f-sds.com/Contact ","http://enbreeze.com/","http://www.gate21.dk/?lang=en","http://www.lohmann-rauscher.com/","http://www.leosphere.com/en/","http://www.oticon.com/","http://www.zeiss.dk/corporate/home.html","https://europeanspallationsource.se/","http://www.chymeia.com/en/","https://airbusdefenceandspace.com/","http://norlase.com/","https://www.labster.com/","http://www.arttic.eu/pages/en/home.php","http://www.blaest.com/","http://www.coloplast.dk/","https://en.tdk.eu/tdk-en ","http://www.ecoxpac.dk/","http://www.carlsberggroup.com/Pages/default.aspx","http://www.northernvo.com/","http://www.jin.ngo/","http://www.oticon.com/","http://www.tie-tech.com/","http://www.maersk.com/en/","https://www.dhi.org/","https://www.plansee.com/en/index.htm/","http://www.danfysik.com/en ","http://3rsmc-aps.com/","http://www.techworks.ie/en/","http://www.akvaplan.niva.no/en/","https://www.90yearsofdesign.philips.com/","http://www.hydratech.co.uk/uk/","http://www.raaco.com/Default.aspx?ID=1056","http://www.flux.dk/","http://bccm.belspo.be/","http://www.abengoa.com/web/en/innovacion/abengoa_research/","http://hexagon.com/","https://www.ngk.de/en/company/ngk-spark-plug-europe-gmbh/","http://www.weibel-engros.dk/shop/frontpage.html","http://www.mayoclinic.org/","http://eyecular.com/","http://www.nxp.com/","https://www.qualiware.com/","http://www.magmasoft.de/de/","http://xnovotech.com/","http://www.gea.com/en/index.jsp","http://www.thirdwavenutrition.com/","http://www.solarlab.dk/","http://alcyomics.com/","https://vito.be/nl ","http://www.3-5lab.fr/","http://www.disagroup.com/en/sites/disa/content/disa_home.aspx","http://www.expres2ionbio.com/","https://nnepharmaplan.com/","http://www.radiometer.com/","https://www.foss.dk/","https://www.intomics.com/","http://www.topsoe.com/","http://www.aalborgportland.dk/","http://www.c-lecta.com/","http://www.widex.dk/da-dk ","http://www.iter.org/","http://windnovation.com/","https://www.dsb.dk/","http://www.panasonic.com/global/home.html","http://www.sintex.com/","http://www.nemlig.com/forside.aspx","http://provivi.com/","http://www.flsmidth.com/","http://www.welltec.com/","http://www.tetrapak.com/","http://www.m.dk/#!/om+metroen/om+os/metroselskabet '","https://www.echa.europa.eu/","http://arbejdstilsynet.dk/da/","https://www.ohb-system.de/","http://www.amabiotics.com/","http://www.orbitalatk.com/","http://www.evolva.com/","http://www.bioplant.dk/","http://www.samsungshi.com/eng/default.aspx","http://www.aalborgcsp.dk/","https://www.seas-nve.dk/","http://www.vestas.dk/","http://www.lithiumbalance.com/en/","http://biomologic.weebly.com/technology.html","http://corporate.evonik.com/en/Pages/default.aspx","http://fusionforenergy.europa.eu/","https://www.bksv.com/en ","https://www.bioneer.dk/","http://www.lundbeck.com/dk ","http://www.gaia-wind.com/","https://www.fuelseurope.eu/","http://www.eastman.com/Pages/Home.aspx","http://new.abb.com/de ","http://www.topsil.com/","http://www.mellanox.com/","http://www.biogaia.com/","https://networks.nokia.com/","http://www.techventures.org/","http://www.helcom.fi/","https://www.astrazeneca.com/","http://www.alectia.com/","http://www.jjxray.dk/","http://www.kruger.dk/en/","http://forsyningenesbjerg.dk/","https://enxray.envestry.com/","http://f-sds.com/","http://signosis.eu/","http://www.ewea.org/","https://www.if-insurance.com/web/industrial/pages/default.aspx","http://www.mscsoftware.com/partner/varinex-informatics-inc","http://www.resound.com/da ","https://www.elringklinger.de/de ","http://2benergy.com/","https://www.phaseone.com/","http://www.weissbiotech.com/","http://www.borean.dk/da/portefolje/cleantech/hydroblasterimpeller ","http://www.collini.eu/","https://www.carbontrust.com/home/","http://www.pdc-argos.com/","http://ilip.dk/","http://www.geus.dk/UK/Pages/default.aspx","http://www.volvocars.com/","http://www.pch-engineering.dk/","https://plasticomnium.com/en/","http://www.dsm.com/corporate/home.html","https://www.arma.ac.uk/","http://dk.madebydelta.com/","http://www.bkultrasound.com/","http://www.velux.dk/","http://www.climate-kic.org/","http://www.amadeus.com","http://www.cosine.nl/","http://www.kpf.dk/","https://www.csc.fi/","http://leapcraft.dk/","https://www.appareo.com/","http://www.antibiotx.com/","http://www.biogasol.dk/","http://www.matthey.com/","http://akretia.com/","https://www.terma.com/","https://www.lego.com/da-dk/aboutus ","http://www.nktphotonics.com/","http://www.bang-olufsen.com/da?gclid=CL7w8P2oydACFQ7gGQodbhsFPw","http://www.jai-alu.dk/","https://www.sprinklr.com/apps/","http://www.volund.dk/","http://kkgroup.my/","http://aproxi.dk/","http://www.bmt.org/","https://eupry.dk/","http://gomspace.com/","http://www.liqtech.dk/","http://www.gaspsolar.com/","https://www.sintef.no/en/sintef-energy/","http://www.biomar.com/denmark ","http://www.leo-pharma.dk/","http://inmoldbiosystems.com/","https://www.intomics.com/","http://www.cobis.dk/dk ","http://www.kraksfond.dk/","http://cellucomp.com/","http://www.welltec.com/","http://www.matis.is/english/","http://www.warrantgroup.it/","http://www.reallycph.com/","http://www.capres.com/","http://www.overspeed.de/en/company.html","http://www.borregaard.com/","http://www.rupprecht-consult.eu/home.html","http://concito.dk/","http://www.ffe-ye.dk/","http://www.novitek.dk/","http://www.statkraft.com/","http://littlesmartthings.com/","http://aquaporin.dk/","https://www.energimidt.dk/","https://www.sika.com/","http://www.vu.nl/nl/over-de-vu/organisatie-en-bestuur/stichting-vu-vumc/","http://www.windarphotonics.com/","http://www.ferrosanmedicaldevices.com/","http://www.danisco.com/food-beverages/","http://www.truenorthgems.com/da/home-da/","http://planenergi.dk/","http://www.forwind.net/","http://www.bane.dk/visForside.asp?artikelID=4268","http://www.gnhearing.dk/","http://www.metacardis.net/","https://www.infineon.com/","http://www.solmates.nl/","http://www.syngaschem.com/","http://www.lji.org/","http://www.ipu.dk/","http://www.gaiasolar.dk/dk/home/","http://wi.mit.edu/","http://www.danskakvakultur.dk/","http://www.micromol.com/start.html","https://www.harman.com/","https://europeanspallationsource.se/","http://bevica.dk/","https://www.mosis.com/","https://www.lely.com/dk/","http://www.rapidis.com/","http://gesim-bioinstruments-microfluidics.com/bioscaffolder-2/","http://www.planetariet.dk/","https://forcetechnology.com/da ","http://www.ntt.co.jp/index_e.html","http://www.junker-consult.dk/","http://www.agilent.com/home","http://www.treibacher.com/en ","http://www.airpohoda.eu/","https://www.blackducksoftware.com/","http://www.oestkraft.dk/","http://dk.madebydelta.com/","http://www.finansraadet.dk/en/Pages/mainpage.aspx","http://www.globalcastings.com/","https://en.tdk.eu/","http://startvaekst.dk/vhsjaelland.dk","http://www.cowi.dk/menu/home/","http://www.rockwool.com/","http://www.agropark.dk/","http://www.agnion.net","http://energinet.dk/EN/Sider/default.aspx","http://www.dfm.dtu.dk/","http://nordicpowerconverters.com","https://www.copac.dk/","http://www.danforel.com/","http://www.white.dk/","http://www.ramboll.com/","http://greenhydrogen.dk/","http://bio-aqua.dk/","http://www.metal-supply.dk/company/view/21702/eltronic_as ","http://nordicpowerconverters.com","http://www.movingenergy.dk/","http://bkultrasound.com/","http://www.thrane.no/en/","http://di.dk/Pages/Forsiden.aspx","http://www.sintef.no/Fiskeri-og-havbruk-AS/","http://www.kl.dk/Menu---fallback/Energiklyngecenter-Sjalland-id180611/","http://www.reka.com/en/","http://www.plh.dk/","https://www.signicat.com/","http://cemitec.com/en/home/","http://www.mcmelectronics.com/","http://www.fujikura.com/","http://www.alfalaval.com/","http://www.magneto.nl/en/","https://www.evalueserve.com/","https://trefor.dk/","https://www.suragus.com/en/","http://www.saebyvarmevaerk.dk/","http://www.arosteknik.dk","http://www.e4sma.com/en/home/","http://www.lithiumbalance.com/en/","http://ctr.dk/","http://nordsoenforskerpark.dk/","http://www.obh-gruppen.dk/da/","http://www.superkol.dk/","https://www.cpkelco.com/","http://planenergi.dk/","https://sshf.no/","http://www.nrel.gov/","http://www.cdc.gov/climateandhealth/default.htm","http://www.jyden-workwear.com/","http://www.fujifilmdiosynth.com/","http://firalis.com/","http://www.alstom.com/germany/","http://www.floatingpowerplant.com/","http://www.zeton.com/site/home.html","https://beof.dk/","https://www.comsol.com/","http://www.whalepumps.com/","http://www.chemstream.be/","http://www.agcocorp.com/","http://www.linaribiomedical.com/index.php?lang=en","http://www.robotool.com/","http://twt.dk/","http://www.cener.com/en/","http://aquaporin.dk/","http://www.daintel.com/","http://vidensby.dk/","http://incentive.dk/","http://www.fibervisions.com/","http://www.lr.org/en/","http://www.silicolife.com/","http://www.nilt.com/","http://www.ecofys.com/en/contact/ecofys-germany-berlin/","http://www.zeuxion.com/","http://www.flux.dk/","http://www.ciemat.es/","http://www.noliac.com/","http://www.staalcentrum.dk/","http://www.largestcompanies.com/company/Damrc-FMBA-2576623/ranking","http://ekolab.dk/","http://www.borregaard.no/","http://www.teknologisk.dk/","http://www.dgc.eu","http://simplight.co/","http://www.helenhard.no/","http://www.grundfos.com/","http://www.brplast.dk/","http://www.coriant.com/","http://www.gensoric.com/","http://www.combigas.dk/","http://www.cenergia.dk/da/","http://www.innoterm.dk/","http://po3.dk/","http://www.eklink.dk/","https://briggen.se/","http://www.rjl.se/Om-regionen/verksamheter/Lanssjukhuset-Ryhov-Jonkoping/","http://www.lomax.dk/","http://www.sanofi.de/l/de/de/index.jsp","http://limmud.org/","https://dechema.de/","https://plmgroup.dk/","http://www.stratasys.com/","http://www.dyadic.nl/","http://www.ihfood.dk/","http://www.as-vst.dk/","http://www.ewea.org/","http://www.levoss.com/","http://www.maier.es/","http://www.cener.com/en/","http://en.cnconsite.dk/","http://livingstrategy.dk/","http://www.arla.com/","http://aquaporin.dk/","http://www.3xn.dk/","http://www.topsoe.com/","http://www.cerpotech.com/","http://www.sustainair.dk/","http://www.energyxxi.com/","http://www.hofor.dk/om-os/organisation/net/hofor-fjernvarme-ps/","http://probyingredients.com/","http://arkitema.com/da ","https://www.fhi.no/","http://www.itwbyg.dk/","http://www.schneider-electric.com/ww/en/","http://www.c-lecta.com/","http://zebicon.com/","http://www.copcap.com/","http://vejdirektoratet.dk/da/Sider/Default.aspx","http://www.nordicsugar.dk/","http://www.teknologisk.dk/","http://www.kmc.dk/","http://energinet.dk/EN/Sider/default.aspx","https://www.qualiware.com/","http://greenday.ebmpapst.com/denmark/","http://www.royalgreenland.com/da/","http://priedemann.net/","http://www.hpt.dk/","http://www.profacto.dk/","http://www.lentikats.eu/cs/","https://www.sprinklr.com/apps/","http://www.carlsberggroup.com/Pages/default.aspx","http://hamletprotein.com/en/","http://www.siemens.com/global/en/home/markets/wind.html","http://www.hempel.com/","http://www.acib.at/"]
    url_start_list.append("http://www.advancedbionics.com/dk/dk/home.html")
    
    print "1) Adding startpoint URLs ... "# + url_start_list
    myWebExplorer.set_explore_start_points(url_start_list)

    ## Exploring configuration
    myWebExplorer.set_redirect_count(3)
    myWebExplorer.set_exploring_depth(3)
    myWebExplorer.set_exploring_depth(2) #Use this one for suggested websites
    
    ## Reset previous result (maintenance functions): 
    #myWebExplorer.clear_all_link_lists()
    #myWebExplorer.remove_www_for_websites()
    
    ## Verbose/debug configuration : 
    myWebExplorer.set_verbose(True)
    #myWebExplorer.set_debug(True)
    
    ## Setting a filename for saving the URL tree
    #TODO: Maybe we should rename that "exploration name" or "run name" 
    #myWebExplorer.set_url_tree_back_up_filename("web_crawler_dtu.p")
    myWebExplorer.set_url_tree_back_up_filename("suggested_url_dicovery_tree.p")

    ## 3) Continue to explore the webpages until we reached degree_depth_level
    #print "2) Exploring web links: this will take VERY long (weeks)"
    myWebExplorer.explore()

    ## 4) Find the CVR numbers we can from the corpuses.
    print "4) Look up the CVR numbers"
    #myWebExplorer.clear_all_CVR_numbers()
    #myWebExplorer.find_CVR_numbers()

    ## 5) Create a R corpus for a certain language - Stored in "main_directory"/web_content/corpus/"Language"
    print "5) Creating a corpus"
    #myWebExplorer.reset_R_corpus("English")    
    #myWebExplorer.create_R_corpuses("English") #Remember to erase the previous corpus if you want to upadate the existing pages
    #myWebExplorer.create_R_corpus("Danish")
    
    ## 6) Play with the resust : 
    #myWebExplorer.list_danish_companies()
    
    ## 7) Create a network graph
    #myWebExplorer.create_web_network_graph()
    
    ## 8) Create a GEPHI csv file
    #myWebExplorer.load_previous_to_visit_url()
    #myWebExplorer.export_csv_dataset_for_GEPHI(True)
    
    
    
##Couple of notes :
#myWebExplorer = webExplorer("/home/shared/Scripts/web_explorer/",1,1)
#myWebExplorer.set_verbose(True)
#myWebExplorer.set_debug(True)
#myWebExplorer.URL_scan("kom.aau.dk","group/12gr1010/Report.pdf")

##In order to check how many websites are left from the 1st level :
#import os
#num = 0    
#for website in myWebExplorer.to_visit_urls[0]:
#    if not os.path.isfile("/home/shared/Scripts/web_explorer/web_content/"+website+"/external_urls_"+str(myWebExplorer.redirect_count)+"_redirect.p"):
#        num+=1
#        
#print str(num) + " sites to visits out of " +str(len(myWebExplorer.to_visit_urls[0]))

