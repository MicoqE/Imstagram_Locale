import os
import random
import sys
import pygame
from ffpyplayer.player import MediaPlayer

# ===== CONFIG =====
VIDEO_FOLDER = r"G:\Vidéo\Instagram"
SUPPORTED_FORMATS = (".mp4", ".mov", ".avi", ".mkv")
FULLSCREEN = True
# ==================

def load_videos():
    return [
        os.path.join(VIDEO_FOLDER, f)
        for f in os.listdir(VIDEO_FOLDER)
        if f.lower().endswith(SUPPORTED_FORMATS)
    ]

def scale_keep_ratio(image, screen):
    screen_w, screen_h = screen.get_size()
    img_w, img_h = image.get_size()

    ratio = min(screen_w / img_w, screen_h / img_h)

    new_w = int(img_w * ratio)
    new_h = int(img_h * ratio)

    image = pygame.transform.scale(image, (new_w, new_h))

    x = (screen_w - new_w) // 2
    y = (screen_h - new_h) // 2

    return image, x, y

def play_video(screen, video_path):
    print("Lecture :", video_path)

    player = MediaPlayer(video_path)

    clock = pygame.time.Clock()

    while True:
        frame, val = player.get_frame()

        if val == 'eof':
            break

        if frame is not None:
            img, t = frame
            w, h = img.get_size()

            image = pygame.image.frombuffer(img.to_bytearray()[0], (w, h), 'RGB')

            image, x, y = scale_keep_ratio(image, screen)

            screen.fill((0, 0, 0))
            screen.blit(image, (x, y))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.close_player()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.close_player()
                    return
                if event.key == pygame.K_ESCAPE:
                    player.close_player()
                    pygame.quit()
                    sys.exit()

        clock.tick(30)

    player.close_player()

def main():
    pygame.init()

    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((400, 700))

    pygame.display.set_caption("Instagram Random Player")

    videos = load_videos()
    if not videos:
        print("Aucune vidéo trouvée.")
        return

    while True:
        video = random.choice(videos)
        play_video(screen, video)

if __name__ == "__main__":
    main()
