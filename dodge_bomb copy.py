import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 800, 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = { #押下キーに合わせた辞書設定
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0)

}

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)

    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    bomb= pg.Surface((20, 20))
    bomb_rct = bomb.get_rect()
    bomb_x = random.randint(0, WIDTH)
    bomb_y = random.randint(0, HEIGHT)
    bomb_rct_center = (bomb_x,bomb_y)#爆弾Rect
    vx = +5
    vy = +5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) #一辺が20の正方形Surface

        key_lst = pg.key.get_pressed()
        #sum_mv = kk(key_lst)
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        """if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5"""
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)#中心に半径10の赤い円を描画
        bomb.set_colorkey((0, 0, 0))#四隅の黒を透過させる
        bomb_rct.move_ip(vx, vy)#爆弾Rectの移動
        screen.blit(bomb, bomb_rct)#爆弾の表示
        if kk_rct.colliderect(bomb_rct) == True:#こうかとんが爆弾と衝突したら
            return #main関数を終了

        pg.display.update()
        kk = check_bound(kk_rct)#こうかとんが画面外に出ていないかチェック
        #if kk == [True, False]:


        #check(bomb_rct)#爆弾が画面外に出ていないかチェック
        bo = check_bound(bomb_rct)
        if bo ==(False, True):
            vx *= -1
        if bo == (True, False):
            vy *= -1
        tmr += 1
        clock.tick(50)



def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT <= obj_rct.bottom:
        tate = False
    return yoko, tate

def display_check(a):
    if a.left < 0:#もし画面外左に出ようとしたら
        a.left = 0#こうかとん
    if a.right > WIDTH:
        a.right = WIDTH
    if a.top < 0:
        a.top = 0
    if a.bottom >= HEIGHT:
        a.bottom = HEIGHT
    
def check(a):
    global vx, vy
    if a.left < 0 or a.right > WIDTH:#もし画面外左に出ようとしたら
        vx *= -1
    if a.top < 0 or a.bottom >= HEIGHT:
        vy *= -1


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
