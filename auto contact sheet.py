import nuke
import os

def auto_contact_sheet_builder():

    folder = nuke.getFilename("Select any image")

    if folder:

        folder = os.path.dirname(folder)

        image_exts = [".jpg", ".jpeg", ".png", ".exr"]

        columns = 5
        column_spacing = 400
        row_spacing = 1000

        start_x = 100
        start_y = 100

        count = 0
        all_nodes = []

        for file in sorted(os.listdir(folder)):

            if os.path.splitext(file)[1].lower() in image_exts:

                path = os.path.join(folder, file)

                col = count % columns
                row = count // columns

                x = start_x + (col * column_spacing)
                y = start_y + (row * row_spacing)

                name = os.path.splitext(file)[0]

                read = nuke.nodes.Read(file=path)
                read["label"].setValue(name)
                all_nodes.append(read)

                colorspace = nuke.nodes.Colorspace()
                colorspace.setInput(0, read)
                all_nodes.append(colorspace)

                reformat = nuke.nodes.Reformat()
                reformat.setInput(0, colorspace)
                all_nodes.append(reformat)

                transform = nuke.nodes.Transform()
                transform.setInput(0, reformat)
                all_nodes.append(transform)

                write = nuke.nodes.Write()
                write.setInput(0, transform)
                all_nodes.append(write)

                write["file"].setValue(
                    "[file dirname [value root.name]]/render/" +
                    name +
                    ".%04d.exr"
                )

                read.setXYpos(x, y)
                colorspace.setXYpos(x, y + 100)
                reformat.setXYpos(x, y + 200)
                transform.setXYpos(x, y + 300)
                write.setXYpos(x, y + 400)

                count += 1

        if not all_nodes:
            nuke.message("No supported images found")
            return

        min_x = min(node.xpos() for node in all_nodes)
        max_x = max(node.xpos() + node.screenWidth() for node in all_nodes)

        min_y = min(node.ypos() for node in all_nodes)
        max_y = max(node.ypos() + node.screenHeight() for node in all_nodes)

        padding = 50

        backdrop = nuke.nodes.BackdropNode(
            xpos=min_x - padding,
            ypos=min_y - padding,
            bdwidth=(max_x - min_x) + (padding * 2),
            bdheight=(max_y - min_y) + (padding * 2),
            label="Auto Contact Sheet\n{} Images".format(count)
        )

        backdrop["note_font_size"].setValue(40)

        nuke.message(
            "Contact sheet setup created successfully"
        )
toolbar=nuke.menu("Nuke")
my_menu=toolbar.addMenu("My Toolbar")
my_menu.addCommand("Auto Contact Sheet", auto_contact_sheet_builder)
