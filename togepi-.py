#(とげぴー(仮)に関するグローバル変数)
my_x = 0       #とげぴー(仮)のx座標
my_y = 0       #とげぴー(仮)のy座標
my_dx = 0      #とげぴー(仮)のx座標の変化量
my_dy = 0      #とげぴー(仮)のy座標の変化量
r = 12.0       #とげぴー(仮)の顔の半径
mode = 0       #mode=0は、横方向のみ mode=1は、ジャンプ中
move_l = 1.0   #とげぴー(仮)のx座標の変化量の値
jamp_dy = 5.06 #とげぴー(仮)のジャンプ中のy座標の変化量の値
aa = -5        #とげぴー(仮)の左目の変化量の値
bb = 5         #とげぴー(仮)の右目の変化量の値

#(名前ブロックに関するグローバル変数)
block_x = 0    #名前ブロックのx座標
block_y = 0    #名前ブロックのy座標
count = 0      #名前ブロックを表示した回数

def setup():
    size(600, 400)   #ウィンドウのサイズを(600, 400)にする
    frameRate(120)   #フレームレートを120にする
    setup_my_chara() #とげぴー(仮)のx座標、y座標、modeの初期値を設定するsetup_my_chara()の呼び出し
    setup_block()    #名前ブロックのx座標、y座標を設定するsetup_block()の呼び出し
    
def draw():
    background(255)   #背景を白色に設定
    move_my_chara()   #とげぴー(仮)の移動を設定するmove_my_chara()の呼び出し
    move_block()      #名前ブロックの移動を設定するmove_block()の呼び出し
    
#とげぴー(仮)のx座標、y座標、modeの初期値を設定する
def setup_my_chara():
    global my_x, my_y, mode
    my_x = 300        #とげぴー(仮)のx座標を300に設定
    my_y = height-r   #とげぴー(仮)のy座標をウィンドウの下端に接する位置に設定
    mode = 0          #modeを0に設定
    
#名前ブロックのx座標、y座標を設定する
def setup_block():
    global block_x, block_y, count
    block_x = 650     #名前ブロックのx座標を650に設定
    block_y = 350     #名前ブロックのy座標を650に設定
    count = 0         #名前ブロックを表示した回数を0回に設定
       
def move_my_chara():
    #とげぴー(仮)のキーボードによる操作を行うmy_chara_key()の呼び出し
    my_chara_key()
    #とげぴー(仮)のx座標の更新を行うupdate_my_chara_x()の呼び出し
    update_my_chara_x()
    #とげぴー(仮)のy座標の更新を行うupdate_my_chara_y()の呼び出し
    update_my_chara_y()
    #とげぴー(仮)の表示を行うdraw_my_chara()の呼び出し
    draw_my_chara()
    
def move_block():
    #名前ブロックのx座標の更新を行うupdate_block_x()の呼び出し
    update_block_x()
    #名前ブロックを表示を行うdraw_block()の呼び出し
    draw_block()
    
#とげぴー(仮)のキーボードによる操作を行う
def my_chara_key():
    global my_dx, my_dy, mode, aa, bb
    #modeが0の時、
    if mode == 0:
        #キーが押されていれば、
        if keyPressed:
            #keyの値が←キーならば、
            if keyCode == LEFT:
                my_dx = -move_l          #とげぴー(仮)のx座標の変化量my_dxを-move_l(左向き)に設定
                aa = -7                  #とげぴー(仮)の左目の変化量aaを-7に設定
                bb = 3                   #とげぴー(仮)の右目の変化量bbを3に設定
            #keyの値が→キーならば、
            elif keyCode == RIGHT:
                my_dx = move_l           #とげぴー(仮)のx座標の変化量my_dxをmove_l(右向き)に設定
                aa = -3                  #とげぴー(仮)の左目の変化量aaを-3に設定
                bb = 7                   #とげぴー(仮)の右目の変化量bbを7に設定
            #keyの値が↑キーならば、
            elif keyCode == UP:
                mode = 1                 #modeを1に設定
                my_dy = -jamp_dy         #とげぴー(仮)のx座標の変化量my_dxを-move_l(左向き)に設定
                aa = -5                  #とげぴー(仮)の左目の変化量aaを-5に設定
                bb = 5                   #とげぴー(仮)の右目の変化量bbを7に設定
            #それ以外の特殊キーならば、
            else:
                my_dx = 0                #とげぴー(仮)のx座標の変化量my_dxを0に設定
        #キーを押されていなかったら、
        else:
            my_dx = 0                    #とげぴー(仮)のx座標の変化量my_dxを0に設定
            
