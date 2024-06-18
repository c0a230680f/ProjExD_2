import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))


DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0)
}


ROTATION = {  # 合計値タプルをキーに、対応したこうかとん画像を値にした辞書
    (0, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0),
    (+5, -5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0), True, False),
    (+5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
    (+5, +5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 75, 2.0), True, False),
    (0, +5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 2.0), True, False),
    (-5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),#
    (-5, 0):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0), True, False),
    (-5, -5):pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0), True, False),
}


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0), True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb_img = pg.Surface((20, 20))  # 爆弾Surface
    pg.draw.circle(bomb_img,(255, 0, 0), (10, 10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rct = bomb_img.get_rect()  # 爆弾Rect
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bg_bo = pg.Surface((WIDTH, HEIGHT))  # ブラックアウト用四角
    pg.draw.rect(bg_bo,(0, 0, 0), (0, 0, WIDTH, HEIGHT))  # ブラックアウト描画
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over",True, (255, 255, 255))  # 白字で"ゲームオーバー"
    vx, vy = +5, +5  # 爆弾の横方向速度、縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bomb_rct) == True:  # こうかとんが爆弾と衝突したら
            break 
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  #こうかとんが画面内にいなかったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 更新前の位置に戻す
        screen.blit(kk_img, kk_rct)

        bomb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bomb_rct)
        if not yoko:  # 爆弾が画面横方向に出たら
            vx *= -1
        if not tate:  # 爆弾が画面縦方向に出たら
            vy *= -1
        screen.blit(bomb_img, bomb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

    # ゲームオーバー画面表示
    screen.blit(bg_bo, [0, 0])
    kk_img_go = pg.transform.flip(pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0), True, False)
    screen.blit(kk_img_go, [WIDTH/2, HEIGHT/2])
    screen.blit(txt, [WIDTH/2, HEIGHT/2])
    time.sleep(5)
    return # ゲームオーバー   


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：真理値タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:  # 横方向判定
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:  # 縦方向判定
        tate = False
    return yoko, tate

def rotate():
    return ROTATION.items()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
