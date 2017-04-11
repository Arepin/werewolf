#-*- coding:cp949 -*-
from werewolf.database.DATABASE import DATABASE
from werewolf.game.GAME_STATE import GAME_STATE
from werewolf.game.entry.Entry import Truecharacter
from werewolf.game.entry.Entry import Race
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
                logging("count: %s", count)
            else:
                break
            injured_list.append(temp['injured'])
        injured = random.choice(injured_list)
        logging.debug("injured: %s in %s", injured, injured_list)
        return self.game.entry.getCharacter(injured)



class HamsterRule(BasicRule):
    min_players = 11
    max_players = 17
    
    # �⺻ ����
    temp_truecharacter ={}
    temp_truecharacter[11] =  [1,1,1,1,2,3,4,5,5,6]
    temp_truecharacter[12] =  [1,1,1,1,1,2,3,4,5,5,6]
    temp_truecharacter[13] =  [1,1,1,1,1,1,2,3,4,5,5,6]
    temp_truecharacter[14] =  [1,1,1,1,1,1,1,2,3,4,5,5,6]
    temp_truecharacter[15] =  [1,1,1,1,1,1,1,2,3,4,5,5,5,6]
    temp_truecharacter[16] =  [1,1,1,1,1,1,2,3,4,5,5,5,6,7,7]    
    temp_truecharacter[17] =  [1,1,1,1,1,1,2,3,4,5,5,5,6,7,7,8]    

    def __init__(self,game):
        WerewolfRule.__init__(self, game)
        logging.debug("Hamstar Rule")

    def nextTurn(self):
        if self.game.state== GAME_STATE.READY:
            if self.min_players <= self.game.players and self.game.players <= self.max_players:
                logging.logging("���� �ʱ�ȭ ����")
                self.initGame()                
            else:
                self.game.deleteGame()
        elif self.game.state==GAME_STATE.PLAYING:
            if self.game.day == 1:
                if self.game.players == 17:
                    self.nexeTurn_2day()                    
                else:
                    BasicRule.nexeTurn_2day(self)
            else:
                if self.game.players == 17:
                    self.nextTurn_Xday()
                else:
                    BasicRule.nextTurn_Xday(self)

    def initGame(self):
        logging.info("init Hamstar")
        WerewolfRule.initGame(self)

    def nexeTurn_2day(self):
        logging.info("2��°�� ���!")

        #�Ϲ� �α׸� ���� ���� ����� üũ�Ѵ�.
        self.game.entry.checkNoCommentPlayer()

        #����� NPC ����
        victim =self.game.entry.getVictim()
        victim.toDeathByWerewolf()
        
        #�ܽ���
        hamsterPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.WEREHAMSTER)[0] 
        
        #�� ��!
        self.assaultByForecast(hamsterPlayer)

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
        logging.info("���� ���� ���!")

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

        #�ܽ���
        hamsterPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.WEREHAMSTER)[0] 
        
        #�� ��!
        self.assaultByForecast(hamsterPlayer)

        #����!
        assaultVictim = self.decideByWerewolf()
        if assaultVictim:
            logging.debug("assaultVictim: %s", assaultVictim)
            self.assaultByWerewolfAndHamster(assaultVictim, victim, hamsterPlayer)

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
            if self.game.termOfDay == 60:
                self.game.setGameState("state", GAME_STATE.TESTOVER)
            else:
                self.game.setGameState("state", GAME_STATE.GAMEOVER)

            if hamsterPlayer.alive == "����":
                logging.info("�ܽ��� �¸�")
                self.game.setGameState("win", "2")
            else:
                logging.info("�ζ� �¸�")
                self.game.setGameState("win", "1")
            
        elif not werewolfRace:
            if self.game.termOfDay == 60:
                self.game.setGameState("state", GAME_STATE.TESTOVER)
            else:
                self.game.setGameState("state", GAME_STATE.GAMEOVER)

            if hamsterPlayer.alive == "����":
                logging.info("�ܽ��� �¸�")
                self.game.setGameState("win", "2")
            else:
                logging.info("�ΰ� �¸�")
                self.game.setGameState("win", "0")
        else:
            logging.info("��� ����")
            #self.game.setGameState("state","������")
        
        self.game.setGameState("day",self.game.day+1)
        
    def assaultByForecast(self, hamsterPlayer):
        logging.debug("�ܺ�!!")
        forecastTarget = {}
        seerPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.SEER)[0]    

        if seerPlayer.alive == "����":
            logging.debug("seerPlayer: %s", seerPlayer)
            forecastTarget = seerPlayer.openEye()
            logging.debug("forecastTarget: %s", forecastTarget)

            if forecastTarget is not None:
                forecastTarget = self.game.entry.getCharacter(forecastTarget['mystery'])

        logging.debug("hamsterPlayer: ", hamsterPlayer)

        if forecastTarget and hamsterPlayer.alive == "����" and hamsterPlayer.id == forecastTarget.id:
            logging.debug("�ܺ� ����: %s", hamsterPlayer)
            hamsterPlayer.toDeath("����")                        
        else:
            logging.debug("�ܺ� ����")
            
    def assaultByWerewolfAndHamster(self, assaultVictim, victim, hamsterPlayer):
        self.game.entry.recordAssaultResult(assaultVictim)

        guard = {}
        hunterPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.BODYGUARD)[0]

        if(hunterPlayer.alive == "����"):
            logging.debug("hunterPlayer: %s", hunterPlayer)
            guard = hunterPlayer.guard()
            if guard is not None:
                guard = self.game.entry.getCharacter(guard['purpose'])
                logging.debug("guard: %s", guard)
                
        if assaultVictim.id == victim.id:
            logging.debug("���� ����: �����")
        elif guard and assaultVictim.id == guard.id:
            logging.debug("���� ����: ����")
        elif assaultVictim.id == hamsterPlayer.id:
            logging.debug("���� ����: ����")
        else:
            logging.debug("���� ����: %s", assaultVictim)
            assaultVictim.toDeath("����")

