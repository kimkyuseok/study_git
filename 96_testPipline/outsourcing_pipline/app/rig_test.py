import pymel.core as pm
# 알아야될꺼 스킨클러스터 ORG  메쉬
# 만들어야할꺼 deltamush
# 알고있는거 메쉬 이름
getMeshName = 'rat_body_mesh'
#getMeshName = 'rat_whiskers_mesh'
source_object = pm.PyNode(getMeshName)
source_skin_cluster = pm.ls(pm.listHistory(source_object), type='skinCluster')[0]
shapes = pm.ls(pm.listHistory(source_object), type='shape')
org_shape=None
out_shape=None
for i in shapes:
    if i.find('Orig')!=-1:
        org_shape=i
    else:
        out_shape=i
if org_shape and out_shape:
    print('ok')
    source_skin_cluster.ihi.set(0)
    dm=pm.createNode('deltaMush',n=source_skin_cluster+'_dm')
    dm.smoothingIterations.set(15)
    dm.smoothingStep.set(1)
    dm.ihi.set(0)
    pw = pm.createNode('proximityWrap',n=source_skin_cluster+'_pw')
    pw.ihi.set(0)
    pw.maxDrivers.set(5)
    pm.PyNode(source_skin_cluster+'.outputGeometry[0]') >> pm.PyNode(dm + '.input[0].inputGeometry')
    pm.PyNode(org_shape + '.outMesh') >> pm.PyNode(dm + '.originalGeometry[0]')
    pm.PyNode(dm + '.outputGeometry[0]') >> pm.PyNode(pw + '.input[0].inputGeometry')
    pm.PyNode(org_shape + '.outMesh') >> pm.PyNode(pw + '.originalGeometry[0]')
    pm.PyNode(pw + '.outputGeometry[0]') >> pm.PyNode(out_shape + '.inMesh')