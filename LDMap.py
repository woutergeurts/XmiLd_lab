#
# Goal of this module:
# Hide all namespace jugling
#
from rdflib import XSD, Literal, XSD, RDF, RDFS, OWL, URIRef, Namespace

ns_dict = {}
ns_dict["rdfs"] = { "prefix": "rdfs:", "IRI": "http://www.w3.org/2000/01/rdf-schema#" }
ns_dict["document"] = { "prefix": "document:", "IRI": "http://localhost.com/document/" }
ns_dict["model"] = { "prefix": "model:", "IRI": "http://localhost.com/model/" }
#
# todo: this is quite dirty
# introduce a def to print PREFIX clauses for the sparqls
#
def ReadNamespaces(file):
    # use cp1252 (windows-1252)
    with open(file,"r",encoding="cp1252") as xml:
        while(True):
            line=xml.readline()
            line = line[:-2] # pragmatic way to strip last 2 chars
            fields = line.split(' ')
            if( fields[0] == "<xmi:XMI" ):
                #bug report: xmi:version is not parsed well. check xmlns: prefix with re
                for field in fields[1:]:
                    prefix, iri = field.split("=")
                    prefix = prefix[6:] # get rid of 'xmlns:' 
                    iri = iri.replace('"','')
                    ns_dict[prefix] = { "prefix": "%s:"%prefix, "IRI": "%s/"%iri }
                return

def BindNamespaces(g, root):
    for ns in ns_dict:
        g.bind(ns_dict[ns]["prefix"][0:-1], ns_dict[ns]["IRI"])

def URIRefFromString(string):
    for ns in ns_dict:
        string = string.replace(ns_dict[ns]["prefix"], ns_dict[ns]["IRI"])
    return URIRef(string)

def URI2prefix(string):
    string = string.replace("{","").replace("}","/")
    for ns in ns_dict:
        string = string.replace(ns_dict[ns]["IRI"], ns_dict[ns]["prefix"])
    return string

