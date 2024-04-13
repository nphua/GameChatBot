import pygame, sys
import openai
import textwrap

openai.api_key = "key"

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def play_special_sound(text, sound):
    magic_keywords = ['magic', 'nuke', 'nukes', 'nuclear', 'atom', 'atomic', 'radiation', 'reactor', 'plutonium', 'uranium', 'missile', 'warhead', 'enrichment', 'fission', 'fusion', 'mushroom cloud']
    for keyword in magic_keywords:
        if keyword in text.lower():
            sound.play()
            break

def render_multiline_text(text, x, y, font, color, surface, sound, special_sound, face_closed, face_open):
    face_size = face_closed.get_size()
    x_offset = 10
    y_offset = 10
    is_speaking = False
    
    for i, char in enumerate(text):
        if char == '\n':
            is_speaking = not is_speaking
        elif char.isalpha():
            is_speaking = not is_speaking
            
        if is_speaking:
            surface.blit(face_open, (x_offset, y_offset))
        else:
            surface.blit(face_closed, (x_offset, y_offset))
        
        text_surface = font.render(char, True, color)
        surface.blit(text_surface, (x, y))
        x += text_surface.get_width()
        pygame.display.flip()
        sound.play()
        pygame.time.wait(60)
        
        if x > surface.get_width() - 50:
            x = input_rect.x + 5
            y += 35

pygame.init()
pygame.mixer.init()

talk_sound = pygame.mixer.Sound('talk.wav')
magic_nuke_sound = pygame.mixer.Sound('magic_nuke.wav')
face_closed = pygame.image.load('face_closed.png')
face_open = pygame.image.load('face_open.png')

clock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])
base_font = pygame.font.Font(None, 32)
user_text = ''
response_text = ''

input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('grey15')
color = color_passive

active = False
clear_screen = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYUP:
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                    if clear_screen:
                        screen.fill((0, 0, 0))
                        clear_screen = False
                elif event.key == pygame.K_RETURN:
                    prompt = f"You are Big Floppa, a mischievous caracal cat with a knack for magic and an unusual interest in making nukes. You're known for your quirky sense of humor and can be a bit rude at times. Remember, you're a nuclear scientist, but don't mention it outright also an advocate for legalizing nuclear bombs. User: {user_text}\nFloppa:"
                    response_text = generate_response(prompt)
                    screen.fill((0, 0, 0))
                    render_multiline_text(response_text, input_rect.x + 5, input_rect.y + 40, base_font, (255, 255, 255), screen, talk_sound, magic_nuke_sound, face_closed, face_open)
                    play_special_sound(response_text, magic_nuke_sound)
                    user_text = ''
                    clear_screen = True
                else:
                    user_text += event.unicode

    if active:
        color = color_active
    else:
        color = color_passive

    if not clear_screen:
        screen.fill((0, 0, 0))

    pygame.draw.rect(screen, color, input_rect, 2)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)

    pygame.display.flip()
    clock.tick(60)
