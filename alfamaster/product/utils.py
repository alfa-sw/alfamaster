totalArray = []

def list2html(lista, currency):
    # lista [
    #   {'bases': [{'g_100g': '25'}, {'g_100g': '5'}, {'g_100g': '0'}],
    #    'RM_cost': '0',
    #    'raw_material': 'H2O',
    #    'specific_weight': '1'},
    #    { .. }
    # ]

    print("lista {}".format(lista))
    print("type lista : {}".format(type(lista)))

    listofFormula = []
    nbases = 0

    for d in lista:
        formula = []
        for k, v in sorted(d.items()):
            # k: RM_cost | v: 0.58
            # k: bases | v: [{'g_100g': '0.1'}, ..]
            # k: raw_material | v: nh3
            # k: specific_weight | v: 1
            # print("k: {} | v: {}".format(k,v))
            if 'RM_cost' in k:
                formula.append(v)
            if 'bases' in k:
                arrayofBases = []
                arrayofBases = convertBasesListToArray(v)
                formula.extend(arrayofBases)
                nbases = len(v)
            if 'raw_material' in k:
                formula.insert(0,v)
            if 'specific_weight' in k:
                formula.insert(1,v)

        listofFormula.append(formula)


    thead1stRow = [None, None, None, 'Base1 (PASTEL)', 'TiO<sub>2</sub> slurry', 'Base2']
    thead2ndRow = ['Raw material', 'Specific weight [g/mL]', 'RM cost']
    theadBase = ['%w/w','mL/100g', '%v/v', 'mL/1000g']
    formulaCost = 'Formula Cost ['+currency+']'
    theadBase.append(formulaCost)
    
    for i in range(nbases):
        thead2ndRow.extend(theadBase)
        if i > 2:
            newBase = 'Base'+str(i)
            thead1stRow.append(newBase)

    # a = populateMatrixFormulaBody(listofFormula, nbases)
    populateMatrixFormulaBody(listofFormula, nbases)
    # print("thead1stRow completed : {}".format(thead1stRow))
    # print("thead2ndRow completed : {}".format(thead2ndRow))
    listofFormula.insert(0,thead1stRow)
    listofFormula.insert(1,thead2ndRow)

    tfooter = ['Total']
    nCellTfooterMissing = len(thead2ndRow) - 3
    for i in range(nCellTfooterMissing):
        tfooter.append(None)

    populateFormulaFooter(tfooter)
    
    listofFormula.append(tfooter)

    return listofFormula
    
def convertBasesListToArray(bases):
    # [{'g_100g': '0'}, {'g_100g': '0'}, {'g_100g': '0'}]
    nbases = len(bases)
    basesListToArray = []

    for base in bases:
        for k,v in base.items():
            # print("k: {} | v: {}".format(k,v))
            basesListToArray.append(v)
            basesListToArray.extend([None, None, None, None])

    return basesListToArray

