import nuke
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
    backdrop["tile_color"].setValue(4278190335)
    backdrop["note_font_size"].setValue(40)