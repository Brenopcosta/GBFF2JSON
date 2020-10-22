import json

def adicionarLOCUS(gbffDict, textoFonte, primeiraLinhaDoGenoma ):
    gbffDict["LOCUS"] = primeiraLinhaDoGenoma[11:].replace("\"","").replace("\'","")


def adicionarDEFINITION(gbffDict, textoFonte):
        linha = textoFonte.readline()
        gbffDict["DEFINITION"] = linha[10:].replace("\"","").replace("\'","")

        while(True):
            linha = textoFonte.readline()
            if (linha[:9] == "ACCESSION"):
                return linha

            gbffDict["DEFINITION"] = gbffDict["DEFINITION"] + linha[12:].replace("\"","").replace("\'","")

def adicionarACCESSION(gbffDict, textoFonte, primeiraLinhaAccession):
    gbffDict["ACCESSION"] = primeiraLinhaAccession[12:].replace("\"","").replace("\'","")

def adicionarVERSION(gbffDict, textoFonte):
    linha = textoFonte.readline()
    gbffDict["VERSION"] = linha[12:].replace("\"","").replace("\'","")

def adicionarDBLINK(gbffDict, textoFonte):
    linha = textoFonte.readline()
    if (linha[:6] == "DBLINK"):
        gbffDict["DBLINK"] = linha[12:].replace("\"","").replace("\'","")
        
        while(True):
            linha = textoFonte.readline()
            
            if (linha[:8] == "KEYWORDS"):
                return linha
                
            gbffDict["DBLINK"] = gbffDict["DBLINK"] + linha[12:].replace("\"","").replace("\'","")
    
    else:
        return linha

def adicionarKEYWORDS(gbffDict, textoFonte, primeiraLinhaKeywords):
    gbffDict["KEYWORDS"] = primeiraLinhaKeywords[12:].replace("\"","").replace("\'","")

def adicionarSOURCE(gbffDict, textoFonte):
    linha = textoFonte.readline()
    gbffDict["SOURCE"] = linha[12:].replace("\"","").replace("\'","").replace("\'","")

def adicionarORGANISM(gbffDict, textoFonte):
    primeiraLinhaOrganism = textoFonte.readline()
    gbffDict["ORGANISM"] = primeiraLinhaOrganism[11:].replace("\"","").replace("\'","")

    while(True):
        linha = textoFonte.readline()
        if(linha[:9] == "REFERENCE"):
            return linha

        gbffDict["ORGANISM"] = gbffDict["ORGANISM"] + linha[12:].replace("\"","").replace("\'","")


def adicionarREFERENCE(gbffDict, textoFonte , primeiraLinhaReference):
    gbffDict["REFERENCE"] = primeiraLinhaReference[12:].replace("\"","").replace("\'","")

    while(True):
        linha = textoFonte.readline()
        if(linha[:9] == "REFERENCE"):
            return adicionarREFERENCE(gbffDict, textoFonte , linha)
        elif(linha[:7] == "COMMENT"):
            return linha
        elif(linha[:8] == "FEATURES"):
            return linha    
        else:
            gbffDict["REFERENCE"] = gbffDict["REFERENCE"] + linha[12:].replace("\"","").replace("\'","")

def adicionarCOMMENT(gbffDict, textoFonte , primeiraLinhaComment):
    if(primeiraLinhaComment[:7] != "COMMENT"):
        return primeiraLinhaComment
    
    gbffDict["COMMENT"] = primeiraLinhaComment[12:].replace("\"","").replace("\'","")

    while(True):
        linha = textoFonte.readline()
        if(linha[:8] == "FEATURES"):
            return linha
        gbffDict["COMMENT"] = gbffDict["COMMENT"] + linha[12:].replace("\"","").replace("\'","")

def adicionarFEATURES(gbffDict, textoFonte , primeiraLinhaFeatures):
    gbffDict["FEATURES"] = primeiraLinhaFeatures[12:].replace("\"","").replace("\'","")
    while(True):
        linha = textoFonte.readline()
        if(linha[:6] == "CONTIG"):
            return linha
        elif(linha[:6] == "ORIGIN"):
            return linha
        else:
            gbffDict["FEATURES"] = gbffDict["FEATURES"] + linha[5:].replace("\"","").replace("\'","")


def adicionarCONTIG(gbffDict, textoFonte , primeiraLinhaContig):
    if(primeiraLinhaContig[:7] != "CONTIG"):
        return primeiraLinhaContig
    
    gbffDict["CONTIG"] = primeiraLinhaFeatures[12:].replace("\"","").replace("\'","")
    return textoFonte.readline()


def adicionarORIGIN(gbffDict, textoFonte , primeiraLinhaOrign):
    gbffDict["ORIGIN"] = ""
    while(True):
        linha = textoFonte.readline()
        if(linha[:2] == "//"):
            return
        #print("Adicionando linha de numero" + linha[:12])
        gbffDict["ORIGIN"] = gbffDict["ORIGIN"] + linha.replace("\"","").replace("\'","")


def main():
    outPutDictionary = dict()
    
    with open('example2.gbff', 'r') as textoFonte:            
        
        primeiraLinhaDoGenoma = textoFonte.readline()

        fimDoArquivo = False

        identificacaoGenoma = 0

        while (fimDoArquivo == False):
            gbffDict = dict()
            
            adicionarLOCUS(gbffDict, textoFonte, primeiraLinhaDoGenoma)
            
            primeiraLinhaAccession = adicionarDEFINITION(gbffDict, textoFonte)
            
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

            outPutDictionary[identificacaoGenoma] = gbffDict

            identificacaoGenoma +=1
            
            linhaAposGenoma = textoFonte.readline()

            if (linhaAposGenoma == ""):
                break
            
            primeiraLinhaDoGenoma = linhaAposGenoma
    
    jsonRetorno = json.dumps(outPutDictionary)

    return jsonRetorno
