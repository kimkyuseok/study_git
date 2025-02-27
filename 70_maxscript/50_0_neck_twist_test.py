import pymxs
rt = pymxs.runtime
# neck bon create 
BaseName = 'Bip001'
joint_neck_name = f"{BaseName} joint neck twist 0"
helperpoint_neck_name = f"{BaseName} pointhelper twist 0"
# get pos
neck = rt.execute(f"$'{BaseName} Neck'")
head = rt.execute(f"$'{BaseName} Head'")
neck_pos = neck.transform.pos
head_pos = head.transform.pos
#print(neck_pos,head_pos)

joint_neck_cre = rt.BoneSys.CreateBone(neck_pos, head_pos, head_pos)
joint_neck_cre.wirecolor = rt.yellow
joint_neck_cre.controller.rotation = neck.transform.rotation
joint_neck_cre.Name = joint_neck_name
joint_neck_cre.Parent = neck

# create point helper
helperpoint_neck_rec = rt.Point(size=3, box=True, cross=False, centerMarker=False, axisTripod=False, wirecolor=rt.green)
helperpoint_neck_rec.Name = helperpoint_neck_name
helperpoint_neck_rec.rotation = neck.transform.rotation
helperpoint_neck_rec.pos = neck.transform.pos
helperpoint_neck_rec.parent = neck

# lookat constraint  connect head weight 50   Bone_Neck << ----
loc_constraint = rt.LookAt_Constraint()
rt.refs.replaceReference(joint_neck_cre.controller, 2, loc_constraint)
loc_constraint.appendTarget(head, 50)
loc_constraint.viewline_length_abs=False
loc_constraint.upnode_world=False
loc_constraint.pickUpnode = helperpoint_neck_rec

#orient_constraint 
orient_constraint = rt.Orientation_Constraint()
rt.refs.replaceReference(helperpoint_neck_rec.controller, 2, orient_constraint)
orient_constraint.appendTarget(head, 50)
orient_constraint.appendTarget(neck, 50)
# error relative True ???
orient_constraint.relative = False

#print 
print("create neck create)