#とげぴー(仮)のx座標の更新を行う
def update_my_chara_x():
    global my_dx, my_dy, my_x, mode
    #とげぴー(仮)のx座標がウィンドウの左端に接した時、
    if my_x == r:
        #modeが1ならば、
        if mode == 1:
            my_dx *= -1                  #とげぴー(仮)のx座標の変化量my_dxを反転させる
        #modeが0ならば、
        else:
            my_dx = move_l               #とげぴー(仮)のx座標の変化量my_dxをmove_l(右向き)に設定
            my_x = r                     #とげぴー(仮)のx座標をr=12に設定
    #とげぴー(仮)のx座標がウィンドウの左端に接した時、
    elif my_x+r == width:
        #modeが1ならば、
        if mode == 1:
            my_dx *= -1                  #とげぴー(仮)のx座標の変化量my_dxを反転させる
        #modeが0ならば、
        else:
            my_dx = -move_l              #とげぴー(仮)のx座標の変化量my_dxを-move_l(左向き)に設定
            my_x = 600 - r               #とげぴー(仮)のx座標をr=12に設定
    my_x += my_dx
    
#とげぴー(仮)のy座標の更新を行う
def update_my_chara_y():
    global my_dy, my_y, mode
    d_move_l =  0.06                     #とげぴー(仮)のy座標の更新量の変化分d_move_lを0.06に設定
    #modeを1の時、
    if mode == 1:
        #とげぴー(仮)のy座標の変化量my_dyがジャンプ中のy座標の変化量の値jamp_dy未満だったら、
        if my_dy < jamp_dy:
            my_dy += d_move_l            #とげぴー(仮)のy座標の変化量my_dyをl更新する
        #とげぴー(仮)のy座標がウィンドウの下端に接した時、
        if my_y+r > height:
            mode = 0                     #modeを0に設定
            my_dy = 0                    #とげぴー(仮)のy座標の変化量my_dyを0に設定
            my_y = height-r              #とげぴー(仮)のy座標my_yを初期位置に再設定
        my_y += my_dy                    #とげぴー(仮)のy座標my_yを更新する
        
#とげぴー(仮)の表示を行う
def draw_my_chara():
    stroke(128, 192, 255)                #輪郭線の色を青色に設定
    strokeWeight(25)                     #輪郭線のh太さを25に設定
    fill(128, 192, 255)                  #塗りつぶし色を青色に設定
    ellipse(my_x, my_y-22, r*2, r*2)     #顔
    ellipse(my_x, my_y-2, r, r+5)        #おなか
    ellipse(my_x-7, my_y+4, r, r)        #左のつばさ
    ellipse(my_x+7, my_y+4, r, r)        #右のつばさ
    
    noStroke()                           #輪郭線を作図しないように設定
    fill(0)                              #塗りつぶし色を黒色に設定
    ellipse(my_x-10, my_y-35, r, r)      #左のまゆ毛
    ellipse(my_x+10, my_y-35, r, r)      #右のまゆ毛
    ellipse(my_x+aa, my_y-27, r/2, r/2)  #左目
    ellipse(my_x+bb, my_y-27, r/2, r/2)  #右目
    fill(200, 0, 0)
    ellipse(my_x, my_y-20, r/3, r/3)     #口
    fill(128, 0, 0)
    ellipse(my_x, my_y-50, r/4, r)       #鶏冠
    fill(255, 150, 0)
    ellipse(my_x-9, my_y+23, r/2, r/4)   #左足
    ellipse(my_x+9, my_y+23, r/2, r/4)   #右足
    
