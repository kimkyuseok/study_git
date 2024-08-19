import pymel.core as pm
import maya.cmds as cmds
import math

ch_name = 'test'


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
    # pmab.output3D >> nodec.rotate
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


def create_cube_with_curves(width=1, height=1, depth=1):
    # Define the vertices of the cube
    vertices = [
        [width / 2, height / 2, depth / 2],
        [-width / 2, height / 2, depth / 2],
        [-width / 2, -height / 2, depth / 2],
        [width / 2, -height / 2, depth / 2],
        [width / 2, height / 2, depth / 2],

        [width / 2, height / 2, -depth / 2],
        [-width / 2, height / 2, -depth / 2],
        [-width / 2, -height / 2, -depth / 2],
        [width / 2, -height / 2, -depth / 2],
        [width / 2, height / 2, -depth / 2],

        [-width / 2, height / 2, -depth / 2],
        [-width / 2, height / 2, depth / 2],
        [-width / 2, -height / 2, depth / 2],
        [-width / 2, -height / 2, -depth / 2],
        [width / 2, -height / 2, -depth / 2],
        [width / 2, -height / 2, depth / 2]
    ]

    # Create the cube with curves
    curve_points = [tuple(vertex) for vertex in vertices]
    curve = pm.curve(p=curve_points, d=1)

    # Create vertical edges of the cube
    # for i in range(4):
    #     pm.curve(p=[vertices[i], vertices[i+5]], d=1)

    return curve


def create_pyramid_with_curves(base_width=1, height=0.5, dn=-0.5):
    # Define the base vertices of the pyramid
    half_width = base_width / 2
    base_vertices = [
        [half_width, dn, half_width],
        [-half_width, dn, half_width],
        [-half_width, dn, -half_width],
        [half_width, dn, -half_width],
        [half_width, dn, half_width],  # Close the base
        [0, height, 0],
        [-half_width, dn, half_width],
        [-half_width, dn, -half_width],
        [0, height, 0],
        [half_width, dn, -half_width]
    ]

    # Define the apex vertex of the pyramid
    # apex = [0, height, 0]

    # Create the base curve
    base_curve = pm.curve(p=base_vertices, d=1)

    # Create the edges from the base to the apex
    # for base_vertex in base_vertices[:-1]:  # Exclude the last vertex to avoid duplicating the first vertex
    #   edge_curve = pm.curve(p=[base_vertex, apex], d=1)

    return base_curve


def create_sphere_curve(radius=1.0, segments=8):
    points = []
    num_circles = 1

    # Create circles along the X, Y, and Z axes
    for axis in ['X', 'Y', 'Z']:
        for i in range(num_circles):
            angle = (i / float(num_circles)) * 180.0
            for j in range(segments):
                theta = 2 * math.pi * j / segments
                if axis == 'X':
                    x = 0
                    y = radius * math.cos(theta)
                    z = radius * math.sin(theta)
                    y, z = (y * math.cos(math.radians(angle)) - z * math.sin(math.radians(angle)),
                            y * math.sin(math.radians(angle)) + z * math.cos(math.radians(angle)))
                elif axis == 'Y':
                    x = radius * math.cos(theta)
                    y = 0
                    z = radius * math.sin(theta)
                    x, z = (x * math.cos(math.radians(angle)) + z * math.sin(math.radians(angle)),
                            -x * math.sin(math.radians(angle)) + z * math.cos(math.radians(angle)))
                elif axis == 'Z':
                    x = radius * math.cos(theta)
                    y = radius * math.sin(theta)
                    z = 0
                    x, y = (x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle)),
                            x * math.sin(math.radians(angle)) + y * math.cos(math.radians(angle)))
                points.append([x, y, z])
            points.append(points[-segments])  # Close the circle by adding the first point again
    insertpoint = points[19]
    if len(points) > 9:
        points.insert(9, insertpoint)

        # Delete existing sphere curve if it exists
    if pm.objExists("sphere_curve"):
        pm.delete("sphere_curve")

    # Create the curve with all points
    sphere_curve = pm.curve(p=points, degree=1, name="sphere_curve")
    pm.select(sphere_curve)
    return sphere_curve


def create_cone_curve(base_radius=1.0, height=1.0, segments=3):
    # Ensure segments is at least 3 for a triangle
    if segments < 3:
        segments = 3

    # Initialize list to hold all points for the single curve
    points = []

    # Create the base triangle points
    base_points = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = base_radius * math.cos(angle)
        y = 0
        z = base_radius * math.sin(angle)
        base_points.append([x, y, z])

    base_points.append(base_points[0])  # Close the base triangle

    # Create the apex of the cone
    apex = [0, height, 0]
    addx = base_points[1][0] * -1

    for i in range(len(base_points)):
        if i not in [0, 3]:
            base_points[i][0] = base_points[i][0] + addx

    # Add the base triangle points to the list
    points.extend(base_points)

    # Add the sides of the cone
    for i in range(segments):
        points.extend([base_points[i], apex])

    # Close the loop by connecting the last point to the first point
    points.append(base_points[0])

    # Delete existing cone curve if it exists
    if pm.objExists("cone_curve"):
        pm.delete("cone_curve")

    # Create the single curve with all points
    cone_curve = pm.curve(p=points, degree=1, name="cone_curve")
    pm.select(cone_curve)
    return cone_curve


