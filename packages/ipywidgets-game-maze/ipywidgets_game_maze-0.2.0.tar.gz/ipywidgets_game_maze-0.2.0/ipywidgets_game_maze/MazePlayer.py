from .Maze import Maze
from valueplayerwidget import ValuePlayerWidget

class MazePlayer(ValuePlayerWidget):
    def __init__(self, UI=None, maze='lab/lab.json', language='en_EN'):
        self.__game=Maze(file=maze, language=language)
        category1 = self.__game.translate("turn")
        category2 = self.__game.translate("else")
        l  = self.__game.translate('left')
        r  = self.__game.translate('right')
        u  = self.__game.translate('up')
        d  = self.__game.translate('down')
        h  = self.__game.translate('horizontal')
        m  = self.__game.translate('move')
        lo = self.__game.translate('look')
        re = self.__game.translate('reset')
        actions={
            category1: [(l,self.left), (r,self.right), (u,self.up), (d,self.down), (h,self.horizontal)],
            category2: [(m,self.move), (lo,self.look), (re,self.reset)],
        }
        ValuePlayerWidget.__init__(self, visualisation=self.__game, UI=UI, actions=actions)
    
    def setAll(self,value,action):
        self.player.set_value(value)
        self.player.set_action(action)
    
    def left(self):
        self.__game.left()
        self.setAll(self.__game.mk_value(),"Left()")
        
    def right(self):
        self.__game.right()
        self.setAll(self.__game.mk_value(),"Right()")
    
    def up(self):
        self.__game.up()
        self.setAll(self.__game.mk_value(),"Up()")
    
    def down(self):
        self.__game.down()
        self.setAll(self.__game.mk_value(),"Down()")
        
    def horizontal(self):
        self.__game.horizontal()
        self.setAll(self.__game.mk_value(),"Horizontal()")
    
    def move(self):
        self.__game.move()
        self.setAll(self.__game.mk_value(),"Move()")
    
    def reset(self):
        self.__game.reset()
        self.player.reset(self.__game.value)
    
    def look(self):
        return self.__game.look()