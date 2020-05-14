import time

from TravianActions import TravianActions
from TravianContract import Tribe, FarmType, TroopsRaidType


class Controller:
    def __init__(self):
        self.travian_actions = TravianActions()
        self.tribe = None

    def auto_mode(self, farm_type, number_of_troops, is_batch, is_barracks, is_stable, troops_training_type,
                  troops_raiding_type):
        counter = 0
        while True:
            start_time = time.time()
            while time.time() - start_time < 30:
                if farm_type == FarmType.OASIS:
                    self.travian_actions.raid_next_farm_in_custom_farm_list(number_of_troops,
                                                                            TroopsRaidType(troops_raiding_type),
                                                                            self.tribe)
                else:
                    self.travian_actions.raid_next_farm_from_farm_list(number_of_troops,
                                                                       TroopsRaidType(troops_raiding_type), self.tribe)
            if is_batch:
                self.travian_actions.raid_batch_farm_list()

            if is_barracks and counter % 2 == 0:
                self.travian_actions.train_soldiers_in_barracks(troops_training_type)
            elif is_stable and counter % 2 == 1:
                self.travian_actions.train_soldiers_in_stable(troops_training_type)

            counter += 1

    def login(self, username_text, password_text):
        self.tribe = Tribe(self.travian_actions.login(username_text, password_text))

    def add_oasis_to_custom_farm_list(self):
        self.travian_actions.add_oasis_to_custom_farm_list()

    def add_farm_account_to_farm_list(self, troops_raid_type, number_of_soldiers):
        self.travian_actions.add_farm_account_to_farm_list(self.tribe, TroopsRaidType(troops_raid_type),
                                                           number_of_soldiers)

    def raid_farms(self, farm_type, troops_type, number_of_troops):
        if FarmType(farm_type) == FarmType.NORMAL_FARM:
            self.travian_actions.raid_farms_from_farm_list(number_of_troops, TroopsRaidType(troops_type), self.tribe)
        else:
            self.travian_actions.raid_custom_farm_list(number_of_troops, TroopsRaidType(troops_type), self.tribe)
