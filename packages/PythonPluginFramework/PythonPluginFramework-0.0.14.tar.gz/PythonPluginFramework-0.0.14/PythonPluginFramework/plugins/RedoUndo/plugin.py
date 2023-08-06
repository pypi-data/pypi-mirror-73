
'''
RedoUndo Plugin:

插件提供了一个基础动作扩展点，基础动作分为了redo和undo两个接口。在支持undo、redo的修改中，添加这个动作实现。
插件内部维护一个undo、redo列表，一个游标标记当前位置。
执行undo时，移动游标，执行redo时，移动游标，添加新动作时，基于当前游标位置压入新的动作。

插件支持监控两个事件，一个是动作记录开始，另一个是动作记录结束。具体一个undo恢复多少执行动作，有动作实现插件决定。


'''
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


context = None

# 记录所有的动作列表
actions_list = []
# 当前游标位置
cur_actions_list_pos = 0

# 当前激活动作
# 假设不会有多个线程同时产生动作列表
cur_actions = None
# 当前动作列表激活次数
# 一次动作记录开始，增加1
# 一次动作记录结束，减少1
cur_stack = 0

# 标记是否处于undo  redo
g_is_undo_redoing = False

# Undo Service
_g_undoservice_ = None

def init(context_):
    global context
    context = context_

# 新建动作记录开始
def action_start():
    global cur_actions
    global cur_stack

    if cur_stack == 0:
        cur_actions = []
    cur_stack += 1

# 动作记录结束
def action_end():
    global cur_actions
    global cur_stack

    if cur_stack == 0:
        return 

    cur_stack -= 1
    if cur_stack == 0:
        add_new_actions(cur_actions)
        cur_actions = []


# 添加新的动作
def add_new_actions(actions):
    global cur_actions_list_pos
    global actions_list

    if len(actions_list) == cur_actions_list_pos:
        actions_list.append(actions)
        cur_actions_list_pos += 1
    else:
        actions_list = actions_list[0:cur_actions_list_pos]
        actions_list.append(actions)
        cur_actions_list_pos += 1

# 执行undo
def do_undo(obj):
    global cur_actions_list_pos
    global actions_list

    global g_is_undo_redoing
    g_is_undo_redoing = True
    if cur_actions_list_pos>0:
        actions = actions_list[cur_actions_list_pos-1]
        cur_actions_list_pos -= 1
        for i in range(0, len(actions)):
            actions[len(actions) - 1 - i].undo()
    g_is_undo_redoing = False

# 执行redo
def do_redo(obj):
    global cur_actions_list_pos
    global actions_list
    
    global g_is_undo_redoing
    g_is_undo_redoing = True
    if cur_actions_list_pos<len(actions_list):
        actions = actions_list[cur_actions_list_pos]
        cur_actions_list_pos += 1
        for i in range(0, len(actions)):
            actions[i].redo()
    g_is_undo_redoing = False


class PaneExtensionToolbar:
    def __init__(self):
        self._file = None
    def priorty(self):
        return 1900
    def add_menu(self, menu_bar):
        self.plugin_menu = menu_bar.addMenu('Edit')
        self.plugin_action = self.plugin_menu.addAction('Undo')
        self.plugin_action.triggered.connect(do_undo)

        self.plugin_action2 = self.plugin_menu.addAction('Redo')
        self.plugin_action2.triggered.connect(do_redo)

# 服务接口描述
def service_declare():
    decl = []
    for fun in dir(_g_undoservice_):
        if type(fun) != type(''):
            continue

        if fun+"_des" in dir(_g_undoservice_):
            decl.append(eval('_g_undoservice_.'+fun+'_des()'))
    
    return decl

class UndoServiceManage:
    def __init__(self):
        pass
    def add_action(self, action):
        global cur_actions
        global cur_stack

        if cur_stack>0:
            cur_actions.append(action)
        else:
            actions = []
            actions.append(action)
            add_new_actions(actions)
    def add_action_des(self):
        return {
            "des":"添加新Undo动作", 
            "name": "add_action",
            "return": ""
        }

_g_undoservice_ = UndoServiceManage()


# 监控基础数据变化
def onNewRootDataNode(event, node):
    class NewRootDataNodeAction:
        def __init__(self, node):
            pass
        def undo(self):
            # 删除新建的节点
            pass
        def redo(self):
            # 新建根节点
            pass

    return
    global _g_undoservice_
    action = NewRootDataNodeAction(node)
    _g_undoservice_.add_action(action)

def onProjectOpen(event, node):
    global actions_list
    global cur_actions_list_pos
    global cur_actions
    global cur_actions

    actions_list = []
    cur_actions_list_pos = 0
    cur_actions = None
    cur_stack = 0

def onProjectClose(event, node):
    global actions_list
    global cur_actions_list_pos
    global cur_actions
    global cur_actions

    actions_list = []
    cur_actions_list_pos = 0
    cur_actions = None
    cur_stack = 0


def onNewDataNode(event, node):
    class NewDataNodeAction:
        def __init__(self, node):
            self.node = node
        def undo(self):
            # 删除新建的节点
            pass
        def redo(self):
            # 新建根节点
            pass
    global g_is_undo_redoing
    if g_is_undo_redoing == True:
        return
    global _g_undoservice_
    action = NewDataNodeAction(node)
    _g_undoservice_.add_action(action)



