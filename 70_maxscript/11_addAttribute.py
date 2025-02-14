from pymxs import runtime as rt

# 포인트 'aa' 생성
point_aa = rt.point()
point_aa.name = "aa"

attribute_holder = rt.EmptyModifier()
attribute_holder.name = 'newEmpyModifier'

# point_aa에 attribute_holder 연결
rt.addModifier(point_aa, attribute_holder)


# 사용자 정의 속성 (Custom Attribute) 정의 (Vector 값 추가)
custom_attribute = """
attributes newAttributes
(
    parameters main rollout:params
    (
        pos type:#point3 default:[0,0,0]
    )
    rollout params "Custom Attributes"
    (
        spinner spn_x "X Position" range:[-1000,1000,0] type:#float ui:pos.x
        spinner spn_y "Y Position" range:[-1000,1000,0] type:#float ui:pos.y
        spinner spn_z "Z Position" range:[-1000,1000,0] type:#float ui:pos.z
    )
)
"""

# 추가한 EmptyModifier 가져오기
mod = None
for m in point_aa.modifiers:
    if m.name == "newEmpyModifier":
        mod = m
        break

# EmptyModifier에 Custom Attribute 추가
rt.custAttributes.add(mod, rt.execute(custom_attribute))
