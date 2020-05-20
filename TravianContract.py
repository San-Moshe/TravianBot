from enum import Enum


class TroopType(Enum):
    INFANTRY = "INFANTRY",
    CAVALRY = "CAVALRY"


class TribeInterface:
    def get_training_id_by_name(self, troops_name) -> str:
        pass

    def get_troops_for_custom_farm_list(self, troops_name) -> str:
        pass

    def get_troops_for_farm_list(self, troops_name) -> str:
        pass

    def get_troops_select_for_farm_list(self, troops_name) -> str:
        pass

    def get_troops_by_type(self, troops_type):
        pass

    def get_troops(self) -> str:
        pass


class Troop:
    def __init__(self, name, training_id, raid_id, farm_list_id, farm_list_selection_id, troop_type):
        self.name = name
        self.training_id = training_id
        self.raid_id = raid_id
        self.farm_list_id = farm_list_id
        self.farm_list_selection_id = farm_list_selection_id
        self.troop_type = troop_type


class TeutonsTribe(TribeInterface):
    display_name = "Teutons"
    troops = {"Clubswinger": Troop("Clubswinger", "_tf11", "t1", "unit1", "u1", TroopType.INFANTRY),
              "Spearman": Troop("Spearman", "_tf12", "t2", "unit2", "u2", TroopType.INFANTRY),
              "Axeman": Troop("Axeman", "_tf13", "t3", "unit3", "u3", TroopType.INFANTRY),
              "Scout": Troop("Scout", "_tf14", "t4", "", "", TroopType.INFANTRY),
              "Paladin": Troop("Paladin", "_tf15", "t5", "unit5", "u5", TroopType.CAVALRY),
              "Teutonic Knight": Troop("Teutonic Knight", "_tf16", "t6", "unit6", "u6", TroopType.CAVALRY)}

    def get_training_id_by_name(self, troops_name) -> str:
        return self.troops[troops_name].training_id

    def get_troops_for_custom_farm_list(self, troops_name) -> str:
        return self.troops[troops_name].raid_id

    def get_troops_for_farm_list(self, troops_name) -> str:
        return self.troops[troops_name].farm_list_id

    def get_troops_select_for_farm_list(self, troops_name) -> str:
        return self.troops[troops_name].farm_list_selection_id

    def get_troops_by_type(self, troops_type):
        return [troop.name for troop in self.troops.values() if troop.troop_type == troops_type]

    def get_troops(self):
        return tuple(map(lambda troop: troop.name, self.troops.values()))


def create_tribe_for_name(tribe_name) -> TribeInterface:
    if tribe_name == Tribe.TEUTONS:
        return TeutonsTribe()


class TroopsStableContract:
    CLUBSWINGER = "_tf11"
    SPEARMAN = "_tf12"


class BuildingsContract:
    STABLE = "Stable"
    BARRACKS = "Barracks"


class TroopsRaidType(Enum):
    INFANTRY_ATTACKER = 1
    STABLE_ATTACKER = 2
    INFANTRY_DEFENDER = 3
    STABLE_DEFENDER = 4


class TroopsType(Enum):
    ATTACKER = 1
    DEFENDER = 2


class Tribe(Enum):
    TEUTONS = "Teutons"
    ROMANS = "Romans"
    GAULS = "Gauls"


# TODO use more OOP so farm will hold it's link, type, etc...
class FarmType(Enum):
    OASIS = 1
    NORMAL_FARM = 2


class FarmRaidLink(Enum):
    OASIS = "» Raid unoccupied oasis"
    NORMAL_FARM = "» Send troops"


class TroopsFarmListContract:
    teutons = {TroopsRaidType.INFANTRY_ATTACKER: "unit1", TroopsRaidType.STABLE_ATTACKER: "unit6",
               TroopsRaidType.INFANTRY_DEFENDER: "unit2", TroopsRaidType.STABLE_DEFENDER: "unit5"}
    romans = {TroopsRaidType.INFANTRY_ATTACKER: "unit1", TroopsRaidType.STABLE_ATTACKER: "unit6",
              TroopsRaidType.INFANTRY_DEFENDER: "unit2", TroopsRaidType.STABLE_DEFENDER: "unit5"}
    gauls = {TroopsRaidType.INFANTRY_ATTACKER: "unit1", TroopsRaidType.STABLE_ATTACKER: "unit6",
             TroopsRaidType.INFANTRY_DEFENDER: "unit2", TroopsRaidType.STABLE_DEFENDER: "unit5"}

    all = {TroopsRaidType.INFANTRY_ATTACKER: "u1", TroopsRaidType.STABLE_ATTACKER: "u6",
           TroopsRaidType.INFANTRY_DEFENDER: "u2", TroopsRaidType.STABLE_DEFENDER: "u5"}

    def get_troops_by_tribe(self, tribe, troops_raid_type):
        if tribe == Tribe.TEUTONS:
            return self.teutons[troops_raid_type]
        elif tribe == Tribe.GAULS:
            return self.gauls[troops_raid_type]
        elif tribe == Tribe.ROMANS:
            return self.romans[troops_raid_type]

    def get_troops_select_by_type(self, troops_raid_type):
        return self.all[troops_raid_type]


class TroopsCustomFarmListContract:
    teutons = {TroopsRaidType.INFANTRY_ATTACKER: "t1", TroopsRaidType.STABLE_ATTACKER: "t6",
               TroopsRaidType.INFANTRY_DEFENDER: "t2", TroopsRaidType.STABLE_DEFENDER: "t5"}
    romans = {TroopsRaidType.INFANTRY_ATTACKER: "unit1", TroopsRaidType.STABLE_ATTACKER: "unit6",
              TroopsRaidType.INFANTRY_DEFENDER: "unit2", TroopsRaidType.STABLE_DEFENDER: "unit5"}
    gauls = {TroopsRaidType.INFANTRY_ATTACKER: "unit1", TroopsRaidType.STABLE_ATTACKER: "unit6",
             TroopsRaidType.INFANTRY_DEFENDER: "unit2", TroopsRaidType.STABLE_DEFENDER: "unit5"}

    def get_troops_by_tribe(self, tribe, troops_raid_type):
        if tribe == Tribe.TEUTONS:
            return self.teutons[troops_raid_type]
        elif tribe == Tribe.GAULS:
            return self.gauls[troops_raid_type]
        elif tribe == Tribe.ROMANS:
            return self.romans[troops_raid_type]
