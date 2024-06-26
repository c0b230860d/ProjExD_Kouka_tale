import os
import sys
import pygame as pg
from pygame.locals import *
import pygame.mixer
import time
import random

# グローバル変数
WIDTH, HEIGHT = 1024, 768 # ディスプレイサイズ
FONT = "font/JF-Dot-MPlusS10.ttf"
FONT_F = "font/JF-Dot-MPlusS10B.ttf"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound1(obj_rct: pg.Rect) -> tuple[bool, bool]:
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

def check_bound(obj_rct:pg.Rect, left:int, right:int, top:int, bottom:int) -> tuple[bool, bool]:
    """
    与えられた引数より外側にあるか否かを判断しそれに応じたTrue or Falseを返す
    """
    yoko, tate = True, True
    if obj_rct.left < left or right < obj_rct.right:
        yoko = False
    if obj_rct.top < top or bottom < obj_rct.bottom:
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
    こうかとんの落単ビーム攻撃に関するクラス
    """
    def __init__(self, color: tuple[int, int, int],start_pos: tuple[int, int]):
        """
        引数に基づき攻撃Surfaceを生成する
        color：色
        start_pos：スタート位置
        """
        self.vx, self.vy = 0, +10

        self.font = pygame.font.Font(FONT, 18)
        self.label = self.font.render("落単", False, (50, 50, 50))
        self.frct = self.label.get_rect()
        self.frct.center = start_pos

        self.img = pg.Surface((100, 20), pg.SRCALPHA)
        pg.draw.rect(self.img, color, (0, 0, 100, 20))
        self.rct = self.img.get_rect()
        self.rct.center = start_pos        


    def update(self, screen: pg.Surface):
        """
        引数1 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)
        self.frct.move_ip(self.vx, self.vy)
        screen.blit(self.label, self.frct)  

class HealthBar:
    """
    体力ゲージに関するクラス
    """
    def __init__(self, x: int, y: int, width: int, max: int, gpa: float):
        """
        引数1 x：表示するx座標
        引数2 y：表示するy座標
        引数3 width：体力ゲージの幅
        引数4 max：体力の最大値
        引数5 gpa：表示するgpaの値
        """
        self.x = x
        self.y = y
        self.width = width
        self.max = max # 最大HP
        self.hp = max # HP
        self.mark = int((self.width - 4) / self.max) # HPバーの1目盛り

        self.font = pg.font.Font(FONT_F, 28)
        # HPとgpa表示の設定
        self.label = self.font.render(f"GPA:{gpa:.1f}  HP ", True, (255, 255, 255))
        # 体力ゲージのバー表示の設定
        self.frame = Rect(self.x + 2 + self.label.get_width(), self.y, self.width, self.label.get_height())
        self.bar = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)
        self.value = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)

    def update(self):
        self.value.width = self.hp * self.mark

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, (255, 0, 0), self.bar)
        pg.draw.rect(screen, (255, 255, 0), self.value)
        screen.blit(self.label, (self.x, self.y))
        # 現在のHPと最大HPの表示
        hp_text = self.font.render(f" {self.hp}/{self.max}", True, (255, 255, 255))
        screen.blit(hp_text, (self.x + self.width + 10 + self.label.get_width(), self.y))

class Dialogue:
    """
    選択画面時のセリフに関するクラス
    """
    def __init__(self) -> None:
        """
        引数なし
        """
        self.font = pg.font.Font(FONT, 35)
        self.txt = "＊ こうかとんがあらわれた！"
        self.txt_len = len(self.txt)
        self.index = 0

    def update(self, screen: pg.Surface,reset=None):
        """
        引数1 screen：画面Surface
        引数2 reset：画面切り替え時に戻す
        """
        if self.index < self.txt_len:
            self.index += 1
        if reset:
            self.index = 0

        rend_txt = self.font.render(self.txt[:self.index], True, (255, 255, 255))
        screen.blit(rend_txt, (40, HEIGHT/2-20))


