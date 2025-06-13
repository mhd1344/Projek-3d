
import pygame
import sys
import math

# Inisialisasi pygame
pygame.init()

# Konstanta aplikasi
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TOOLBAR_HEIGHT = 100 # Diperbesar untuk menampung color picker
CANVAS_HEIGHT = WINDOW_HEIGHT - TOOLBAR_HEIGHT

# Definisi warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Palet warna yang tersedia untuk menggambar (opsional, bisa tetap ada atau dihapus)
# COLOR_PALETTE = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, CYAN]

class DrawingApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Aplikasi Menggambar - Python Drawing Tool")

        self.canvas = pygame.Surface((WINDOW_WIDTH, CANVAS_HEIGHT))
        self.canvas.fill(WHITE)

        self.drawing_mode = "point"
        self.current_color = BLACK
        self.is_drawing = False
        self.start_pos = None
        self.temp_surface = None
        self.connected_points = []

        # Font untuk UI
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # UI Elements
        self.mode_buttons = []
        # self.color_buttons = [] # Tidak digunakan jika pakai color picker custom

        # Clear button
        self.clear_button_rect = pygame.Rect(WINDOW_WIDTH - 100, 15, 80, 30)

        # Prepare mode buttons rect and labels for click detection
        mode_labels = ["Titik", "Garis", "Persegi", "Lingkaran", "Elipse"]
        mode_keys = ["point", "line", "rectangle", "circle", "ellipse"]
        x = 10
        for label, key in zip(mode_labels, mode_keys):
            rect = pygame.Rect(x, 10, 80, 30)
            self.mode_buttons.append((rect, label, key))
            x += 85
        
        # Color Picker Sliders
        self.slider_width = 150
        self.slider_height = 15
        self.slider_padding = 5
        self.slider_x = WINDOW_WIDTH - self.slider_width - 150 # Posisi slider
        self.slider_y_start = 10

        self.red_slider_rect = pygame.Rect(self.slider_x, self.slider_y_start, self.slider_width, self.slider_height)
        self.green_slider_rect = pygame.Rect(self.slider_x, self.slider_y_start + self.slider_height + self.slider_padding, self.slider_width, self.slider_height)
        self.blue_slider_rect = pygame.Rect(self.slider_x, self.slider_y_start + 2*(self.slider_height + self.slider_padding), self.slider_width, self.slider_height)
        
        self.r_val = self.current_color[0]
        self.g_val = self.current_color[1]
        self.b_val = self.current_color[2]
        
        self.is_dragging_slider = None # 'r', 'g', 'b'

    def draw_toolbar(self):
        toolbar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, toolbar_rect)
        pygame.draw.line(self.screen, GRAY, (0, TOOLBAR_HEIGHT), (WINDOW_WIDTH, TOOLBAR_HEIGHT), 2)

        # Mode buttons
        for rect, label, key in self.mode_buttons:
            if self.drawing_mode == key:
                pygame.draw.rect(self.screen, BLUE, rect)
                text_color = WHITE
            else:
                pygame.draw.rect(self.screen, WHITE, rect)
                text_color = BLACK
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            text = self.small_font.render(label, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        # Clear button
        pygame.draw.rect(self.screen, RED, self.clear_button_rect)
        pygame.draw.rect(self.screen, BLACK, self.clear_button_rect, 2)
        clear_text = self.small_font.render("Clear", True, WHITE)
        clear_text_rect = clear_text.get_rect(center=self.clear_button_rect.center)
        self.screen.blit(clear_text, clear_text_rect)

        # Color Picker
        self.draw_slider(self.red_slider_rect, self.r_val, RED, 'R')
        self.draw_slider(self.green_slider_rect, self.g_val, GREEN, 'G')
        self.draw_slider(self.blue_slider_rect, self.b_val, BLUE, 'B')

        # Display current selected color
        color_display_rect = pygame.Rect(self.slider_x + self.slider_width + 20, self.slider_y_start + 10, 40, 40)
        pygame.draw.rect(self.screen, self.current_color, color_display_rect)
        pygame.draw.rect(self.screen, BLACK, color_display_rect, 2)
        
        # Instruction text
        instruction_text = f"Mode: {self.drawing_mode.title()}"
        if self.drawing_mode == "point":
            instruction_text += " - Klik kiri untuk titik, klik kanan untuk titik bersambung"
        elif self.drawing_mode in ["line", "rectangle", "circle", "ellipse"]:
            instruction_text += " - Drag mouse untuk menggambar"
        
        text = self.small_font.render(instruction_text, True, BLACK)
        self.screen.blit(text, (10, 50)) # Pindahkan instruksi ke bawah tombol mode
        
        # Display current color RGB values
        rgb_text = self.small_font.render(f"RGB: ({self.r_val}, {self.g_val}, {self.b_val})", True, BLACK)
        self.screen.blit(rgb_text, (self.slider_x + self.slider_width + 20, self.slider_y_start + 60))

    def draw_slider(self, rect, value, slider_color, label):
        # Draw track
        pygame.draw.rect(self.screen, GRAY, rect)
        
        # Draw fill based on value
        fill_width = int((value / 255) * rect.width)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(self.screen, slider_color, fill_rect)

        # Draw handle
        handle_x = rect.x + fill_width
        pygame.draw.circle(self.screen, BLACK, (handle_x, rect.centery), self.slider_height // 2 + 3)
        pygame.draw.circle(self.screen, WHITE, (handle_x, rect.centery), self.slider_height // 2)

        # Draw label
        text = self.small_font.render(f"{label}: {value}", True, BLACK)
        self.screen.blit(text, (rect.x - 30, rect.y + (rect.height // 2) - (text.get_height() // 2)))

    def handle_click(self, pos, button):
        x, y = pos

        # Toolbar area
        if y < TOOLBAR_HEIGHT:
            # Check mode buttons clicks
            for rect, label, key in self.mode_buttons:
                if rect.collidepoint(pos):
                    self.drawing_mode = key
                    self.connected_points = []
                    self.is_drawing = False
                    self.start_pos = None
                    self.temp_surface = None
                    self.is_dragging_slider = None # Berhenti drag slider
                    return

            # Check clear button clicks
            if self.clear_button_rect.collidepoint(pos):
                self.canvas.fill(WHITE)
                self.connected_points = []
                self.is_drawing = False
                self.start_pos = None
                self.temp_surface = None
                self.is_dragging_slider = None # Berhenti drag slider
                return

            # Check slider clicks
            if self.red_slider_rect.collidepoint(pos):
                self.is_dragging_slider = 'r'
            elif self.green_slider_rect.collidepoint(pos):
                self.is_dragging_slider = 'g'
            elif self.blue_slider_rect.collidepoint(pos):
                self.is_dragging_slider = 'b'
            
            # If a slider was clicked, update its value immediately
            if self.is_dragging_slider:
                self.update_slider_value(pos[0])
                self.current_color = (self.r_val, self.g_val, self.b_val)
                return

        # Canvas area
        else:
            canvas_y = y - TOOLBAR_HEIGHT
            self.handle_canvas_click((x, canvas_y), button)

    def update_slider_value(self, mouse_x):
        if self.is_dragging_slider == 'r':
            norm_x = max(0, min(mouse_x - self.red_slider_rect.x, self.slider_width))
            self.r_val = int((norm_x / self.slider_width) * 255)
        elif self.is_dragging_slider == 'g':
            norm_x = max(0, min(mouse_x - self.green_slider_rect.x, self.slider_width))
            self.g_val = int((norm_x / self.slider_width) * 255)
        elif self.is_dragging_slider == 'b':
            norm_x = max(0, min(mouse_x - self.blue_slider_rect.x, self.slider_width))
            self.b_val = int((norm_x / self.slider_width) * 255)
        
        self.current_color = (self.r_val, self.g_val, self.b_val)


    def handle_mouse_motion(self, pos):
        # Update slider value if dragging
        if self.is_dragging_slider:
            self.update_slider_value(pos[0])
            self.current_color = (self.r_val, self.g_val, self.b_val) # Update current color immediately
            return # Jangan lanjutkan ke drawing jika sedang drag slider

        if self.is_drawing and self.start_pos:
            x, y = pos[0], pos[1] - TOOLBAR_HEIGHT
            
            self.canvas.blit(self.temp_surface, (0, 0))

            if self.drawing_mode == "line":
                pygame.draw.line(self.canvas, self.current_color, self.start_pos, (x, y), 2)

            elif self.drawing_mode == "rectangle":
                left = min(self.start_pos[0], x)
                top = min(self.start_pos[1], y)
                width = abs(self.start_pos[0] - x)
                height = abs(self.start_pos[1] - y)
                rect = pygame.Rect(left, top, width, height)
                pygame.draw.rect(self.canvas, self.current_color, rect, 2)

            elif self.drawing_mode == "circle":
                center = self.start_pos
                radius = int(math.dist(center, (x, y)))
                if radius > 0:
                    pygame.draw.circle(self.canvas, self.current_color, center, radius, 2)

            elif self.drawing_mode == "ellipse":
                centerX = (self.start_pos[0] + x) / 2
                centerY = (self.start_pos[1] + y) / 2
                radiusX = abs(self.start_pos[0] - x) / 2
                radiusY = abs(self.start_pos[1] - y) / 2
                rect = pygame.Rect(centerX - radiusX, centerY - radiusY, radiusX * 2, radiusY * 2)
                if radiusX > 0 and radiusY > 0:
                    pygame.draw.ellipse(self.canvas, self.current_color, rect, 2)

    def handle_mouse_up(self):
        self.is_drawing = False
        self.start_pos = None
        self.temp_surface = None
        self.is_dragging_slider = None # Hentikan drag slider

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)

                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up()

                elif event.type == pygame.KEYDOWN:
                    key_map = {
                        pygame.K_p: "point",
                        pygame.K_l: "line",
                        pygame.K_r: "rectangle",
                        pygame.K_c: "circle",
                        pygame.K_e: "ellipse",
                        pygame.K_SPACE: "clear",
                    }
                    if event.key in key_map:
                        mode = key_map[event.key]
                        if mode == "clear":
                            self.canvas.fill(WHITE)
                            self.connected_points = []
                            self.is_drawing = False
                            self.start_pos = None
                            self.temp_surface = None
                        else:
                            self.drawing_mode = mode
                            self.connected_points = []
                            self.is_drawing = False
                            self.start_pos = None
                            self.temp_surface = None

            self.screen.fill(WHITE)
            self.screen.blit(self.canvas, (0, TOOLBAR_HEIGHT))
            self.draw_toolbar()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = DrawingApp()
    app.run()