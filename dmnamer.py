from lxml import etree
from common_functions import Exclusion, Write_DMC, Write_PMC, NameAndCode, Refresh_DMC
import pathlib
import os, logging
from validateEntities import valent


class CollectInput():

    def __init__(self):
        inputpath = pathlib.Path(input("Input Path: "))
        os.chdir(inputpath)
        log = self.build_log()
        prepmc = list(inputpath.glob('PMC-HON*-*-0*-*.xml'))[0]
        pmc = valent(prepmc.name, prepmc.parent) # str        
        par = etree.XMLParser(no_network=True, recover=True) # lxml.etree.XMLParser
        pmroot = etree.parse(pmc, par).getroot()
        Refresh_DMC().refresh(prepmc.parent, log)
        DMExtension(prepmc.parent, pmroot, par)
        Write_PMC(pmroot, pmc, prepmc.parent)


    def build_log(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(levelname)s]: [%(message)s]')
        filehandler = logging.FileHandler('extension_addition.log', 'w')
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)

        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)

        logger.addHandler(filehandler)
        logger.addHandler(streamhandler)
        return logger



class DMExtension():
    DMN = {}

    def __init__(self, rootdir:pathlib.WindowsPath, pmroot:etree._Element, xmlparser:etree.XMLParser):
        self.rootdir = rootdir
        self.xmlparser = xmlparser
        excluded = Exclusion().parsable_list(rootdir)
        self.MAIN = [NameAndCode().dmcode_from_name(name)[1]
                        for name in excluded if name.startswith('DMC-HON')]
        cage = pmroot.find('.//pmCode').attrib['pmIssuer']
        ata = pmroot.find('.//externalPubCode/[@pubCodingScheme="CMP"]').text
        all_dmrefs = pmroot.findall('.//content//dmRef')
        self.pmextension(ata, cage, all_dmrefs)


    def pmextension(self, ATA:str, CAGE:str, dmref_list:list):
        for dmref in dmref_list:
            dmcode = dmref.find('.//dmCode')
            mic = dmcode.attrib['modelIdentCode']
            if mic != "HONAERO":
                dmident = dmref.find('dmRefIdent')
                preextension_list = dmident.findall('identExtension')
                if preextension_list == []:
                    extension = self.extend_in_pm(str(ATA), str(CAGE), dmident)
                else:
                    [dmident.remove(preextension) for preextension in preextension_list]
                    extension = self.extend_in_pm(str(ATA), str(CAGE), dmident)
                dmname = NameAndCode().name_from_dmcode(dmcode.attrib)
                self.DMN.update({dmname:extension})
        self.extend_in_dm()


    def extend_in_dm(self):
        if self.DMN != []:         
            for dmname in list(self.DMN.keys()):
                dmc = list(self.rootdir.glob('{0}*.xml'.format(dmname)))
                if dmc != []:
                    dmroot = etree.parse(dmc[0], self.xmlparser).getroot()
                    reference_list = dmroot.xpath('.//*[self::dmRef or self::dmAddress]')
                    extcode = self.DMN[dmname].attrib['extensionCode']
                    extvendor = self.DMN[dmname].attrib['extensionProducer']                       
                    for reference in reference_list:
                        indexdmc = reference.find('.//dmCode')
                        if str(NameAndCode().name_from_dmcode(indexdmc.attrib)) in self.DMN:
                            extparent = indexdmc.getparent()
                            ext_list = extparent.findall('.//identExtension')
                            if ext_list == []:
                                extparent.insert(0, etree.Element('identExtension', 
                                    extensionCode = extcode, extensionProducer = extvendor))
                            else:
                                for ext in ext_list:
                                    extparent.remove(ext)
                                    extparent.insert(0, etree.Element('identExtension', 
                                        extensionCode = extcode, extensionProducer = extvendor))                                    
                    Write_DMC(dmroot, dmc[0].name, dmc[0].parent)
                    dmc[0].rename(str('DME-'+extvendor+'-'+extcode+dmc[0].name.replace('DMC', '')))


    def extend_in_pm(self, ATA:str, CAGE:str, dmrefident:etree._Element):
        identext = etree.Element('identExtension', extensionCode=str(ATA),
                                  extensionProducer = str(CAGE))
        dmrefident.insert(0, identext)
        return identext

CollectInput()