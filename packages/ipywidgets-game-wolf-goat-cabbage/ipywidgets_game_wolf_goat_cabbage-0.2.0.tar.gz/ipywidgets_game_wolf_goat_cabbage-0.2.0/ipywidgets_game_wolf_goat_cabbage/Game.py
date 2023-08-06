import ipywidgets as widgets
import os
import time
from IPython.display import display
from .Field import Field
import traitlets

__version__ = "0.1"
global translation
translation = {
    "en_EN": {
        "Board": "Board",
        "Unboard": "Unboard",
        "Cross": "Cross",
        "Reset": "Reset",
        "Goat": "Goat",
        "Cabbage": "Cabbage",
        "Wolf": "Wolf",
        "Win": "images/win.jpg",
        "Lost": "images/lost.png",
        "actions": "Actions",
    },
    "fr_FR": {
        "Board": "Monter",
        "Unboard": "Descendre",
        "Cross": "Traverser",
        "Reset": "Reset",
        "Goat": "Chèvre",
        "Cabbage": "Chou",
        "Wolf": "Loup",
        "Win": "images/gagne.jpg",
        "Lost": "images/lost.png",
        "actions": "Actions",
    },
}


def mkImageWidget(file_name, im_format, w=50, h=50):
    assert isinstance(file_name, str), "file_name has to be a string"
    assert isinstance(im_format, str), "im_format has to be a string"
    file = open(file_name, "rb")
    image = file.read()
    return widgets.Image(
        value=image,
        format=im_format,
        width=w,
        height=h,
        layout=widgets.Layout(border="none", margin="0px", padding="0 px"),
    )


