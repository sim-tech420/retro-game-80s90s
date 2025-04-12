import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 14
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 40
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horoscope of Horrors")
clock = pygame.time.Clock()

# Load retro font (use default if no font file; download "Press Start 2P" for authenticity)
try:
    font = pygame.font.Font("PressStart2P-Regular.ttf", FONT_SIZE)
except FileNotFoundError:
    font = pygame.font.SysFont("monospace", FONT_SIZE)

# Game state
game_state = "intro"
clues = []
suspects = ["Leo Vance", "Scorpio Reed", "Virgo Lane"]
current_text = []
choices = []
killer = "Scorpio Reed"  # Fixed for simplicity; randomize later if desired

def wrap_text(text, max_width):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_text(text_lines, y_start):
    """Draw wrapped text lines at y_start."""
    for i, line in enumerate(text_lines):
        text_surface = font.render(line, True, GREEN)
        screen.blit(text_surface, (50, y_start + i * (FONT_SIZE + 10)))

def draw_button(text, x, y, action):
    """Draw a clickable button with text."""
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]

    # Highlight if hovered
    color = RED if button_rect.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(screen, color, button_rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    # Return action if clicked
    if clicked and button_rect.collidepoint(mouse_pos):
        return action
    return None

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # State machine
    if game_state == "intro":
        current_text = wrap_text(
            "Horoscope of Horrors: A killer stalks the city, leaving zodiac clues. "
            "You're Detective Archer, tasked with stopping them. A new crime scene awaits.",
            WIDTH - 100
        )
        choices = [("Investigate Scene", "crime_scene")]

    elif game_state == "crime_scene":
        current_text = wrap_text(
            "A body lies in an alley, a Scorpio symbol carved nearby. You find a bloody knife "
            "and a star chart. What do you do?",
            WIDTH - 100
        )
        choices = [
            ("Examine Knife", "knife"),
            ("Study Star Chart", "star_chart"),
            ("Interrogate Suspects", "suspects")
        ]

    elif game_state == "knife":
        if "knife" not in clues:
            clues.append("knife")
        current_text = wrap_text(
            "The knife has a monogram: 'S.R.' Could it point to Scorpio Reed? "
            "What next?",
            WIDTH - 100
        )
        choices = [("Interrogate Suspects", "suspects"), ("Return to Scene", "crime_scene")]

    elif game_state == "star_chart":
        if "star_chart" not in clues:
            clues.append("star_chart")
        current_text = wrap_text(
            "The chart highlights Scorpio's constellation. A clue to the killer's identity? "
            "What now?",
            WIDTH - 100
        )
        choices = [("Interrogate Suspects", "suspects"), ("Return to Scene", "crime_scene")]

    elif game_state == "suspects":
        current_text = wrap_text(
            f"Clues found: {', '.join(clues) if clues else 'None'}. "
            "Who do you interrogate?",
            WIDTH - 100
        )
        choices = [
            (f"Question {suspect}", f"question_{suspect.replace(' ', '_').lower()}")
            for suspect in suspects
        ]

    elif game_state == "question_leo_vance":
        current_text = wrap_text(
            "Leo Vance: 'I was at the observatory all night!' He seems nervous. "
            "Accuse him or move on?",
            WIDTH - 100
        )
        choices = [("Accuse Leo", "accuse_leo"), ("Back to Suspects", "suspects")]

    elif game_state == "question_scorpio_reed":
        current_text = wrap_text(
            "Scorpio Reed: 'I don’t know anything about knives!' His eyes dart. "
            "Accuse him or continue?",
            WIDTH - 100
        )
        choices = [("Accuse Scorpio", "accuse_scorpio"), ("Back to Suspects", "suspects")]

    elif game_state == "question_virgo_lane":
        current_text = wrap_text(
            "Virgo Lane: 'I’m just a librarian!' She’s calm. Accuse her or move on?",
            WIDTH - 100
        )
        choices = [("Accuse Virgo", "accuse_virgo"), ("Back to Suspects", "suspects")]

    elif game_state == "accuse_leo":
        current_text = wrap_text(
            "You accuse Leo Vance. He has an alibi backed by logs. Wrong choice. "
            "The killer escapes. Game Over.",
            WIDTH - 100
        )
        choices = [("Quit", "quit")]

    elif game_state == "accuse_virgo":
        current_text = wrap_text(
            "You accuse Virgo Lane. No evidence ties her to the crime. "
            "The killer strikes again. Game Over.",
            WIDTH - 100
        )
        choices = [("Quit", "quit")]

    elif game_state == "accuse_scorpio":
        current_text = wrap_text(
            "You accuse Scorpio Reed. The knife’s monogram and star chart match. "
            "He confesses! You’ve stopped the killer. Victory!",
            WIDTH - 100
        )
        choices = [("Quit", "quit")]

    # Draw text
    draw_text(current_text, 50)

    # Draw buttons
    for i, (text, action) in enumerate(choices):
        result = draw_button(text, WIDTH // 2 - BUTTON_WIDTH // 2, 400 + i * (BUTTON_HEIGHT + 20), action)
        if result:
            game_state = result

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Quit state
    if game_state == "quit":
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
