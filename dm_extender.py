from lxml import etree
from generalfunctions.helper_classes import Write_DOC, NameAndCode, validate_entities
import pathlib
import os
import sys
import logging


class CollectInput():

    def __init__(self, inputpath: pathlib.Path, choice: bool):
        log = self.build_log(inputpath)
        prepmc = list(inputpath.glob('PMC-HON*-*-0*-*.xml'))[0]
        validate_entities(prepmc)  # str
        # lxml.etree.XMLParser
        par = etree.XMLParser(no_network=True, recover=True)
        pmroot = etree.parse(prepmc, par).getroot()
        log.info('\n\nGetting PMC:: {0}'.format(prepmc))
        if choice == True:
            log.info('ADDING EXTENSIONS')
            DMExtension(prepmc.parent, pmroot, par, log)
        else:
            log.info('REMOVING EXTENSIONS')
            pmroot = self.remove_extension(
                pathlib.Path(prepmc.parent), par, pmroot, log)
        Write_DOC().pub_module(pmroot, prepmc, prepmc.parent)
        log.info('Task Completed:: Add/Remove DM Extension')

    def remove_extension(self, mainpath: pathlib.Path,
                         xmlparser: etree.XMLParser, root: etree._Element,
                         log: logging.Logger):
        log.info('Removing Extensions in PMC')
        idext = root.findall('.//identExtension')
        [ext.getparent().remove(ext) for ext in idext]
        all_extended = mainpath.glob('DME-*-HON*.xml')
        for extdm in all_extended:
            validate_entities(extdm)
            dmroot = etree.parse(extdm, xmlparser).getroot()
            dmcode = dmroot.find('.//dmIdent//dmCode')
            dmname = NameAndCode().name_from_dmcode(dmcode.attrib)
            dmext = dmroot.findall('.//identExtension')
            log.info('Removing Extensions:: {0}'.format(dmname))
            [ext.getparent().remove(ext) for ext in dmext]
            Write_DOC().data_module(dmroot, extdm, mainpath)
            extdm.rename(dmname+'.xml')
        return root

    def build_log(self, rootdir: pathlib.Path):
        os.chdir(rootdir)
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

    def __init__(self, rootdir: pathlib.WindowsPath,
                 pmroot: etree._Element, xmlparser: etree.XMLParser, log: logging.Logger):
        self.rootdir = rootdir
        self.xmlparser = xmlparser
        cage = pmroot.find('.//pmCode').attrib['pmIssuer']
        ata = pmroot.find('.//externalPubCode/[@pubCodingScheme="CMP"]').text
        all_dmrefs = list(pmroot.findall('.//dmRef'))
        for dmref in all_dmrefs:
            actref = dmref.find('.//dmCode')
            if (actref != None) and (actref.attrib['infoCode'] == "00W"):
                actname = NameAndCode().name_from_dmcode(actref.attrib)
                act = list(rootdir.glob('{0}*.xml'.format(actname)))[0]
                if act != []:
                    validate_entities(act)
                    actroot = etree.parse(act, xmlparser).getroot()
                    added_dmref = actroot.findall('.//dmRef')
                    [all_dmrefs.append(each) for each in added_dmref]
                else:
                    log.warn('ACT is referenced but not found in the directory')
        self.pmextension(ata, cage, all_dmrefs, log)

    def pmextension(self, ATA: str, CAGE: str, dmref_list: list, log: logging.Logger):
        for dmref in dmref_list:
            dmcode = dmref.find('.//dmCode')
            mic = dmcode.attrib['modelIdentCode']
            if mic != "HONAERO":
                dmident = dmref.find('dmRefIdent')
                preextension_list = dmident.findall('identExtension')
                if preextension_list == []:
                    extension = self.extend_in_pm(str(ATA), str(CAGE), dmident)
                else:
                    [dmident.remove(preextension)
                     for preextension in preextension_list]
                    extension = self.extend_in_pm(str(ATA), str(CAGE), dmident)
                dmname = NameAndCode().name_from_dmcode(dmcode.attrib)
                self.DMN.update({dmname: extension})
        self.extend_in_dm(log)

    def extend_in_dm(self, log: logging.Logger):
        if self.DMN != []:
            for dmname in list(self.DMN.keys()):
                dmc = list(self.rootdir.glob('{0}*.xml'.format(dmname)))
                if dmc != []:
                    dmroot = etree.parse(dmc[0], self.xmlparser).getroot()
                    reference_list = dmroot.xpath(
                        './/*[self::dmRef or self::dmAddress]')
                    extcode = self.DMN[dmname].attrib['extensionCode']
                    extvendor = self.DMN[dmname].attrib['extensionProducer']
                    for reference in reference_list:
                        indexdmc = reference.find('.//dmCode')
                        if str(NameAndCode().name_from_dmcode(indexdmc.attrib)) in self.DMN:
                            extparent = indexdmc.getparent()
                            ext_list = extparent.findall('.//identExtension')
                            if ext_list == []:
                                extparent.insert(0, etree.Element('identExtension',
                                                                  extensionCode=extcode, extensionProducer=extvendor))
                            else:
                                for ext in ext_list:
                                    extparent.remove(ext)
                                    extparent.insert(0, etree.Element('identExtension',
                                                                      extensionCode=extcode, extensionProducer=extvendor))
                    extended_name = str(
                        'DME-'+extvendor+'-'+extcode+dmc[0].name.replace('DMC', ''))
                    Write_DOC().data_module(dmroot, dmc[0].name, dmc[0].parent)
                    log.info(
                        'Extension:: {0} --> {1}'.format(dmc[0].name, extended_name))
                    dmc[0].rename(extended_name)

    def extend_in_pm(self, ATA: str, CAGE: str, dmrefident: etree._Element):
        identext = etree.Element('identExtension', extensionCode=str(ATA),
                                 extensionProducer=str(CAGE))
        dmrefident.insert(0, identext)
        return identext


def choose_bool(user_ip):
    if user_ip == 1:
        bool_ip = True
    else:
        bool_ip = False
    return bool_ip


mainpath = pathlib.Path(sys.argv[1])
input_choice = int(sys.argv[2])
boolean_input = choose_bool(input_choice)
CollectInput(mainpath, boolean_input)
