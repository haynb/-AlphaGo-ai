from board_display import Board
from alphazero.train import TrainModel

"""
    本来想把人类封装成一个类的，但是懒得搞了，就这么用着吧，反正除了好看也没啥区别
"""

train_config = {
    'lr': 1e-2,
    'c_puct': 3,
    'board_len': 9,
    'batch_size': 500,
    'is_use_gpu': True,
    'n_test_games': 10,
    'n_mcts_iters': 500,
    'n_self_plays': 4000,
    'is_save_game': False,
    'n_feature_planes': 6,
    'check_frequency': 100,
    'start_train_size': 500
}
train_model = TrainModel(**train_config)


train_model.policy_value_net.eval()
train_model.chess_board.clear_board()
train_model.mcts.set_self_play(False)
bord_len = 9
is_over =False
player = 0                                #m默认ai先手
board = Board(9)
while True:
    if (player == 1):
        is_over, winner, action = train_model.do_mcts_action(train_model.mcts)
        x = action//bord_len
        y = action % bord_len
        print("AI:           ",x,y)
        board.draw_circle(pos=(y*50+75,x*50+75),player=player)
        board.update()
        player = 0
        if is_over is not False:
            break
    #该我了
    if player == 0:
        board.clear()
        a,b = board.get_click()                       #返回鼠标的点击
        print("a,b        ",a,b)
        x,y = board.change_pos(abs(a-75),abs(b-75))                   #把鼠标的点击转换为棋盘的9*9
        fg = False
        if (x<9 and y<9):
            fg = train_model.chess_board.do_action_((y,x))
        print (y,x,fg)
        if fg is not False:
            board.draw_circle(pos=(x*50+75,y*50+75),player=player)
            board.update()
            player = 1
            is_over, winner = train_model.chess_board.is_game_over()
            if is_over is not False:
                break      
            
            
if winner == 0:
    print('你赢了')
elif winner == 1:
    print('ai赢了')
else:
    print('不明原因，联系管理员')
    