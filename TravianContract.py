from enum import Enum


class TroopsBarracksContract:
    CLUBSWINGER = "_tf11"
    SPEARMAN = "_tf12"


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

    def get_troops_by_tribe(self, tribe, troops_raid_type):
        if tribe == Tribe.TEUTONS:
            return self.teutons[troops_raid_type]
        elif tribe == Tribe.GAULS:
            return self.gauls[troops_raid_type]
        elif tribe == Tribe.ROMANS:
            return self.romans[troops_raid_type]


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
