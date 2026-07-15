import nuke
class NodeTool:
    def __init__(self):
        self.node=None
        self.node_type=None
        self.label=""
        self.connect_viewer_enabled=True
        self.add_backdrop_enabled=True
        self.node_map={
                 "Blur":nuke.nodes.Blur,
                 "Grade":nuke.nodes.Grade,
                 "Transform":nuke.nodes.Transform,
                 "ColorCorrect":nuke.nodes.ColorCorrect,
                 "Merge2":nuke.nodes.Merge2
                 }
    def show_panel(self):
        panel=nuke.Panel("My Node")
        panel.addEnumerationPulldown("Node_type","Blur Grade Transform ColorCorrect Merge2")
        panel.addSingleLineInput("label","")
        panel.addBooleanCheckBox("Connect Viewer",True)
        panel.addBooleanCheckBox("Create Backdrop",True)
        if not panel.show():
            return False
        self.node_type=panel.value("Node_type")
        self.label=panel.value("label")
        self.connect_viewer_enabled=panel.value("Connect Viewer")
        self.add_backdrop_enabled=panel.value("Create Backdrop")
        return True
    def create_node(self):
        creator=self.node_map.get(self.node_type)
        if creator is None:
            nuke.message("Invalid node type")
            return False
        self.node=creator()
            return True
    def apply_label(self):
        self.node["label"].setValue(self.label)
    def connect_viewer(self):
        if nuke.activeViewer():
           viewer=nuke.activeViewer().node()
           viewer.setInput(0,self.node)
    def create_backdrop(self):
        nodes=nuke.selectedNodes()
        if not nodes:
           return
        min_x=min(node.xpos()for node in nodes)
        min_y=min(node.ypos()for node in nodes)
        max_x=max(node.xpos()+node.screenWidth()for node in nodes)
        max_y=max(node.ypos()+node.screenHeight()for node in nodes)
        padding=50
        self.backdrop=nuke.nodes.BackdropNode(
        xpos=min_x-padding,
        ypos=min_y-padding,
        bdwidth=(max_x-min_x)+(padding*2),
        bdheight=(max_y-min_y)+(padding*2),
        label=self.label
        )
    def run(self):
        if not self.show_panel():
           return 
        if not self.create_node():
           return 
        self.apply_label()
        if self.connect_viewer_enabled:
           self.connect_viewer()
        if self.add_backdrop_enabled:
           self.create_backdrop()
         
        