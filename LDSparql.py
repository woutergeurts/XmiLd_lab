#
# utility class to run a series of sparqls from a directory
#

import os
class Sparql:
    def __init__(self, sparqldir):
        self.sparqldir = sparqldir

    def run_all(self,graph):
        #
        # you can enforce seqence with numbering
        #
        sparql_list = os.listdir(self.sparqldir)
        sparql_list.sort()
        for sparqlfile in sparql_list:
            ext = os.path.splitext(sparqlfile)[1]
            if( ext == ".sparql" ):
                with open("%s/%s" % (self.sparqldir,sparqlfile), "r") as f:
                    print( "run_sparqls: run %s"% sparqlfile)
                    query = f.read()
                    graph.update(query)
            else:
                print( "run_sparqls: skip %s"% sparqlfile)
