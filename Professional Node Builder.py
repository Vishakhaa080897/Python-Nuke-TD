import nuke
class PanelManager:
    def show(self):
        panel=nuke.Panel("Panel Manager")
        panel.addEnumerationPulldown("Node Type","Blur Transform Grade Merge2 ColorCorrect")
        panel.addSingleLineInput("Label","My label")
        panel.addBooleanCheckBox("Connect Viewer",True)
        panel.addBooleanCheckBox("Create Backdrop",True)
        if not panel.show():
           return None
        return{
                  "node_type":panel.value("Node Type"),
                  "label":panel.value("Label"),
                  "connect_viewer":panel.value("Connect Viewer"),
                  "create_backdrop":panel.value("Create Backdrop"),
        }
class Validator:
    def __init__(self):
        self.allowed_nodes=["Blur","Grade","Transform","Merge2","ColorCorrect"]
    def validate_label(self,label):
        if not label or label.strip()=="": 
            raise ValueError("Label cannot be empty")
        return True
    def validate_node_type(self,node_type):
        if node_type not in self.allowed_nodes:
           raise ValueError ("Invalid node type")
        return True
    def validate(self,data):
        self.validate_label(data["label"])
        self.validate_node_type(data["node_type"])
        return True
class NodeFactory:
    def __init__(self):
        self.node_map={
                      "Blur":nuke.nodes.Blur,
                      "Grade":nuke.nodes.Grade,
                      "Transform":nuke.nodes.Transform,
                      "Merge2":nuke.nodes.Merge2,
                      "ColorCorrect":nuke.nodes.ColorCorrect
                      }
    def create(self,node_type):
        creator=self.node_map.get(node_type)
        if creator is None:
           raise ValueError ("Invalid node type")
        return creator()
class LabelManager:
    def apply(self,node,label):
        if node is None:
           raise ValueError ("Node cannot be None")
        if not label or label.strip()=="":
           raise ValueError ("Label cannot be empty")
        node["label"].setValue(label)
        return True
class ViewerConnector:
    def connect(self,node):
        if node is None:
           raise ValueError ("Node cannot be None")
        viewer=nuke.activeViewer()
        if viewer is None:
           raise RuntimeError("No active viewer found")
        viewer.node().setInput(0,node)
        return True
class BackdropCreator:
    def create(self,label):
        nodes=nuke.selectedNodes()
        if not nodes:
           raise RuntimeError ("No nodes selected")
        min_x=min(node.xpos()for node in nodes)
        min_y=min(node.ypos()for node in nodes)
        max_x=max(node.xpos()+node.screenWidth()for node in nodes)
        max_y=max(node.ypos()+node.screenHeight()for node in nodes)
        padding=50
        backdrop=nuke.nodes.BackdropNode(
             xpos=min_x-padding,
             ypos=min_y-padding,
             bdwidth=(max_x-min_x)+(padding*2),
             bdheight=(max_y-min_y)+(padding*2),
             label=label
        )
        return backdrop
class NodeBuilder:
    def __init__(self):
        self.panel=PanelManager()
        self.validator=Validator()
        self.factory=NodeFactory()
        self.label=LabelManager()
        self.viewer=ViewerConnector()
        self.backdrop_creator=BackdropCreator()
        self.node=None
        self.backdrop=None
    def run(self):
        try:
           data=self.panel.show()
           if data is None:
              return
           self.validator.validate(data)
           self.node=self.factory.create(data["node_type"])
           self.label.apply(self.node,data["label"])
           if data["connect_viewer"]:
              self.viewer.connect(self.node)
           if data["create_backdrop"]:
              self.backdrop=self.backdrop_creator.create(data["label"])
        except Exception as e:
            nuke.message(str(e))
builder = NodeBuilder()
builder.run()