def populateMatrixFormulaBody(matrixFormula, nbases):
    # this formula has no header no footer
    sum_ml100g = 0
    sum_vv = 0
    sum_ml1000g = 0
    sum_fcost = 0

    swArray = []
    rmcostArray = []
    ml100gArray = []
    vvArray = []
    ml1000gArray = []
    fcostArray = []
    # totalArray = []

    for array in matrixFormula:
        swArray.append(array[1])
        rmcostArray.append(array[2])

    for i in range(nbases):
        # print("i:{} in range{}".format(i, nbases))
        sumofMl100g = 0.0
        sumofVv = 0.0
        sumofMl1000g = 0.0
        sumofFcost = 0.0
        sumofWW = 0.0

        for array in matrixFormula:
            index = i*5
            ww = array[3+index]
            # ww = "{:.3f}".format(operand1_ww)
            # print("ww : {}".format(operand1_ww))
            sumofWW += float(ww)
        # wwArray.append(sumofWW)

        for array in matrixFormula:
            index = i*5
            operand1_ml100g = array[3+index]
            operand2_ml100g = array[1]
            # print("{} / {}".format(operand1_ml100g, operand2_ml100g))
            _ml100g = float(operand1_ml100g)/float(operand2_ml100g)
            ml100g = "{:.3f}".format(_ml100g)
            # print("ml100g : {}".format(ml100g))
            sumofMl100g += float(ml100g)
            ml100gArray.append(ml100g)


        # for array in matrixFormula:
        for idx,array in enumerate(matrixFormula):
            index = i*5
            operand1_vv = ml100gArray[idx+index]
            operand2_vv = sumofMl100g
            # print("operand1_vv:{} / operand2_vv:{}".format(operand1_vv, operand2_vv))
            _vv = (float(operand1_vv)*100)/float(operand2_vv)
            vv = "{:.3f}".format(_vv)
            # print("vv : {}".format(vv))
            sumofVv += float(vv)
            vvArray.append(vv)

        for idx,array in enumerate(matrixFormula):
            index = i*5
            operand1_ml1000g = vvArray[idx+index]
            # print("operand1_ml1000g: {}".format(operand1_ml1000g))
            _ml1000g = float(operand1_ml1000g)*10
            ml1000g = "{:.3f}".format(_ml1000g)
            # print("vv : {}".format(vv))
            sumofMl1000g += float(ml1000g)
            ml1000gArray.append(ml1000g)

        for idx,array in enumerate(matrixFormula):
            index = i*5
            # print("         swArray[idx] -> {}".format(swArray[idx]))
            operand1_fcost = swArray[idx]
            operand2_fcost = rmcostArray[idx]
            operand3_fcost = vvArray[idx+index]
            # print("operand1_vv:{} / operand2_vv:{}".format(operand1_vv, operand2_vv))
            _fcost = ((float(operand1_fcost)*float(operand2_fcost))/1000)*(float(operand3_fcost))
            fcost = "{:.3f}".format(_fcost)
            # print("vv : {}".format(vv))
            sumofFcost += float(fcost)
            fcostArray.append(fcost)

        totalArray.extend([sumofWW,sumofMl100g , sumofVv, sumofMl1000g, sumofFcost])

        print("sumofMl100g -> {}".format(sumofMl100g))
        print("ml100gArray -> {}".format(ml100gArray))
        print("vvArray -> {}".format(vvArray))
        print("ml1000gArray -> {}".format(ml1000gArray))
        print("fcostArray -> {}".format(fcostArray))
        print("totalArray -> {}".format(totalArray))
        print(".")

    matrixCalculatedValues = [ml100gArray, vvArray, ml1000gArray, fcostArray]
    matrixCalculatedValuesTransposed = [[matrixCalculatedValues[j][i] for j in range(len(matrixCalculatedValues))] for i in range(len(matrixCalculatedValues[0]))] 
    # print("matrixCalculatedValuesTransposed :\n{}".format(matrixCalculatedValuesTransposed))
    # print("matrixCalculatedValues :\n{}".format(matrixCalculatedValues))


    # ! ~~ create base listofIndex depending on base's number
    listofIndex = [0,5,10]
    if nbases > 3:
        nbasesDefault = len(listofIndex)
        missingIndex = nbases - nbasesDefault
        for i in range(missingIndex):
            try:
                lastVal = listofIndex[-1]
                lastVal += 5
                listofIndex.append(lastVal)
            except:
                print(" @ exception @")
                break

    # ! ~~ create calcuted listofIndex based on [ml100gArray, vvArray, ml1000gArray, fcostArray]
    lunghezza = len(matrixCalculatedValues)
    listofIndexCalculated = []
    for i in range(lunghezza):
        for idx,v in enumerate(listofIndex):
            val = listofIndex[idx]
            val += 1+i
            limit = listofIndex[-1] + 4
            if val <= limit:
                listofIndexCalculated.append(val)        
    listofIndex.extend(listofIndexCalculated)
    # print("listofIndex :\n{}".format(listofIndex))
    # [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]

    numofRawMat = len(matrixFormula)

    # ! ~~ create empty matrix containter
    matrix = []
    for i in range(numofRawMat):
        tmp = []
        matrix.append(tmp)

    # ! ~~ populate empty matrix with values
    '''
        eg matrix
        [
            ['25.000', '44.117', '441.170', '0.000', '5.000', '12.500', '125.000', '0.000', '0.000', '0.000', '0.000', '0.000'],
            ['20.000', '35.294', '352.940', '0.141', '10.000', '25.000', '250.000', '0.100', '0.500', '100.000', '1000.000', '0.400'],
            ['11.667', '20.589', '205.890', '0.191', '25.000', '62.500', '625.000', '0.581', '0.000', '0.000', '0.000', '0.000'],
            ['0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000'],
            ['0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000']
        ]
    '''
    counter = 0
    for i in range(numofRawMat):
        idx = i + (2*i)
        # print("idx -> {}".format(idx))
        for k,v in enumerate(listofIndex):
            if idx == 0:
                if k < nbases:
                    # print("k {} -> v {}".format(k,matrixCalculatedValuesTransposed[v]))
                    matrix[i].extend(matrixCalculatedValuesTransposed[v])
            elif k>=idx and k < (idx + nbases ) :
                # print("k {} -> v {}".format(k,matrixCalculatedValuesTransposed[v]))
                matrix[i].extend(matrixCalculatedValuesTransposed[v])


    # ! ~~ substitute None with specific values from matrix
    for idx, array in enumerate(matrixFormula):
        counter = 0
        for v in array:
            if v is None:
                idxNone = array.index(v)
                # print("spotted a None at index : {}".format(idxNone))
                # print("specific value -> {}".format(matrix[idx].pop(0)))
                array[idxNone] = matrix[idx].pop(0)


    return matrixFormula

def populateFormulaFooter(tfooter):
    innerTotalArray = totalArray
    for v in tfooter:
        if v is None:
            idxNone = tfooter.index(v)
            tfooter[idxNone] = innerTotalArray.pop(0)