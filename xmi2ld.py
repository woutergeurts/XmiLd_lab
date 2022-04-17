#! /usr/bin/python3
#
# This module reads an XMI (2.5 exported from Enterprise Architect) 
# and transforms this to linked data using the mapping in the module LDMap
# 
# The metamodel itself is not (yet) linked data, but reflects the xmi tags and
# attributes one-to-one.
#
# While reading the XMI, the TAG/attribute pairs translate to predicates and their
# values to objects. xmi:id and xmi:idref are taken as subjects
# xmi:type is mapped rdfs:type.
#
# If one also translates the xmi descriptions of UML UMLDI to linked data, the uml
# model is produced, and added for analysis
#
# 
# Elements are XML-elements from the tree. One of the Element tags
# is called 'element' (consequently in lowercase)
#
# Disclaimer: development is experimental, supporting all constructs 
# from test data. NOT SUPPORTING FULL XMI standards
# 
# Only tested with xmi as exported by Sparx Enterprise Architect
# 
import xml.etree.ElementTree as ET
from  LDMap import PropertyMap, URIRefFromString, BindNamespaces, ReadNamespaces, URI2prefix

from rdflib import Graph, Literal, RDF, RDFS, URIRef
g = Graph()
#
# elements hold all tags read, dependent on tag, they might be a Relation
#
# key = tag, value is hash to map the attribs for 'from' and 'to'
RelationHash = {}
RelationHash['Generalization'] = { 'From': 'start', 'To' : 'end' }
#RelationHash['Abstraction'] = { 'From': 'start', 'To' : 'end' }
#RelationHash['Dependency'] = { 'From': 'start', 'To' : 'end' }
#RelationHash['Realisation'] = { 'From': 'start', 'To' : 'end' }
#RelationHash['InformationFlow'] = { 'From': 'start', 'To' : 'end' }
modelprefix = "test:"

class Element:
    def __init__(self, node):
        self.tag = URI2prefix(node.tag)
        self.id = "id"
        self.URIref = "URIref"
        self.label = "no label"
        self.type = "xmi:"+self.tag
        self.idref = "idref"
        self.attrib = {}
        self.From = None
        self.To = None
        self.Predicate = None
        self.hasText = False
        self.text = "" 
        self.URIRef = URIRefFromString(modelprefix+"Anonymous")
        for attr_key in node.attrib.keys():
            attr_key_prefixed = URI2prefix(attr_key)
            if( attr_key_prefixed == "xmi:type" ):
                self.type = node.attrib[attr_key]
            elif( attr_key_prefixed == "xmi:idref" ):
                self.idref = node.attrib[attr_key]
            elif( attr_key_prefixed == "xmi:id" ):
                self.id = node.attrib[attr_key]
            elif( attr_key_prefixed == "name" ):
                self.label = node.attrib[attr_key]
            else:
                self.attrib[attr_key] = node.attrib[attr_key]

        self.typeURIRef = URIRefFromString(self.type)

        if( self.id != "id" ):
            self.URIRef = URIRefFromString(modelprefix+self.id)
        if( self.idref != "idref" ):
            self.URIRef = URIRefFromString(modelprefix+self.idref)
        self.hasText = (node.text != None)
        if( self.hasText ):
            self.text = node.text

    def print(self, spaces):
        print(spaces+"  %s: %s/%s [%s] (%s), attrib=%s" % (self.tag, self.id, self.idref, self.URIRef, self.type, self.attrib))

    def isRelation(self):
        if( self.tag in RelationHash.keys() ):
            self.From = self.attrib[RelationHash[self.tag]['From']]
            self.To = self.attrib[RelationHash[self.tag]['To']]
            return True
        else:
            return False

    def isEntity(self):
        return( self.id != "id" )

    def isReference(self):
        return( self.idref != "idref" )

def handleModelElement(P,C,propertyMap):
    if( C.isEntity() ):
        #g.add((C.URIRef, URIRefFromString("xmi:partOf"), P.URIRef))
        g.add((C.URIRef, URIRefFromString("xmi:"+C.tag), P.URIRef))
        g.add((C.URIRef, RDF.type, C.typeURIRef))
        if( C.label != "no label" ):
            g.add((C.URIRef, RDFS.label, Literal(C.label, lang="nl")))
        for attr_key in C.attrib:
            attrib = C.attrib[attr_key]
            propertyMap.addProperty(g, C.URIRef, C.tag, attr_key, attrib)
        #C.print("DONE: ")
    if( C.hasText ):
        g.add((P.URIRef, RDFS.comment, Literal(C.text, lang="nl")))

    if( C.isRelation() ):
        g.add((URIRefFromString(propertyMap.modelPrefix+C.From),URIRef(C.type), 
            URIRefFromString(propertyMap.modelPrefix+C.To)))

def parseModelElement(parent,propertyMap):
    P = Element(parent)
    for child in parent:
        C = Element(child)
        handleModelElement(P,C,propertyMap)
        parseModelElement(child,propertyMap)