class Choice:
    """
    選択肢に関するクラス
    """
    def __init__(self, ls: list[str], x: int, y: int):
        """
        引数1 ls：表示する選択肢のリスト
        引数2 x：表示するx座標
        引数3 y：表示するy座標
        """
        self.choice_ls = ls
        self.x = x
        self.y = y
        
        self.font = pg.font.Font(FONT_F, 40)
        self.index = 0  # 選択しているものの識別用 

        self.whle = 50  # 四角形との間の距離 
        self.width = (WIDTH - (self.whle*(len(ls)-1)) - 20)/len(ls)
        self.height = 70
        
    def draw(self, screen: pg.Surface, atk = False):
        """
        選択肢を表示する
        引数1 screen：画面Surface
        """
        for i, choice in enumerate(self.choice_ls):
            rect = pg.Rect(
                self.x + (self.width + self.whle) * i, # 四角形を描く開始座標
                self.y, 
                self.width, 
                self.height
                )
            if atk:
                color = (248, 138, 52)
            elif i == self.index:
                color = (255, 255, 0)
            else:
                color = (248, 138, 52)
            pg.draw.rect(screen, color, Rect(rect), 5)
            txt = self.font.render(choice, True, color)
            txt_rect = txt.get_rect()
            txt_rect.center = rect.center
            screen.blit(txt, txt_rect)

    def update(self, key):
        """
        キー入力による選択肢の変更
        引数1 key：押されたキーの識別
        """
        if key == pg.K_LEFT:
            self.index = (self.index - 1) % len(self.choice_ls)  # 右端から左端へ
        elif key == pg.K_RIGHT:
            self.index = (self.index + 1) % len(self.choice_ls)  # 左端から右端へ

class AfterChoice:
    """
    選択肢を選んだあとの画面に関するクラス
    """
    def __init__(self, ls: list[str]):
        """
        引数1 ls：選択肢のリスト
        """
        self.x = 40
        self.y = HEIGHT/2-20

        self.font = pg.font.Font(FONT, 35)
        self.txt_ls = ls

    def draw(self, screen: pg.Surface):
        for i, choice in enumerate(self.txt_ls):
            rend_txt = self.font.render(choice, True, (255, 255, 255))
            screen.blit(rend_txt, (self.x, self.y))
            if i % 2 == 0:
                self.x = WIDTH/2 + 40
            else:
                self.x = 40
                self.y += 60


class AttackBar:
    """
    敵を攻撃するアタックバーに関する関数
    """
    img = pg.transform.rotozoom(
        pg.image.load("fig/Attack_Bar.png"),
        0,1.8
    )
    def __init__(self):
        # アタックの確率バーの描画
        self.vx, self.vy = +30, 0
        self.rimg = pg.Surface((10, 300), pg.SRCALPHA)
        pg.draw.rect(self.rimg, (255, 255, 255), (0, 0, 20, 300))
        self.rrct = self.rimg.get_rect()
        self.rrct.center = (20, HEIGHT/2+100)

        # アタックバーの描画
        self.img = __class__.img
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = WIDTH/2, HEIGHT/2+100

    def update(self, screen: pg.Surface):
        """
        アタックバーを表示
        """
        screen.blit(self.img, self.rct)

        yoko, tate = check_bound(self.rrct, 15, WIDTH-15, HEIGHT/2-55, HEIGHT/2+255)
        if not yoko:
            self.vx *= -1
        self.rrct.move_ip(self.vx, self.vy)
        screen.blit(self.rimg, self.rrct)
    

