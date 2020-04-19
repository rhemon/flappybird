from core.bird import Bird


class ReinforcedBird(Bird):

    def jump(self, action):
        if action == 1:
            super().jump()
    
    