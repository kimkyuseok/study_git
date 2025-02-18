"""
-- Script Name: expression controller test
-- Description: Create a helper to generate local position normalization
-- Version: 1.0
-- Author: kimkyuseok
-- Date Created: 2025-02-18
-- Date Modified: 2025-02-19
-- References: https://help.autodesk.com/view/MAXDEV/2024/ENU/?guid=MAXDEV_Python_using_pymxs_pymxs_custattributes_html
-- Requirements: 3ds Max 2024 or later
-- Usage: Run the script from the MAXScript editor. Select the objects you want to align.
"""
from pymxs import runtime as rt

def delete_all_objects():
    rt.delete(rt.objects)
    
def create_vector_attribute():
    # ExposeTM 헬퍼 생성
    helper = rt.ExposeTransform()
    helper.name = "aa"

    # 빈 모디파이어 추가 (Attribute Holder 사용)
    attr_holder = rt.EmptyModifier()
    rt.addModifier(helper, attr_holder)

    # 커스텀 어트리뷰트 정의
    custom_attribute = """
    attributes VectorAttr
    (
        parameters main rollout:params
        (
            pos type:#point3 default:[0,0,0]
        )
        rollout params "VectorAttr"
        (
            spinner spn_x "X Position" range:[-1000,1000,0] type:#float
            spinner spn_y "Y Position" range:[-1000,1000,0] type:#float
            spinner spn_z "Z Position" range:[-1000,1000,0] type:#float
        )
    )
    """

    # 커스텀 어트리뷰트 추가
    rt.custAttributes.add(attr_holder, rt.execute(custom_attribute))

    #print(help(helper))
    helper_pos_local = rt.getPropertyController(helper,'LocalPosition')
    #rt.select(helper)
    expr_pos_ctl = rt.Point3_Expression()
    #print(helper_pos_local)
    expr_pos_ctl.addVectorTarget('aaLocalPos', helper_pos_local)
    # then add the expression that uses that variable
    expr_pos_ctl.setExpression('[aaLocalPos.x/sqrt(aaLocalPos.x^2 + aaLocalPos.y^2 + aaLocalPos.z^2), aaLocalPos.y/sqrt(aaLocalPos.x^2 + aaLocalPos.y^2 + aaLocalPos.z^2), aaLocalPos.z/sqrt(aaLocalPos.x^2 + aaLocalPos.y^2 + aaLocalPos.z^2)]')
    # finally, set the controller    
    rt.setPropertyController(attr_holder, "pos", expr_pos_ctl)




    

delete_all_objects()

# 스크립트 실행
create_vector_attribute()