def rotate_shape_in_direction(transform_node, rotation_vector):
    """
    Rotates the shape under the given transform node around the specified direction vector.

    :param transform_node: The name of the transform node.
    :param rotation_vector: A list or tuple containing the rotation vector [rx, ry, rz] in degrees.
    """
    # Get the shape node under the transform node
    shape_node = pm.listRelatives(transform_node, shapes=True)[0]

    # Get the vertices of the shape node
    vertices = pm.ls(f"{shape_node}.cv[*]", flatten=True)
    pm.rotate(vertices, rotation_vector, relative=True)
    # rotate -r -p 0cm 0.2cm 0cm -ws -fo 6.166124 5.430031 -89.412247


def move_shape_in_direction(transform_node, direction_vector):
    """
    Moves the shape under the given transform node in the specified direction vector.

    :param transform_node: The name of the transform node.
    :param direction_vector: A list or tuple containing the direction vector [dx, dy, dz].
    """
    # Get the shape node under the transform node
    shape_node = pm.listRelatives(transform_node, shapes=True)[0]

    # Get all the vertices of the shape node
    vertices = pm.ls(f"{shape_node}.cv[*]", flatten=True)
    # print(vertices)
    # Move each vertex by the direction vector
    for vertex in vertices:
        # print(vertex)
        current_position = pm.pointPosition(vertex)
        new_position = [
            current_position[0] + direction_vector[0],
            current_position[1] + direction_vector[1],
            current_position[2] + direction_vector[2]
        ]
        pm.xform(vertex, translation=new_position, worldSpace=True)


def create_rectangle_curve(center=(0, 0, 0), width=1.0, height=1.0):
    """
    Creates a rectangle curve at the specified center with the given width and height.

    :param center: A tuple (x, y, z) specifying the center of the rectangle.
    :param width: The width of the rectangle.
    :param height: The height of the rectangle.
    """
    half_width = width / 2.0
    half_height = height / 2.0

    # Define the vertices of the rectangle
    points = [
        (center[0] - half_width, center[1], center[2] - half_height),
        (center[0] - half_width, center[1], center[2] + half_height),
        (center[0] + half_width, center[1], center[2] + half_height),
        (center[0] + half_width, center[1], center[2] - half_height),
        (center[0] - half_width, center[1], center[2] - half_height)
    ]

    # Create the curve
    curve = pm.curve(p=points, degree=1)

    return curve


def create_ellipse_curve(center=(0, 0, 0), radius_x=1.0, radius_y=1.0, num_points=36):
    """
    Creates an ellipse curve at the specified center with the given radii.

    :param center: A tuple (x, y, z) specifying the center of the ellipse.
    :param radius_x: The radius along the x-axis.
    :param radius_y: The radius along the y-axis.
    :param num_points: The number of points to define the ellipse (default is 36).
    """
    points = []

    # Calculate the points on the ellipse
    for i in range(num_points):
        angle = (2 * math.pi * i) / num_points
        x = center[0] + radius_x * math.cos(angle)
        y = center[1]
        z = center[2] + radius_y * math.sin(angle)
        points.append((x, y, z))

    points.append(points[0])
    # Create the curve
    curve = pm.curve(p=points, degree=3)

    return curve


def set_controller_color(controller, color_index):
    """
    Sets the color of the given controller.

    :param controller: The name of the controller transform node.
    :param color_index: The color index to set. (0-31 for standard colors in Maya)
    """
    # Get the shape nodes under the transform node
    shapes = pm.listRelatives(controller, shapes=True)

    if not shapes:
        pm.warning(f"No shape nodes found under {controller}.")
        return

    for shape in shapes:
        # Enable override color
        pm.setAttr(f"{shape}.overrideEnabled", 1)

        # Set the override color
        pm.setAttr(f"{shape}.overrideColor", color_index)


def parent_curve_shape_to_transform(curve, transform_node):
    """
    Parents the shape of the given curve to the specified transform node and deletes the original curve.

    :param curve: The name of the curve transform node.
    :param transform_node: The name of the target transform node.
    """
    # Get the shape nodes of the curve
    curve_shapes = pm.listRelatives(curve, shapes=True, fullPath=True)

    if not curve_shapes:
        pm.warning(f"No shape nodes found in {curve}.")
        return

    for curve_shape in curve_shapes:
        # Parent the curve shape to the transform node
        pm.parent(curve_shape, transform_node, relative=True, shape=True)

    # Delete the original curve transform node
    pm.delete(curve)