import base64
docdir = ""
from io import BytesIO
from zipfile import ZipFile

# Docs are stored as files. Both rtf and images.
# todo: convert rtf to run pandoc-ast/json keep the png and jpg
# rtf_to_text might work
#from striprtf.striprtf import rtf_to_text
#text = rtf_to_text(b.decode())
#with open("%s-%s.text" % (name, docid), "w") as f:
#    f.write(text)
def unpackDocumentText(docid,document):
    textbytes = base64.b64decode(document.text)
    bio = BytesIO(textbytes)
    with ZipFile(bio) as z:
        print("DOCUMENT docid = ", docid, document.attrib, z.namelist())
        for name in z.namelist():
            b = z.read(name)
            with open("%s-%s" % (name, docid), "bw") as f:
                f.write(b)

def handleDocument(parentURI, document,propertyMap):
    if( document.text != None ):
        if( 'docid' in document.attrib.keys() ):
            docid = document.attrib['docid'].replace('{','').replace('}','')
            g.add((URIRefFromString("document:"+docid), 
                URIRefFromString("xmi:"+document.tag), parentURI))
            for attribkey in document.attrib:
                propertyMap.addProperty(g, URIRefFromString("document:"+docid), 
                   document.tag, attribkey, document.attrib)
            unpackDocumentText(docid, document)
        else:
            print("DOCID UNDEF")
            docid = "DOCID undef"

    else:
        print("DOCUMENT EMPTY", document.attrib)

def handleExtensionItem(element,propertyMap):
    E = Element(element)
    for tag in element:
        for attribkey in tag.attrib:
            attrib = tag.attrib[attribkey]
            propertyMap.addProperty(g, E.URIRef, tag.tag, attribkey, attrib)
        if( tag.tag == 'modelDocument' or tag.tag == 'tdoc2' ):
            handleDocument(E.URIRef, tag,propertyMap)


class ProfileElement:
    def __init__(self, node):
        self.tag = URI2prefix(node.tag)
        self.URIref = "URIref"
        self.Predicate = RDF.type
        self.Object = URIRefFromString(self.tag)
        self.id = None
        self.value = "N/A"
        for attr_key in node.attrib.keys():
            if( attr_key[0:5] == "base_" ):
                self.id = modelprefix+node.attrib[attr_key]
            elif( self.value == "N/A" ):
                #predicate is tag, value is object
                self.value = node.attrib[attr_key]
                self.Predicate = URIRefFromString(self.tag)
                self.Object = Literal(self.value)
            else:
                if( self.tag[0:6] != "mofext" ):
                    print("ERROR: extra arguments")

    def print(self):
        print("ProfileElement[%s] -> [%s] -> [%s]" % (self.id, self.tag, self.value))

    def add(self,g):
        if( self.tag[0:6] != "mofext" ):
            g.add((URIRefFromString(self.id), self.Predicate, self.Object))

def handleProfiledata(pd,propertyMap):
    P = ProfileElement(pd)
    P.print()
    P.add(g)

def parseXML(tree,propertyMap):
    root = tree.getroot()
    for section in root:
        Section = Element(section)
        print("  section: [%s]" % Section.tag, end=" ")
        if(Section.tag[0:4] == "uml:"):
            print("processing ...")
            for child in section:
                C = Element(child)
                handleModelElement(Section,C,propertyMap)
                parseModelElement(child,propertyMap)
        elif(Section.tag == "xmi:Extension"):
            print("processing ...")
            for subsection in section:
                for element in subsection:
                    E = Element(element)
                    g.add((E.URIRef, RDF.type, E.typeURIRef))
                    if( E.label != "no label" ):
                        g.add((E.URIRef, RDFS.label, Literal(E.label, lang="nl")))
                    handleExtensionItem(element,propertyMap)
        elif(Section.tag == "xmi:Documentation"):
            print("skip")
        else:
            handleProfiledata(section,propertyMap)

from LDSparql import Sparql

if __name__ == "__main__":
    import sys
    import getopt
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, 'p:o:i:s:' )
    xmifile = "test.xmi"
    ttlfile = "test.ttl"
    modelprefix = "test:"
    sparqldir = "sparql"
    docdir = "tmpdoc"
    for (opt, value) in opts:
        if opt == "-i": 
            xmifile = value
        if opt == "-o": 
            ttlfile = value
        if opt == "-p": 
            modelprefix = value
        if opt == "-s": 
            sparqldir = value
        if opt == "-d": 
            docdir = value

    print("Convert %s to %s with modelprefix [%s] docdir=%s" % (xmifile, ttlfile, modelprefix, docdir))
    ReadNamespaces(xmifile)
    tree = ET.ElementTree(file=xmifile)
    BindNamespaces(g, tree.getroot())
    propertyMap = PropertyMap(modelprefix)
    parseXML(tree,propertyMap)
    propertyMap.toGraph(g)
    ldSparql = Sparql(sparqldir)
    ldSparql.run_all(g)

    with open(ttlfile, "w") as f:
        g.print(out=f) 
