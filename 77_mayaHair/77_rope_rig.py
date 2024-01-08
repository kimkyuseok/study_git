# 로프 리깅  
# 인풋  시작과 끝  조인트 갯수  기본 100개 에  트렌스 11개  디테일 컨트롤러 21개  # 아웃풋  리깅된 로프 
import pymel.core as pm
chackStartEnd=False
selObj=pm.ls(sl=1,fl=1)
startObj=None
endObj=None
startPOS=None
endPOS=None
# 시작과 끝 
if len(selObj)==2:
    startObj = selObj[0]
    endObj = selObj[1]
    chackStartEnd=True
    startPOS = startObj.getTranslation(space='world')    
    endPOS = endObj.getTranslation(space='world')
# 기본 컨트롤러     3개  +1 개 만들꺼임
prop_all_C=None
prop_move_C=None
prop_move1_C=None
rope_aim_C=None
if chackStartEnd:    
    # 기본 컨트롤러  서클 3개  prop_all_C   prop_move_C   prop_move1_C   
    prop_all_C=pm.circle(r=2, nr=(0, 1, 0), c=(0, 0, 0) ,n='prop_all_C')
    prop_move_C=pm.circle( nr=(0, 1, 0), c=(0, 0, 0) ,n='prop_move_C')
    prop_move1_C=pm.circle( nr=(0, 1, 0), c=(0, 0, 0) ,n='prop_move1_C')
    # 기본 컨트롤러  박스 1개  rope_aim_C
    rope_aim_C=pm.curve( d=1, p=[(0.5, 0, -0.5), (-0.5, 0, -0.5), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5)] ,n='rope_aim_C')
# 기본 컨트롤러 포지션
# prop_all_C 는 기본상태로 있자
# prop_move_C , rope_aim_C  는 end 위치    
# prop_move1_C 는 str 위치에 놓자 
prop_move1_C[0].t.set(startPOS)
prop_move_C[0].t.set(endPOS)
rope_aim_C.t.set(endPOS)
# rotate 작업 ??? 일단 패스 
# 커브를 만들어 
rope_srtend_curve = pm.curve( d=1, p=[(startPOS), (endPOS)] , n='rope_srtend_curve')
# length joint position list
# lengthPos11
lengthPos11=[]
Length_Joint_pointOnCurveInfo = pm.createNode('pointOnCurveInfo',n='Length_Joint_pointOnCurveInfo')
rope_srtend_curveShape = pm.PyNode(rope_srtend_curve).getChildren()[0]
rope_srtend_curveShape.worldSpace[0] >> Length_Joint_pointOnCurveInfo.inputCurve
Length_Joint_pointOnCurveInfo.turnOnPercentage.set(1)
for i in range(0,11):
    Length_Joint_pointOnCurveInfo.parameter.set(i*0.1)
    getPOS=Length_Joint_pointOnCurveInfo.position.get()
    lengthPos11.append(getPOS)
# 조인트 만들기 11개
ropeLengthJoint=[]
numi=0    
for i in lengthPos11:
    newjoint = pm.createNode('joint',n=f'ropeLength00{numi}_jnt')
    newjoint.t.set(i)
    numi = numi+1
    ropeLengthJoint.append(newjoint)
# 조인트 리스트를 주면 순서대로 페어런츠 해주기 
ropeLengthJoint.reverse()
for i in range(0,len(ropeLengthJoint)-1):
    pm.parent(ropeLengthJoint[i],ropeLengthJoint[i+1])
