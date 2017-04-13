#-*- coding:cp949 -*-
from werewolf.database.DATABASE import DATABASE
from werewolf.game.GAME_STATE import GAME_STATE
from werewolf.game.entry.Entry import Truecharacter
from werewolf.game.entry.Entry import Race
import logging
import random
import copy

class Rule:
    def __init__(self, game):
        self.game = game

class WerewolfRule(Rule):
    def nextTurn(self):
        if self.game.state== GAME_STATE.READY:
            if(self.min_players <= self.game.players and self.game.players <= self.max_players):
                logging.info("���� �ʱ�ȭ ����")
                self.initGame()
            else:
                self.game.deleteGame()
        elif self.game.state==GAME_STATE.PLAYING:
            if(self.game.day == 1):
                self.nexeTurn_2day()
            else:
                self.nextTurn_Xday()
            
    def initGame(self):
        #�÷����غ� ���
        expertPlayers = self.game.entry.getExpertPlayers()
        #print "expertPlayers",expertPlayers

        #�ʺ���
        novicePlayers = self.game.entry.getNovicePlayers()
        #print "novicePlayers",novicePlayers

        truecharacterList = copy.copy(self.temp_truecharacter[len(novicePlayers) + len(expertPlayers) + 1])
        logging.info("players: %d", len(novicePlayers) + len(expertPlayers) + 1)

        #���� ��� ��ġ
        random.shuffle(novicePlayers)
        logging.debug("noviceEntry: %s", novicePlayers)
        while novicePlayers:
            try:
                truecharacterList.remove(Truecharacter.HUMAN)
            except ValueError:
                logging.debug("�ʺ��� �Ҵ�: ���� ������� ���� %d��", len(truecharacterList))
                break
            player = novicePlayers.pop()
            logging.debug("player: %d with job %d", player.id, Truecharacter.HUMAN)
            player.setTruecharacter(Truecharacter.HUMAN)

        restPlayers = expertPlayers + novicePlayers
        random.shuffle(restPlayers)
        logging.debug("restEntry: %s", restPlayers)
        logging.debug("restJob: %s", truecharacterList)
        while restPlayers:
            player = restPlayers.pop()
            job = truecharacterList.pop()
            logging.debug("player: %d with job %d", player.id, job)
            player.setTruecharacter(job)
        if not truecharacterList:
            logging.error("Some roles are NOT assigned: %s", truecharacterList)

        #2. ������� �ڸ�Ʈ
        victim = self.game.entry.getVictim()
        logging.debug("victim: %s", victim)
        victim.writeWill()

        #3. ���� ���� ������Ʈ
        self.game.setGameState("state", GAME_STATE.PLAYING)
        self.game.setGameState("day", self.game.day+1)

        #���� ������..
        cursor = self.game.db.cursor
        query = "update `zetyx_board_werewolf` set `%s` = '%s'  where no = '%s'"
        query %= ("is_secret", 0, self.game.game)
        logging.debug(query)
        cursor.execute(query)

        #4. �ڸ�Ʈ �ʱ�ȭ
        self.game.entry.initComment()

    def decideByMajority(self):
        cursor = self.game.db.cursor

        logging.info("��ǥ!")
        alivePlayers = self.game.entry.getAliveEntry()

        #��� �ִ� ����� 1�� �ʰ��� ��쿡�� ��ǥ�� �����Ѵ�.
        if len(alivePlayers) < 2:
            return
        #��� ������� ��ǥ�� �����ߴ��� Ȯ���Ѵ�.
        for alivePlayer in alivePlayers:
            #��ǥ�� ���ߴٸ�! ���� ��ǥ ����
            if not alivePlayer.hasVoted():
                alivePlayer.voteRandom(alivePlayers)

        #���� ǥ�� ���� ���� ����� ã�´�.
        query = '''select `candidacy`, count(*) as count from `zetyx_board_werewolf_vote` 
        where game = '%s' and day ='%s' 
        group by `candidacy` 
        order by `count`  DESC '''
        query %= (self.game.game, self.game.day)
        logging.debug(query)

        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug(result)
        #print result

        count = 0
        candidacy_list = []

        for temp in result:
            if count <= temp['count']:
                count = temp['count']
                logging.debug("count: %s", count)
            else:
                break
            candidacy_list.append(temp['candidacy'])
        candidacy = random.choice(cadidacy_list)
        return self.game.entry.getCharacter(candidacy)

    def decideByWerewolf(self):
        cursor = self.game.db.cursor

        logging.info("����!!")
        #������ ������...
        humanRace = self.game.entry.getEntryByRace(Race.HUMAN)
        logging.debug("%s", alivePlayers)

        #������!
        werewolfPlayers = self.game.entry.getPlayersByTruecharacter(Truecharacter.WEREWOLF, "('����')")
        logging.debug("%s", werewolfPlayers)

        #��� �ִ� �ζ��� ���� ���� ������ �����Ѵ�.
        if not werewolfPlayers:
            return

        #�ζ����� ������ �����ߴ��� Ȯ���Ѵ�.
        for werewolfPlayer in werewolfPlayers:
            #������ ���ߴٸ�! ���� ���� ����
            if not werewolfPlayer.hasAssault():
                werewolfPlayer.assaultRandom(humanRace)


        #�ζ����� ���� �����ϴ� ����� ã�´�.
        query = '''select `injured`, count(*) as count from `zetyx_board_werewolf_deathNote` 
        where game = '%s' and day ='%s' 
        group by `injured` 
        order by `count`  DESC '''
        query %= (self.game.game, self.game.day)
        logging.debug(query)

        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug(result)

        count = 0
        injured_list = []

        for temp in result:
            if count <= temp['count']:
                count = temp['count']
                logging.debug("count: %s", count)
            else:
                break
            injured_list.append(temp['injured'])
        injured = random.choice(injured_list)
        logging.debug("injured: %s in %s", injured, injured_list)
        return self.game.entry.getCharacter(injured)