#名前ブロックのx座標の更新を行う
def update_block_x():
    global block_x, count
    #名前ブロックが画面から消えたら,
    if 0 > block_x+50:
        block_x = 650                    #名前ブロックのx座標を650に再設定
        count += 1                       #名前ブロックを表示した回数を1増やす
    #名前ブロックがウィンドウに表示されている間、
    else:
        block_x -= 1                     #名前ブロックのx座標を更新する
        
    #countが 6 のとき,
    if count == 6:
        dot_digit(60, height/2 - 70, 0)        #Kを表示するdot_digit(60, height/2 - 70, 0)を呼び出す
        dot_digit(150, height/2 - 70, 1)       #Aを表示するdot_digit(150, height/2 - 70, 1)を呼び出す
        dot_digit(240, height/2 - 70, 2)       #Zを表示するdot_digit(240, height/2 - 70, 2)を呼び出す
        dot_digit(330, height/2 - 70, 3)       #Uを表示するdot_digit(330, height/2 - 70, 3)を呼び出す
        dot_digit(420, height/2 - 70, 0)       #Kを表示するdot_digit(420, height/2 - 70, 0)を呼び出す
        dot_digit(490, height/2 - 70, 4)       #Iを表示するdot_digit(490, height/2 - 70, 4)を呼び出す
        noLoop()                               #プログラムの停止
        
#名前ブロックを表示を行う
def draw_block():
    noStroke()
    fill(255, 128, 0)
    #countが 0 か 4 のとき,
    if count == 0 or count == 4:
        #Kを作図する
        rect(block_x-50, block_y-50, 25, 100) 
        beginShape()
        vertex(block_x+25, block_y-50)
        vertex(block_x+50, block_y-50)
        vertex(block_x, block_y)
        vertex(block_x+50, block_y+50)
        vertex(block_x+25, block_y+50)
        vertex(block_x-25, block_y)
        endShape()
        #ジャンプしている時としていない時での当たり判定
        #ジャンプしていない時,
        if  mode == 0:
            #名前ブロックに当たると,
            if block_x-50 <= my_x+r*2 <= block_x+50 or block_x-50 <=  my_x-r*2 <= block_x+50:
                setup( )#初期値に戻す
        #ジャンプしている時,        
        elif mode ==1 :
            #名前ブロックに当たると,
            if (block_x-50 <= my_x+r*2 <= block_x+50 or block_x-50 <=  my_x-r*2 <= block_x+50) and (block_y-50 <= my_y+r*2):
                setup( )#初期値に戻す
                
    #countが 1 のとき,    
    elif count == 1:
              #Aを作図する
        beginShape()                        
        vertex(block_x, block_y-50)
        vertex(block_x-25, block_y+50)
        vertex(block_x, block_y+50)
        vertex(block_x+7, block_y+15)
        vertex(block_x+18, block_y+15)
        vertex(block_x+25, block_y+50)
        vertex(block_x+50, block_y+50)
        vertex(block_x+25, block_y-50)
        endShape()
        fill(255)
        beginShape()
        vertex(block_x+6, block_y-5)
        vertex(block_x+17, block_y-5)
        vertex(block_x+15, block_y-25)
        vertex(block_x+8, block_y-25)
        endShape()
        #ジャンプしている時としていないときでの当たり判定
        #ジャンプしていない時,
        if  mode == 0:
            if block_x-25 <= my_x+r*2 <= block_x+50 or block_x-25 <=  my_x-r*2 <= block_x+50:
                setup( )#初期値に戻す
        #ジャンプしている時,
        elif mode ==1 :
            if (block_x-25 <= my_x+r*2 <= block_x+50 or block_x-25 <=  my_x-r*2 <= block_x+50) and (block_y-50 <= my_y+r*2):
                setup( )#初期値に戻す
        
    #countが 2 のとき,
    elif count == 2:
             #Zを作図する
        fill(255, 128, 0)
        beginShape()                         
        vertex(block_x-50, block_y-50)
        vertex(block_x+50, block_y-50)
        vertex(block_x-15, block_y+30)
        vertex(block_x+50, block_y+30)
        vertex(block_x+50, block_y+50)
        vertex(block_x-50, block_y+50)
        vertex(block_x+15, block_y-30)
        vertex(block_x-50, block_y-30)
        endShape()
        #ジャンプしている時としていないときでの当たり判定
        #ジャンプしていない時,
        if  mode == 0:
            if block_x-50 <= my_x+r*2 <= block_x+50 or block_x-50 <=  my_x-r*2 <= block_x+50:
                setup( )#初期値に戻す
        #ジャンプしている時,
        elif mode ==1 :
            if (block_x-50 <= my_x+r*2 <= block_x+50 or block_x-50 <=  my_x-r*2 <= block_x+50) and (block_y-50 <= my_y+r*2):
                setup( )#初期値に戻す
        
    #countが 3 のとき,
    elif count % 6 == 3:
        #Uを作図する
        rect(block_x-50, block_y-50, 25, 50)   
        rect(block_x+25, block_y-50, 25, 50)
        arc(block_x, block_y, 100, 100, radians(0), radians(180))
        fill(255)
        arc(block_x, block_y, 50, 50, radians(0), radians(180))
        # ジャンプしている時としていないときでの当たり判定
        #ジャンプしていない時,
        if  mode == 0:
            if block_x-50 <= my_x+r*2 <= block_x+50 or block_x-50 <=  my_x-r*2 <= block_x+50:
                setup( )#初期値に戻す
        #ジャンプしている時,
        elif mode ==1 :
            if (block_x-50 <= my_x+r*2 <= block_x+50 or block_x-50 <=  my_x-r*2 <= block_x+50) and (block_y-50 <= my_y+r*2):
                setup( )#初期値に戻す
        
        
    #countが 5 のとき,
    elif count == 5:
        #Iを作図する
        fill(255, 128, 0)                      
        beginShape()
        vertex(block_x-20, block_y-50)
        vertex(block_x-20, block_y-35)
        vertex(block_x-7, block_y-35)
        vertex(block_x-7, block_y+35)
        vertex(block_x-20, block_y+35)
        vertex(block_x-20, block_y+50)
        vertex(block_x+20, block_y+50)
        vertex(block_x+20, block_y+35)
        vertex(block_x+7, block_y+35)
        vertex(block_x+7, block_y-35)
        vertex(block_x+20, block_y-35)
        vertex(block_x+20, block_y-50)
        endShape()
        # ジャンプしている時としていないときでの当たり判定
        #ジャンプしていない時,
        if  mode == 0:
            if block_x-20 <= my_x+r*2 <= block_x+20 or block_x-20 <=  my_x-r*2 <= block_x+20:
                setup( )#初期値に戻す
        #ジャンプしている時,
        elif mode ==1 :
            if (block_x-20 <= my_x+r*2 <= block_x+20 or block_x-20 <=  my_x-r*2 <= block_x+20) and (block_y-50 <= my_y+r*2):
                setup( )#初期値に戻す
                
