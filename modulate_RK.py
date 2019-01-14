import sys

def RK(peptides):
    'Receives a list of peptides and returns the proportion R/K'
    lista = []
    for peptide in peptides:
        nR = float(peptide.count('R'))
        nK = float(peptide.count('K'))
        if nK == 0:
            nK = 1
            result = nR/nK
            lista.append(result)
        elif nR == 0:
            nR = 1
            result = nR/nK
            lista.append(result)
        elif nK == 0 and nR == 0:
            result = 0
            lista.append(result)
        else:
            result = nR/nK
            lista.append(result)
    return lista

def evaluate_RK(lista,ratio):
    'Receives a list of R/K values for each stretch and evaluates if it is greater than or equal the chosen cut-off'
    count = 0
    for i in lista:
        if i >= ratio:
            count += 1
    return count

def evaluate(prote, fieldSize,value):
    minCharge = value
    lenght = len(prote)
    last = len(prote)-fieldSize
    find = False
    peptides = []

    if lenght < fieldSize: #prote size < fieldsize
        text = ''
        charge = 0.0
        #read the next lenght caracteres
        for j in range(lenght):
            #hold the sequence of characteres
            text += prote[j]
            #compute the netCharge
            if prote[j] == 'R':
                charge += 1.0
            elif prote[j] == 'K':
                charge += 1.0
            elif prote[j] == 'D':
                charge += -1.0
            elif prote[j] == 'E':
                charge += -1.0
        if charge >= minCharge:
            result = RK([text]), [text]
        else:
            result = [],[]
        return result
    
    #for each character (does not include the last fieldsize characteres)
    for i in range(len(prote)-fieldSize+1):
        text = ''
        charge = 0.0
        #read the next fieldSize caracteres
        for j in range(fieldSize):
            #hold the sequence of characteres
            text += prote[i+j]
            #compute the netCharge
            if text[j] == 'R':
                charge += 1.0
            elif text[j] == 'K':
                charge += 1.0
            elif text[j] == 'D':
                charge += -1.0
            elif text[j] == 'E':
                charge += -1.0
        if charge >= minCharge:
            find = True
            peptides.append(text)
            
    if find:
        result = RK(peptides), peptides
    else:
        result = [],[] #does not find the charge
    return result

#main function
def main():
    names = []
    fieldSize = 30
    #read the program arguments
    if len(sys.argv) < 3:
        print "Use: python", sys.argv[0], "<input complete file name>", "<output root file name>"
        sys.exit(0)

    filein = sys.argv[1] #input file name
    rootfileout = sys.argv[2] #output root file name

    Charges = input('Net Charge: ')
    ratio = input('R/K: ')
    if ratio < 0:
        print 'Do not enter negative values for R/K.'
        sys.exit()

    #read the file's contents
    fin = open(filein, 'r')
    contents = fin.read()
    
    #open the first block of the output file
    fileout  = rootfileout + '_' + '1' + '.txt'
    fout = open(fileout, 'w')
    
    #split the file's contents by '>'
    proteins = str.split(contents, '>')[1:] #the file header is discarded
    #handle each protein...
    for prot in proteins:
        seq = []
        lista = str.split(prot, '\n') #split each protein 
        names.append([lista[0]]) #save the names
        #concatenate the sequences of amino acids of the protein
        for temp in lista[1:]:
            seq.append(temp[:])
            
        seqfinal = ''.join(seq) 
        protName = str.split(lista[0]) #take the first name
        rk, peptides = evaluate(seqfinal, fieldSize,Charges)
        n = evaluate_RK(rk,ratio)

        results = {}
        for name in names[-1]:
            name = str(name)
            results[(name)] = n
            for pair in results:
                if results[pair] > 0:
                    fout.write('>' + pair +'\n')
                    fout.write('Stretches: '+ str(results[pair])+'\n')
                    fout.write('\n')
                    
        
        print protName[0]        

    
    fin.close()
    fout.close()
    print 'Done!'

main()

        

