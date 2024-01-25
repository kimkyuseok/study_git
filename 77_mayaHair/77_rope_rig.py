# 로프 리깅  
# 인풋  시작과 끝  ( 로케이터 2개 선택하고 실행 )
# 조인트 갯수  기본 100개 에  트렌스 11개  디테일 컨트롤러 21개  # 아웃풋  리깅된 로프 
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
    prop_move_C=pm.circle(r=1.5, nr=(0, 1, 0), c=(0, 0, 0) ,n='prop_move_C')
    prop_move1_C=pm.circle( nr=(0, 1, 0), c=(0, 0, 0) ,n='prop_move1_C')
    # 기본 컨트롤러  박스 1개  rope_aim_C
    rope_aim_C=pm.curve( d=1, p=[(0.5, 0, -0.5), (-0.5, 0, -0.5), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5)] ,n='rope_aim_C')
    pm.select(rope_aim_C+'.cv[*]')
    pm.scale(1.7,1.7,1.7,r=True)    
# 기본 컨트롤러 포지션
# prop_all_C 는 기본상태로 있자
# prop_move_C , rope_aim_C  는 end 위치    
# prop_move1_C 는 str 위치에 놓자 
prop_all_C[0].t.set(startPOS)
prop_move1_C[0].t.set(startPOS)
prop_move_C[0].t.set(startPOS)
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
ropeLengthIkHandle=pm.ikHandle(n='ropeLengthIkHandle',sol='ikSplineSolver',ccv=0,scv=0,pcv=0,sj=ropeLengthJoint[-1],ee=ropeLengthJoint[0],c=rope_srtend_curve)
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
    pm.select(boxctrl+'.cv[*]')
    pm.scale(0.7,0.7,0.7,r=True)    
    tenctrl=pm.curve(n=f'rope_in_{i}_C', d=1, p=[(-1,0,-1),(-1,0,-2),(1,0,-2),(1,0,-1),(2,0,-1),(2,0,1),(1,0,1),(1,0,2),(-1,0,2),(-1,0,1),(-2,0,1),(-2,0,-1),(-1,0,-1)])
    pm.select(tenctrl+'.cv[*]')
    pm.scale(0.4,0.4,0.4,r=True)
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
# create Joint 
# 조인트 만들기 21개
ropeBaseJoint=[]
numi=0    
for i in basePos21:
    newjoint = pm.createNode('joint',n=f'ropeBase00{numi}_jnt')
    newjoint.t.set(i)
    numi = numi+1
    ropeBaseJoint.append(newjoint)
# 조인트 리스트를 주면 순서대로 페어런츠 해주기 
ropeBaseJoint.reverse()
for i in range(0,len(ropeBaseJoint)-1):
    pm.parent(ropeBaseJoint[i],ropeBaseJoint[i+1])
# 스플라인 ik를 적용 
ropeBaseIkHandle=pm.ikHandle(n='ropeBaseIkHandle',sol='ikSplineSolver',ccv=0,scv=0,pcv=0,sj=ropeBaseJoint[-1],ee=ropeBaseJoint[0],c=rope_base_curve)
# 클러스터 & in_C 컨트롤러 연결
for i in range(0,11):
    clusterNode=f'ropebase00{i}_clusterHandle'
    inCtrlNodje=f'rope_in_{i}_C'
    pm.parentConstraint(inCtrlNodje,clusterNode,mo=1)
"""
여기서부터는  21개 컨트롤러 
"""    
# 21개 클러스터 생성 할  커브 생성 커브 위치는 이전 조인트 위치를 포인트로 바꿔서 만든다. 
rope_detail_curve=pm.curve( d=3, p=basePos21 ,n='rope_detail_curve')
# 클러스터 21개를 만들고 
rope_detail_curve_cluster=[]
for i in range(0,21):
    _cluster=pm.cluster(rope_detail_curve+f'.cv[{i}]',n=f'ropedetail00{i}_cluster')
    rope_detail_curve_cluster.append(_cluster)
