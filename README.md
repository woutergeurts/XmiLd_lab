# XmiLd_lab
Simple experimental tools to read XMI (UML XML) and express the model in other formats

# Introduction

This script reads an xmi and produces the contained model in Turtle 
format (linked data). the used predicated (xmi: namespace) have not 
(yet) been added to the xmi or uml taxonomy. 

The objective of this exercise is to represent the UML model and metamodel in linked data such that the power of sparql can be used to query information from the model. Ultimately, to gather documentation information (notes, ModelDocuments, documents etc.)

Disclaimer: the code is highly experimental. Development is done using a specific test data (operational models in xmi) and official xmi from OMG. 

# needed packages

```bash
pip3 install rdflib
``` 

# Quick start guide

Install pac
As test type

```bash
. ./go
```
converts the xmi from OMG to uml.ttl umldi.ttl etc.
Study and ament the 'go' script to run your own model.

* xmi2ld.py is the driver script
* LDmap.py contains the mapping from XML to linked data predicates. Every tag and attribute needs to be mapped. Missing mappings lead to error messages.

# WHY??

Modeling tools are strong in modeling, while semantic techniques are strong in combining data and metadata across sources.

Communicating models to stakeholders requires consistent view with viewpoints that address the stakeholder concerns. 
An effective view-style is a text document with tables and pictures. 
This introduces the topic to the reader and guides the reader through the model. 
Building such narrative and generate it with the latest-and-greatest information from the model is best done using different sources of information, otherwise alle text must be added to the model. 

# Approach

## Overview information model
The information model describes that data in a one-to-one fashion. We stay as close as possible to the source, after building the information model we have true linked data.

```xml
<packagedElement xmi:id='abc' xmi:type='uml:Class' attrib1='value1' attrib2='value2'>
  <childtag attrib3='value3'/>
</packagedElement>
``` 

Is in the basis transformed to 
```
model:abc a uml:Class;
   xmi:attrib1 'value1';
   xmi:attrib2 'value2' .

anonimous a xmi:childtag;
   xmi:childof model:abc   
   xmi:attrib3 'value3' 
```

xmi:id, xmi:idref and xmi:type are filtered out to play a role as identity and classifier. All the other attributes are predicates. 

The mapping is not automatically, since the mapping is the place to interpret the values (datatype value or Literal vs ModelElement)

## a note on sequence
A subtle item is sequence
```
<packagedElement xmi:id='M'...>
   <packagedElement xmi:id='A' .../>
   <packagedElement xmi:id='B' .../>
   <packagedElement xmi:id='C' .../>
</packagedElement ...>
```
means 'A,B,C is child of M' but also A, B, C are ordered.

## a note on relations
Relations are instances themselves in the information model

## overview knowledge model
After construction of the information model. We build the knowledge model. There the fun starts.

1) adding owl structures: by adding owl and adding information on the predicates, the resuling triple store can be viewed in e.g. ontodia. Ontodia needs to determine the owl:Class (and subclass structure) and the 'individuals' 
2) adding 'relation' predicates reduce the complexity of sparqls that really matter.

The script scans the directly 'sparql' and just fires these to derive knowledge form the information model.

# Documents

How do you define a document?

# Research
Documents (EA linked documents) are exported as rtf, how can we convert the rtf to useable text (right encoding of diacrites and font conventions (e.g. code blocks)?

How to use the exported diagram jpegs?

Can we use this to transform a model to e.g. SysMLv2

# TODO

There is still lots to be done

* the mapping can be implemented more generically
* the mapping can be based on the XMI standard
* a semantic description of the xmi: predicates might help
* elements and connectors seem redundant with the XMI model, might be ignored (using a switch)
* xml-child-tag within the xml-mother-tag encode an ordering, the LD result does not have that order (yet)
* structure module as a chain (xml -> xmi2ld -> ttl; ttl -> sparql -> ttl; ttl -> ld2doc -> md) with the possibility to combine two or all steps