# choice made here: we map ('tag','attrib'), this is the safest, yet more cumbersome
# way. The XMI standard might allow to to map on attrib only. For this, we need to 
# align the mapping to the standard. The mapping now is made by printing not yet mapped
# (tag,attrib) pairs.
# 
class PropertyMap:
    def __init__(self, modelPrefix):
        self.modelPrefix = modelPrefix
        self.dict = {}
        tmpdict = {}
        tmpdictkeys =                              ['predicateURI',  'subjectType', 'datetype'   ]
        tmpdict['ownedComment/annotatedElement'] = ['xmi:annotatedElement',   'ModelObject',     XSD.string   ]
        tmpdict['defaultValue/instance']         = ['xmi:instance',    'Literal',   XSD.string ]
        tmpdict['defaultValue/type']             = ['xmi:type',    'ModelObject',   XSD.string ]
        tmpdict['defaultValue/value']            = ['xmi:value',    'Literal',   XSD.string ]
        tmpdict['generalization/general']        = ['xmi:general',    'ModelObject',   XSD.string ]
        tmpdict['lowerValue/value']              = ['xmi:value',    'Literal',   XSD.string ]
        tmpdict['ownedAttribute/aggregation']    = ['xmi:aggregation',    'MultiModelObject',   XSD.string ]
        tmpdict['ownedAttribute/association']    = ['xmi:association',    'MultiModelObject',   XSD.string ]
        tmpdict['ownedAttribute/isDerivedUnion'] = ['xmi:isDerivedUnion',    'Literal',   XSD.boolean ]
        tmpdict['ownedAttribute/isDerived']      = ['xmi:isDerived',    'Literal',   XSD.boolean ]
        tmpdict['ownedAttribute/isOrdered']      = ['xmi:isOrdered',    'Literal',   XSD.boolean ]
        tmpdict['ownedAttribute/isReadOnly']     = ['xmi:isReadonly',    'Literal',   XSD.boolean ]
        tmpdict['ownedAttribute/isUnique']       = ['xmi:isUnique',    'Literal',   XSD.string ]
        tmpdict['ownedAttribute/redefinedProperty'] = ['xmi:refinedProperty',    'MultiModelObject',   XSD.string ]
        tmpdict['ownedAttribute/subsettedProperty'] = ['xmi:subsettedProperty',    'MultiModelObject',   XSD.string ]
        tmpdict['ownedAttribute/type']           = ['xmi:ype',    'ModelObject',   XSD.string ]
        tmpdict['ownedEnd/association']          = ['xmi:association',    'ModelObject',   XSD.string ]
        tmpdict['ownedEnd/isDerivedUnion']       = ['xmi:isDerivedUnion',    'Literal',   XSD.boolean ]
        tmpdict['ownedEnd/isDerived']            = ['xmi:isDerived',    'Literal',   XSD.boolean ]
        tmpdict['ownedEnd/isOrdered']            = ['xmi:isOrdered',    'Literal',   XSD.boolean ]
        tmpdict['ownedEnd/isReadOnly']           = ['xmi:isReadOnly',    'Literal',   XSD.boolean ]
        tmpdict['ownedEnd/redefinedProperty']    = ['xmi:redefinedProperty',    'MultiModelObject',   XSD.string ]
        tmpdict['ownedEnd/subsettedProperty']    = ['xmi:subsettedProperty',    'MultiModelObject',   XSD.string ]
        tmpdict['ownedEnd/type']                 = ['xmi:type',    'ModelObject',   XSD.string ]
        tmpdict['ownedOperation/bodyCondition']  = ['xmi:bodyCondition',    'Literal',   XSD.string ]
        tmpdict['ownedOperation/isAbstract']     = ['xmi:isAbstract',    'Literal',   XSD.boolean ]
        tmpdict['ownedOperation/isQuery']        = ['xmi:isQuery',    'Literal',   XSD.boolean ]
        tmpdict['ownedOperation/precondition']   = ['xmi:precondition',    'Literal',   XSD.string ]
        tmpdict['ownedOperation/redefinedOperation'] = ['xmi:redefinedOperation' ,    'MultiModelObject',   XSD.string ]
        tmpdict['ownedParameter/direction']      = ['xmi:direction',    'Literal',   XSD.string ]
        tmpdict['ownedParameter/isOrdered']      = ['xmi:isOrdered',    'Literal',   XSD.boolean ]
        tmpdict['ownedParameter/isUnique']       = ['xmi:isUnique',    'Literal',   XSD.boolean ]
        tmpdict['ownedParameter/type']           = ['xmi:type',    'ModelObject',   XSD.string ]
        tmpdict['ownedRule/constrainedElement']  = ['xmi:constrainedElement', 'MultiModelObject',XSD.string ]
        tmpdict['packageImport/importedPackage'] = ['xmi:importedPackage',    'ModelObject',   XSD.string ]
        tmpdict['packagedElement/isAbstract']    = ['xmi:isAbstract',    'Literal',   XSD.boolean ]
        tmpdict['packagedElement/isDerived']     = ['xmi:isDerived',    'Literal',   XSD.boolean ]
        tmpdict['packagedElement/memberEnd']     = ['xmi:memberEnd',    'MultiModelObject',   XSD.string ]
        tmpdict['specification/language']        = ['xmi:language',    'Literal',   XSD.string ]
        tmpdict['upperValue/value']              = ['xmi:value',    'Literal',   XSD.string ]

        #                               ['predicateURI',    'subjectType', 'datetype'   ]
        tmpdict['times/created']      = ['xmi:created',      'Literal', XSD.dateTime ]
        tmpdict['times/modified']     = ['xmi:modified',     'Literal', XSD.dateTime   ]
        tmpdict['times/lastloaddate'] = ['xmi:lastloaddate', 'Literal', XSD.dateTime   ]
        tmpdict['times/lastsavedate'] = ['xmi:lastsavedate', 'Literal', XSD.dateTime   ]
        tmpdict['packageproperties/version'] = ['xmi:version','Literal',XSD.string ]
        tmpdict['packageproperties/tpos'] = ['xmi:tpos',     'Literal', XSD.string ]
        tmpdict['flags/iscontrolled'] = ['xmi:iscontrolled', 'Literal', XSD.boolean ]
        tmpdict['flags/isprotected']  = ['xmi:isprotected',  'Literal', XSD.boolean ]
        tmpdict['flags/batchsave']    = ['xmi:batchsave',    'Literal', XSD.string ]
        tmpdict['flags/batchload']    = ['xmi:batchload',    'Literal', XSD.string ]
        tmpdict['flags/usedtd']       = ['xmi:usedtd',       'Literal', XSD.string ]
        tmpdict['flags/logxml']       = ['xmi:logxml',       'Literal', XSD.string ]
        tmpdict['flags/packageFlags'] = ['xmi:packageFlags', 'Literal', XSD.string ]
        tmpdict['model/package2']     = ['xmi:package2',     'Literal', XSD.string ]
        tmpdict['model/package']      = ['xmi:package',      'ModelObject', XSD.string ]
        tmpdict['model/tpos']         = ['xmi:tpos',         'Literal', XSD.string ]
        tmpdict['model/ea_localid']   = ['xmi:ea_localid',   'Literal', XSD.string ]
        tmpdict['model/ea_eleType']   = ['xmi:ea_eleType',   'Literal', XSD.string ]
        tmpdict['model/owner']        = ['xmi:owner',        'Literal', XSD.string ]
        tmpdict['model/name']         = ['xmi:name',         'Literal', XSD.string ]
        tmpdict['properties/isSpecification'] = ['xmi:isSpecification', 'Literal', XSD.boolean ]
        tmpdict['properties/sType']   = ['xmi:sType',        'Literal', XSD.string ]
        tmpdict['properties/nType']   = ['xmi:nType',        'Literal', XSD.string ]
        tmpdict['properties/scope']   = ['xmi:scope',        'Literal', XSD.string ]
        tmpdict['properties/stereotype'] = ['xmi:stereotype','Literal', XSD.string ]
        tmpdict['properties/isRoot']  = ['xmi:isRoot',       'Literal', XSD.boolean ]
        tmpdict['properties/isLeaf']  = ['xmi:isLeaf',       'Literal', XSD.boolean ]
        tmpdict['properties/isAbstract'] = ['xmi:isAbstract','Literal', XSD.boolean ]
        tmpdict['properties/isActive'] = ['xmi:isActive',    'Literal', XSD.boolean ]
        tmpdict['properties/documentation'] = ['xmi:comment','Literal', XSD.string ]
        tmpdict['properties/alias']   = ['xmi:alias',        'Literal', XSD.string ]
        tmpdict['properties/classname'] = ['xmi:classname',  'Literal', XSD.string ]
        tmpdict['project/author']     = ['xmi:author',       'Literal', XSD.string ]
        tmpdict['project/version']    = ['xmi:version',      'Literal', XSD.string ]
        tmpdict['project/phase']      = ['xmi:phase',        'Literal', XSD.string ]
        tmpdict['project/created']    = ['xmi:created',      'Literal', XSD.dateTime ]
        tmpdict['project/modified']   = ['xmi:modified',     'Literal', XSD.dateTime ]
        tmpdict['project/complexity'] = ['xmi:complexity',   'Literal', XSD.string ]
        tmpdict['project/status']     = ['xmi:status',       'Literal', XSD.string ]
        tmpdict['project/difficulty'] = ['xmi:difficulty',   'Literal', XSD.string ]
        tmpdict['project/priority']   = ['xmi:priority',     'Literal', XSD.string ]
        tmpdict['project/keywords']   = ['xmi:keywords',     'Literal', XSD.string ]
        tmpdict['code/gentype']       = ['xmi:gentype',      'Literal', XSD.string ]
        tmpdict['code/product_name']  = ['xmi:product_name', 'Literal', XSD.string ]
        tmpdict['style/appearance']   = ['xmi:appearance',   'Literal', XSD.string ]
        tmpdict['style/styleex']      = ['xmi:styleex',      'Literal', XSD.string ]
        tmpdict['style/object_style'] = ['xmi:object_style', 'Literal', XSD.string ]
        tmpdict['extendedProperties/tagged']       = ['xmi:tagged',       'Literal', XSD.string ]
        tmpdict['extendedProperties/package_name'] = ['xmi:package_name', 'Literal', XSD.string ]
        tmpdict['extendedProperties/relatedlinks'] = ['xmi:relatedlinks', 'Literal', XSD.string ]
        tmpdict['extendedProperties/diagram']      = ['xmi:diagram',      'Literal', XSD.string ]
        tmpdict['extendedProperties/propertyType'] = ['xmi:propertyType', 'Literal', XSD.string ]
        tmpdict['extendedProperties/multiplicity'] = ['xmi:multiplicity', 'Literal', XSD.string ]
        tmpdict['xrefs/value']            = ['xmi:xrefs',                 'Literal', XSD.string ]
        tmpdict['modelDocument/{urn:schemas-microsoft-com:datatypes}dt'] = ['xmi:microsoft-dt', 'Literal', XSD.string ]
        tmpdict['modelDocument/type']     = ['xmi:type',     'Literal', XSD.string ]
        tmpdict['modelDocument/docid']    = ['xmi:docid',    'Literal', XSD.string ]
        tmpdict['modelDocument/name']     = ['xmi:name',     'Literal', XSD.string ]
        tmpdict['modelDocument/date']     = ['xmi:date',     'Literal', XSD.string ]
        tmpdict['modelDocument/notes']    = ['xmi:notes',    'Literal', XSD.string ]
        tmpdict['modelDocument/style']    = ['xmi:style',    'Literal', XSD.string ]
        tmpdict['modelDocument/elementtype'] = ['xmi:elementtype', 'Literal', XSD.string ]
        tmpdict['modelDocument/strcontent'] = ['xmi:strcontent',   'Literal', XSD.string ]
        tmpdict['modelDocument/author']   = ['xmi:author',   'Literal', XSD.string ]
        tmpdict['modelDocument/version']  = ['xmi:version',  'Literal', XSD.string ]
        tmpdict['modelDocument/isactive'] = ['xmi:isactive', 'Literal', XSD.string ]
        tmpdict['modelDocument/sequence'] = ['xmi:sequence', 'Literal', XSD.string ]
        tmpdict['tdoc2/{urn:schemas-microsoft-com:datatypes}dt'] = ['xmi:dt', 'Literal', XSD.string ]
        tmpdict['tdoc2/type']        = ['xmi:type',        'Literal', XSD.string ]
        tmpdict['tdoc2/docid']       = ['xmi:docid',       'Literal', XSD.string ]
        tmpdict['tdoc2/name']        = ['xmi:name',        'Literal', XSD.string ]
        tmpdict['tdoc2/date']        = ['xmi:date',        'Literal', XSD.string ]
        tmpdict['tdoc2/notes']       = ['xmi:notes',       'Literal', XSD.string ]
        tmpdict['tdoc2/style']       = ['xmi:style',       'Literal', XSD.string ]
        tmpdict['tdoc2/elementtype'] = ['xmi:elementtype', 'Literal', XSD.string ]
        tmpdict['tdoc2/strcontent']  = ['xmi:strcontent',  'Literal', XSD.string ]
        tmpdict['tdoc2/author']      = ['xmi:author',      'Literal', XSD.string ]
        tmpdict['tdoc2/version']     = ['xmi:version',     'Literal', XSD.string ]
        tmpdict['tdoc2/isactive']    = ['xmi:isactive',    'Literal', XSD.string ]
        tmpdict['tdoc2/sequence'] = ['xmi:sequence',       'Literal', XSD.string ]
        tmpdict['tdoc2/documents'] = ['xmi:tdoc2',         'Literal', XSD.string ]
        tmpdict['modelDocument/documents'] = ['xmi:modelDocument', 'Literal', XSD.string ]
        tmpdict['ownedComment/body'] = [ 'xmi:body', 'Literal', XSD.string ]
        tmpdict['ownedEnd/aggregation'] = [ 'xmi:aggregation', 'Literal', XSD.string ]
        tmpdict['packagedElement/supplier'] = [ 'xmi:supplier', 'ModelObject', XSD.string ]
        tmpdict['packagedElement/client'] = [ 'xmi:client', 'ModelObject', XSD.string ]
        tmpdict['end/role'] = [ 'xmi:role', 'ModelObject', XSD.string ]
        tmpdict['nestedClassifier/isAbstract'] = [ 'xmi:isAbstract', 'Literal', XSD.string ]
        tmpdict['packagedElement/informationSource'] = [ 'xmi:informationSource', 'ModelObject', XSD.string ]
        tmpdict['packagedElement/informationTarget'] = [ 'xmi:informationTarget', 'ModelObject', XSD.string ]
        tmpdict['lifeline/represents'] = [ 'xmi:represents', 'ModelObject', XSD.string ]
        tmpdict['fragment/covered'] = [ 'xmi:covered', 'Literal', XSD.string ]
        tmpdict['message/messageKind'] = [ 'xmi:messageKind', 'Literal', XSD.string ]
        tmpdict['message/sendEvent'] = [ 'xmi:sendEvent', 'ModelObject', XSD.string ]
        tmpdict['message/receiveEvent'] = [ 'xmi:receiveEvent', 'ModelObject', XSD.string ]
        tmpdict['transition/kind'] = [ 'xmi:kind', 'Literal', XSD.string ]
        tmpdict['transition/source'] = [ 'xmi:source', 'ModelObject', XSD.string ]
        tmpdict['transition/target'] = [ 'xmi:target', 'ModelObject', XSD.string ]
        tmpdict['specification/body'] = [ 'xmi:body', 'Literal', XSD.string ]
        tmpdict['effect/body'] = [ 'xmi:body', 'Literal', XSD.string ]
        tmpdict['subvertex/kind'] = [ 'xmi:kind', 'Literal', XSD.string ]
        tmpdict['edge/source'] = [ 'xmi:source', 'ModelObject', XSD.string ]
        tmpdict['edge/target'] = [ 'xmi:target', 'ModelObject', XSD.string ]
        tmpdict['guard/body'] = [ 'xmi:body', 'Literal', XSD.string ]
        tmpdict['ownedAttribute/visibility'] = [ 'xmi:visibility', 'Literal', XSD.string ]
        tmpdict['packagedElement/classifier'] = [ 'xmi:classifier', 'ModelObject', XSD.string ]
