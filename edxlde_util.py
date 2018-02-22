"""Python Utilities for EDXL-DE"""
import xml.etree.ElementTree as ET
import ConfigParser
import datetime
from datetime import timedelta

def generate_de(lat, lon):
    """Generates a DE Message"""
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    unitprefix = config.get('Main', 'UnitPrefix')
    unitid = config.get('Main', 'UnitID')
    sender = config.get('Main', 'Sender')
    restype = config.get('Main', 'Type')
    desc = config.get('Main', 'ContentDesc')
    keyword = config.get('Main', 'Keyword')
    typeenum = restype.replace("_", ".")
    fullid = unitprefix +'.'+unitid
    distref = fullid+','+sender+','+'1753-01-01T00:00:00.0000000Z'
    stale = config.getint('Main', 'Stale')
    staledelta = timedelta(minutes=stale)
    sent = datetime.datetime.utcnow()
    sentstr = sent.strftime('%Y-%m-%dT%H:%M:%SZ')
    staletime = sent + staledelta
    stalestr = staletime.strftime('%Y-%m-%dT%H:%M:%SZ')
    emlc = "http://release.niem.gov/niem/domains/emergencyManagement/3.1/emevent/0.1/emlc/"
    mof = "http://example.com/milops/1.1/"
    niemcore = "http://release.niem.gov/niem/niem-core/3.0/"
    emevent = "http://release.niem.gov/niem/domains/emergencyManagement/3.1/emevent/0.1/"
    gml = "http://www.opengis.net/gml/3.2"
    xmlns = {'de': 'urn:oasis:names:tc:emergency:EDXL:DE:1.0',
             'emlc': emlc, 'mof': mof, 'nc': niemcore, 'emevent': emevent, 'gml': gml}
    ET.register_namespace('', "urn:oasis:names:tc:emergency:EDXL:DE:1.0")
    ET.register_namespace('emlc', emlc)
    ET.register_namespace('mof', mof)
    ET.register_namespace('nc', niemcore)
    ET.register_namespace('emevent', emevent)
    ET.register_namespace('gml', gml)
    tree = ET.parse('DEtemplate.xml')
    root = tree.getroot()
    ele = root.find('de:distributionID', xmlns)
    ele.text = fullid
    ele = root.find('de:senderID', xmlns)
    ele.text = sender
    ele = root.find('de:dateTimeSent', xmlns)
    ele.text = sentstr
    ele = root.find('de:distributionReference', xmlns)
    ele.text = distref
    ele = root.find('de:contentObject', xmlns)
    subele = ele.find('de:contentDescription', xmlns)
    subele.text = desc
    subele = ele.find('de:contentKeyword', xmlns)
    ET.SubElement(subele, "value").text = keyword
    ET.SubElement(subele, "value").text = fullid
    ET.SubElement(subele, "value").text = restype
    ele = ele.find('de:xmlContent', xmlns)
    ele = ele.find('de:embeddedXMLContent', xmlns)
    ele = ele.find('emlc:Event', xmlns)
    subele = ele.find('mof:EventID', xmlns)
    subele = subele.find('nc:IdentificationID', xmlns)
    subele.text = fullid
    subele = ele.find('emevent:EventTypeDescriptor', xmlns)
    sub2 = subele.find('emevent:EventTypeCode', xmlns)
    sub2.text = typeenum
    sub2 = subele.find('emevent:EventTypeDescriptorExtension', xmlns)
    sub2.text = typeenum
    subele = ele.find('mof:EventLocation', xmlns)
    sub2 = subele.find('mof:LocationCylinder', xmlns)
    sub2 = sub2.find('mof:LocationPoint', xmlns)
    sub2 = sub2.find('gml:Point', xmlns)
    sub2 = sub2.find('gml:pos', xmlns)
    sub2.text = lat+' '+lon
    subele = ele.find('mof:EventValidityDateTimeRange', xmlns)
    sub2 = subele.find('nc:StartDate', xmlns)
    sub2 = sub2.find('nc:DateTime', xmlns)
    sub2.text = sentstr
    sub2 = subele.find('nc:EndDate', xmlns)
    sub2 = sub2.find('nc:DateTime', xmlns)
    sub2.text = stalestr
    subele = ele.find('mof:EventMessageDateTime', xmlns)
    sub2 = subele.find('nc:DateTime', xmlns)
    sub2.text = sentstr
    subele = ele.find('emlc:ResourceDetail', xmlns)
    sub2 = subele.find('emlc:ResourceStatus', xmlns)
    sub2 = sub2.find('emlc:ResourceSecondaryTextStatus', xmlns)
    sub2.set('SourceID', unitprefix)
    sub2 = subele.find('emlc:ResourceControllingOrganization', xmlns)
    sub2 = sub2.find('nc:OrganizationIdentification', xmlns)
    sub2 = sub2.find('nc:IdentificationID', xmlns)
    sub2.text = unitprefix
    sub2 = subele.find('emlc:ResourceControllingOrganization', xmlns)
    sub2 = sub2.find('emlc:ResourceIdentifier', xmlns)
    sub2 = sub2.find('nc:IdentificationID', xmlns)
    sub2.text = fullid
    #tree = ET.ElementTree(root)
    #tree.write('filename.xml')
    xmlstr = ET.tostring(root, encoding='utf8', method='xml')
    xmlstr = xmlstr.split("\n", 1)[1]
    return xmlstr