class ExpansionRule(WerewolfRule):
    min_players = 9
    max_players = 17

    # �⺻ ����
    temp_truecharacter = {}
    temp_truecharacter[9] = [2,3,6,11,15,4,5,9]
    temp_truecharacter[10] = [1,2,3,6,11,12,4,5,9]
    temp_truecharacter[11] = [1,1,15,2,3,6,13,4,5,10]
    temp_truecharacter[12] = [1,1,1,1,2,3,6,13,4,5,10]
    temp_truecharacter[13] = [1,15,2,3,6,11,12,13,4,5,9,10]
    temp_truecharacter[14] = [1,1,1,2,3,6,11,12,13,4,5,9,10]
    temp_truecharacter[15] = [1,1,15,2,3,6,11,12,13,4,5,5,9,10]
    temp_truecharacter[16] = [1,1,1,1,2,3,6,11,12,13,4,5,5,9,10]
    temp_truecharacter[17] = [1,1,1,1,2,3,6,11,12,13,4,5,5,9,10,14]

    def __init__(self,game):
        WerewolfRule.__init__(self, game)
        logging.debug("expansion rule")

    def initGame(self):
        logging.info("init expansion rule")
        WerewolfRule.initGame(self)

    def nexeTurn_2day(self):
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
        self.game.setGameState("state","������")
        self.game.setGameState("day",self.game.day+1)

    def nextTurn_Xday(self):
        logging.info("���� ���� ���!")
        #�Ϲ� �α׸� ���� ���� ����� üũ�Ѵ�.
        self.game.entry.checkNoCommentPlayer()
        
        #��ǥ -��� �ִ� �����ڰ� ��ǥ�� �ߴ��� üũ, ���ߴٸ� ���� ��ǥ
        victim = self.decideByMajority()
        if victim:
            if victim.truecharacter == Truecharacter.DIABLO:
                if victim.awaken():
                    self.game.setGameState("win", "3")
                    if self.game.termOfDay == 60:
                        self.game.setGameState("state",GAME_STATE.TESTOVER)
                    else:
                        self.game.setGameState("state",GAME_STATE.GAMEOVER)
                    logging.info("��ƺ�� �¸�")
                    self.game.setGameState("day", self.game.day+1)
                    return
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
            logging.debug("assaultVictim: %s", assaultVictim)
            self.assaultByWerewolf(assaultVictim,victim)
            
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
            if(self.game.termOfDay == 60):
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
        
        self.game.setGameState("day",self.game.day+1)

    def assaultByWerewolf(self, assaultVictim, victim):
        self.game.entry.recordAssaultResult(assaultVictim)
            
        guard = {}
        hunterPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.BODYGUARD)[0]    

        if(hunterPlayer.alive == "����"):
            logging.debug("hunberPlayer: %s", hunterPlayer)
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

    def decideByWerewolf(self):
        cursor = self.game.db.cursor
        
        logging.debug("����!!!")
        #������ ������...
        humanRace = self.game.entry.getEntryByRace(Race.HUMAN)
        logging.debug("%s", alivePlayers)

        #������!
        werewolfPlayers = self.game.entry.getPlayersByTruecharacter(Truecharacter.WEREWOLF,"('����')")
        readerwerewolfPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.READERWEREWOLF)
        lonelywerewolfPlayer = self.game.entry.getPlayersByTruecharacter(Truecharacter.LONELYWEREWOLF)
        logging.debug("%s", werewolfPlayers)
	
        if readerwerewolfPlayer:
            readerwerewolfPlayer = readerwerewolfPlayer[0]

        if lonelywerewolfPlayer:
            lonelywerewolfPlayer = lonelywerewolfPlayer[0]
        
        #��� �ִ� �ζ��� ���� ���� ������ �����Ѵ�.
        if not werewolfRace and (not readerwerewolfPlayer or readerwerewolfPlayer.alive=="���") \
                            and (not lonelywerewolfPlayer or lonelywerewolfPlayer.alive =="���"):
            return        

        #�ζ����� ������ �����ߴ��� Ȯ���Ѵ�.
        if not werewolfRace:
            for werewolfPlayer in werewolfPlayers:
                #������ ���ߴٸ�! ���� ���� ����     
                if not werewolfPlayer.hasAssault():
                    werewolfPlayer.assaultRandom(humanRace)
        if readerwerewolfPlayer and readerwerewolfPlayer.alive=="����":
            if not readerwerewolfPlayer.hasAssault():
                readerwerewolfPlayer.assaultRandom(humanRace)
        if lonelywerewolfPlayer and lonelywerewolfPlayer.alive=="����":
            if not lonelywerewolfPlayer.hasAssault():
                lonelywerewolfPlayer.assaultRandom(humanRace)

        #�ζ����� ���� �����ϴ� ����� ã�´�.
        query = '''select `injured`, count(*)*2 as count from `zetyx_board_werewolf_deathNote` 
        where game = '%s' and day ='%s' 
        group by `injured` 
        order by `count`  DESC '''
        query %= (self.game.game, self.game.day)
        logging.debug(query)
        
        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug(result)

        if lonelywerewolfPlayer and lonelywerewolfPlayer.alive=="����":
            query = '''select `injured`, count(*) as count from `zetyx_board_werewolf_deathnotehalf` 
            where game = '%s' and day ='%s' 
            group by `injured` 
            order by `count`  DESC '''
            query %= (self.game.game, self.game.day)
            logging.debug(query)

        cursor.execute(query)
        result2 = cursor.fetchall()
        logging.debug(result2)

        if not result:
            result2 = result2[0]
            resultList =[]
            for temp in result:
                if temp['injured'] == result2['injured']:
                    temp['count'] += 1
                resultList.append(temp)
            result = resultList
        else:
            result = result2
        
        count = 0
        injured_list = []
        logging.debug(result)

        for temp in result:
            if count < temp['count']:
                injured_list = []
                count = temp['count']
                injured_list.append(temp['injured'])
            elif count == temp['count']:
                logging.debug("count: %s", count)
                injured_list.append(temp['injured'])
            else:
                break
        injured = random.choice(injured_list)
        logging.debug("injured: %s in %s", injured, injured_list)
        return self.game.entry.getCharacter(injured)


class ConfidenceRule(BasicRule):
    min_players = 11
    max_players = 16
    
    # �⺻ ����
    temp_truecharacter = {}
    temp_truecharacter[11] = [1,1,1,1,16,3,4,17,17,6]
    temp_truecharacter[12] = [1,1,1,1,1,16,3,4,17,17,6]
    temp_truecharacter[13] = [1,1,1,1,1,1,16,3,4,17,17,6]
    temp_truecharacter[14] = [1,1,1,1,1,16,3,4,17,17,17,6,12]
    temp_truecharacter[15] = [1,1,1,1,1,1,16,3,4,17,17,17,6,12]
    temp_truecharacter[16] = [1,1,1,1,1,1,1,16,3,4,17,17,17,6,12]