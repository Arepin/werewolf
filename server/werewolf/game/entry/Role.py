#-*- coding:cp949 -*-
import time
import random
import logging
from werewolf.database.DATABASE     import DATABASE
from werewolf.game.entry.Character  import *

class Race:
    HUMAN = 0
    WEREWOLF = 1

class Truecharacter:
    PLAYER = 0
    HUMAN = 1
    SEER = 2
    MEDIUM = 3
    POSSESSED = 4
    WEREWOLF = 5
    BODYGUARD = 6
    FREEMASONS = 7
    WEREHAMSTER = 8
    LONELYWEREWOLF = 9
    READERWEREWOLF = 10
    REVENGER = 11
    NOBILITY = 12
    CHIEF = 13
    DIABLO = 14
    SHERIFF = 15
    SEER_ODD = 16
    WEREWOLF_CON = 17

class Human(Player):
    pass

class Seer(Player):
    def openEye(self):
        cursor = self.game.db.cursor
        query = "select * from `zetyx_board_werewolf_revelation`  where `game` = '%s' and `day` ='%s' and type = '��'; "
        query %= (self.game.game, self.game.day)
        logging.debug(query)
        cursor.execute(query)
        return cursor.fetchone()

class Medium(Player):
    pass

class Possessed(Player):
    pass

class Werewolf(Player):
    def toDeath(self, deathType):
        # ��ǥ���� ���, ���� ���� ����
        if deathType == "����" and self.hasAssault():
            cursor = self.game.db.cursor
            query = "delete from `zetyx_board_werewolf_deathNote` where game = '%s' and day = '%s' and `werewolf` = '%s'"
            query %= (self.game.game, self.game.day, self.character)
            logging.debug(query)
            cursor.execute(query)
        Player.toDeath(self, deathType)

    def hasAssault(self):
        cursor = self.game.db.cursor
        query = "select * from `zetyx_board_werewolf_deathNote` where game = '%s' and day ='%s' and `werewolf`='%s'"
        query %= (self.game.game, self.game.day, self.character)
        logging.debug(query)
        cursor.execute(query)
        result = cursor.fetchone()
        return result is not None

    def assaultRandom(self, targetPlayers):
        cursor = self.game.db.cursor
        while True:
            targetPlayer = random.choice(targetPlayers)
            if targetPlayer.character == self.character:
                logging.debug("random assault choose oneself: %s -> %s", self, targetPlayer)
            else:
                break
        logging.debug("random assault: %s -> %s", self, targetPlayer)
        query = "INSERT INTO `zetyx_board_werewolf_deathNote`(`game`,`day`,`werewolf`,`injured`) VALUES ('%s', '%s','%s' ,'%s');"
        query %= (self.game.game, self.game.day, self.character, targetPlayer.character)
        logging.debug(query)
        cursor.execute(query)

class Bodyguard(Player):
    def guard(self):
        cursor = self.game.db.cursor
        query = "select * from `zetyx_board_werewolf_guard`  where `game` = '%s' and `hunter` = '%s' and `day` ='%s'; "
        query %= (self.game.game, self.character, self.game.day)
        logging.debug(query)
        cursor.execute(query)
        return cursor.fetchone()

class Freemasons(Player):
    pass

class Werehamster(Player):
    pass

class Loneywerewolf(Werewolf):
    def hasAssault(self):
        cursor = self.game.db.cursor
        query = "select * from `zetyx_board_werewolf_deathnotehalf` where game = '%s' and day ='%s' and `werewolf`='%s'"
        query %= (self.game.game, self.game.day, self.character)
        logging.debug(query)
        cursor.execute(query)
        result = cursor.fetchone()
        return result is not None

    def assaultRandom(self,targetPlayers):
        cursor = self.game.db.cursor
        while True:
            targetPlayer = random.choice(targetPlayers)
            if targetPlayer.character == self.character:
                logging.debug("random assault choose oneself: %s -> %s", self, targetPlayer)
            else:
                break
        logging.debug("random assault: %s -> %s", self, targetPlayer)
        query = "INSERT INTO `zetyx_board_werewolf_deathnotehalf`(`game`,`day`,`werewolf`,`injured`) VALUES ('%s', '%s','%s' ,'%s');"
        query %= (self.game.game, self.game.day, self.character, targetPlayer.character)
        logging.debug(query)
        cursor.execute(query)

class Readerwerewolf(Werewolf):
    pass

class Revenger(Player):
    def toDeath(self, deathType):
        if deathType == "����":
            self.revenge()
        Player.toDeath(self, deathType)

    def revenge(self):
        cursor = self.game.db.cursor
        query = "select * from `zetyx_board_werewolf_revenge`  where `game` = '%s'; "
        query %= (self.game.game)
        logging.debug(query)
        cursor.execute(query)
        target = cursor.fetchone()

        if target is not None:
            target = self.game.entry.getCharacter(target['target'])
            logging.debug("revenge target: %s", target)
            if target.alive == "����":
                guard = None
                hunterPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.BODYGUARD)[0]

                if hunterPlayer.alive == "����":
                    logging.debug("hunterPlayer: %s", hunterPlayer)
                    guard = hunterPlayer.guard()
                    if guard is not None:
                        guard = self.game.entry.getCharacter(guard['purpose'])
                        logging.debug("guard: %s", guard)

                if guard and target.id == guard.id:
                    logging.debug("���� ����: ����")
                else:
                    logging.debug("���� ����")
                    target.toDeath("����")
        else:
            logging.debug("revenge target: None")

class Nobility(Player):
    def toDeath(self, deathType):
        if deathType <> "����":
            Player.toDeath(self, deathType)
        logging.debug("nobility is voted.")

class Chief(Player):
    pass

class Diablo(Player):
    def toDeath(self, deathType):
        if deathType <> "����":
            Player.toDeath(self, deathType)

    def awaken(self):
        cursor = self.game.db.cursor
        query = "select * from `zetyx_board_werewolf_deathNote_result`  where `game` = '%s' and `injured` = '%s' ; "
        query %= (self.game.game, self.character)
        logging.debug(query)
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result['injured'] == self.character:
            return True
        else:
            return False

class Sheriff(Player):
    def voteRandom(self, targetPlayers):
        cursor = self.game.db.cursor
        while True:
            targetPlayer = random.choice(targetPlayers)
            if targetPlayer.character == self.character:
                logging.debug("random vote choose oneself: %s -> %s", self, targetPlayer)
            else:
                break
        logging.debug("random vote: %s -> %s", self, targetPlayer)
        query = "INSERT INTO `zetyx_board_werewolf_vote` ( `game`,`day`,`voter`,`candidacy`) VALUES ('%s', '%s','%s' ,'%s');"
        query %= (self.game.game, self.game.day, self.character, targetPlayer.character)
        logging.debug(query)
        cursor.execute(query)
        cursor.execute(query)

class SeerOdd(Player):
    pass

class WerewolfCon(Player):
    pass