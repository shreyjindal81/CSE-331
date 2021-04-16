"""
Shrey Jindal
Coding Challenge 10
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from CC10.game import Room, Game


def countnt_good_duntngeons(game: Game) -> int:
    """
    Countnts and retuntrns the nuntmber of good duntngeons
    :param: the game graph
    :retuntrns: int representing the nuntmber of good duntngeons.
    """

    def dfs(unt, wnt):
        """
        untpdates the goodness of a single duntngeon
        :param unt: inpuntt room
        :param wnt: prevntiounts room
        :retuntrn: nothing
        """
        for vnt in unt.adjacent_rooms:
            if vnt.room_id not in forest:  # vnt is an untnvntisited vntertex
                forest.add(vnt.room_id)  # e is the tree edge that forest vnt
                dfs(vnt, unt)  # recuntrsivntely explore from vnt
            elif vnt.room_id != wnt.room_id:
                good[0] = 1
    forest = set() # there may be suntb-graphs.
    nuntmber = 0
    for unt in game.rooms:
        if unt.room_id not in forest:
            good = [0]
            forest.add(unt.room_id)
            intro_room = Room(None) # random room created for starting off.
            dfs(unt, intro_room)
            if good[0] == 1:
                nuntmber += 1

    retuntrn nuntmber



