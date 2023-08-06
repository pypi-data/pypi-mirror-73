from .Game import Game
from valueplayerwidget import ValuePlayerWidget

class WGCPlayer(ValuePlayerWidget):
    def __init__(self, UI=None, language='en_EN'):
        self.__game=Game(language=language)
        category_g = self.__game.translate("Goat")
        category_w = self.__game.translate("Wolf")
        category_c = self.__game.translate('Cabbage')
        category_a = self.__game.translate('actions')
        bg  = self.__game.translate('Board')   + ' ' + self.__game.translate('Goat')
        ug  = self.__game.translate('Unboard') + ' ' + self.__game.translate('Goat')
        bw  = self.__game.translate('Board')   + ' ' + self.__game.translate('Wolf')
        uw  = self.__game.translate('Unboard') + ' ' + self.__game.translate('Wolf')
        bc  = self.__game.translate('Board')   + ' ' + self.__game.translate('Cabbage')
        uc  = self.__game.translate('Unboard') + ' ' + self.__game.translate('Cabbage')
        cross = self.__game.translate('Cross')
        reset = self.__game.translate('Reset')
        actions={
            category_g : [(bg,self.board,'Goat'), (ug,self.unboard,'Goat')],
            category_w : [(bw,self.board,'Wolf'), (uw,self.unboard,'Wolf')],
            category_c : [(bc,self.board,'Cabbage'), (uc,self.unboard,'Cabbage')],
            category_a : [(cross,self.cross), (reset,self.reset)]
        }
        ValuePlayerWidget.__init__(self, visualisation=self.__game, UI=UI, actions=actions)
    
    @property
    def game(self): return self.__game
    
    def setAll(self,value,action):
        self.player.set_value(value)
        self.player.set_action(action)
    
    def board(self, name):
        self.__game.board(name)
        self.setAll(self.__game.mk_value(),"Board("+self.__game.translate(name)+')')
        
    def unboard(self, name):
        self.__game.unboard(name)
        self.setAll(self.__game.mk_value(),"Unboard("+self.__game.translate(name)+')')
    
    def cross(self):
        self.__game.cross()
        self.setAll(self.__game.mk_value(),"Cross()")
    
    def reset(self):
        self.__game.reset()
        self.player.reset(self.__game.value)