def main():
    pg.display.set_caption("koukAtale")
    screen = pg.display.set_mode((WIDTH, HEIGHT))   
    # シーン状態の推移
    gameschange = 0  # 0：選択画面, 1：攻撃

    # こうかとんの初期化
    kkton = Koukaton()

    # ハートの初期化
    hurt = Hurt((WIDTH/2, HEIGHT/2+100 ))

    # こうかとんビーム（仮）の初期化
    beams = [] 

    # セリフに関する初期化
    dialog = Dialogue()

    # ヘルスバーに関する初期化
    gpa = random.uniform(1, 4)
    max_hp = int(gpa*20)
    hp =HealthBar(WIDTH/4, 5*HEIGHT/6, max_hp+4, max_hp, gpa) # maxの値はwidth-4を割り切れる数にする

    # 選択肢の初期化
    choice_ls = ["たたかう", "こうどう", "アイテム", "みのがす"]
    choice = Choice(choice_ls, 10, HEIGHT - 80)

    # アタックバーの初期化
    attack_bar = AttackBar()

    clock = pg.time.Clock()  # time
    select_tmr = 0  # 選択画面時のタイマーの初期値
    attack_tmr = 0  # 攻撃中のタイマーの初期値

    pygame.mixer.init()
    sound = pg.mixer.Sound("./sound/Megalovania.mp3")
    sound.play(-1)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                # 選択画面なら
                if gameschange == 0:  
                    choice.update(event.key)
                    if event.key == pg.K_RETURN:  # エンターキーを押されたら
                        if choice.index == 0:  # こうげきを選択していたら
                            gameschange = 1
                        elif choice.index == 1:  # こうどうを選択していたら
                            pass
                        elif choice.index == 2:  # アイテムを選択していたら
                            pass
                        elif choice.index == 3:  # みのがすを選択していたら
                            pass
                # 攻撃相手選択画面なら
                elif gameschange == 1:      
                    if event.key == pg.K_ESCAPE:
                        gameschange = 0
                    elif event.key == pg.K_RETURN:
                        gameschange = 2
                # アタックバーなら
                elif gameschange == 2:
                    if event.key == pg.K_RETURN:
                        gameschange = 3             

        # GameOver          
        if hp.hp <= 0:
            print("Game Over")
            return
        
        # 背景関連
        screen.fill((0,0,0))

        if gameschange == 0:  # 選択画面
            attack_tmr = 0
            pg.draw.rect(screen,(255,255,255), Rect(10, HEIGHT/2-50, WIDTH-20, 300), 5)
            kkton.update(screen)

            dialog.update(screen)

            hp.draw(screen)
            hp.update()

            choice.draw(screen)

            select_tmr += 1

        elif gameschange == 1:  # こうげきを選択した場合
            pg.draw.rect(screen,(255,255,255), Rect(10, HEIGHT/2-50, WIDTH-20, 300), 5)

            # 選択肢後の画面に関する初期化
            afterchoice = AfterChoice(["＊　こうかとん"])   
            kkton.update(screen)

            afterchoice.draw(screen)

            hp.draw(screen)
            hp.update()

            choice.draw(screen)

        elif gameschange == 2:
            pg.draw.rect(screen,(255,255,255), Rect(10, HEIGHT/2-50, WIDTH-20, 300), 5)
            kkton.update(screen)

            attack_bar.update(screen)

            hp.draw(screen)
            hp.update()

            choice.draw(screen)
            pass

        elif gameschange == 3:  # 攻撃画面
            pg.draw.rect(screen,(255,255,255), Rect(WIDTH/2-150, HEIGHT/2-50, 300, 300), 5)

            # 落単ビームの発生
            if attack_tmr % 9 == 0:  # 一定時間ごとにビームを生成
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
                if not check_bound1(beam.rct)[1]:  # 画面外に出たビームを削除
                    beams.remove(beam)
            if attack_tmr > 300: # 選択画面に戻る
                dialog.update(screen, reset=True)
                hurt = Hurt((WIDTH/2, HEIGHT/2+100))
                for beam in beams[:]:
                    beams.remove(beam)
                gameschange = 0 

            # HPの表示と更新
            hp.draw(screen)
            hp.update()

            # 選択肢の表示
            choice.draw(screen, True)
            
            attack_tmr += 1 

        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()