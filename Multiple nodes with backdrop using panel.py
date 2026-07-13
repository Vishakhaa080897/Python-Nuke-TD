import nuke
def main_panel():
    panel=nuke.Panel("Node Type")
    panel.addEnumerationPulldown("Node Type","Blur Transform Grade ColorCorrect")
    panel.addSingleLineInput("Label","")
    panel.addBooleanCheckBox("Select Created Node", True)
    if not panel.show():
       return
    node_type=panel.value("Node Type")
    label=panel.value("Label")
    select_node=panel.value("Select Created Node")
    node=node_handler(node_type,label,select_node)
    if node:
       active_viewer(node)
def node_handler(node_type,label,select_node):
    node_handlers={
         "Blur":nuke.nodes.Blur,
         "Transform":nuke.nodes.Transform,
         "Grade":nuke.nodes.Grade,
         "ColorCorrect":nuke.nodes.ColorCorrect
     }
    handler=node_handlers[node_type]
    node=handler()
    node["label"].setValue(label)
    node.setSelected(select_node)
    return node
def active_viewer(node):
     if nuke.activeViewer():
        viewer=nuke.activeViewer().node()
        viewer.setInput(0,node)
def add_backdrop():
    nodes=nuke.selectedNodes()
    if not nodes:
       nuke.message("Please select atleast one node")
       return
    min_x=min(node.xpos()for node in nodes)
    max_x=max(node.xpos()+ node.screenWidth()for node in nodes)
    min_y=min(node.ypos()for node in nodes)
    max_y=max(node.ypos()+ node.screenHeight()for node in nodes)
    label=nuke.getInput("Enter backdrop label","My Backdrop")
    if not label:
       label="My Backdrop"
    padding=50
    backdrop=nuke.nodes.BackdropNode(
         xpos=min_x-padding,
         ypos=min_y-padding,
         bdwidth=(max_x-min_x)+(padding*2),
         bdheight=(max_y-min_y)+(padding*2),
         label=label
         )
toolbar=nuke.menu("Nuke")
my_menu=toolbar.addMenu("My Toolbar")
my_menu.addCommand("Create Node",main_panel)
my_menu.addCommand("Add Backdrop",add_backdrop)
         
   
