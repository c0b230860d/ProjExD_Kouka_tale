import os
import sys
import pygame as pg
from pygame.locals import *
import pygame.mixer
import time
import random

# グローバル変数
WIDTH, HEIGHT = 1024, 768 # ディスプレイサイズ
FONT_F = "font/JF-Dot-MPlusS10B.ttf"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def check_bound2(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数:ハートRect
    戻り値:タプル(横方向判定結果, 縦方向判定結果)
    行動範囲内ならTrue, 行動範囲外ならFalseを返す
    """
    # WIDTH/2-150, HEIGHT/2-50, 300, 300
    yoko, tate = True, True
    if obj_rct.left < WIDTH/2-150+5 or WIDTH/2+150-5 < obj_rct.right:  # 横判定
        yoko = False
    if obj_rct.top < HEIGHT/2-50+5 or (HEIGHT/2-50)+300-5 < obj_rct.bottom:  # 縦判定
        tate = False
    return yoko, tate

class Koukaton:
    """
    こうかとんに関するクラス
    """
    img = pg.transform.rotozoom(
        pg.image.load("fig/dot_kk_negate.png"),
        0,1.5
    )

    def __init__(self):
        """
        こうかとん画像Surfaceを生成する
        """
        self.img = __class__.img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = WIDTH/2, HEIGHT/4+30

    def update(self, screen: pg.Surface):
        """
        こうかとんを表示
        """
        screen.blit(self.img, self.rct)


class Hurt:
    """
    プレイヤー（ハート）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
    img = pg.transform.rotozoom(
        pg.image.load("fig/Undertale_hurt.png"), 
        0, 0.02
        ) 
    
    def __init__(self, xy: tuple[int, int]):
        """
        ハート画像Surfaceを生成する
        引数 xy：ハート画像の初期位置座標タプル
        """
        self.img = __class__.img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてハートを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound2(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.img
        if sum_mv != [0, 0]:
            self.dire = sum_mv
        screen.blit(self.img, self.rct)

class AttackBeam:
    """
    こうかとんのビーム攻撃に関するクラス
    """
    def __init__(self, color: tuple[int, int, int],start_pos: tuple[int, int]):
        """
        引数に基づき攻撃Surfaceを生成する
        color：色
        start_pos：スタート位置
        """
        self.vx, self.vy = 0, +10

        self.font = pygame.font.Font(FONT_F, 18)
        self.label = self.font.render("落単", False, (50, 50, 50))
        self.frct = self.label.get_rect()
        self.frct.center = start_pos

        self.img = pg.Surface((100, 20), pg.SRCALPHA)
        pg.draw.rect(self.img, color, (0, 0, 100, 20))
        self.rct = self.img.get_rect()
        self.rct.center = start_pos        


    def update(self, screen: pg.Surface):
        """

        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)
        self.frct.move_ip(self.vx, self.vy)
        screen.blit(self.label, self.frct)  

class HealthBar:
    """
    """
    def __init__(self, x, y, width, max, gpa):
        self.x = x
        self.y = y
        self.width = width
        self.max = max # 最大HP
        self.hp = max # HP
        self.mark = int((self.width - 4) / self.max) # HPバーの1目盛り

        self.font = pygame.font.Font(FONT_F, 28)
        self.label = self.font.render(f"GPA:{gpa:.1f}  HP", True, (255, 255, 255))
        self.frame = Rect(self.x + 2 + self.label.get_width(), self.y, self.width, self.label.get_height())
        self.bar = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)
        self.value = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)

    def update(self):
        self.value.width = self.hp * self.mark

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.bar)
        pygame.draw.rect(screen, (255, 255, 0), self.value)
        screen.blit(self.label, (self.x, self.y))


def main():
    pg.display.set_caption("koukAtale")
    screen = pg.display.set_mode((WIDTH, HEIGHT))   
    #こうかとんの初期化
    kkton = Koukaton()

    # ハートの初期化
    hurt = Hurt((WIDTH/2, 3* HEIGHT/4 ))

    # こうかとんビーム（仮）の初期化
    beams = [] 

    hp =HealthBar(WIDTH/3, 5*HEIGHT/6, 100, 96, random.uniform(1, 4)) # maxの値はwidth-4を割り切れる数にする

    clock = pg.time.Clock()  # time
    tmr = 0  # タイマーの初期値

    pygame.mixer.init()
    sound = pygame.mixer.Sound("./sound/Megalovania.mp3")
    sound.play(-1)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        # 背景関連
        screen.fill((0,0,0))
        pg.draw.rect(screen,(255,255,255), Rect(WIDTH/2-150, HEIGHT/2-50, 300, 300), 5)

        # 落単ビームの発生 
        if tmr % 7 == 0:  # 一定時間ごとにビームを生成
            start_pos = (random.randint(WIDTH/2-100,WIDTH/2+100), 40)
            beams.append(AttackBeam((255, 255, 255), start_pos))
        
        # ヘルスの現象
        for bm in range(len(beams)):
            if beams[bm] is not None:
                if hurt.rct.colliderect(beams[bm].rct):
                    hp.hp -= 1

        kkton.update(screen)
    
        key_lst = pg.key.get_pressed()
        # ハートの移動
        hurt.update(key_lst, screen)

        # 落単ビームの更新と削除
        for beam in beams[:]:
            beam.update(screen)
            if not check_bound(beam.rct)[1]:  # 画面外に出たビームを削除
                beams.remove(beam)

        # HPの表示と更新
        hp.draw(screen)
        hp.update()

        pg.display.update()
        tmr += 1 
        clock.tick(30)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()