#        tmpdict['uml:UMLDI/Diagram/isFrame'] = [ 'xmi:isFrame', 'Literal', XSD.string ]
#        tmpdict['uml:UMLDI/Diagram/modelElement'] = [ 'xmi:modelElement', 'Literal', XSD.string ]
        tmpdict['heading/text'] = [ 'rdfs:label', 'Literal', XSD.string ]
        tmpdict['ownedElement/modelElement'] = [ 'xmi:modelElement', 'ModelObject', XSD.string ]
        tmpdict['ownedElement/text'] = [ 'rdfs:label', 'Literal', XSD.string ]
        tmpdict['bounds/x'] = [ 'xmi:x', 'Literal', XSD.string ]
        tmpdict['bounds/y'] = [ 'xmi:y', 'Literal', XSD.string ]
        tmpdict['bounds/width'] = [ 'xmi:width', 'Literal', XSD.string ]
        tmpdict['bounds/height'] = [ 'xmi:height', 'Literal', XSD.string ]
        tmpdict['ownedElement/source'] = [ 'xmi:source', 'ModelObject', XSD.string ]
        tmpdict['ownedElement/target'] = [ 'xmi:target', 'ModelObject', XSD.string ]
        tmpdict['waypoint/x'] = [ 'xmi:x', 'Literal', XSD.string ]
        tmpdict['waypoint/y'] = [ 'xmi:y', 'Literal', XSD.string ]
