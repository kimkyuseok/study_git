"""
-- Script Name: Toolbar test
-- Description: Creating a "hello world" toolbar in Autodesk Max
-- Version: 1.0
-- Author: kimkyuseok
-- Date Created: 2025-02-18
-- Date Modified: 2025-02-19
-- References: https://help.autodesk.com/view/MAXDEV/2024/ENU/?guid=MAXDEV_Python_using_pymxs_pymxs_macroscripts_menus_html
-- Requirements: 3ds Max 2024 or later
-- Usage: Run the script from the MAXScript editor. Select the objects you want to align.
"""
from pymxs import runtime as rt


def myfunc():
    print('hello world')

# Connect to a gobal in the runtime:
rt.mxs_hello = myfunc

def remove_existing_menu(menu_name):
    main_menu = rt.menuMan.getMainMenuBar()
    for i in range(main_menu.numItems()):
        item = main_menu.getItem(i+1)
        if item.getTitle() == menu_name:
            main_menu.removeItem(item)
            rt.menuMan.unRegisterMenu(rt.menuMan.findMenu(menu_name))
            print(f"Existing menu '{menu_name}' removed.")
            return True
    return False

def create_custom_menu(menu_name):
    remove_existing_menu(menu_name)
    
    main_menu = rt.menuMan.getMainMenuBar()
    custom_menu = rt.menuMan.createMenu(menu_name)
    
    menu_item = rt.menuMan.createSubMenuItem(menu_name, custom_menu)
    
    pos = main_menu.numItems() - 1
    main_menu.addItem(menu_item, pos)
    
    print(f"New menu '{menu_name}' created.")
    return custom_menu

def create_or_update_menu_action(action_name, category, script):
    try:
        rt.macros.new(category, action_name, "tool-tip", action_name, script)
        print(f"Action '{action_name}' created or updated.")
    except Exception as e:
        print(f"Error creating/updating action '{action_name}': {str(e)}")

def add_action_to_menu(menu, action_name, category):
    action_item = rt.menuMan.createActionItem(action_name, category)
    if action_item:
        existing_items = [menu.getItem(i) for i in range(1, menu.numItems() + 1)]
        if action_item not in existing_items:
            menu.addItem(action_item, -1)
            print(f"Action '{action_name}' added to menu.")
            return True
        else:
            print(f"Action '{action_name}' already in menu.")
            return True
    print(f"Failed to create action item for '{action_name}'.")
    return False

# 메인 실행 부분
try:
    my_menu = create_custom_menu("MyCustomMenu")
    macroscript_content = 'mxs_hello()'    
    
    create_or_update_menu_action("MyAction", "MyScripts", macroscript_content)
    
    if add_action_to_menu(my_menu, "MyAction", "MyScripts"):
        rt.menuMan.updateMenuBar()
        print("Menu creation and update completed successfully.")
    else:
        print("Failed to add action to menu. Menu update incomplete.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
