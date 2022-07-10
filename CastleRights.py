class CastleRights():
    """Stores castle rights of a game

    Variable:
        wks(bool): white King side castle right
        bks(bool): black King side castle right
        wqs(bool): white Queen side castle right
        bqs(bool): black Queen side castle right
    """

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs