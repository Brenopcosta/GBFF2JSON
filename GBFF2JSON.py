
def adicionarLOCUS(gbffDict, textoFonte ):
    while(True):
        linha = textoFonte.readline()
        
        if (linha[:10] == "DEFINITION"):
            return linha
        
        gbffDict["LOCUS"] = linha[11:]


def adicionarDEFINITION(gbffDict, textoFonte, primeiraLinhaDefinition):
        gbffDict["DEFINITION"] = primeiraLinhaDefinition[10:]

        while(True):
            linha = textoFonte.readline()
            if (linha[:9] == "ACCESSION"):
                return linha

            gbffDict["DEFINITION"] = gbffDict["DEFINITION"] + linha[12:]

def adicionarACCESSION(gbffDict, textoFonte, primeiraLinhaAccession):
    gbffDict["ACCESSION"] = primeiraLinhaAccession[12:]

def adicionarVERSION(gbffDict, textoFonte):
    linha = textoFonte.readline()
    gbffDict["VERSION"] = linha[12:]

def adicionarDBLINK(gbffDict, textoFonte):
    linha = textoFonte.readline()
    if (linha[:6] == "DBLINK"):
        gbffDict["DBLINK"] = linha[12:]
        
        while(True):
            linha = textoFonte.readline()
            
            if (linha[:8] == "KEYWORDS"):
                return linha
                
            gbffDict["DBLINK"] = gbffDict["DBLINK"] + linha[12:]
    
    else:
        return linha

def adicionarKEYWORDS(gbffDict, textoFonte, primeiraLinhaKeywords):
    gbffDict["KEYWORDS"] = primeiraLinhaKeywords[12:]

def adicionarSOURCE(gbffDict, textoFonte):
    linha = textoFonte.readline()
    gbffDict["SOURCE"] = linha[12:]

def adicionarORGANISM(gbffDict, textoFonte):
    primeiraLinhaOrganism = textoFonte.readline()
    gbffDict["ORGANISM"] = primeiraLinhaOrganism[11:]

    while(True):
        linha = textoFonte.readline()
        if(linha[:9] == "REFERENCE"):
            return linha

        gbffDict["ORGANISM"] = gbffDict["ORGANISM"] + linha[12:]


def adicionarREFERENCE(gbffDict, textoFonte , primeiraLinhaReference):
    gbffDict["REFERENCE"] = primeiraLinhaReference[12:]

    while(True):
        linha = textoFonte.readline()
        if(linha[:9] == "REFERENCE"):
            return adicionarREFERENCE(gbffDict, textoFonte , linha)
        elif(linha[:7] == "COMMENT"):
            return linha
        elif(linha[:8] == "FEATURES"):
            return linha    
        else:
            gbffDict["REFERENCE"] = gbffDict["REFERENCE"] + linha[12:]

def adicionarCOMMENT(gbffDict, textoFonte , primeiraLinhaComment):
    if(primeiraLinhaComment[:7] != "COMMENT"):
        return primeiraLinhaComment
    
    gbffDict["COMMENT"] = primeiraLinhaComment[12:]

    while(True):
        linha = textoFonte.readline()
        if(linha[:8] == "FEATURES"):
            return linha
        gbffDict["COMMENT"] = gbffDict["COMMENT"] + linha[12:]

def adicionarFEATURES(gbffDict, textoFonte , primeiraLinhaFeatures):
    gbffDict["FEATURES"] = primeiraLinhaFeatures[12:]
    while(True):
        linha = textoFonte.readline()
        if(linha[:6] == "CONTIG"):
            return linha
        elif(linha[:6] == "ORIGIN"):
            return linha
        else:
            gbffDict["FEATURES"] = gbffDict["FEATURES"] + linha[5:]


def adicionarCONTIG(gbffDict, textoFonte , primeiraLinhaContig):
    if(primeiraLinhaContig[:7] != "CONTIG"):
        return primeiraLinhaContig
    
    gbffDict["CONTIG"] = primeiraLinhaFeatures[12:]
    return textoFonte.readline()


def adicionarORIGIN(gbffDict, textoFonte , primeiraLinhaOrign):
    gbffDict["ORIGIN"] = ""
    while(True):
        linha = textoFonte.readline()
        if(linha[:2] == "//"):
            return
        print("Adicionando linha de numero" + linha[:12])
        gbffDict["ORIGIN"] = gbffDict["ORIGIN"] + linha

def main():
    gbffDict = dict()
    with open('example.gbff', 'r') as textoFonte:            
        
        primeiraLinhaDefinition = adicionarLOCUS(gbffDict, textoFonte)
        
        primeiraLinhaAccession = adicionarDEFINITION(gbffDict, textoFonte, primeiraLinhaDefinition)
        
        adicionarACCESSION(gbffDict, textoFonte, primeiraLinhaAccession)
        
        adicionarVERSION(gbffDict, textoFonte)

        primeiraLinhaKeywords = adicionarDBLINK(gbffDict, textoFonte)

        adicionarKEYWORDS(gbffDict, textoFonte, primeiraLinhaKeywords)
        
        adicionarSOURCE(gbffDict, textoFonte)

        primeiraLinhaReference = adicionarORGANISM(gbffDict, textoFonte)

        primeiraLinhaComment = adicionarREFERENCE(gbffDict, textoFonte , primeiraLinhaReference)

        primeiraLinhaFeatures = adicionarCOMMENT(gbffDict, textoFonte , primeiraLinhaComment)
        
        primeiraLinhaContig = adicionarFEATURES(gbffDict, textoFonte , primeiraLinhaFeatures)

        primeiraLinhaOrigin = adicionarCONTIG(gbffDict, textoFonte , primeiraLinhaContig)
        
        adicionarORIGIN(gbffDict, textoFonte , primeiraLinhaOrigin)

    return gbffDict
