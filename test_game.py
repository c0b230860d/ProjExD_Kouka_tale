import os
import sys
import pygame as pg
from pygame.locals import *


WIDTH, HEIGHT = 1024, 768 # ディスプレイサイズ
DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, 5), 
    pg.K_LEFT:(-5, 0), 
    pg.K_RIGHT:(5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数:ハートRect
    戻り値:タプル(横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalseを返す
    """
    yoko, tate = True, True
    if obj_rct.left < WIDTH/3+10 or (WIDTH/3)+(WIDTH/3)-10 < obj_rct.right:  # 横判定
        yoko = False
    if obj_rct.top < HEIGHT/3+110 or HEIGHT/3+90 + HEIGHT/2.5 < obj_rct.bottom:  # 縦判定
        tate = False
    return yoko, tate


def main():
    # ゲームの初期化
    pg.display.set_caption("Kouka tale")  # 画面タイトル設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 画面用のSurfaceインスタンスを生成
    
    # ハートの読み込み
    # 'rotezoom':読み込んだ画像に回転、拡大縮小を書ける
    hurt_img = pg.transform.rotozoom(
        pg.image.load("fig/Undertale_hurt.png"), 
        0, 0.02
        ) 
    hurt_img = pg.transform.flip(hurt_img, True, False)
    hurt_rect = hurt_img.get_rect()
    hurt_rect.center = WIDTH/2, 3*HEIGHT/4  #画像の中心座標を設定
    
    clock = pg.time.Clock()  # time
    tmr = 0  # タイマーの初期値
    # font = pg.font.Font(None, 80)  # フォントサイズの設定

    # ゲームのループ
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return       
        screen.fill((0, 0, 0))  # 画面の色を指定（背景画像があるときは不要）

        # ハートの動ける範囲
        pg.draw.rect(screen,(255,255,255), Rect(WIDTH/3, HEIGHT/3+100, WIDTH/3, HEIGHT/2.5), 10)
    
        #キーボード操作
        sum_mv = [0, 0]
        key_lst = pg.key.get_pressed()  # キーが押されているか？
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        hurt_rect.move_ip(sum_mv)
        if check_bound(hurt_rect) != (True, True):
            hurt_rect.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(hurt_img, hurt_rect)

        pg.display.update()  # ディスプレイを更新する
        tmr += 1  # 1フレーム事にタイマーに1加える
        clock.tick(200)  # 1秒あたり何フレーム進むか決める    


if __name__ == "__main__":
    pg.init()  # モジュールを初期化
    main()  
    pg.quit()  # モジュールの初期化を解除
    sys.exit()  # 終了