import json
import pygame
import random
from pathlib import Path
from game.player import Player,LANE_W
from game.traffic import Car,make_car

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
DAY_NIGHT_INTERVAL_MS=30000
BG=(60,60,60)
RAFT_LANE=3
TRAFFIC_LANES=tuple(lane for lane in range(LANES) if lane!=RAFT_LANE)
HIGH_SCORE_FILE=Path(__file__).resolve().parent.parent/"high_scores.json"

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.high_score_path=HIGH_SCORE_FILE
        self.high_scores=self._load_high_scores()
        self.day_night_start=pygame.time.get_ticks()
        self.is_night=False
        self.reset()

    def _load_high_scores(self):
        try:
            with self.high_score_path.open(encoding="utf-8") as file:
                scores=json.load(file)
        except (OSError,json.JSONDecodeError):
            return []
        if not isinstance(scores,list):
            return []
        valid_scores=[score for score in scores if isinstance(score,int) and not isinstance(score,bool)]
        return sorted(valid_scores,reverse=True)[:5]

    def _record_score(self):
        if self.score_recorded:
            return
        self.score_recorded=True
        self.high_scores=sorted(self.high_scores+[self.score//10],reverse=True)[:5]
        with self.high_score_path.open("w",encoding="utf-8") as file:
            json.dump(self.high_scores,file)

    def reset(self):
        self.start_x=WIDTH//2
        self.start_y=HEIGHT-80
        self.player=Player(self.start_x,self.start_y)
        self.cars=[]
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=3
        self.hit_cooldown=0
        self.raft=pygame.Rect(RAFT_LANE*LANE_W+3,HEIGHT//2-32,LANE_W-6,64)
        self.raft_direction=-1
        self.raft_speed=2
        self.player_on_raft=False
        self.player_headlight_direction=-1
        self.game_over=False
        self.won=False
        self.score_recorded=False

    def _move_raft(self):
        old_y=self.raft.y
        self.raft.y+=self.raft_direction*self.raft_speed
        if self.raft.top<=30:
            self.raft.top=30
            self.raft_direction=1
        elif self.raft.bottom>=HEIGHT-50:
            self.raft.bottom=HEIGHT-50
            self.raft_direction=-1
        return self.raft.y-old_y

    def _player_lane(self):
        return self.player.rect.centerx//LANE_W

    def _miss_raft(self):
        self.lives-=1
        self.player=Player(self.start_x,self.start_y)
        self.player_on_raft=False
        if self.lives<=0:
            self.game_over=True
            self._record_score()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        elapsed=pygame.time.get_ticks()-self.day_night_start
        self.is_night=(elapsed//DAY_NIGHT_INTERVAL_MS)%2==1
        if self.game_over or self.won: return
        if self.hit_cooldown>0: self.hit_cooldown-=1
        previous_player_y=self.player.rect.y
        raft_delta=self._move_raft()
        if self.player_on_raft:
            self.player.rect.y+=raft_delta
        previous_lane=self._player_lane()
        keys=pygame.key.get_pressed()
        self.player.move(keys,0,WIDTH)
        if self.player.rect.y!=previous_player_y:
            self.player_headlight_direction=1 if self.player.rect.y>previous_player_y else -1
        current_lane=self._player_lane()
        if self.player_on_raft:
            if current_lane!=RAFT_LANE:
                self.player_on_raft=False
            elif not self.raft.colliderect(self.player.rect):
                self._miss_raft()
                return
        elif current_lane==RAFT_LANE:
            if self.raft.colliderect(self.player.rect):
                self.player_on_raft=True
                self.player.rect.centerx=self.raft.centerx
            else:
                self._miss_raft()
                return
        if self.game_over: return
        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.choice(TRAFFIC_LANES)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)
        remaining_cars=[]
        for c in self.cars:
            c.update()
            if self.hit_cooldown==0 and c.rect.colliderect(self.player.rect):
                self.lives-=1
                self.hit_cooldown=60
                continue
            if not c.off_screen(HEIGHT):
                remaining_cars.append(c)
        self.cars=remaining_cars
        if self.lives<=0:
            self.game_over=True
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if not self.game_over and self.player.rect.top<=10:
            self.won=True
        if self.game_over or self.won:
            self._record_score()

    def draw(self):
        self.screen.fill(BG)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,(100,100,100),(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                pygame.draw.rect(self.screen,(200,200,100),pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # sidewalks
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,HEIGHT-50,WIDTH,50))
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,0,WIDTH,30))
        for c in self.cars: c.draw(self.screen)
        pygame.draw.rect(self.screen,(112,67,36),self.raft,border_radius=12)
        for y in range(self.raft.top+12,self.raft.bottom,16):
            pygame.draw.line(self.screen,(158,102,55),(self.raft.left+5,y),(self.raft.right-5,y),2)
        self.player.draw(self.screen)
        if self.is_night:
            darkness=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            darkness.fill((5,10,24,165))
            self.screen.blit(darkness,(0,0))
            headlights=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            for car in self.cars:
                center_x=car.rect.centerx
                if car.direction>0:
                    front_y=car.rect.bottom
                    far_y=min(HEIGHT,front_y+180)
                    points=[(center_x-12,front_y-4),(center_x+12,front_y-4),(center_x+55,far_y),(center_x-55,far_y)]
                    bulb_y=front_y-3
                else:
                    front_y=car.rect.top
                    far_y=max(0,front_y-180)
                    points=[(center_x-12,front_y+4),(center_x+12,front_y+4),(center_x+55,far_y),(center_x-55,far_y)]
                    bulb_y=front_y+3
                pygame.draw.polygon(headlights,(255,239,165,78),points)
                pygame.draw.circle(headlights,(255,245,185,230),(center_x-17,bulb_y),5)
                pygame.draw.circle(headlights,(255,245,185,230),(center_x+17,bulb_y),5)
            center_x=self.player.rect.centerx
            if self.player_headlight_direction>0:
                front_y=self.player.rect.bottom
                far_y=min(HEIGHT,front_y+180)
                points=[(center_x-8,front_y-4),(center_x+8,front_y-4),(center_x+45,far_y),(center_x-45,far_y)]
                bulb_y=front_y-3
            else:
                front_y=self.player.rect.top
                far_y=max(0,front_y-180)
                points=[(center_x-8,front_y+4),(center_x+8,front_y+4),(center_x+45,far_y),(center_x-45,far_y)]
                bulb_y=front_y+3
            pygame.draw.polygon(headlights,(255,239,165,78),points)
            pygame.draw.circle(headlights,(255,245,185,230),(center_x-12,bulb_y),4)
            pygame.draw.circle(headlights,(255,245,185,230),(center_x+12,bulb_y),4)
            self.screen.blit(headlights,(0,0))
        hud=pygame.Rect(0,0,WIDTH,30)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.font.render(f"Score: {self.score//10}  Lives: {self.lives}  R=Restart",True,(220,220,220))
        self.screen.blit(s,(6,4))
        if self.game_over:
            self._msg("GAME OVER",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,HEIGHT//2+20))
        heading=self.font.render("TOP 5 SCORES",True,(240,220,120))
        self.screen.blit(heading,(WIDTH//2-heading.get_width()//2,HEIGHT//2+60))
        for index,score in enumerate(self.high_scores):
            entry=self.font.render(f"{index+1}. {score}",True,(220,220,220))
            self.screen.blit(entry,(WIDTH//2-entry.get_width()//2,HEIGHT//2+88+index*24))
        if not self.high_scores:
            empty=self.font.render("No scores yet",True,(200,200,200))
            self.screen.blit(empty,(WIDTH//2-empty.get_width()//2,HEIGHT//2+88))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
