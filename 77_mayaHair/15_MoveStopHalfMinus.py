import pymel.core as pm
# 움직임을 인풋할 컨트롤러 하고  최종 결과를 받을  루트 그룹   총 2개를 선택해서 실행 
selObj=pm.ls(sl=1,type='transform')
Moveshape =pm.createNode('locator',n='moveShape')
Move= Moveshape.getParent()
deleteA = pm.pointConstraint(selObj[0] , Move ,mo = 0)
pm.delete(deleteA)
#positionT=Move.translate.get()
#Move.translate.set(0,0,0)
#Moveshape.localPosition.set(positionT)
pm.makeIdentity(Move,a=1,t=1,r=1,s=1,n=0,pn=1)
Move1=pm.duplicate(Move,rr=1)
Move2=pm.duplicate(Move,rr=1)
Move3=pm.duplicate(Move,rr=1)
Stop = Move1[0].rename('stop')
Half = Move2[0].rename('half')
Minus = Move3[0].rename('minus')
#Half
HalfPointConstraint = pm.pointConstraint(Move,Stop,Half,mo=1)
HalfPointConstraint.moveW0.set(0.99)
HalfPointConstraint.stopW1.set(0.01)
#Minus 
hairSystemMinus=pm.createNode('multiplyDivide',n='hairSystemMinus')
hairSystemMinus.input2.set(-1,-1,-1)
Half.t >> hairSystemMinus.input1
hairSystemMinus.output >> Minus.t
#Move
deleteB = pm.pointConstraint(selObj[0] , Move ,mo = 0)
startFrame = pm.playbackOptions(q=True, minTime=True)
endFrame = pm.playbackOptions(q=True, maxTime=True)
pm.bakeResults(Move,simulation=1,t=[startFrame,endFrame],sampleBy=1,oversamplingRate=1,disableImplicitControl=1,preserveOutsideKeys=1,sparseAnimCurveBake=0,removeBakedAttributeFromLayer=0)
pm.delete(deleteB)
#Output
pm.pointConstraint(Minus,selObj[1],mo=1) 


