import os
import random
import sys
import cv2
import pygame

# ===== CONFIG =====
VIDEO_FOLDER = r"G:\Vidéo\Instagram"
SUPPORTED_FORMATS = (".mp4", ".mov", ".avi", ".mkv")
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 700
# ==================

def load_videos():
    return [
        os.path.join(VIDEO_FOLDER, f)
        for f in os.listdir(VIDEO_FOLDER)
        if f.lower().endswith(SUPPORTED_FORMATS)
    ]

def play_video(screen, video_path):
    print("Lecture :", video_path)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erreur ouverture vidéo")
        return

    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Redimensionner au format vertical
        frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(frame, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cap.release()
                    return  # vidéo suivante
                if event.key == pygame.K_ESCAPE:
                    cap.release()
                    pygame.quit()
                    sys.exit()

        clock.tick(30)  # limite FPS

    cap.release()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
