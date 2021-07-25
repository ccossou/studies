

class Rhum(object):

    def __init__(self, prix, vol, name):
        self.prix = prix  # Price / liter
        self.vol = vol / 100.  # Alcool content (50 % vol = 0.5)
        self.name = name

    def alcool_price(self):
        msg = "{}: {}".format(self.name, self.prix / self.vol)

        print(msg)

damoiseau_50 = Rhum(6.95, 50, name="Damoiseau 50") # Bouteille 6.95, Cubi 8.13
damoiseau_40 = Rhum(7.12, 40, name="Damoiseau 40")  # Bouteille
damoiseau_55 = Rhum(9.26, 55, name="Damoiseau 55")  # Bouteille

longueteau_50 = Rhum(6.68, 50, name="longueteau_50")

rhums = [damoiseau_40, damoiseau_50, damoiseau_55, longueteau_50]

for rhum in rhums:
    rhum.alcool_price()