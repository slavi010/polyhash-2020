# For drawing
import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
# My stuff (not yours...)
from src.model.Grille import Grille
from src.model.ItemCase import ItemCase
from src.model.PointMontage import PointMontage
from src.model.Robot import Robot
from src.model.Tache import Tache


class DebugCanvas:
    def __init__(self, grille: Grille, cells_size: int=3):
        self.cpt: int = 0
        self.grille: Grille = grille

        # tkinter main class
        self.master: tk.Tk = tk.Tk()
        # a few parameters
        self.cell_size: int = cells_size
        self.width: int = cells_size*grille.longueur
        self.height: int = cells_size*grille.hauteur
        # the debug image will be drawn on a label
        self.label: tk.Label = tk.Label(self.master, width = self.width, height = self.height)
        # a new PIL image of the right size. We'll draw on that one
        self.img = Image.new("RGB", (self.width, self.height))
        # the PIL class for drawing on PIL images
        self.draw = ImageDraw.Draw(self.img)
        # resize the label and make the TK windows (always) topmost
        self.label.pack()
        self.master.attributes('-topmost', 'true')

        # To speed up things, we draw the grid and other stuffs once for all
        # draw all the cells
        self.img.paste( (255,255,255), [0,0,self.img.size[0],self.img.size[1]])
        for y in range(self.grille.hauteur):
            for x in range(self.grille.longueur):
               self.draw.rectangle([x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size], outline='grey')

        # then assembly points
        tache : Tache
        for tache in self.grille.taches:
            for i in range(len(tache.etapes)):
                fill_c = 'orange'
                pt = tache.etapes[i]
                self.draw.rectangle([pt.x*self.cell_size, pt.y*self.cell_size, pt.x*self.cell_size+self.cell_size, pt.y*self.cell_size+self.cell_size], fill=fill_c)

        self.update()

    def update(self):
        try:
            # cpt is just an index used when saving the debug frames (to create a gif for example)
            self.cpt+=1

            # Copy the pre-rendred image on a new image
            img=self.img.copy()
            self.draw = ImageDraw.Draw(img)

            #--------- The following part depends on your data structures so here it is just an example ----------#

            # debug : draw occupied cells in purple
            #for y in range(self.grille.height):
            #    for x in range(self.grille.width):
            #        if self.grille.robots_map[y][x] > 0:
            #            self.draw.rectangle([x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size], fill='purple')


            for robot in self.grille.robots:
                pince = robot.coordonnees_pince()
                for tache in robot.taches:
                    for etape_from, etape_to in zip(tache.etapes[0::1], tache.etapes[1::1]):
                        self.draw.rectangle([etape_from.x*self.cell_size, etape_from.y*self.cell_size, etape_to.x*self.cell_size+self.cell_size, etape_to.y*self.cell_size+self.cell_size], fill=(255,robot.point_montage.x*150//self.grille.longueur, robot.point_montage.y*150//self.grille.hauteur), width=self.cell_size//3)
                    self.draw.rectangle([pince.x*self.cell_size, pince.y*self.cell_size, tache.etapes[0].x*self.cell_size+self.cell_size, tache.etapes[0].y*self.cell_size+self.cell_size], fill=(255,robot.point_montage.x*150//self.grille.longueur, robot.point_montage.y*150//self.grille.hauteur), width=self.cell_size//3)


        # then mount points (grey circles)
            pt : ItemCase
            for pt in self.grille.point_montages:
                self.draw.ellipse([pt.x*self.cell_size, pt.y*self.cell_size, pt.x*self.cell_size+self.cell_size, pt.y*self.cell_size+self.cell_size], fill='grey')

            # then assembly points (color depends on their state)
            # tache : Tache
            # for tache in self.grille.taches:
            #     for i in range(min(tache.etapes[0]+1,len(tache.assembly_points))):
            #         if i < tache.current_assembly_point:
            #             fill_c = 'green'
            #         elif i == tache.current_assembly_point:
            #             fill_c = 'red'
            #
            #         pt = tache.assembly_points[i]
            #         self.draw.rectangle([pt.x*self.cell_size, pt.y*self.cell_size, pt.x*self.cell_size+self.cell_size, pt.y*self.cell_size+self.cell_size], fill=fill_c)

            robot: Robot
            # then robots mount points (blue circles)
            for robot in self.grille.robots:
                pt: PointMontage = robot.point_montage
                self.draw.ellipse([pt.x*self.cell_size, pt.y*self.cell_size, pt.x*self.cell_size+self.cell_size, pt.y*self.cell_size+self.cell_size], fill='blue')

            # then validated and current steps (black lines)
            for robot in self.grille.robots:
                first: bool = True
                previous: ItemCase = None
                for pt in robot.bras:
                    if first:
                        first = False
                    else:
                        self.draw.line([self.cell_size/2+previous.x*self.cell_size, self.cell_size/2+previous.y*self.cell_size, self.cell_size/2+pt.x*self.cell_size, self.cell_size/2+pt.y*self.cell_size], fill='black', width=self.cell_size//3)
                    previous = pt
                # draw gripper (black square)
                pt=robot.coordonnees_pince()
                if len(robot.bras) > 0:
                    self.draw.line([self.cell_size/2+previous.x*self.cell_size, self.cell_size/2+previous.y*self.cell_size, self.cell_size/2+pt.x*self.cell_size, self.cell_size/2+pt.y*self.cell_size], fill='black', width=self.cell_size//3)
                self.draw.rectangle([pt.x*self.cell_size, pt.y*self.cell_size, pt.x*self.cell_size+self.cell_size, pt.y*self.cell_size+self.cell_size], fill='black', width=self.cell_size//3)

            #----------------------------------- end of drawing --------------------------------------#

            # We need to flkip the image horizontally because because axis are not the same in my arrays and in images
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            # Create a new Photoimage from the PIL image
            self.PhotoImage = ImageTk.PhotoImage(img)
            # Update the image
            self.label.configure(image=self.PhotoImage)
            self.label.update()
            # We can same the image if we want (to create an animated GIF ?)
            #img.save("debug/{:4d}.jpg".format(self.cpt))
        except:
            pass