class Game(widgets.VBox):
    """
        Visualisation of the game Goat-Wolf-Cabbage
    """
    value = traitlets.List()

    def __init__(self, language="en_EN"):
        """
            Initialization of the visualisation
            
            Parameter
            ----------
            lang : (default value='en_EN') (type=string) game's language
            
            Tests
            -----------
            >>> grid=Grid()
            >>> grid.field.boat.side
            True
            >>> grid.field.leftCoast.goat
            True
            >>> grid.field.rightCoast.goat
            False
            >>> grid.field.leftCoast.wolf
            True
            >>> grid.field.rightCoast.wolf
            False
            >>> grid.field.leftCoast.cabbage
            True
            >>> grid.field.rightCoast.cabbage
            False
            >>> c1=mkImageWidget('images/goat.jpg','jpg')
            >>> grid.map[1][1].value==c1.value
            True
            >>> c2=mkImageWidget('images/wolf.png','png')
            >>> grid.map[1][2].value==c2.value
            True
            >>> c3=mkImageWidget('images/cabbage.jpg','jpg')
            >>> grid.map[1][3].value==c3.value
            True
            >>> grid.value
            ['Left', (1, 1), (1, 2), (1, 3), None]
            
        """
        if language in translation:
            self.__language = language
        else:
            self.__language = "en_EN"
        self.__lost = False
        self.__lCoastLoc = {"Goat": (1, 1), "Wolf": (1, 2), "Cabbage": (1, 3)}
        self.__rCoastLoc = {"Goat": (8, 1), "Wolf": (8, 2), "Cabbage": (8, 3)}
        self.__boatLocation = {
            "Left": {"First": (2, 2), "Second": (3, 2)},
            "Right": {"First": (6, 2), "Second": (7, 2)},
        }
        self.__data = {
            "Goat": ("images/goat.jpg", "jpg"),
            "Cabbage": ("images/cabbage.jpg", "jpg"),
            "Wolf": ("images/wolf.png", "png"),
            "Water": ("images/water.jpg", "jpg"),
            "Ground": ("images/ground.jpg", "jpg"),
            "Wood": ("images/wood.jpg", "jpg"),
        }
        self.__field = Field()
        self.__map = self.mkMap()
        self.__message = mkImageWidget("images/blank.jpg", "jpg", 180, 60)
        self.__action = widgets.Label(
            value="", layout=widgets.Layout(justify_content="center", margin="10px")
        )

        # Display
        myCol = [None for j in range(0, self.__field.columns)]
        for i in range(0, self.__field.columns):
            myCol[i] = widgets.VBox(
                self.__map[i],
                layout=widgets.Layout(border="none", margin="0px", padding="0px"),
            )
        game = widgets.HBox(
            myCol, layout=widgets.Layout(border="none", margin="0px", padding="0px")
        )
        message_box = widgets.VBox(
            [self.__message],
            layout=widgets.Layout(justify_content="center", margin="10px"),
        )
        
        self.__value = self.mk_value()
        self.__visualisation = widgets.HBox([game, message_box])

        category_g    = self.translate("Goat")
        category_w    = self.translate("Wolf")
        category_cab  = self.translate("Cabbage")
        category_else = self.translate("actions")
        bg  = self.translate("Board")   + " " + self.translate("Goat")
        ug  = self.translate("Unboard") + " " + self.translate("Goat")
        bw  = self.translate("Board")   + " " + self.translate("Wolf")
        uw  = self.translate("Unboard") + " " + self.translate("Wolf")
        bc  = self.translate("Board")   + " " + self.translate("Cabbage")
        uc  = self.translate("Unboard") + " " + self.translate("Cabbage")
        cr  = self.translate("Cross")
        res = self.translate("Reset")

        actions = {
            category_g: [(bg, self.board, "Goat"), (ug, self.unboard, "Goat")],
            category_w: [(bw, self.board, "Wolf"), (uw, self.unboard, "Wolf")],
            category_cab: [(bc, self.board, "Cabbage"), (uc, self.unboard, "Cabbage")],
            category_else: [(cr, self.cross), (res, self.reset)],
        }
        #self.__player = ValuePlayerWidget(
        #    visualisation=self.__visualisation,
        #    UI=UI,
        #    actions=actions,
        #    language=self.__language,
        #)
        #self.__player.player.reset(self.mk_value())
        self.value=self.mk_value()
        widgets.VBox.__init__(self, [self.__visualisation])

    @traitlets.observe("value")
    def _observe_value(self, change):
        self.update_display(change["new"])


    @property
    def field(self):
        return self.__field

    @property
    def map(self):
        return self.__map

    def translate(self, word):
        return translation[self.__language][word]

    def mk_value(self, action=None):
        """
            Returns the updated value of Grid
            
            Parameter
            ----------
            action : (type=string) the last action made
            
            Tests
            -----------
            >>> grid=Grid()
            >>> grid.value
            ['Left', (1, 1), (1, 2), (1, 3), None]
            >>> grid.board('Goat')
            >>> grid.cross()
            >>> grid.mk_value('Cross')
            ['Right', (6, 2), (1, 2), (1, 3), 'Cross']
            
        """
        t = []
        # Boat
        if self.__field.boat.side:
            t.append("Left")
        else:
            t.append("Right")
        # Goat
        if self.__field.leftCoast.goat == True:
            t.append(self.__lCoastLoc["Goat"])
        elif self.__field.rightCoast.goat == True:
            t.append(self.__rCoastLoc["Goat"])
        elif self.__field.boat.first == "Goat":
            t.append(self.__boatLocation[t[0]]["First"])
        elif self.__field.boat.second == "Goat":
            t.append(self.__boatLocation[t[0]]["Second"])
        # Wolf
        if self.__field.leftCoast.wolf == True:
            t.append(self.__lCoastLoc["Wolf"])
        elif self.__field.rightCoast.wolf == True:
            t.append(self.__rCoastLoc["Wolf"])
        elif self.__field.boat.first == "Wolf":
            t.append(self.__boatLocation[t[0]]["First"])
        elif self.__field.boat.second == "Wolf":
            t.append(self.__boatLocation[t[0]]["Second"])
        # Cabbage
        if self.__field.leftCoast.cabbage == True:
            t.append(self.__lCoastLoc["Cabbage"])
        elif self.__field.rightCoast.cabbage == True:
            t.append(self.__rCoastLoc["Cabbage"])
        elif self.__field.boat.first == "Cabbage":
            t.append(self.__boatLocation[t[0]]["First"])
        elif self.__field.boat.second == "Cabbage":
            t.append(self.__boatLocation[t[0]]["Second"])
        # Action
        t.append(action)
        return t

    def update_display(self, change):
        """
            Update the visualisation when self.__value has changed
            
            Parameter
            ----------
            change : (type=list) the value describing the state of the field
            
        """
        # Display Boat
        if change[0] == "Left":
            side = "Right"
        else:
            side = "Left"
        self.update_image(
            self.__boatLocation[change[0]]["First"][0],
            self.__boatLocation[change[0]]["First"][1],
            self.__data["Wood"][0],
            self.__data["Wood"][1],
        )
        self.update_image(
            self.__boatLocation[change[0]]["Second"][0],
            self.__boatLocation[change[0]]["Second"][1],
            self.__data["Wood"][0],
            self.__data["Wood"][1],
        )
        self.update_image(
            self.__boatLocation[side]["First"][0],
            self.__boatLocation[side]["First"][1],
            self.__data["Water"][0],
            self.__data["Water"][1],
        )
        self.update_image(
            self.__boatLocation[side]["Second"][0],
            self.__boatLocation[side]["Second"][1],
            self.__data["Water"][0],
            self.__data["Water"][1],
        )
        # All Grass
        for p in self.__lCoastLoc:
            self.update_image(
                self.__lCoastLoc[p][0],
                self.__lCoastLoc[p][1],
                self.__data["Ground"][0],
                self.__data["Ground"][1],
            )
        for p in self.__rCoastLoc:
            self.update_image(
                self.__rCoastLoc[p][0],
                self.__rCoastLoc[p][1],
                self.__data["Ground"][0],
                self.__data["Ground"][1],
            )

        # Goat
        self.update_image(
            change[1][0], change[1][1], self.__data["Goat"][0], self.__data["Goat"][1]
        )
        # Wolf
        self.update_image(
            change[2][0], change[2][1], self.__data["Wolf"][0], self.__data["Wolf"][1]
        )
        # Cabbage
        self.update_image(
            change[3][0],
            change[3][1],
            self.__data["Cabbage"][0],
            self.__data["Cabbage"][1],
        )

        # Message
        if change[1:4] == [
            self.__rCoastLoc["Goat"],
            self.__rCoastLoc["Wolf"],
            self.__rCoastLoc["Cabbage"],
        ]:
            self.win()
        elif (
            change[0] == "Right"
            and change[1] == self.__lCoastLoc["Goat"]
            and change[2] == self.__lCoastLoc["Wolf"]
        ) or (
            change[0] == "Left"
            and change[1] == self.__rCoastLoc["Goat"]
            and change[2] == self.__rCoastLoc["Wolf"]
        ):
            self.win(False)
        elif (
            change[0] == "Right"
            and change[1] == self.__lCoastLoc["Goat"]
            and change[3] == self.__lCoastLoc["Cabbage"]
        ) or (
            change[0] == "Left"
            and change[1] == self.__rCoastLoc["Goat"]
            and change[3] == self.__rCoastLoc["Cabbage"]
        ):
            self.win(False)
        else:
            file = open("images/blank.jpg", "rb")
            image = file.read()
            self.__message.format = "jpg"
            self.__message.value = image

    def update_image(self, c, r, file_name, file_format):
        """
            Update the widget Image line r column c
            
            Parameters
            -----------
            c : (type=int) column
            r : (type=int) row
            file_name : (type=string) the file's name
            file_format : (type=string) the file's format
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/goat.jpg','jpg')
            >>> grid.map[0][0].value==c1.value
            True
            >>> grid.update_image(0,0,'images/goat.jpg','jpg')
            >>> grid.map[0][0].value==c1.value
            False
            >>> grid.map[0][0].value==c2.value
            True
            
        """
        file = open(file_name, "rb")
        image = file.read()
        self.__map[c][r].format = file_format
        self.__map[c][r].value = image

    def reset(self):
        """
            Reset the game
            
            Tests
            -----------
            >>> grid=Grid()
            >>> grid.board('Cabbage')
            >>> grid.board('Wolf')
            >>> grid.cross()
            >>> grid.unboard('Wolf')
            >>> grid.reset()
            >>> grid.value==['Left', (1, 1), (1, 2), (1, 3), None]
            True
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/goat.jpg','jpg')
            >>> grid.map[8][1].value==c1.value
            True
            >>> grid.map[1][1].value==c2.value
            True
            >>> grid.field.boat.side
            True
            >>> grid.field.leftCoast.goat
            True
            >>> grid.field.rightCoast.goat
            False
            >>> grid.field.leftCoast.wolf
            True
            >>> grid.field.rightCoast.wolf
            False
            >>> grid.field.leftCoast.cabbage
            True
            >>> grid.field.rightCoast.cabbage
            False
            
        """
        self.__lost = False
        self.__field.__init__()
        file = open("images/blank.jpg", "rb")
        image = file.read()
        self.__message.format = "jpg"
        self.__message.value = image
        self.value=self.mk_value()

    def mkElem(self, name=None):
        """
            Get the data linked to name and give it as parameters to mkImageWidget
            
            Parameter
            ----------
            name : (type=string) the element to display
            
        """
        if name != None:
            return mkImageWidget(self.__data[name][0], self.__data[name][1])

    def mkMap(self):
        """
            Create a map containing all the widgets Image
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c3=mkImageWidget('images/water.jpg','jpg')
            >>> c4=mkImageWidget('images/goat.jpg','jpg')
            >>> c5=mkImageWidget('images/cabbage.jpg','jpg')
            >>> c6=mkImageWidget('images/wolf.png','png')
            >>> map=grid.mkMap()
            >>> map[0][0].value==c1.value
            True
            >>> map[1][1].value==c4.value
            True
            >>> map[1][2].value==c6.value
            True
            >>> map[1][3].value==c5.value
            True
            >>> map[2][2].value==c2.value
            True
            >>> map[3][2].value==c2.value
            True
            
        """
        items = [
            [None for r in range(0, self.__field.rows)]
            for c in range(0, self.__field.columns)
        ]
        if self.__field.leftCoast.goat:
            items[1][1] = self.mkElem("Goat")
        if self.__field.leftCoast.wolf:
            items[1][2] = self.mkElem("Wolf")
        if self.__field.leftCoast.cabbage:
            items[1][3] = self.mkElem("Cabbage")

        if self.__field.rightCoast.goat:
            items[8][1] = self.mkElem("Goat")
        if self.__field.rightCoast.wolf:
            items[8][2] = self.mkElem("Wolf")
        if self.__field.rightCoast.cabbage:
            items[8][3] = self.mkElem("Cabbage")

        i1, i2 = 0, 0
        if self.__field.boat.side:  # coast gauche
            i1 = 2
            i2 = 3
        else:
            i1 = 6
            i2 = 7

        if (
            self.__field.boat.first != None
        ):  
            items[i1][2] = self.mkElem(self.__field.boat.first)
        else:  
            items[i1][2] = self.mkElem("Wood")
        if (
            self.__field.boat.second != None
        ):  
            items[i2][2] = self.mkElem(self.__field.boat.second)
        else:
            items[i2][2] = self.mkElem("Wood")

        for r in range(0, self.__field.rows):
            for c in [0, 1, 8, 9]:
                if items[c][r] == None:
                    items[c][r] = self.mkElem("Ground")
            for c in range(2, 8):
                if items[c][r] == None:
                    items[c][r] = self.mkElem("Water")
        return items

    def win(self, win=True):
        """
            Display a winning or a loosing message
            
            Parameter
            ----------
            win : (default value=True) (type=boolean) True to display a winning message, False otherwise
            
        """
        if win == True:
            file = open(translation[self.__language]["Win"], "rb")
            image = file.read()
            self.__message.format = "jpg"
        else:
            file = open(translation[self.__language]["Lost"], "rb")
            image = file.read()
            self.__message.format = "png"
        self.__message.value = image

    def board(self, name):
        """
            Board the element name
            
            Parameter
            ----------
            name : (type=string) the element to board
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c1=mkImageWidget('images/ground.jpg','jpg')
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c3=mkImageWidget('images/water.jpg','jpg')
            >>> c4=mkImageWidget('images/goat.jpg','jpg')
            >>> c5=mkImageWidget('images/cabbage.jpg','jpg')
            >>> c6=mkImageWidget('images/wolf.png','png')
            >>> grid.board('Goat')
            >>> grid.map[1][1].value==c1.value
            True
            >>> grid.map[2][2].value==c4.value
            True
            >>> grid.field.leftCoast.goat
            False
            >>> grid.field.boat.first
            'Goat'
            
        """
        assert isinstance(name, str), "name has to be a string"
        done, coast, side = self.__field.board(name)
        if side:  
            boat_side = "First"
        else:
            boat_side = "Second"
        if done:  
            if coast: 
                coast_side = "Left"
                loc = self.__lCoastLoc[name]
            else:
                coast_side = "Right"
                loc = self.__rCoastLoc[name]
            im_info = self.__data["Ground"]
            loc2 = self.__boatLocation[coast_side][boat_side]
            im_info2 = self.__data[name]

    def unboard(self, name):
        """
            Unboard the element name
            
            Parameter
            ----------
            name : (type=string) the element to unboard
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c6=mkImageWidget('images/wolf.png','png')
            >>> grid.board('Wolf')
            >>> grid.cross()
            >>> grid.unboard('Wolf')
            >>> grid.map[8][2].value==c6.value
            True
            >>> grid.map[6][2].value==c2.value
            True
            
        """
        assert isinstance(name, str), "name has to be a string"
        done, coast, side, win = self.__field.unboard(name)
        if side:  
            boat_side = "First"
        else:
            boat_side = "Second"
        if done:  
            if coast:  
                coast_side = "Left"
                loc = self.__lCoastLoc[name]
            else:
                coast_side = "Right"
                loc = self.__rCoastLoc[name]
            loc2 = self.__boatLocation[coast_side][boat_side]
            im_info2 = self.__data["Wood"]
            im_info = self.__data[name]

        if win == True:
            self.win()

    def cross(self):
        """
            Make the boat cross the river
            
            Tests
            -----------
            >>> grid=Grid()
            >>> c2=mkImageWidget('images/wood.jpg','jpg')
            >>> c3=mkImageWidget('images/water.jpg','jpg')
            >>> grid.cross()
            >>> grid.map[2][2].value==c3.value
            True
            >>> grid.map[3][2].value==c3.value
            True
            >>> grid.map[6][2].value==c2.value
            True
            >>> grid.map[7][2].value==c2.value
            True
            >>> grid.field.boat.side
            False
            
        """
        self.__lost = self.__field.cross()
        if self.__lost == True:
            self.win(False)
        if self.__field.boat.first != None:
            case1 = self.__data[self.__field.boat.first]
        else:
            case1 = self.__data["Wood"]
        if self.__field.boat.second != None:
            case2 = self.__data[self.__field.boat.second]
        else:
            case2 = self.__data["Wood"]
        replace = self.__data["Water"]
        if self.__field.boat.side:  
            for j in range(0, 4):
                i = 7 - j
                self.update_image(i, 2, replace[0], replace[1])
                self.update_image(i - 1, 2, case2[0], case2[1])
                self.update_image(i - 2, 2, case1[0], case1[1])
                time.sleep(0.2)
        else:  
            for i in range(2, 6):
                self.update_image(i, 2, replace[0], replace[1])
                self.update_image(i + 1, 2, case1[0], case1[1])
                self.update_image(i + 2, 2, case2[0], case2[1])
                time.sleep(0.2)
