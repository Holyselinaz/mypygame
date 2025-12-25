import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def title_screen(screen):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)

    options = ["Play Game", "Guide / Controls", "Quit"]
    selected_index = 0  # start with the first option selected

    while True:
        screen.fill("black")
        # Title
        title_surf = font.render("Lillen's ASTEROIDS Clone", True, "white")
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4)))

        # Menu options
        for i, option in enumerate(options):
            color = "yellow" if i == selected_index else "white"
            option_surf = small_font.render(option, True, color)
            screen.blit(option_surf, option_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 50)))

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(options)  # move up
                elif event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(options)  # move down
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if options[selected_index] == "Play Game":
                        return  # start the game
                    elif options[selected_index] == "Guide / Controls":
                        guide_screen(screen)  # show guide
                    elif options[selected_index] == "Quit":
                        pygame.quit()
                        exit()

def guide_screen(screen):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    while True:
        screen.fill("black")
        screen.blit(font.render("Guide / Controls", True, "white"), (SCREEN_WIDTH//2 - 180, 50))

        
        screen.blit(small_font.render("Move: W A S D", True, "white"), (50, 150))
        screen.blit(small_font.render("Shoot: SPACE", True, "white"), (50, 200))

        
        screen.blit(small_font.render("Power-ups Squares:", True, "white"), (50, 270))
        screen.blit(small_font.render("Fast Shoot - increases shooting speed", True, "yellow"), (70, 310))
        screen.blit(small_font.render("Double Shot - adds extra bullets", True, "cyan"), (70, 350))

        
        screen.blit(small_font.render("Press ESC to go back", True, "white"), (50, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Go back to title screen
            
def game_over_screen(screen, score):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    while True:
        screen.fill("black")
        over_surf = font.render("GAME OVER", True, "red")
        score_surf = small_font.render(f"Score: {score}", True, "white")
        restart_surf = small_font.render("Press R to Restart or Q to Quit", True, "white")
        title_surf = small_font.render("Press T for Title Screen", True, "white")

        screen.blit(over_surf, over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4)))
        screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        screen.blit(restart_surf, restart_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)))
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart" 
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_t:
                    return "title"  
                
def pause_menu(screen):
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    options = ["Continue", "Exit to Title"]
    selected = 0

    
    paused_surface = screen.copy()

    while True:
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)  # 0 = fully transparent, 255 = fully opaque
        overlay.fill((0, 0, 0))
        screen.blit(paused_surface, (0, 0))
        screen.blit(overlay, (0, 0))

       
        pause_text = font.render("PAUSED", True, "white")
        screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

        
        for i, option in enumerate(options):
            color = "yellow" if i == selected else "white"
            option_surf = small_font.render(option, True, color)
            screen.blit(option_surf, option_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40)))

        pygame.display.flip()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return "continue" if options[selected] == "Continue" else "title"