import pymel.core as pm

ch_name = 'test'


def spineOption(s_name, i_joint, b_axis, b_mirror):
    outGrp = pm.createNode('transform', n=ch_name + s_name)
    parentGrp = pm.createNode('transform', n=ch_name + s_name + 'Parent')
    TopGrp = pm.createNode('transform', n=ch_name + s_name + 'Top')
    intCount = 0
    NumGrpList = []
    for i in range(0, intCount):
        NumGrp = pm.createNode('transform', n=f'{ch_name}_{s_name}_{i:02}Grp')
        pm.parent(NumGrp, parentGrp)
        NumGrpList.append(NumGrp)
    NumGrpWeight = [(i + 1) / (n + 1) for i in range(i_joint)]
    NumGrpWeightRev = NumGrpWeight.reverse()
    for i in range(i_joint):
    # NumGrpList 를 불러와서 웨이트 를 각각 넣어주면 끝.
    return outGrp


def qrpct(nodea, nodeb, nodec, weighta, weightb):
    nodea = pm.PyNode(nodea)
    nodeb = pm.PyNode(nodeb)
    nodec = pm.PyNode(nodec)
    weighta = pm.PyNode(weighta)
    weightb = pm.PyNode(weightb)
    # create multMatrixa
    mtma = pm.createNode('multMatrix', n=nodea + '_a_MTM')
    mtmb = pm.createNode('multMatrix', n=nodeb + '_b_MTM')
    # create decomposeMatrix
    dcma = pm.createNode('decomposeMatrix', n=nodea + '_a_DCM')
    dcmb = pm.createNode('decomposeMatrix', n=nodeb + '_b_DCM')
    # create multiplyDivide
    mtdta = pm.createNode('multiplyDivide', n=nodea + '_ta_MTD')
    mtdtb = pm.createNode('multiplyDivide', n=nodeb + '_tb_MTD')
    mtdra = pm.createNode('multiplyDivide', n=nodea + '_ra_MTD')
    mtdrb = pm.createNode('multiplyDivide', n=nodeb + '_rb_MTD')
    # create plusMinusAverage
    pmaa = pm.createNode('plusMinusAverage', n=nodea + '_a_PMA')
    pmab = pm.createNode('plusMinusAverage', n=nodeb + '_b_PMA')
    # connect multmatrix
    nodea.worldMatrix[0] >> mtma.matrixIn[0]
    nodec.parentInverseMatrix >> mtma.matrixIn[1]
    nodeb.worldMatrix[0] >> mtmb.matrixIn[0]
    nodec.parentInverseMatrix >> mtmb.matrixIn[1]
    # connect decomposematrix
    mtma.matrixSum >> dcma.inputMatrix
    mtmb.matrixSum >> dcmb.inputMatrix
    # connect multiply translate
    dcma.outputTranslate >> mtdta.input1
    dcmb.outputTranslate >> mtdtb.input1
    mtdta.output >> pmaa.input3D[0]
    mtdtb.output >> pmaa.input3D[1]
    pmaa.output3D >> nodec.translate
    # connect multiply rotate
    dcma.outputRotate >> mtdra.input1
    dcmb.outputRotate >> mtdrb.input1
    mtdra.output >> pmab.input3D[0]
    mtdrb.output >> pmab.input3D[1]
    pmab.output3D >> nodec.rotate
    # connect weight attribute
    weighta >> mtdta.input2X
    weighta >> mtdta.input2Y
    weighta >> mtdta.input2Z
    weightb >> mtdtb.input2X
    weightb >> mtdtb.input2Y
    weightb >> mtdtb.input2Z
    weighta >> mtdra.input2X
    weighta >> mtdra.input2Y
    weighta >> mtdra.input2Z
    weightb >> mtdrb.input2X
    weightb >> mtdrb.input2Y
    weightb >> mtdrb.input2Z


def qrrv(input1, input2, name='subtract'):
    input1 = pm.PyNode(input1)
    input2 = pm.PyNode(input2)
    # reverse subtract
    fms = pm.createNode('floatMath', n=name + '_FMS')
    input1 >> fms.floatB
    fms.operation.set(1)
    # output
    fms.outFloat >> input2


qrrv('pCube4.test', 'pCube4.retest')
qrpct('pCube1', 'pCube2', 'pCube3', 'pCube3.test', 'pCube3.retest')    