# 디테일 컨트롤러 생성 동그라미 sphere
spherectrllist=[]    
for i in range(0,21):
    rope_detail_=cmds.curve(n=f'rope_detail_{i}_C', d=1, p=[(0, 0, 3),(2, 0, 2),(3, 0, 0),(2, 0, -2),(0, 0, -3),(-2, 0, -2),(-3, 0, 0),(-2, 0, 2),(0, 0, 3),(0, 0, 3),(0, 2, 2),(0, 3, 0),(0, 2, -2),(0, 0, -3),(0, -2, -2),(0, -3, 0),(0, -2, 2),(0, 0, 3),(0, 0, 3),(0, 2, 2),(0, 3, 0),(-2, 2, 0),(-3, 0, 0),(-2, -2, 0),(0, -3, 0),(2, -2, 0),(3, 0, 0),(2, 2, 0),(0, 3, 0)] )
    pm.select(rope_detail_+'.cv[*]')
    pm.scale(0.09,0.09,0.09,r=True)    
    spherectrllist.append(rope_detail_)
pm.select(cl=1)
rope_detail_CG = pm.createNode('transform',n='rope_detail_CG')    
for i in range(0,21):
    _G = pm.group(spherectrllist[i],n = spherectrllist[i]+'_G')
    _G.t.set(basePos21[i])
    pm.parent(_G,rope_detail_CG)
for i in range(0,21):
    pm.parentConstraint(f'rope_detail_{i}_C',f'ropedetail00{i}_clusterHandle',mo=1)
    pm.parentConstraint(f'ropeBase00{i}_jnt',f'rope_detail_{i}_C_G',mo=1)
    
# joint100
"""
조인트 101개 
"""
# 베이스 101개 조인트 생성
skinJointPos101=[]
for i in range(0,101):
    Length_Joint_pointOnCurveInfo.parameter.set(i*0.01)
    getPOS=Length_Joint_pointOnCurveInfo.position.get()
    skinJointPos101.append(getPOS)
# 조인트 만들기 101개
ropeSkinJoint=[]
numi=0    
for i in skinJointPos101:
    newjoint = pm.createNode('joint',n=f'ropeSkin00{numi}_jnt')
    newjoint.t.set(i)
    numi = numi+1
    ropeSkinJoint.append(newjoint)
# 조인트 리스트를 주면 순서대로 페어런츠 해주기 
ropeSkinJoint.reverse()
for i in range(0,len(ropeSkinJoint)-1):
    pm.parent(ropeSkinJoint[i],ropeSkinJoint[i+1])