def onDataNodeDelete(event, node):
    class DataNodeDeleteAction:
        def __init__(self, node):
            self.node = node
        def undo(self):
            # 删除新建的节点
            pass
        def redo(self):
            # 新建根节点
            pass
    global g_is_undo_redoing
    if g_is_undo_redoing == True:
        return
    global _g_undoservice_
    action = DataNodeDeleteAction(node)
    _g_undoservice_.add_action(action)



def onDataNodeModifyName(event, node, str_old_name):
    class DataNodeModifyNameAction:
        def __init__(self, node, str_old_name):
            self.node = node
            self.str_old_name = str_old_name
            self.str_new_name = self.node.get_name()
        def undo(self):
            # 删除新建的节点
            self.node.set_name(self.str_old_name)
        def redo(self):
            # 新建根节点
            self.node.set_name(self.str_new_name)

    global g_is_undo_redoing
    if g_is_undo_redoing == True:
        return
    global _g_undoservice_
    action = DataNodeModifyNameAction(node, str_old_name)
    _g_undoservice_.add_action(action)

def onDataNodeModifyProp(event, node, prop_key, old_prop_value):
    class DataNodeModifyPropAction:
        def __init__(self, node, prop_key, old_prop_value):
            self.node = node
            self.prop_key = prop_key
            self.old_prop_value = old_prop_value
            self.new_prop_value = self.node.get_prop(self.prop_key)
        def undo(self):
            # 删除新建的节点
            self.node.set_prop(self.prop_key, self.old_prop_value)
        def redo(self):
            # 新建根节点
            self.node.set_prop(self.prop_key, self.new_prop_value)

    global g_is_undo_redoing
    if g_is_undo_redoing == True:
        return
    global _g_undoservice_
    action = DataNodeModifyPropAction(node, prop_key, old_prop_value)
    _g_undoservice_.add_action(action)

def onDataNodeModifyAddChild(event, node, child):
    class DataNodeModifyAddChildAction:
        def __init__(self, node, child):
            self.node = node
            self.child = child
            self.index = 0
            children = self.node.get_children()
            for i in range(0, len(children)):
                if children[i] == child:
                    self.index = i
                    break
        def undo(self):
            # 删除新建的节点
            self.node.remove_child(child)
        def redo(self):
            # 新建根节点
            children = self.node.get_children()
            if self.index < len(children):
                self.node.insert_child(self.child, children[self.index])
            else:
                self.node.add_child(self.child)  

    global g_is_undo_redoing
    if g_is_undo_redoing == True:
        return
    global _g_undoservice_
    action = DataNodeModifyAddChildAction(node, child)
    _g_undoservice_.add_action(action)


def onDataNodeModifyRemoveChild(event, node, child, index):
    class DataNodeModifyRemoveChildAction:
        def __init__(self, node, child):
            self.node = node
            self.child = child
            self.index = index
        def undo(self):
            # 删除新建的节点
            children = self.node.get_children()
            if self.index < len(children):
                self.node.insert_child(self.child, children[self.index])
            else:
                self.node.add_child(self.child)  
        def redo(self):
            # 新建根节点
            self.node.remove_child(child)

    global g_is_undo_redoing
    if g_is_undo_redoing == True:
        return
    global _g_undoservice_
    action = DataNodeModifyRemoveChildAction(node, child)
    _g_undoservice_.add_action(action)


# 注册菜单 redo undo
# 监控动作开始、停止事件
config = {
    'pluginid': 'Core::UndoRedo',
    "services" : [
        {
            "name": "UndoService",
            "define": _g_undoservice_,
            'declare': service_declare()
        }
    ],
    "extensions" : [
        {
            "name": "PL::Basic::Menu",
            "id": "PL::Basic::Menu::RedoUndo",
            "impl": PaneExtensionToolbar()
        }
    ],
    "subscribes" : [
        {
            "name": 'event::RedoUndo::Start',
            "define": action_start
        },
        {
            "name": 'event::RedoUndo::Stop',
            "define": action_end
        },
        {
            'name': 'event::NewRootDataNode',
            "define": onNewRootDataNode
        },
        {
            'name': 'event::Project::Open',
            "define": onProjectOpen
        },
        {
            'name': 'event::Project::Close',
            "define": onProjectClose
        },
        {
            'name': 'event::NewDataNode',
            "define": onNewDataNode
        },
        {
            'name': 'event::DataNode::Delete',
            "define": onDataNodeDelete
        },
        {
            'name': 'event::DataNode::Modify::Name',
            "define": onDataNodeModifyName

        },
        {
            'name': 'event::DataNode::Modify::Prop',
            "define": onDataNodeModifyProp
        },
        {
            'name': 'event::DataNode::Modify::AddChild',
            "define": onDataNodeModifyAddChild
        },
        {
            'name': 'event::DataNode::Modify::RemoveChild',
            "define": onDataNodeModifyRemoveChild
        }
    ],
    'events' : [
        {
            'name': 'event::RedoUndo::Start'
        },
        {
            'name': 'event::RedoUndo::Stop'
        }
    ]
}