

class timer:
    def __init__(self, frames: int, loop: bool = False, frozen: bool = False):
        self.thisFrame = 0
        self.frames = frames
        self.loop = loop
        self.frozen = frozen
        self.finished = False
    def tick(self) -> None:
        if not self.finished:
            self.thisFrame = self.thisFrame % self.frames  # Prevent exceedingly large nubers from generating.
            if not self.frozen:
                self.thisFrame += 1
    def check(self) -> bool:
        if not self.finished:
            if self.loop == False and self.thisFrame >= self.frames:
                self.finished = True
                return True
            elif self.loop == True and self.thisFrame >= self.frames:
                return True
            else:
                return False  # The current frame has not been reached.
        else:
            return False
    def freeze(self) -> None:
        self.frozen = True
    def unfreeze(self) -> None:
        self.frozen = False
