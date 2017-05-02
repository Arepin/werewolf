#-*- coding:cp949 -*-
import logging
import random
import copy
from werewolf.game.GAME_STATE import GAME_STATE
from werewolf.game.entry.Role import Truecharacter
from werewolf.game.entry.Role import Race
from werewolf.game.rule.Rule import WerewolfRule

class BasicRule(WerewolfRule):
    min_players = 9
    max_players = 16

    # �⺻ ����
    temp_truecharacter = {}
    temp_truecharacter[9] = [1, 1, 1, 2, 3, 6, 5, 7, 7]
    temp_truecharacter[10] = [1, 1, 1, 1, 2, 3, 6, 5, 7, 7]
    temp_truecharacter[11] = [1, 1, 1, 1, 2, 3, 4, 5, 5, 6]
    temp_truecharacter[12] = [1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 6]
    temp_truecharacter[13] = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 6]
    temp_truecharacter[14] = [1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 6]
    temp_truecharacter[15] = [1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 5, 6]
    temp_truecharacter[16] = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7, 7]

    def __init__(self, game):
        WerewolfRule.__init__(self, game)
        logging.debug("basicRule")

    def initGame(self):
        logging.info("init Basic Rule")
        WerewolfRule.initGame(self)

    def nextTurn_2day(self):
        logging.info("2��°�� ���!")

        #�Ϲ� �α׸� ���� ���� ����� üũ�Ѵ�.
        self.game.entry.checkNoCommentPlayer()

        #����� NPC ����
        victim = self.game.entry.getVictim()
        victim.toDeathByWerewolf()

        #������ ��Ŵ
        noMannerPlayers = self.game.entry.getNoMannerPlayers()
        for noMannerPlayer in noMannerPlayers:
            noMannerPlayer.toDeath("���� ")

        #�ڸ��� �ʱ�ȭ
        self.game.entry.initComment()

        #3. ���� ���� ������Ʈ
        self.game.setGameState("state", "������")
        self.game.setGameState("day", self.game.day+1)

    def nextTurn_Xday(self):
        logging.info("�������� ���!")
        #�Ϲ� �α׸� ���� ���� ����� üũ�Ѵ�.
        self.game.entry.checkNoCommentPlayer()

        #��ǥ -��� �ִ� �����ڰ� ��ǥ�� �ߴ��� üũ, ���ߴٸ� ���� ��ǥ
        victim = self.decideByMajority()
        if victim:
            victim.toDeath("����")

        #������ ��Ŵ
        noMannerPlayers = self.game.entry.getNoMannerPlayers()
        for noMannerPlayer in noMannerPlayers:
            noMannerPlayer.toDeath("���� ")

        #�ڸ��� �ʱ�ȭ
        self.game.entry.initComment()

        #����!
        assaultVictim = self.decideByWerewolf()
        if assaultVictim:
            logging.info("assaultVictim: %s", assaultVictim)
            self.assaultByWerewolf(assaultVictim, victim)
            
        #���� ���� Ȯ��
        #���!
        humanRace = self.game.entry.getEntryByRace(Race.HUMAN)
        #for human in humanRace :
        #    print human
        
        #������!
        werewolfRace = self.game.entry.getEntryByRace(Race.WEREWOLF)
        #for werewolf in werewolfRace :
        #    print werewolf
        
        if (len(humanRace) <= len(werewolfRace)) or not humanRace:
            logging.info("�ζ� �¸�")
            self.game.setGameState("win", "1")
            if self.game.termOfDay == 60:
                self.game.setGameState("state", GAME_STATE.TESTOVER)
            else:
                self.game.setGameState("state", GAME_STATE.GAMEOVER)

        elif not werewolfRace:
            logging.info("�ΰ� �¸�")
            self.game.setGameState("win", "0")
            if self.game.termOfDay == 60:
                self.game.setGameState("state", GAME_STATE.TESTOVER)
            else:
                self.game.setGameState("state", GAME_STATE.GAMEOVER)
        else:
            logging.info("��� ����")
            #self.game.setGameState("state","������")

        self.game.setGameState("day", self.game.day+1)

    def assaultByWerewolf(self, assaultVictim, victim):
        self.game.entry.recordAssaultResult(assaultVictim)

        guard = None
        hunterPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.BODYGUARD)[0]

        if hunterPlayer.alive == "����":
            logging.debug("hunterPlayer: %s", hunterPlayer)
            guard = hunterPlayer.guard()
            if guard is not None:
                guard = self.game.entry.getCharacter(guard['purpose'])
                logging.debug("guard: %s", guard)

        if assaultVictim.id == victim.id:
            logging.debug("���� ����: �����")
        elif guard and assaultVictim.id == guard.id:
            logging.debug("���� ����: ����")
        else:
            logging.debug("���� ����: %s", assaultVictim)
            assaultVictim.toDeath("����")
