import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((900, 400))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont(None, 36)

player = MusicPlayer("music")

print("Controls:")
print("P - Play")
print("Space - Pause/Unpause")
print("S - Stop")
print("N - Next")
print("B - Previous")
print("Q - Quit")

done = False
is_playing = False

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

while not done:
    screen.fill((30, 30, 30))
    current_time = player.get_time()
    time_text = font.render(format_time(current_time), True, (255, 255, 255))
    screen.blit(time_text, (220, 100))

    if player.playlist:
        song_name = player.playlist[player.current_index]
        song_text = font.render(song_name, True, (200, 200, 200))
        screen.blit(song_text, (150, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not is_playing:
                    player.play()
                    is_playing = True
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    player.pause()
                    is_playing = True
                else:
                    player.unpause()
                    is_playing = False
            elif event.key == pygame.K_s:
                player.stop()
                is_playing = False
            elif event.key == pygame.K_n:
                player.next()
                is_playing = True
            elif event.key == pygame.K_b:
                player.previous()
                is_playing = True
            elif event.key == pygame.K_q:
                done = True
    
    pygame.display.flip()

pygame.quit()