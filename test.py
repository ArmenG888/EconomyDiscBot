import discord
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

class main:
    def __init__(self):
        self.chess_board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' '],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ]
m = main()


def chess_move():
    # pe7,pe5
    move = input("Enter move: ")
    move = move.split(",")
    print(move)
    print(str(ord(move[0][0])-97))
    print(str(8-(int(move[1][1])+1)))
    piece = m.chess_board[(int(move[0][1]))-1][ord(move[0][0])-97]
    #m.chess_board[(int(move[1][1]))-1][ord(move[0][0])-97] = piece
    #m.chess_board[(int(move[0][1]))-1][ord(move[0][0])-97] = " "


    if piece == " ":
        print("invalid")
    elif piece.lower() == "p":
        if move[0][1] == "7" or move[0][1] == "2":
            max_move = 2
        else:
            max_move = 1
        if int(move[0][1])-int(move[1][1]) <= max_move:
            if m.chess_board[(int(move[1][1]))-1][ord(move[0][0])-97] == " ":
                m.chess_board[(int(move[1][1]))-1][ord(move[0][0])-97] = piece
                m.chess_board[(int(move[0][1]))-1][ord(move[0][0])-97] = " "
            if m.chess_board[(int(move[1][1]))-1][ord(move[0][0])-98] != " " or m.chess_board[(int(move[1][1]))-1][ord(move[0][0])-96] != "": 
                m.chess_board[(int(move[1][1]))-1][ord(move[1][0])-97] = piece
                m.chess_board[(int(move[0][1]))-1][ord(move[0][0])-97] = " "
        else:
            print("invalid")
    chess_board_text = "  a b c d e f g h \n"
    for indx,i in enumerate(m.chess_board):
        chess_board_text += str(indx+1) + " " + " ".join(i) + " " + str(indx+1)  + "\n"
    chess_board_text += "  a b c d e f g h "

    
    print(chess_board_text)
while True:
    chess_move()