def set_shape_template(nodea):
    shapes = pm.listRelatives(nodea, shapes=True)
    for shape in shapes:
        # Enable override color
        pm.setAttr(f"{shape}.overrideEnabled", 1)
        pm.setAttr(f"{shape}.overrideDisplayType", 1)


"""
# Example usage
create_ellipse_curve(center=(0, 0, 0), radius_x=3.0, radius_y=5.0)
# Example usage
create_rectangle_curve(center=(0, 0, 0), width=3.0, height=5.0)
# Example usage
move_shape_in_direction('curve1', [0,0.5,0])
# Example usage
create_cone_curve(base_radius=0.8, height=0.7, segments=3)
# Example usage
create_sphere_curve(radius=0.5, segments=8)
# Run the function to create a pyramid with the default base width (1) and height (1)
create_pyramid_with_curves(1,0.7,-0.3)
# Run the function to create a cube with the default dimensions (1x1x1)
create_cube_with_curves(0.3,1.0,0.3)
create_cube_with_curves()
qrrv('pCube4.test','pCube4.retest')    
qrpct('pCube1','pCube2','pCube3','pCube3.test','pCube3.retest')    
-2*-1
"""


def main():
    # main ( rack )
    qr_main = pm.createNode('transform', n='qr_main')
    # root ( box - sphere )
    qr_root = pm.createNode('transform', n='qr_root')
    # cog ( cicle )
    qr_cog = pm.createNode('transform', n='qr_cog')
    # shape
    m1 = create_rectangle_curve(center=(0, 0, 0), width=12.0, height=17.0)
    m2 = create_rectangle_curve(center=(0, 0, 0), width=17.0, height=12.0)
    m3 = create_rectangle_curve(center=(0, 0, 0), width=11.0, height=11.0)
    c1 = create_ellipse_curve(center=(0, 0, 0), radius_x=3.5, radius_y=5.5)
    c2 = create_ellipse_curve(center=(0, 0, 0), radius_x=5.5, radius_y=3.5)
    c3 = create_ellipse_curve(center=(0, 0, 0), radius_x=3.3, radius_y=3.3)
    r1 = create_sphere_curve()
    r2 = create_cube_with_curves(2, 2, 2)
    set_controller_color(m1, 6)
    set_controller_color(m2, 6)
    set_controller_color(m3, 6)
    set_controller_color(c1, 20)
    set_controller_color(c2, 20)
    set_controller_color(c3, 20)
    set_controller_color(r1, 22)
    set_controller_color(r2, 22)
    pm.rename(m1, 'qr_main_s01')
    pm.rename(m2, 'qr_main_s02')
    pm.rename(m3, 'qr_main_s03')
    pm.rename(c1, 'qr_cog_s01')
    pm.rename(c2, 'qr_cog_s02')
    pm.rename(c3, 'qr_cog_s03')
    pm.rename(r1, 'qr_root_s01')
    pm.rename(r2, 'qr_root_s02')
    for i in ['qr_main_s01', 'qr_main_s02', 'qr_main_s03',
              'qr_cog_s01', 'qr_cog_s02', 'qr_cog_s03',
              'qr_root_s01', 'qr_root_s02']:
        parent_curve_shape_to_transform(i, i.rsplit('_', 1)[0])
    pm.parent(qr_cog, qr_root)
    pm.parent(qr_root, qr_main)
    set_shape_template(qr_cog)
    pm.select(qr_root)
    return qr_main


def create_aimlocator(nodea, nodeb, nodec):
    # ctrla
    nodea = pm.PyNode(nodea)
    # ctrlb
    nodeb = pm.PyNode(nodeb)
    # out parent
    nodec = pm.PyNode(nodec)
    # 커브 _Connector_crv
    crv = pm.curve(p=[[0, 0, 0], [1, 1, 1]], degree=1, name=f"{nodea}_{nodeb}_Connector_crv")
    shapes = pm.listRelatives(crv, shapes=True)
    a_loc = pm.createNode('locator', n=f"{nodea}_{nodeb}_aim_locShape")
    # 로케이터 에임 _aim_loc
    t_loc = pm.createNode('locator', n=f"{nodea}_{nodeb}_taget_locShape")
    # 로케이터 타겟 -taget_loc
    pointA = pm.PyNode(shapes[0] + '.controlPoints[0]')
    pointB = pm.PyNode(shapes[0] + '.controlPoints[1]')
    # create multMatrixa
    mtma = pm.createNode('multMatrix', n=nodea + '_a_MTM')
    mtmb = pm.createNode('multMatrix', n=nodeb + '_b_MTM')
    # create decomposeMatrix
    dcma = pm.createNode('decomposeMatrix', n=nodea + '_a_DCM')
    dcmb = pm.createNode('decomposeMatrix', n=nodeb + '_b_DCM')
    # connect
    a_loc.getParent().worldMatrix[0] >> mtma.matrixIn[0]
    crv.worldInverseMatrix >> mtma.matrixIn[1]
    t_loc.getParent().worldMatrix[0] >> mtmb.matrixIn[0]
    crv.worldInverseMatrix >> mtmb.matrixIn[1]
    # connect decomposematrix
    mtma.matrixSum >> dcma.inputMatrix
    mtmb.matrixSum >> dcmb.inputMatrix
    # connect multiply translate
    dcma.outputTranslate >> pointA
    dcmb.outputTranslate >> pointB
    # parent
    pm.parent(pm.PyNode(t_loc).getParent(), pm.PyNode(a_loc).getParent())
    pm.parent(pm.PyNode(a_loc).getParent(), nodec)
    pm.parent(crv, nodec)
    # parentConstraint
    a_loc_mtm = pm.createNode('multMatrix', n=a_loc + 'MTM')
    a_loc_dcm = pm.createNode('decomposeMatrix', n=a_loc + '_DCM')
    nodea.worldMatrix[0] >> a_loc_mtm.matrixIn[0]
    a_loc.getParent().parentInverseMatrix >> a_loc_mtm.matrixIn[1]
    a_loc_mtm.matrixSum >> a_loc_dcm.inputMatrix
    a_loc_dcm.outputTranslate >> a_loc.getParent().t
    # a_loc_dcm.outputRotate >> a_loc.getParent().r
    # pointConstraint
    t_loc_mtm = pm.createNode('multMatrix', n=t_loc + 'MTM')
    t_loc_dcm = pm.createNode('decomposeMatrix', n=t_loc + '_DCM')
    nodeb.worldMatrix[0] >> t_loc_mtm.matrixIn[0]
    t_loc.getParent().parentInverseMatrix >> t_loc_mtm.matrixIn[1]
    t_loc_mtm.matrixSum >> t_loc_dcm.inputMatrix
    t_loc_dcm.outputTranslate >> t_loc.getParent().t
    # decomposematrix 2
    nodea_dcm = pm.createNode('decomposeMatrix', n=nodea + '_a_DCM')
    nodeb_dcm = pm.createNode('decomposeMatrix', n=nodeb + '_b_DCM')
    # plusminusaverage 1
    a_loc_minus_pma = pm.createNode('plusMinusAverage', n=a_loc + '_minus_PMA')
    # vectorProduct 4
    a_locX_vpt = pm.createNode('vectorProduct', n=a_loc + '_X_VPT')
    a_locY_vpt = pm.createNode('vectorProduct', n=a_loc + '_Y_VPT')
    a_locZ_vpt = pm.createNode('vectorProduct', n=a_loc + '_Z_VPT')
    a_locA_vpt = pm.createNode('vectorProduct', n=a_loc + '_A_VPT')
    # fourByFourMatrix
    a_loc_FBF = pm.createNode('fourByFourMatrix', n=a_loc + '_FBF')
    # decomposematirx 1
    a_loc_r_dcm = pm.createNode('decomposeMatrix', n=a_loc + '_R_DCM')
    # distanceBetween 1
    a_loc_dtb = pm.createNode('distanceBetween', n=a_loc + '_DTB')
    a_loc_cdt = pm.createNode('condition', n=a_loc + '_CDT')
    #
    nodea.worldMatrix[0] >> nodea_dcm.inputMatrix
    nodeb.worldMatrix[0] >> nodeb_dcm.inputMatrix
    nodea_dcm.outputTranslate >> a_loc_minus_pma.input3D[0]
    nodeb_dcm.outputTranslate >> a_loc_minus_pma.input3D[1]
    a_loc_minus_pma.operation.set(2)
    #
    nodea_dcm.outputTranslate >> a_loc_dtb.point1
    nodeb_dcm.outputTranslate >> a_loc_dtb.point2
    a_loc_dtb.distance >> a_loc_cdt.firstTerm
    a_loc_minus_pma.output3D >> a_loc_cdt.colorIfFalse
    a_loc_cdt.colorIfTrueG.set(1)
    for i in [a_locX_vpt, a_locY_vpt, a_locZ_vpt, a_locA_vpt]:
        i.normalizeOutput.set(1)
    a_loc_cdt.outColor >> a_locY_vpt.input1
    a_locA_vpt.input1Z.set(1)
    a_locA_vpt.operation.set(0)
    a_locY_vpt.operation.set(0)
    a_locY_vpt.output >> a_locX_vpt.input1
    a_locA_vpt.output >> a_locX_vpt.input2
    a_locX_vpt.operation.set(2)
    a_locX_vpt.output >> a_locZ_vpt.input1
    a_locY_vpt.output >> a_locZ_vpt.input2
    a_locZ_vpt.operation.set(2)
    a_locX_vpt.outputX >> a_loc_FBF.in00
    a_locX_vpt.outputY >> a_loc_FBF.in01
    a_locX_vpt.outputZ >> a_loc_FBF.in02
    a_locY_vpt.outputX >> a_loc_FBF.in10
    a_locY_vpt.outputY >> a_loc_FBF.in11
    a_locY_vpt.outputZ >> a_loc_FBF.in12
    a_locZ_vpt.outputX >> a_loc_FBF.in20
    a_locZ_vpt.outputY >> a_loc_FBF.in21
    a_locZ_vpt.outputZ >> a_loc_FBF.in22
    a_loc_FBF.output >> a_loc_r_dcm.inputMatrix
    a_loc_r_dcm.outputRotate >> a_loc.getParent().r
    a_loc.getParent().v.set(0)
    crv.template.set(1)


