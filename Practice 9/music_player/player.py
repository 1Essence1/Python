import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.playlist = self.load_music()
        self.current_index = 0
        self.start_time = 0
        self.paused_time = 0
        self.is_paused = False

    def load_music(self):
        files = []
        for file in os.listdir(self.music_folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                files.append(file)
        return files

    def play(self):
        if not self.playlist:
            print("No music found!")
            return

        song = self.playlist[self.current_index]
        path = os.path.join(self.music_folder, song)

        self.start_time = pygame.time.get_ticks()
        self.paused_time = 0
        self.is_paused = False
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        print(f"Playing: {song}")

    def stop(self):
        pygame.mixer.music.stop()
        self.start_time = 0
        self.paused_time = 0
        self.is_paused = False

    def pause(self):
        self.paused_time = pygame.time.get_ticks()
        pygame.mixer.music.pause()
        self.is_paused = True

    def unpause(self):
        pygame.mixer.music.unpause()
        self.start_time += pygame.time.get_ticks() - self.paused_time
        self.is_paused = False

    def next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous(self):
        if self.start_time < 3:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()
        else:
            self.play()
    
    def get_time(self):
        if self.start_time == 0:
            return 0
        if self.is_paused:
            return (self.paused_time - self.start_time) // 1000
        else:
            return (pygame.time.get_ticks() - self.start_time) // 1000