#ゲームクリア後に名前を表示する
def dot_digit(x, y, n):
    digit = [[1,0,0,1,1,
              1,0,0,1,1,
              1,0,0,1,0,
              1,1,1,0,0,
              1,0,0,1,0,
              1,0,0,1,1,
              1,0,0,1,1],#K
             [0,1,1,1,0,
              1,0,0,1,1,
              1,0,0,1,1,
              1,1,1,1,1,
              1,0,0,1,1,
              1,0,0,1,1,
              1,0,0,1,1],#A
             [1,1,1,1,1,
              0,0,0,1,1,
              0,0,1,1,0,
              0,1,1,0,0,
              1,1,0,0,0,
              1,0,0,0,0,
              1,1,1,1,1],#Z
             [1,0,0,1,1,
              1,0,0,1,1,
              1,0,0,1,1,
              1,0,0,1,1,
              1,0,0,1,1,
              1,0,1,1,1,
              0,1,1,1,0],#U
             [0,0,1,1,0,
              0,0,0,1,0,
              0,0,1,0,0,
              0,0,1,1,0,
              0,0,1,1,0,
              0,0,1,1,0,
              0,0,1,1,0]]#I
              
    d = 15                       #ドットの間隔を15に設定
    for i in range(35):          #iを0から34まで1ずつ増やしながら35回繰り返す
        if digit[n][i] == 1:     #digit[n][i]が1なら
            #色を０～２５５の間でランダムに設定する
            fill(random(0, 255), random(0, 255), random(0, 255))
            #(x+i%5*d, y+i/5*d)を中心とする直径10の円を作図する
            rect(x+i%5*d, y+i/5*d, 10, 10)