import nuke
def create_custom_blur():
    path=nuke.getFilename("Select any Image")
    if not path:
        return
    read=nuke.nodes.Read()
    blur=nuke.nodes.Blur()
    blur.setInput(0,read)
    size=nuke.getInput("Enter blur node size","20")
    if size and float(size)>=0:
       blur["size"].setValue(float(size))
    else:
        nuke.message("Please Enter a valid size")
    name=nuke.getInput("Enter blur node")
    if name:
       blur["label"].setValue(name)
    filter_type=nuke.getInput(
        "enter blur filter type(cubic,gaussian,box)",
        "gaussion"
    )
    if filter_type and filter_type.lower()                                 in("cubic","gaussian","box"):
        blur["filter"].setValue(filter_type.lower())
    else:
        nuke.message("Please enter a valid filter")
    mix=nuke.getInput("enter blur mix(0-1)","1")
    if 0<=mix<=1:
       blur["mix"].setValue(mix)
    else:
        nuke.message("Enter a valid mix")
    if nuke.activeViewer():
       viewer=nuke.activeViewer().node()
       viewer.setInput(0,blur)
toolbar=nuke.menu("Nuke")
my_menu=toolbar.addMenu("My Toolbar")
my_menu.addCommand("Custom Blur",create_custom_blur) 
# create custom blur viewer node
import nuke
def create_blur_viewer_node():
    path=nuke.getFilename("Select an image")
    if not path:
       return
    read=nuke.nodes.Read(file=path)
    blur=nuke.nodes.Blur()
    blur.setInput(0,read)
    size=nuke.getInput("Enter blur node size","20")
    try:
        size=float(size)
        if size>=0:
            blur["size"].setValue(float(size))
        else:
            nuke.message("size must be greater than 0")
    except:
        nuke.message("Please enter a valid size")
    name=nuke.getInput("Enter blur label","Blur Node")
    if name:
        blur["label"].setValue(name)
    filter_type=nuke.getInput("Enter Filter type(box,gaussian,cubic)","Gaussian")
    if filter_type and filter_type.lower()in ("box","gaussian","cubic"):
       blur["filter"].setValue(filter_type.lower())
    mix=nuke.getInput("Enter mix between(0-1)","1")
    try:
        mix=float(mix)
        if 0<=mix<=1:
           blur["mix"].setValue(mix)
        else:
            nuke.message("mix must be between 0 and 1")
    except:
        nuke.message("Please enter a valid mix")
    if nuke.activeViewer():
        viewer=nuke.activeViewer().node()
        viewer.setInput(0,blur)
    write=nuke.nodes.Write()
    write.setInput(0,blur)
    output_path=nuke.getFilename("Select output file",".exr .jpg .jpeg .png")
    write["file"].setValue(output_path)
    x=100
    y=100
    read.setXYpos(x,y)
    blur.setXYpos(x,y+100)
    write.setXYpos(x,y+200)
    nodes=[read,blur,write]
    min_x=min(node.xpos()for node in nodes)
    max_x=max(node.xpos()+ node.screenWidth()for node in nodes)
    min_y=min(node.ypos()for node in nodes)
    max_y=max(node.ypos()+ node.screenHeight()for node in nodes)
    backdrop=nuke.nodes.BackdropNode(
        xpos=min_x-50,
        ypos=min_y-50,
        bdwidth=(max_x-min_x)+100,
        bdheight=(max_y-min_y)+100,
        label="Custom Blur Script"
        )
toolbar=nuke.menu("Nuke")
my_menu=toolbar.addMenu("My Toolbar")
my_menu.addCommand("Custom Blur Script",create_blur_viewer_node)
        
