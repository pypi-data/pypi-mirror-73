import cmd2
from baboossh import Endpoint, Creds, User

class ExtStr(type):
    def __str__(self):
        return self.getKey()

class BaboosshExt(object,metaclass=ExtStr):
    @classmethod
    def getModType(cls):
        return "export"

    @classmethod
    def getKey(cls):
        return "comprograph"

    @classmethod
    def descr(cls):
        return "Export compromission graph as a dot file"

    @classmethod
    def buildParser(cls,parser):
        parser.add_argument("-f", "--findings", help="List findings",action="store_true")
        parser.add_argument('output',help='Output file path',completer_method=cmd2.Cmd.path_complete)

    @classmethod
    def run(cls,stmt,workspace):
        outfile = getattr(stmt,'output')
        findings = getattr(stmt,'findings',False)
        dotcode = 'digraph compromission_graph {\nnode [shape=plain,fontname="monospace"];\nrankdir="LR";\n'
        for endpoint in workspace.get_objects(endpoints=True,scope=True):
            label = "<table cellborder='1' cellspacing='0'><tr><td>"+str(endpoint)+"</td></tr>"
            if endpoint.host is not None:
                label = label + '<tr><td>'+str(endpoint.host)+'</td></tr>'
            if findings:
                foundEndpoints = Endpoint.find_all(found=endpoint,scope=True)
                foundUsers = User.find_all(found=endpoint,scope=True)
                foundCreds = Creds.find_all(found=endpoint,scope=True)

                if foundEndpoints or foundUsers or foundCreds:
                    label = label + "<tr><td><table cellborder='1' cellspacing='0'><tr><td colspan='2'>Findings</td></tr>"

                    if foundEndpoints :
                        label = label + '<tr><td>Endpoints</td><td>'
                        first = True
                        for foundEndpoint in foundEndpoints:
                            if not first:
                                label = label + '<br />'
                            else:
                                first = False
                            label = label + str(foundEndpoint)
                        label = label + '</td></tr>'

                    if foundUsers :
                        label = label + '<tr><td>Users</td><td>'
                        first = True
                        for user in foundUsers:
                            if not first:
                                label = label + '<br />'
                            else:
                                first = False
                            label = label + str(user)
                        label = label + '</td></tr>'
        
                    if foundCreds :
                        label = label + '<tr><td>Creds</td><td>'
                        first = True
                        for cred in foundCreds:
                            if not first:
                                label = label + '<br />'
                            else:
                                first = False
                            label = label + str(cred)
                        label = label + '</td></tr>'
                    label = label + "</table></td></tr>"
            label = label + "</table>"

            dotcode = dotcode + 'node_'+str(endpoint.id)+' [label=<'+label+'>]\n'
            if endpoint.found is None:
                dotcode = dotcode + '"local" -> "node_'+str(endpoint.id)+'"\n'
            else:
                dotcode = dotcode + '"node_'+str(endpoint.found.id)+'" -> "node_'+str(endpoint.id)+'"\n'
        dotcode = dotcode + '}'
        with open(outfile,"w") as f:
            f.write(dotcode)
        print("Export saved as "+outfile)
        return True
    
