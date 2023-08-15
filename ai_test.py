from board_display import Board
from alphazero.train import TrainModel
import random
from multiprocessing import Process,Queue,Manager


def play_chess(q:Queue,q2:Queue,choice):
    
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

    print("初始化中………………")
    train_model = TrainModel(**train_config)
    train_model.policy_value_net.eval()
    train_model.chess_board.clear_board()
    train_model.mcts.set_self_play(False)
    bord_len = 9
    if choice == '2':
        print("不观看棋谱，直接测试(ai先手):")
            #ai黑子
        win = 0
        #测试10局之后输出胜率
        for i in range(10):
            player = 0 
            is_over =False
            train_model.chess_board.clear_board()
            while True:
                if (player == 0):
                    is_over, winner, action = train_model.do_mcts_action(train_model.mcts)
                    x = action//bord_len
                    y = action % bord_len
                    print("AI落子为:           ",x,y)
                    player = 1
                    if is_over is not False:
                        break
                    #随机走子---白子
                if (player == 1):
                    action = train_model.chess_board.available_actions[random.randint(0,len(train_model.chess_board.available_actions)-1)]
                    x = action//bord_len
                    y = action % bord_len
                    fg = train_model.chess_board.do_action_((x,y))
                    print('随机落子为          ',x,y,fg)
                    if fg is not False:
                        player = 0
                        is_over, winner = train_model.chess_board.is_game_over()
                        if is_over is not False:
                            break  
                        
            if winner == 0:
                print('第',i+1,'局,随机落子赢了')
            elif winner == 1:
                print('第',i+1,'局,ai赢了')
                win +=1
            else:
                print('不明原因，联系管理员')
        print("最终胜率为：     ",win/10)
    else:
        print("正在绘制棋盘")
        win = 0
        print("ai先手")
        for i in range(10):
            player = 0 
            train_model.chess_board.clear_board()
            is_over =False
            while True:
                if (player == 0):
                    is_over, winner, action = train_model.do_mcts_action(train_model.mcts)
                    x = action//bord_len
                    y = action % bord_len
                    print("AI:           ",x,y)
                    # board.draw_circle(pos=(y*50+75,x*50+75),player=player)
                    q.put(((y*50+75,x*50+75),player),block = False)
                    # board.update()
                    player = 1
                    if is_over is not False:
                        break
                #该随机了
                if (player == 1):
                    action = train_model.chess_board.available_actions[random.randint(0,len(train_model.chess_board.available_actions)-1)]
                    x = action//bord_len
                    y = action % bord_len
                    fg = train_model.chess_board.do_action_((x,y))
                    print('随机：    ',x,y,fg)
                    if fg is not False:
                        q.put(((y*50+75,x*50+75),player),block = False)
                        # board.draw_circle(pos=(y*50+75,x*50+75),player=player)
                        # board.update()
                        player = 0
                        is_over, winner = train_model.chess_board.is_game_over()
                        if is_over is not False:
                            break
            if winner == 0:
                print('第',i+1,'局,随机落子赢了')
                q2.put(0)
            elif winner == 1:
                print('第',i+1,'局,ai赢了')
                q2.put(0)
                win +=1
            else:
                print('不明原因，联系管理员')
        print("最终胜率为：     ",win/10*100,'%')
    
    
    
    


if __name__ == '__main__':
    q = Manager().Queue(maxsize=-1)
    q2 = Manager().Queue(maxsize=-1)
    print("是否观看棋谱？       1:yes         2:no")
    choice = input()
    p = Process(target=play_chess, args=(q,q2,choice))
    p.start()
    if choice == '1':
        board = Board(9)
        while True:
            board.clock.tick(60)
            board.quit()
            while not q2.empty():
                q2.get()
                while not q.empty():
                    q.get()
                board.new_game()
                
            while not q.empty():
                pos, player = q.get()
                board.draw_circle(pos=pos,player=player)
            board.update()