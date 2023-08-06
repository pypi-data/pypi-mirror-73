from .Jugs import Jugs
from valueplayerwidget import ValuePlayerWidget

class JugsPlayer(ValuePlayerWidget):
    def __init__(self, UI=None, capacity1=None, capacity2=None, language='en_EN'):
        if capacity1==None or capacity2==None:
            self.__game=Jugs(lang=language)
        else:
            self.__game=Jugs(capacity1=capacity1, capacity2=capacity2, lang=language)
        category_l = self.__game.translate("left_jug")
        category_r = self.__game.translate("right_jug")
        pl = self.__game.translate("pour")  + " " + self.__game.translate("left")
        pr = self.__game.translate("pour")  + " " + self.__game.translate("right")
        el = self.__game.translate("empty") + " " + self.__game.translate("left")
        er = self.__game.translate("empty") + " " + self.__game.translate("right")
        fl = self.__game.translate("fill")  + " " + self.__game.translate("left")
        fr = self.__game.translate("fill")  + " " + self.__game.translate("right")
        actions={
            category_l: [(fl, self.fill, 0), (pl, self.pour, 0), (el, self.empty, 0)],
            category_r: [(fr, self.fill, 1), (pr, self.pour, 1), (er, self.empty, 1)],
        }
        ValuePlayerWidget.__init__(self, visualisation=self.__game, UI=UI, actions=actions)
    
    def setAll(self,value,action):
        self.player.set_value(value)
        self.player.set_action(action)
    
    def fill(self,num):
        self.__game.fill(num)
        self.setAll(self.__game.mk_value(),"fill("+str(num)+")")
    
    def pour(self,num):
        self.__game.pour(num)
        self.setAll(self.__game.mk_value(),"pour("+str(num)+")")
    
    def empty(self,num):
        self.__game.empty(num)
        self.setAll(self.__game.mk_value(),"empty("+str(num)+")")
    
    def set_volumes(self, capacity1, capacity2):
        self.__game.set_volumes(capacity1, capacity2)
        self.player.reset(self.__game.value)
    
    def obtained(self):
        return self.__game.obtained