#        tmpdict['uml:UMLDI/Diagram/kind'] = [ 'xmi:kind', 'Literal', XSD.string ]
#        tmpdict['uml:UMLDI/Diagram/sLifelineDashed'] = [ 'xmi:sLifelineDashed', 'Literal', XSD.string ]
        tmpdict['ownedElement/isIcon'] = [ 'xmi:isIcon', 'Literal', XSD.string ]

        tmpdict['properties/ea_type'] = [ 'xmi:ea_type', 'Literal', XSD.string ]
        tmpdict['properties/direction'] = [ 'xmi:direction', 'Literal', XSD.string ]
        tmpdict['appearance/linemode'] = [ 'xmi:linemode', 'Literal', XSD.string ]
        tmpdict['appearance/linecolor'] = [ 'xmi:linecolor', 'Literal', XSD.string ]
        tmpdict['appearance/linewidth'] = [ 'xmi:linewidth', 'Literal', XSD.string ]
        tmpdict['appearance/seqno'] = [ 'xmi:seqno', 'Literal', XSD.string ]
        tmpdict['appearance/headStyle'] = [ 'xmi:headStyle', 'Literal', XSD.string ]
        tmpdict['appearance/lineStyle'] = [ 'xmi:lineStyle', 'Literal', XSD.string ]
        tmpdict['extendedProperties/virtualInheritance'] = [ 'xmi:virtualInheritance', 'Literal', XSD.string ]
        tmpdict['properties/subtype'] = [ 'xmi:subtype', 'Literal', XSD.string ]
        tmpdict['modifiers/isRoot'] = [ 'xmi:isRoot', 'Literal', XSD.string ]
        tmpdict['modifiers/isLeaf'] = [ 'xmi:isLeaf', 'Literal', XSD.string ]
        tmpdict['labels/mt'] = [ 'xmi:mt', 'Literal', XSD.string ]
        tmpdict['labels/mb'] = [ 'xmi:mb', 'Literal', XSD.string ]
        tmpdict['extendedProperties/conditional'] = [ 'xmi:conditional', 'Literal', XSD.string ]
        tmpdict['labels/lt'] = [ 'xmi:lt', 'Literal', XSD.string ]
        tmpdict['labels/rb'] = [ 'xmi:rb', 'Literal', XSD.string ]
        tmpdict['labels/lb'] = [ 'xmi:lb', 'Literal', XSD.string ]
        tmpdict['labels/rt'] = [ 'xmi:rt', 'Literal', XSD.string ]
        tmpdict['properties/name'] = [ 'xmi:name', 'Literal', XSD.string ]
        tmpdict['extendedProperties/stateflags'] = [ 'xmi:stateflags', 'Literal', XSD.string ]
        tmpdict['extendedProperties/privatedata1'] = [ 'xmi:privatedata1', 'Literal', XSD.string ]
        tmpdict['extendedProperties/privatedata2'] = [ 'xmi:privatedata2', 'Literal', XSD.string ]
        tmpdict['extendedProperties/privatedata3'] = [ 'xmi:privatedata3', 'Literal', XSD.string ]
        tmpdict['extendedProperties/privatedata4'] = [ 'xmi:privatedata4', 'Literal', XSD.string ]
        tmpdict['extendedProperties/privatedata5'] = [ 'xmi:privatedata5', 'Literal', XSD.string ]
        tmpdict['extendedProperties/sequence_points'] = [ 'xmi:sequence_points', 'Literal', XSD.string ]
        tmpdict['documentation/value'] = [ 'xmi:value', 'Literal', XSD.string ]
        tmpdict['style/value'] = [ 'xmi:value', 'Literal', XSD.string ]
        tmpdict['packagedElement/name'] = [ 'xmi:name', 'Literal', XSD.string ]
        tmpdict['model/localID'] = [ 'xmi:localID', 'Literal', XSD.string ]
        tmpdict['properties/type'] = [ 'xmi:type', 'Literal', XSD.string ]
        tmpdict['style1/value'] = [ 'xmi:value', 'Literal', XSD.string ]
        tmpdict['style2/value'] = [ 'xmi:value', 'Literal', XSD.string ]
        tmpdict['swimlanes/value'] = [ 'xmi:value', 'Literal', XSD.string ]
        tmpdict['matrixitems/value'] = [ 'xmi:value', 'Literal', XSD.string ]
        tmpdict['model/parent'] = [ 'xmi:parent', 'Literal', XSD.string ]
        for key in tmpdict:
            (element,attrib) = key.split('/')
            if(element not in self.dict):
                self.dict[element] = {}
            self.dict[element].update({attrib:dict(zip(tmpdictkeys, tmpdict[key]))})

    def addProperty(self, g, subjectURI, tag, attribkey, attrib):
        ldmap = self.ldmap(tag, attribkey)
        if( ldmap['subjectType'] == 'Literal' ):
            g.add((subjectURI, URIRefFromString(ldmap['predicateURI']), Literal(attrib)))
        elif( ldmap['subjectType'] == 'ModelObject' ):
            g.add((subjectURI, URIRefFromString(ldmap['predicateURI']), URIRefFromString(self.modelPrefix+attrib)))
        elif( ldmap['subjectType'] == 'MultiModelObject' ):
            objects = attrib.split(' ')
            for obj in objects:
                g.add((subjectURI, URIRefFromString(ldmap['predicateURI']), 
                   URIRefFromString(self.modelPrefix+obj)))

    def toGraph(self, g):
        for tag in self.dict:
            for attrib in self.dict[tag]:
                g.add((URIRefFromString(self.dict[tag][attrib]['predicateURI']), 
                    RDF.type, OWL.ObjectProperty))
                g.add((URIRefFromString(self.dict[tag][attrib]['predicateURI']), RDFS.label,
                    Literal(tag+"."+attrib, lang="en")))

    def ldmap(self, tag, attribkey):
        if(tag not in self.dict):
            self.dict[tag] = {}
        if(attribkey not in self.dict[tag]):
            print("ldmap: UNKNOWN(not found): tmpdict['%s/%s'] = [ 'xmi:%s', 'Literal', XSD.string ]" % (tag, attribkey, attribkey))
            self.dict[tag][attribkey] = {'predicateURI': 'xmi:UNKNOWN', 'subjectType': 'Literal', 'datatype': XSD.string}
        return self.dict[tag][attribkey] 

    def modelprefix(self):
        return self.modelPrefix
