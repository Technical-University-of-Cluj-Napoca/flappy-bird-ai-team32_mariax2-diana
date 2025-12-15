from bird import Bird
from brain import Brain
from settings import *

class AIBird(Bird):
    def __init__(self, brain=None):
        super().__init__()
        self.flap_cooldown=0
        self.brain=brain if brain else Brain()
        self.fitness=0
        self.is_flapping=False

    def think(self, pipes):
        if not pipes:
            return

        #select next pipe
        next_pipe = None
        for p in pipes:
            if p.x + PIPE_WIDTH > self.x:
                next_pipe = p
                break

        if not next_pipe:
            return

        # inputs
        i0=(self.y-(next_pipe.gap_y-PIPE_GAP//2)) /WIN_HEIGHT       #dist to top pipe
        i1=(next_pipe.x-self.x)/WIN_WIDTH      #dist to next pipe
        i2=((next_pipe.gap_y+PIPE_GAP//2)-self.y)/WIN_HEIGHT        #dist to bottom pipe
        bias=1

        inputs=[i0, i1, i2, bias]

        # decision
        if self.flap_cooldown > 0:
            self.flap_cooldown -= 1
            return

        if self.brain.decide(inputs, threshold=0.3):
            self.flap()
            self.flap_cooldown = 10  # frames

    def update(self):
        super().update()