def spineOption(s_name, i_joint, b_axis, b_mirror, s_parent, s_parentsub):
    # 부모 데이터 필요하네
    s_parent = pm.PyNode(s_parent)
    s_parentsub = pm.PyNode(s_parentsub)
    #
    outGrp = pm.createNode('transform', n='qr_' + s_name)
    # 박스 쉐입
    parentGrp = pm.createNode('transform', n='qr_' + s_name + '_Parent')
    # 피라미드 쉐입
    TopMove = pm.createNode('transform', n='qr_' + s_name + '_TopGrp')
    TopGrp = pm.createNode('transform', n='qr_' + s_name + '_Top')
    parent01 = create_cube_with_curves(0.2, 0.7, 0.2)
    parent02 = create_cube_with_curves(0.6, 0.6, 0.6)
    move_shape_in_direction(parent01, [0, 0.5, 0])
    top01 = create_pyramid_with_curves(1, 0.7, -0.3)
    top02 = create_sphere_curve(radius=0.3, segments=8)
    pm.rename(parent01, parentGrp + '_s01')
    pm.rename(parent02, parentGrp + '_s02')
    pm.rename(top01, TopGrp + '_s01')
    pm.rename(top02, TopGrp + '_s02')
    for i in [parent01, parent02, top01, top02]:
        set_controller_color(i, 29)
        parent_curve_shape_to_transform(i, i.rsplit('_', 1)[0])
    pm.parent(parentGrp, outGrp)
    pm.parent(TopMove, parentGrp)
    pm.parent(TopGrp, TopMove)
    intCount = 0
    NumGrpList = []
    ctrlList = [s_parent, parentGrp]
    for i in range(0, i_joint):
        NumGrp = pm.createNode('transform', n=f'qr_{s_name}_{i:02}Grp')
        pm.parent(NumGrp, parentGrp)
        NumGrpList.append(NumGrp)
        NumGrp.addAttr('nodea', at='float', k=1)
        NumGrp.addAttr('nodeb', at='float', k=1)
        NumShape = pm.createNode('transform', n=f'qr_{s_name}_{i:02}')
        ctrlList.append(NumShape)
        pm.parent(NumShape, NumGrp)
        # 커브 생성
        s01 = create_cone_curve(base_radius=0.4, height=0.4, segments=3)
        s02 = create_sphere_curve(radius=0.25, segments=8)
        pm.rename(s01, NumShape + '_s01')
        pm.rename(s02, NumShape + '_s02')
        for i in [s01, s02]:
            set_controller_color(i, 29)
            parent_curve_shape_to_transform(i, i.rsplit('_', 1)[0])
    ctrlList.append(TopGrp)
    n = i_joint
    NumGrpWeightRev = [(i + 1) / (n + 1) for i in range(i_joint)]
    NumGrpWeight = NumGrpWeightRev[::-1]
    print(NumGrpWeight)
    print(NumGrpWeightRev)

    # print(parentGrp,TopGrp,NumGrpList)
    for i in range(i_joint):
        print(i, parentGrp, TopGrp, NumGrpList[i], NumGrpWeight[i], NumGrpWeightRev[i])
        qrpct(parentGrp, TopGrp, NumGrpList[i], NumGrpList[i] + '.nodea', NumGrpList[i] + '.nodeb')
        pm.PyNode(NumGrpList[i] + '.nodea').set(NumGrpWeight[i])
        pm.PyNode(NumGrpList[i] + '.nodeb').set(NumGrpWeightRev[i])
        # NumGrpList 를 불러와서 웨이트 를 각각 넣어주면 끝.
    TopMove.ty.set(8)
    # connectorGrp
    connectorGrp = pm.createNode('transform', n=f'qr_{s_name}_connectorGrp')
    pm.parent(connectorGrp, parentGrp)
    pm.parent(outGrp, s_parent)
    outGrp.addAttr('nodea', at='float', k=1)
    outGrp.addAttr('nodeb', at='float', k=1)
    outGrp.nodea.set(1)
    qrpct(s_parent, s_parentsub, outGrp, outGrp + '.nodea', outGrp + '.nodeb')
    # locator
    for i in range(len(ctrlList) - 1):
        create_aimlocator(ctrlList[i], ctrlList[i + 1], connectorGrp)
    return outGrp