# 스플라인 ik를 적용 
ropeSkinIkHandle=pm.ikHandle(n='ropeSkinIkHandle',sol='ikSplineSolver',ccv=0,scv=0,pcv=0,sj=ropeSkinJoint[-1],ee=ropeSkinJoint[0],c=rope_detail_curve)
# 해야할꺼
# 그룹정리 
# 컨트롤러 그룹정리
rig = pm.createNode('transform',n='rig')
prop_all_C_G = pm.createNode('transform',n='prop_all_C_G')
prop_move_C_G = pm.createNode('transform',n='prop_move_C_G')
prop_move1_C_G = pm.createNode('transform',n='prop_move1_C_G')
rope_aim_C_G = pm.createNode('transform',n='rope_aim_C_G')
prop_move1_C_G.t.set(startPOS)
prop_move_C_G.t.set(endPOS)
rope_aim_C_G.t.set(endPOS)
pm.parent(prop_all_C[0],prop_all_C_G)
pm.parent(prop_move_C[0],prop_move_C_G)
pm.parent(prop_move1_C[0],prop_move1_C_G)
pm.parent(rope_aim_C,rope_aim_C_G)
pm.parent(rope_aim_C_G,prop_move1_C[0])
pm.parent(prop_move1_C_G,prop_move_C[0])
pm.parent(prop_move_C_G,prop_all_C[0])
pm.parent(prop_all_C_G,rig)
pm.parent(rope_detail_CG,prop_all_C_G)
pm.parent(rope_CG,prop_all_C_G)
# 아이케이핸들 그룹정리
ikHandle_G = pm.createNode('transform',n='ikHandle_G')
pm.parent(ropeSkinIkHandle[0],ropeBaseIkHandle[0],ropeLengthIkHandle[0],ikHandle_G)
ikHandleCurve_G = pm.createNode('transform',n='ikHandleCurve_G')
# 아이케이커브 
pm.parent(rope_detail_curve,rope_base_curve,rope_srtend_curve,ikHandleCurve_G)
# 클러스터 그룹정리
cluster_G = pm.createNode('transform',n='cluster_G')
ropedetailcluster_G = pm.createNode('transform',n='ropedetailcluster_G')
ropeLengthcluster_G = pm.createNode('transform',n='ropeLengthcluster_G')
ropebasecluster_G = pm.createNode('transform',n='ropebasecluster_G')
pm.parent(rope_detail_curve_cluster,ropedetailcluster_G)
pm.parent(rope_base_curve_cluster,ropebasecluster_G)
pm.parent(ropeLengthJointCluster_Str,ropeLengthJointCluster_End,ropeLengthcluster_G)
pm.parent(ropeLengthcluster_G,ropebasecluster_G,ropedetailcluster_G,cluster_G)
# 조인트 그룹정리
joint_G = pm.createNode('transform',n='joint_G')
ropeLengthjoint_G = pm.createNode('transform',n='ropeLengthjoint_G')
ropeBasejoint_G = pm.createNode('transform',n='ropeBasejoint_G')
ropeSkinjoint_G = pm.createNode('transform',n='ropeSkinjoint_G')
pm.parent( ropeLengthjoint_G,ropeBasejoint_G,ropeSkinjoint_G,joint_G )
pm.parent( ropeLengthJoint[-1],ropeLengthjoint_G)
pm.parent( ropeBaseJoint[-1],ropeBasejoint_G)
pm.parent( ropeSkinJoint[-1],ropeSkinjoint_G)
rigSystem=pm.createNode('transform',n='rigSystem')
pm.parent(cluster_G,ikHandle_G,ikHandleCurve_G,scaleSet,rigSystem)
pm.parent(rigSystem,joint_G,rig)
# 컨트롤러 색상
def colorChange(ctrlNode,colorNumber):
    Node_=pm.PyNode(ctrlNode)
    Shape_=Node_.getChildren(type='shape')
    Shape_[0].overrideEnabled.set(1)
    Shape_[0].overrideColor.set(colorNumber)
# 파랑
colorChange(prop_all_C[0],6)
# 하늘
colorChange(prop_move_C[0],18)
colorChange(prop_move1_C[0],18)
for i in spherectrllist:
    colorChange(i,18)
# 적색
for i in boxctrllist:
    colorChange(i,12)
# 핑크
for i in tenctrllist:
    colorChange(i,20)
# 노랑
colorChange(rope_aim_C,17)
# 숨기고 보이고 정리
rigSystem.v.set(0)
ropeLengthjoint_G.v.set(0)
ropeBasejoint_G.v.set(0)
# 기능 추가 
 
# 트렌스 
rope_aim_C.addAttr('rope_tranFollow',type='float',min=0,max=1,dv=0,k=1)
ctrlVisibility=pm.createNode('reverse',n='ctrlVisibility')  
rope_aim_C.rope_tranFollow >>  ctrlVisibility.inputX

for i in range(1,11):
    pm.pointConstraint(f'ropeLength00{i}_jnt',f'rope_{i}_C_G',mo=1)
    pm.setKeyframe(f'rope_{i}_C_G', attribute='t', t=0 )
    rope_aim_C.rope_tranFollow >> pm.PyNode(f'rope_{i}_C_G').blendPoint1
    ctrlVisibility.outputX >> pm.PyNode(f'rope_{i}_CShape').v

