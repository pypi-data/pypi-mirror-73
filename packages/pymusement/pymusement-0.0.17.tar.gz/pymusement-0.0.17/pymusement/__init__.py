from pymusement.parks.disney.MagicKingdom import MagicKingdom
from pymusement.parks.disney.Epcot import Epcot
from pymusement.parks.disney.HollywoodStudios import HollywoodStudios
from pymusement.parks.disney.AnimalKingdom import AnimalKingdom
from pymusement.parks.disney.Disneyland import Disneyland
from pymusement.parks.disney.CaliforniaAdventure import CaliforniaAdventure
from pymusement.parks.disney.DisneylandParis import DisneylandParis
from pymusement.parks.universal.UniversalStudiosFlorida import UniversalStudiosFlorida
from pymusement.parks.universal.IslandsOfAdventure import IslandsOfAdventure
from pymusement.parks.universal.UniversalHollywood import UniversalHollywood
from pymusement.parks.universal.UniversalVolcano import UniversalVolcano
from pymusement.parks.universal.UniversalJapan import UniversalJapan
from pymusement.parks.seaworld.SeaworldOrlando import SeaworldOrlando
from pymusement.parks.seaworld.BuschGardensTampa import BuschGardensTampa
from pymusement.parks.seaworld.SeaworldSanAntonio import SeaworldSanAntonio
from pymusement.parks.seaworld.SeaworldSanDiego import SeaworldSanDiego
from pymusement.parks.seaworld.BuschGardensWilliamsburg import BuschGardensWilliamsburg
from pymusement.parks.HersheyPark import HersheyPark


PARKS = {
    'magic-kingdom' : MagicKingdom(),
    'epcot' : Epcot(),
    'hollywood-studios' : HollywoodStudios(),
    'animal-kingdom' : AnimalKingdom(),
    'disneyland' : Disneyland(),
    'ca-adventure' : CaliforniaAdventure(),
    'disney-paris' : DisneylandParis(),
    'universal-florida' : UniversalStudiosFlorida(),
    'islands-adventure' : IslandsOfAdventure(),
    'universal-hollywood' : UniversalHollywood(),
    'volcano-bay' : UniversalVolcano(),
    'universal-japan' : UniversalJapan(),
    'seaworld-orlando' : SeaworldOrlando(),
    'busch-gardens-tampa' : BuschGardensTampa(),
    'seaworld-san-antonio' : SeaworldSanAntonio(),
    'seaworld-san-diego' : SeaworldSanDiego(),
    'busch-gardens-williamsburg' : BuschGardensWilliamsburg(),
    'hersheypark' : HersheyPark()
}
