import pymel.core as pm
mainCount=31

# 커브 를 알면 조인트를 거기에 배치할수 있어. 균일하게 
curve=pm.ls(sl=1,fl=1)[0]
# 커브를 알아내고
Curve_pointOnCurveInfo = pm.createNode('pointOnCurveInfo',n='Curve_pointOnCurveInfo')
Curve_curveShape = pm.PyNode(curve).getChildren()[0]
Curve_curveShape.worldSpace[0] >> Curve_pointOnCurveInfo.inputCurve
Curve_pointOnCurveInfo.turnOnPercentage.set(1)
# 퍼센티지로 길이로 알아내고
CurvePos11=[]
# 배치를하고
CurveInterval = 1.0 / (mainCount - 1)
forCount=0.0
for i in range(0,mainCount):
    Curve_pointOnCurveInfo.parameter.set(forCount)
    getPOS=Curve_pointOnCurveInfo.position.get()
    forCount=forCount+CurveInterval
    CurvePos11.append(getPOS)
# 포지션에 조인트 생성하고
CurveJoint=[]

numi=0    
for i in CurvePos11:
    newjoint = pm.createNode('joint',n=f'CurveJoint00{numi}_jnt')
    #newNull = pm.createNode('transform',n=f'CJP00{numi}_GRP')
    #pm.parent(newNull,newjoint)
    #newNull.rz.set(180)
    newjoint.t.set(i)
    numi = numi+1
    CurveJoint.append(newjoint)
CurveJoint.reverse()
for i in range(0,len(CurveJoint)-1):
    pm.parent(CurveJoint[i],CurveJoint[i+1])    
    
# 조인트 오리엔트
pm.select(CurveJoint[-1])
pm.mel.eval('joint -e  -oj yzx -secondaryAxisOrient xup -ch -zso;')
pm.select(CurveJoint[0])
pm.mel.eval('joint -e  -oj none -ch -zso;')
# 빈 그룹 추가 
CurveJointParent=[]
numi=0    
for i in CurvePos11:
    newNull = pm.createNode('transform',n=f'CJP00{numi}_GRP')
    pm.parent(newNull,f'CurveJoint00{numi}_jnt')
    newNull.t.set(0,0,0)
    newNull.r.set(0,0,180)
    numi = numi+1
    CurveJointParent.append(newNull)    
# 컨트롤러하고 페어런츠 하고  
for i in range(0,len(CurveJointParent)):     
    deleteA=pm.parentConstraint(f'CJP00{i}_GRP',f'rope_{i}_C',mo=0)
    pm.delete(deleteA)
# 끝
pm.delete(CurveJoint)