# 로테이트  
rope_aim_C.addAttr('rope_rotFollow',type='float',min=0,max=1,dv=0,k=1)
pm.orientConstraint('rope_aim_C','rope_10_C_G',mo=1)
pm.setKeyframe('rope_10_C_G', attribute='r', t=0 )
rope_aim_C.rope_rotFollow >> pm.PyNode(f'rope_10_C_G').blendOrient1

# 스태치
rope_aim_C.addAttr('rope_length',type='float',min=1,max=10,dv=10,k=1)

# 조인트 21개 스테치 
# curveInfo 를 만들어서 길이 겟.  69
baseCurveBase=None
rope_base_curveShape = pm.PyNode(rope_base_curve).getChildren()[0]
Base_Joint_CurveInfo = pm.createNode('curveInfo',n='Base_Joint_CurveInfo')
rope_base_curveShape.worldSpace[0] >> Base_Joint_CurveInfo.inputCurve
baseCurveBase=Base_Joint_CurveInfo.arcLength.get()
#
Base_MDL = pm.createNode('multDoubleLinear',n='Base_MDL')
scaleSet.sx >> Base_MDL.input1
Base_MDL.input2.set(baseCurveBase)
Base_MDD = pm.createNode('multiplyDivide',n='Base_MDD')
Base_Joint_CurveInfo.arcLength >> Base_MDD.input1X
Base_MDL.output    >> Base_MDD.input2X
Base_MDD.operation.set(2)
# 스테치 적용 
for i in ropeBaseJoint:
    _MDL=pm.createNode('multDoubleLinear',n=i+'_MDL')
    jointTY=i.ty.get()
    _MDL.input2.set(jointTY)
    Base_MDD.outputX >> _MDL.input1
    _MDL.output >> i.ty
    
# 조인트 101개 스테치     
detailCurveBase=None
rope_detail_curveShape = pm.PyNode(rope_detail_curve).getChildren()[0]
detail_Joint_CurveInfo = pm.createNode('curveInfo',n='detail_Joint_CurveInfo')
rope_detail_curveShape.worldSpace[0] >> detail_Joint_CurveInfo.inputCurve
detailCurveBase=detail_Joint_CurveInfo.arcLength.get()
#
detail_MDL = pm.createNode('multDoubleLinear',n='detail_MDL')
scaleSet.sx >> detail_MDL.input1
detail_MDL.input2.set(detailCurveBase)
detail_MDD = pm.createNode('multiplyDivide',n='detail_MDD')
detail_Joint_CurveInfo.arcLength >> detail_MDD.input1X
detail_MDL.output    >> detail_MDD.input2X
detail_MDD.operation.set(2)

# 스킨 조인트 스테치 추가 부분  디테치 커브 대신 
skinA_MDL = pm.createNode('multDoubleLinear',n='skin_MDL')
rope_aim_C.rope_length >> skinA_MDL.input1
skinA_MDL.input2.set(0.1)
# 스테치 적용 
for i in ropeSkinJoint:
    _MDL=pm.createNode('multDoubleLinear',n=i+'_MDL')
    _A_MDL=pm.createNode('multDoubleLinear',n=i+'_A_MDL')    
    jointTY=i.ty.get()    
    detail_MDD.outputX >> _MDL.input1
    _MDL.input2.set(jointTY)    
    _MDL.output >> _A_MDL.input1
    skinA_MDL.output >> _A_MDL.input2
    _A_MDL.output >> i.ty
# 스케일 적용
pm.scaleConstraint(scaleSet,rope_detail_CG,mo=1)
pm.scaleConstraint(scaleSet,rope_CG,mo=1)
pm.scaleConstraint(scaleSet,ropeLengthjoint_G,mo=1)
pm.scaleConstraint(scaleSet,ropeBasejoint_G,mo=1)
pm.scaleConstraint(scaleSet,ropeSkinjoint_G,mo=1)
pm.select(rope_aim_C)
