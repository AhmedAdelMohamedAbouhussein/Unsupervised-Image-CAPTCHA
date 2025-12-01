import os
import sys
import pygame
from pygame.locals import *
from PIL import Image

from generate_captcha import generate_captcha  # import your function

# ---------------------- Configuration ----------------------
IMAGE_DIR = "images"

WINDOW_W, WINDOW_H = 1000, 900
GRID_ROWS, GRID_COLS = 3, 3
TILE_PADDING = 12
TILE_W = (WINDOW_W - (GRID_COLS + 1) * TILE_PADDING) // GRID_COLS
TILE_H = int(TILE_W * 0.75)  # keep images roughly 4:3
FONT_NAME = None  # default pygame font
BG_COLOR = (245, 245, 245)
BUTTON_COLOR = (60, 120, 180)
BUTTON_TEXT_COLOR = (255, 255, 255)

# ---------------------- PyGame UI Classes ----------------------

class Button:
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback

    def draw(self, surf):
        pygame.draw.rect(surf, BUTTON_COLOR, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()


class ImageTile:
    def __init__(self, image_surface, filename, answer):
        self.image_surface = image_surface
        self.filename = filename
        self.answer = bool(answer)
        self.selected = False
        self.revealed = False  # set true after submission to show correct/incorrect

    def draw(self, surf, rect):
        # draw image
        surf.blit(self.image_surface, rect)
        # draw border depending on state
        border_color = (180, 180, 180)
        border_width = 2
        if self.selected and not self.revealed:
            border_color = (80, 160, 80)  # selected (green)
            border_width = 4
        if self.revealed:
            if self.answer and self.selected:
                border_color = (20, 120, 20)  # correct selected -> dark green
                border_width = 6
            elif self.answer and not self.selected:
                border_color = (20, 100, 180)  # missed correct -> blue
                border_width = 6
            elif not self.answer and self.selected:
                border_color = (180, 40, 40)  # wrong selected -> red
                border_width = 6
        pygame.draw.rect(surf, border_color, rect, border_width, border_radius=6)


def load_and_scale_image(path, size):
    """Scale an image (PIL -> pygame surface)."""
    img = Image.open(path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)
    surf = pygame.Surface(size, pygame.SRCALPHA)
    w, h = img.size
    pg_img = pygame.image.fromstring(img.tobytes(), (w, h), img.mode)
    x = (size[0] - w) // 2
    y = (size[1] - h) // 2
    surf.fill((255, 255, 255, 0))
    surf.blit(pg_img, (x, y))
    return surf


# ---------------------- Main PyGame CAPTCHA ----------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Clustering CAPTCHA — Pick all images from cluster X")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_NAME, 20)
    big_font = pygame.font.Font(FONT_NAME, 28)

    grid_top = 120
    grid_left = TILE_PADDING
    tile_size = (TILE_W, TILE_H)

    # State variables
    tiles = []
    target_cluster = None
    submitted = False
    correct_answers_count = 0
    result_text = ""

    # ---------------------- Functions ----------------------

    def create_new_captcha():
        nonlocal tiles, target_cluster, submitted, result_text, correct_answers_count
        submitted = False
        result_text = ""
        correct_answers_count = 0

        # Generate CAPTCHA using your imported function
        data = generate_captcha()
        target_cluster = data["target_cluster"]
        images = data["images"]
        answers = data["answers"]

        tiles.clear()
        for fname, ans in zip(images, answers):
            path = os.path.join(IMAGE_DIR, fname)
            if not os.path.exists(path):
                print("Missing image:", path)
                surf = pygame.Surface(tile_size)
                surf.fill((220, 220, 220))
            else:
                try:
                    surf = load_and_scale_image(path, tile_size)
                except Exception as e:
                    print("Failed to load", path, e)
                    surf = pygame.Surface(tile_size)
                    surf.fill((220, 220, 220))
            tiles.append(ImageTile(surf, fname, ans))

    def on_submit():
        nonlocal submitted, result_text, correct_answers_count
        if submitted:
            return
        submitted = True
        correct_answers_count = sum(1 for t in tiles if t.answer and t.selected)
        total_correct = sum(1 for t in tiles if t.answer)
        wrong_selected = any(t.selected and not t.answer for t in tiles)
        missed = any(t.answer and not t.selected for t in tiles)

        # Reveal answers
        for t in tiles:
            t.revealed = True

        if not wrong_selected and not missed:
            result_text = f"Correct! +{total_correct}/{total_correct}"
        else:
            result_text = f"Result: {correct_answers_count}/{total_correct}. " \
                          f"{'Wrong selections.' if wrong_selected else ''} {'Missed some.' if missed else ''}"

    def on_next():
        create_new_captcha()

    # Buttons
    submit_btn = Button((WINDOW_W - 220, 40, 100, 40), "Submit", font, on_submit)
    next_btn = Button((WINDOW_W - 110, 40, 100, 40), "Next", font, on_next)

    # Start first CAPTCHA
    create_new_captcha()

    # ---------------------- Main loop ----------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for idx, t in enumerate(tiles):
                    row = idx // GRID_COLS
                    col = idx % GRID_COLS
                    x = grid_left + col * (TILE_W + TILE_PADDING)
                    y = grid_top + row * (TILE_H + TILE_PADDING)
                    rect = pygame.Rect(x, y, TILE_W, TILE_H)
                    if rect.collidepoint((mx, my)) and not submitted:
                        t.selected = not t.selected
                submit_btn.handle_event(event)
                next_btn.handle_event(event)

        # Draw background
        screen.fill(BG_COLOR)

        # Title & instructions
        title = big_font.render("CAPTCHA: Pick 6 images that belong to the same cluster", True, (30, 30, 30))
        screen.blit(title, (20, 20))
        instruct = font.render(f"Target cluster: {target_cluster} — select all 6 images that belong to it.", True, (40, 40, 40))
        screen.blit(instruct, (20, 60))

        # Draw tiles
        for idx, t in enumerate(tiles):
            row = idx // GRID_COLS
            col = idx % GRID_COLS
            x = grid_left + col * (TILE_W + TILE_PADDING)
            y = grid_top + row * (TILE_H + TILE_PADDING)
            rect = pygame.Rect(x, y, TILE_W, TILE_H)
            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=6)
            t.draw(screen, rect)

        # Draw buttons
        submit_btn.draw(screen)
        next_btn.draw(screen)

        # Result text
        result_surf = font.render(result_text, True, (20, 20, 20))
        screen.blit(result_surf, (20, WINDOW_H - 60))

        # Hint
        hint = font.render("Click images to select. Submit to check. Next for new CAPTCHA.", True, (90, 90, 90))
        screen.blit(hint, (20, WINDOW_H - 35))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()