# 스플라인 ik를 적용 
pm.ikHandle(n='test',sol='ikSplineSolver',ccv=0,scv=0,pcv=0,sj=ropeLengthJoint[-1],ee=ropeLengthJoint[0],c=rope_srtend_curve)
# 클러스터를 적용
ropeLengthJointCluster_Str=pm.cluster(rope_srtend_curve+'.cv[0]',n='ropeLengthJointCluster_Str')
ropeLengthJointCluster_End=pm.cluster(rope_srtend_curve+'.cv[1]',n='ropeLengthJointCluster_End')
# curveInfo 를 만들어서 길이 겟. 
lengthCurveBase=None
Length_Joint_CurveInfo = pm.createNode('curveInfo',n='Length_Joint_CurveInfo')
rope_srtend_curveShape.worldSpace[0] >> Length_Joint_CurveInfo.inputCurve
lengthCurveBase=Length_Joint_CurveInfo.arcLength.get()
# 스케일을 적용하자 
scaleSet = pm.createNode('transform',n='scaleSet')
pm.PyNode(prop_all_C[0]).sx >> pm.PyNode(prop_all_C[0]).sy
pm.PyNode(prop_all_C[0]).sx >> pm.PyNode(prop_all_C[0]).sz
pm.PyNode(prop_all_C[0]).s >>  scaleSet.s  
Length_MDL = pm.createNode('multDoubleLinear',n='Length_MDL')
scaleSet.sx >> Length_MDL.input1
Length_MDL.input2.set(lengthCurveBase)
Length_MDD = pm.createNode('multiplyDivide',n='Length_MDD')
Length_Joint_CurveInfo.arcLength >> Length_MDD.input1X
Length_MDL.output    >> Length_MDD.input2X
Length_MDD.operation.set(2)
# 스테치 적용 
for i in ropeLengthJoint:
    _MDL=pm.createNode('multDoubleLinear',n=i+'_MDL')
    jointTY=i.ty.get()
    _MDL.input2.set(jointTY)
    Length_MDD.outputX >> _MDL.input1
    _MDL.output >> i.ty
# 클러스터 연결
pm.parentConstraint(prop_move1_C[0],ropeLengthJointCluster_Str,mo=1)
pm.parentConstraint(rope_aim_C,ropeLengthJointCluster_End,mo=1)
"""
여기서부터는  11개 컨트롤러 
"""

# 11개 클러스터 생성 할  커브 생성 커브 위치는 이전 조인트 위치를 포인트로 바꿔서 만든다. 
rope_base_curve=pm.curve( d=3, p=lengthPos11 ,n='rope_base_curve')
# 클러스터 11개를 만들고 
rope_base_curve_cluster=[]
for i in range(0,11):
    _cluster=pm.cluster(rope_base_curve+f'.cv[{i}]',n=f'ropebase00{i}_cluster')
    rope_base_curve_cluster.append(_cluster)
# 로테이션 되면서 트렌스되는 중간 컨트롤러 생성 박스 십자가
boxctrllist=[]
tenctrllist=[]
for i in range(0,11):
    boxctrl=pm.curve(n=f'rope_{i}_C' ,d=1, p=[(-0.5, 0.5, 0.5),(0.5, 0.5, 0.5),(0.5, 0.5, -0.5),(-0.5, 0.5, -0.5),(-0.5, 0.5, 0.5),(-0.5, -0.5, 0.5),(-0.5, -0.5, -0.5),(0.5, -0.5, -0.5),(0.5, -0.5, 0.5),(-0.5, -0.5, 0.5),(0.5, -0.5, 0.5),(0.5, 0.5, 0.5),(0.5, 0.5, -0.5),(0.5, -0.5, -0.5),(-0.5, -0.5, -0.5),(-0.5, 0.5, -0.5)] )    
    tenctrl=pm.curve(n=f'rope_in_{i}_C', d=1, p=[(-1,0,-1),(-1,0,-2),(1,0,-2),(1,0,-1),(2,0,-1),(2,0,1),(1,0,1),(1,0,2),(-1,0,2),(-1,0,1),(-2,0,1),(-2,0,-1),(-1,0,-1)])
    pm.select(tenctrl+'.cv[*]')
    pm.scale(0.5,0.5,0.5,r=True)
    boxctrllist.append(boxctrl)
    tenctrllist.append(tenctrl)    
pm.select(cl=1)
rope_CG = pm.createNode('transform',n='rope_CG')
parentNode=rope_CG 
for i in range(0,11):
    _G = pm.group(boxctrllist[i],n = boxctrllist[i]+'_G')
    _in_G = pm.group(tenctrllist[i],n = tenctrllist[i]+'in_G')
    pm.parent(_in_G,boxctrllist[i])
    _G.t.set(lengthPos11[i])
    pm.parent(_G,parentNode)
    parentNode= boxctrllist[i]

# Length Joint To rppe_0_CG 연결
pm.parentConstraint('ropeLength000_jnt','rope_0_C_G',mo=1)

# 베이스 21개 조인트 생성
basePos21=[]
for i in range(0,21):
    Length_Joint_pointOnCurveInfo.parameter.set(i*0.05)
    getPOS=Length_Joint_pointOnCurveInfo.position.get()
    basePos21.append(getPOS)
#    