def armOption(s_name, i_upperjoint, i_lowerjoint, b_oneelbow, b_mirror, b_leftright, s_parent, s_parentsub):
    # 부모 데이터 필요하네
    s_parent = pm.PyNode(s_parent)
    s_parentsub = pm.PyNode(s_parentsub)
    # 왼쪽 오른쪽 두번 만들껀지
    s_leftright = 'l_'
    f_leftright = 0.7
    a_leftright = -90
    i_leftright = 1
    # 옵션 미러 이면 일단 왼쪽 만듬
    if b_mirror == True:
        s_leftright = 'l_'
        f_leftright = 0.7
        a_leftright = -90
        i_leftright = 1
    else:
        s_leftright = 'r_'
        f_leftright = -0.7
        a_leftright = 90
        i_leftright = -1
    # 왼쪽 진행하자
    if s_leftright == 'l_':
        outGrp = pm.createNode('transform', n='qr_' + s_leftright + s_name)
        # 박스 쉐입
        parentGrp = pm.createNode('transform', n='qr_' + s_leftright + s_name + '_Parent')
        # 피라미드 쉐입
        TopMove = pm.createNode('transform', n='qr_' + s_leftright + s_name + '_wristGrp')
        TopGrp = pm.createNode('transform', n='qr_' + s_leftright + s_name + '_wrist')
        parent01 = create_cube_with_curves(f_leftright, 0.2, 0.2)
        parent02 = create_cube_with_curves(0.6, 0.6, 0.6)
        move_shape_in_direction(parent01, [f_leftright * 0.5, 0.0, 0])
        top01 = create_pyramid_with_curves(1, 0.7, -0.3)
        top02 = create_sphere_curve(radius=0.3, segments=8)
        pm.rename(parent01, parentGrp + '_s01')
        pm.rename(parent02, parentGrp + '_s02')
        pm.rename(top01, TopGrp + '_s01')
        pm.rename(top02, TopGrp + '_s02')
        for i in [parent01, parent02, top01, top02]:
            set_controller_color(i, 26)
            parent_curve_shape_to_transform(i, i.rsplit('_', 1)[0])
        pm.select(TopGrp)
        rotate_shape_in_direction(TopGrp, [0, 0, a_leftright])
        pm.parent(parentGrp, outGrp)
        pm.parent(TopMove, parentGrp)
        pm.parent(TopGrp, TopMove)
        TopMove.tx.set(8)
        s_ctrl = ['_clavicle', '_shoulder', '_elbow', '_wrist']
        i_ctrl = [1, 3, 5.5]
        for i in range(0, 3):
            grp = pm.createNode('transform', n='qr_' + s_leftright + s_name + s_ctrl[i] + 'Grp')
            ctl = pm.createNode('transform', n='qr_' + s_leftright + s_name + s_ctrl[i])
            crv = create_sphere_curve(radius=0.3, segments=8)
            set_controller_color(crv, 26)
            # print(crv)
            pm.rename(crv, ctl + '_s01')
            parent_curve_shape_to_transform(crv, crv.rsplit('_', 1)[0])
            pm.parent(ctl, grp)
            grp.tx.set(i_ctrl[i] * i_leftright)
        nodeA = pm.PyNode('qr_' + s_leftright + s_name + s_ctrl[1])
        nodeB = pm.PyNode('qr_' + s_leftright + s_name + s_ctrl[3])
        nodeC = pm.PyNode('qr_' + s_leftright + s_name + s_ctrl[2] + 'Grp')
        nodeC.addAttr('nodea', at='float', k=1)
        nodeC.addAttr('nodeb', at='float', k=1)
        nodeC.nodea.set(0.5)
        nodeC.nodeb.set(0.5)
        qrpct(nodeA, nodeB, nodeC, nodeC + '.nodea', nodeC + '.nodeb')
        # Aimloc
        aim_r_grp = pm.createNode('transform', n='qr_' + s_leftright + s_name + s_ctrl[1] + '_aim_r_Grp')
        aim_r_elbow_grp = pm.createNode('transform', n='qr_' + s_leftright + s_name + s_ctrl[1] + '_aim_r_elbow_Grp')
        pm.parent(aim_r_elbow_grp, aim_r_grp)
        s_str = 'qr_' + s_leftright + s_name + '_aim_r_'
        # decomposematrix 2
        aim_ra_dcm = pm.createNode('decomposeMatrix', n=nodeA + '_a_DCM')
        aim_rb_dcm = pm.createNode('decomposeMatrix', n=nodeB + '_b_DCM')
        # plusminusaverage 1
        aim_ra_loc_minus_pma = pm.createNode('plusMinusAverage', n=s_str + '_minus_PMA')
        # vectorProduct 4
        aim_ra_locX_vpt = pm.createNode('vectorProduct', n=s_str + '_X_VPT')
        aim_ra_locY_vpt = pm.createNode('vectorProduct', n=s_str + '_Y_VPT')
        aim_ra_locZ_vpt = pm.createNode('vectorProduct', n=s_str + '_Z_VPT')
        aim_ra_locA_vpt = pm.createNode('vectorProduct', n=s_str + '_A_VPT')
        # fourByFourMatrix
        aim_ra_loc_FBF = pm.createNode('fourByFourMatrix', n=s_str + '_FBF')
        # decomposematirx 1
        aim_ra_loc_r_dcm = pm.createNode('decomposeMatrix', n=s_str + '_R_DCM')
        # distanceBetween 1
        aim_ra_loc_dtb = pm.createNode('distanceBetween', n=s_str + '_DTB')
        aim_ra_loc_cdt = pm.createNode('condition', n=s_str + '_CDT')
        #
        nodeB.worldMatrix[0] >> aim_ra_dcm.inputMatrix
        nodeA.worldMatrix[0] >> aim_rb_dcm.inputMatrix
        aim_ra_dcm.outputTranslate >> aim_ra_loc_minus_pma.input3D[0]
        aim_rb_dcm.outputTranslate >> aim_ra_loc_minus_pma.input3D[1]
        aim_ra_loc_minus_pma.operation.set(2)
        #
        aim_ra_dcm.outputTranslate >> aim_ra_loc_dtb.point1
        aim_rb_dcm.outputTranslate >> aim_ra_loc_dtb.point2
        aim_ra_loc_dtb.distance >> aim_ra_loc_cdt.firstTerm
        aim_ra_loc_minus_pma.output3D >> aim_ra_loc_cdt.colorIfFalse
        aim_ra_loc_cdt.colorIfTrueR.set(1)
        for i in [aim_ra_locX_vpt, aim_ra_locY_vpt, aim_ra_locZ_vpt, aim_ra_locA_vpt]:
            i.normalizeOutput.set(1)
        aim_ra_loc_cdt.outColor >> aim_ra_locX_vpt.input1
        aim_ra_locA_vpt.input1Z.set(1)
        aim_ra_locA_vpt.operation.set(0)
        aim_ra_locX_vpt.operation.set(0)
        aim_ra_locA_vpt.output >> aim_ra_locY_vpt.input1
        aim_ra_locX_vpt.output >> aim_ra_locY_vpt.input2
        aim_ra_locY_vpt.operation.set(2)
        aim_ra_locX_vpt.output >> aim_ra_locZ_vpt.input1
        aim_ra_locY_vpt.output >> aim_ra_locZ_vpt.input2
        aim_ra_locZ_vpt.operation.set(2)
        aim_ra_locX_vpt.outputX >> aim_ra_loc_FBF.in00
        aim_ra_locX_vpt.outputY >> aim_ra_loc_FBF.in01
        aim_ra_locX_vpt.outputZ >> aim_ra_loc_FBF.in02
        aim_ra_locY_vpt.outputX >> aim_ra_loc_FBF.in10
        aim_ra_locY_vpt.outputY >> aim_ra_loc_FBF.in11
        aim_ra_locY_vpt.outputZ >> aim_ra_loc_FBF.in12
        aim_ra_locZ_vpt.outputX >> aim_ra_loc_FBF.in20
        aim_ra_locZ_vpt.outputY >> aim_ra_loc_FBF.in21
        aim_ra_locZ_vpt.outputZ >> aim_ra_loc_FBF.in22
        aim_ra_loc_FBF.output >> aim_ra_loc_r_dcm.inputMatrix
        aim_ra_loc_r_dcm.outputRotate >> pm.PyNode(aim_r_grp).r
        pm.PyNode(aim_r_grp).v.set(0)
        pm.parent(aim_r_grp, nodeA)
        aim_r_grp.t.set(0, 0, 0)
        # pole vector
        # 디컴포즈
        aim_elbow_dcm = pm.createNode('decomposeMatrix', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_DCM')
        # plusminusaverage 1
        aim_elbow_minus_pma = pm.createNode('plusMinusAverage',
                                            n='qr_' + s_leftright + s_name + s_ctrl[2] + '_minus_PMA')
        # 벡터프로덕션 노말라이즈
        aim_nomal_VPT = pm.createNode('vectorProduct', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_nomal_VPT')
        # 벡터프로덕션 닷
        aim_dot_VPT = pm.createNode('vectorProduct', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_dot_VPT')
        elbow_node = pm.PyNode('qr_' + s_leftright + s_name + s_ctrl[2])
        elbow_node.worldMatrix[0] >> aim_elbow_dcm.inputMatrix
        #
        aim_ra_loc_minus_pma.output3D >> aim_nomal_VPT.input1
        aim_nomal_VPT.operation.set(0)
        aim_nomal_VPT.normalizeOutput.set(1)
        #
        aim_elbow_dcm.outputTranslate >> aim_elbow_minus_pma.input3D[0]
        aim_rb_dcm.outputTranslate >> aim_elbow_minus_pma.input3D[1]
        aim_elbow_minus_pma.operation.set(2)
        #
        aim_elbow_minus_pma.output3D >> aim_dot_VPT.input1
        aim_nomal_VPT.output >> aim_dot_VPT.input2
        aim_dot_VPT.operation.set(1)
        # tx
        aim_dot_VPT.outputX >> aim_r_elbow_grp.tx
        # 로테이션
        # 디컴포즈
        aim_elbow_rotate_dcm = pm.createNode('decomposeMatrix',
                                             n='qr_' + s_leftright + s_name + s_ctrl[2] + '_rotate_DCM')
        aim_r_elbow_grp.worldMatrix[0] >> aim_elbow_rotate_dcm.inputMatrix
        # plusminusaverage 1
        aim_elbow_rotate_minus_PMA = pm.createNode('plusMinusAverage',
                                                   n='qr_' + s_leftright + s_name + s_ctrl[2] + '_rotate_minus_PMA')
        #
        aim_elbow_rotate_dcm.outputTranslate >> aim_elbow_rotate_minus_PMA.input3D[0]
        aim_elbow_dcm.outputTranslate >> aim_elbow_rotate_minus_PMA.input3D[1]
        aim_elbow_rotate_minus_PMA.operation.set(2)  # z
        # 벡터프로덕션 크로스
        _cross_VPT = pm.createNode('vectorProduct', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_cross_VPT')
        # fourByFourMatrix
        _rotate_FBF = pm.createNode('fourByFourMatrix', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_rotate_FBF')
        # decomposematirx 1
        _rotate_DCM = pm.createNode('decomposeMatrix', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_rotate_DCM')
        # distanceBetween 1
        _d_DTB = pm.createNode('distanceBetween', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_d_DTB')
        _c_CDT = pm.createNode('condition', n='qr_' + s_leftright + s_name + s_ctrl[2] + '_c_CDT')
        # dis
        # condition
        #
        aim_elbow_rotate_dcm.outputTranslate >> _d_DTB.point1
        aim_elbow_dcm.outputTranslate >> _d_DTB.point2
        _d_DTB.distance >> _c_CDT.firstTerm
        aim_elbow_rotate_minus_PMA.output3D >> _c_CDT.colorIfFalse
        _c_CDT.colorIfTrueB.set(1)
        #
        # _c_CDT.operation.set(2)
        _c_CDT.outColor >> _cross_VPT.input1
        aim_ra_loc_minus_pma.output3D >> _cross_VPT.input2

        _cross_VPT.operation.set(2)
        _cross_VPT.normalizeOutput.set(1)
        #
        aim_nomal_VPT.outputX >> _rotate_FBF.in00
        aim_nomal_VPT.outputY >> _rotate_FBF.in01
        aim_nomal_VPT.outputZ >> _rotate_FBF.in02
        _cross_VPT.outputX >> _rotate_FBF.in10
        _cross_VPT.outputY >> _rotate_FBF.in11
        _cross_VPT.outputZ >> _rotate_FBF.in12
        aim_elbow_rotate_minus_PMA.output3Dx >> _rotate_FBF.in20
        aim_elbow_rotate_minus_PMA.output3Dy >> _rotate_FBF.in21
        aim_elbow_rotate_minus_PMA.output3Dz >> _rotate_FBF.in22
        #
        _rotate_FBF.output >> _rotate_DCM.inputMatrix
        _rotate_DCM.outputRotate >> elbow_node.r


main()
armOption('arm', 3, 3, True, True, True, 'qr_root', 'qr_main')
# spineOption('spine',4,False,False,'qr_root','qr_main')
# spineOption('neck',5,False,False,'qr_spine_Top','qr_spine_Parent')

# rotate_shape_in_direction('qr_l_arm_Top', [0,0,-90])

# give me a second
# i need to get my story straight
# my friend are in the bathroom getting higher than the empire state
# my lover, acose

# is gemma the smithy your new game crush?
# Are you smitten with Gemma the smithy?
# Monster Hunter fans have fallen head over heels in love with this cute
# new character, so much so that they brute-forced the 'Dating Sim' tag onto wild on stem for all to see.
# loads of gemma fan art has appeared on social media after
# the release of the new Monster Hunter Wils trailer during PlayStation State of Play
# monster huntet wilds producer said
# " when we designed her, of course,we knew she was gonna be an appealing character and that was the intention.
# but it's honestly gone beyond our expectations in terms of how much love has been poured out for."


# 제마 대장장이는 당신의 새로운 픽인가요?
# 당신은 제마 대장장이에 반했나요?
# 몬스터헌터 팬은 이 귀여운것에 푹 빠졌어?
# 새로운 케릭터가,너무마음에들어서 그들이 데이트시뮬  야생 스팀에 강제로 태그 했어. 모두가 볼수 있게.
# 젬마의 팬아트가 소셜미디어에 업로드 되고있어
# PlayStation State of Play 동안 새로운 Monster Hunter Wils 트레일러가 공개되었습니다.
# "몬스터 헌터 와일드의 프로듀서는 '우리가 그녀를 디자인했을 때, 물론 그녀가 매력적인 캐릭터가 될 거라는 것을 알고 있었고 그것이 의도였습니다. 하지만 솔직히 말해, 그녀에게 쏟아진 사랑의 정도는 우리의 기대를 넘어서고 있습니다.'라고 말했습니다."




