# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:34:27 2024

@author: sahil
"""


import pygame
import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import pandas as pd
from datetime import datetime
import os
import time
import sys
import textwrap

def load_images_from_folder(folder_path, grayscale=False):
    """Load images from a folder. Convert to grayscale if specified."""
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            img_path = os.path.join(folder_path, filename)
            image = pygame.image.load(img_path)
            if grayscale:
                image = convert_to_grayscale(image)
            images.append(image)
    return images

def convert_to_grayscale(image):
    """Convert a Pygame surface to grayscale."""
    arr = pygame.surfarray.pixels3d(image)
    gray = np.dot(arr[..., :3], [0.299, 0.587, 0.114])
    arr[..., :3] = np.stack([gray] * 3, axis=-1)
    return image.copy()

def load_icons(icon_folder):
    """Load icons for choices from a folder and return a dictionary with icons."""
    icons = {}
    choices = ['male', 'female', 'city', 'landscape']
    
    for choice in choices:
        icon_path = os.path.join(icon_folder, f"{choice}.png")
        if os.path.exists(icon_path):
            icon_image = pygame.image.load(icon_path)
            # Scale the icon down to 25% of its original size
            width, height = icon_image.get_size()
            scaled_icon_image = pygame.transform.scale(icon_image, (int(width * 0.15), int(height * 0.15)))
            icons[choice] = scaled_icon_image
        else:
            print(f"Warning: Icon for {choice} not found at {icon_path}")
    
    return icons

# Load scene and face images
rural_scenes = load_images_from_folder(os.getcwd() + '\\Scenes\\rural', grayscale = True)
urban_scenes = load_images_from_folder(os.getcwd() + '\\Scenes\\urban', grayscale = True)
male_faces = load_images_from_folder(os.getcwd() + '\\Faces\\male')
female_faces = load_images_from_folder(os.getcwd() + '\\Faces\\female')

# Load the icons
icon_folder = os.getcwd() + '\\Icons'  # Adjust the path to your icons folder
icons = load_icons(icon_folder)

# Initialize tkinter and create a popup to collect experiment info
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        self.x, self.y, _, _ = self.widget.bbox("insert")
        self.x += self.widget.winfo_rootx() + 25
        self.y += self.widget.winfo_rooty() + 25
        self.create_tip_window()

    def create_tip_window(self):
        if self.tip_window or not self.text:
            return
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{self.x}+{self.y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("Arial", 10, "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class ExperimentInfoDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dot Cloud Task")
        self.geometry("700x500")
        self.configure(bg="#2E3440")  # Background color
        
        self.method_var = tk.StringVar(value="BEH")
        self.subject_var = tk.StringVar()
        self.block_var = tk.StringVar(value="0")
        self.easiest_diff_var = tk.StringVar(value="0.30")
        self.easy_diff_var = tk.StringVar(value="0.18")
        self.medium_diff_var = tk.StringVar(value="0.12")
        self.hard_diff_var = tk.StringVar(value="0.06")
        self.isilow_var = tk.StringVar(value="0.1")
        self.isihigh_var = tk.StringVar(value="0.5")
        self.itilow_var = tk.StringVar(value="3")
        self.itihigh_var = tk.StringVar(value="6")
        self.self_guided_var = tk.BooleanVar()
        self.tutorial_var = tk.BooleanVar()
        self.stimulipres_var = tk.StringVar(value="1.5")
        self.responsewindow_var = tk.StringVar(value="5")
        
        # Styling
        label_style = {"font": ("Arial", 12, "bold"), "bg": "#2E3440", "fg": "#D8DEE9"}
        entry_style = {"bg": "#4C566A", "fg": "#D8DEE9", "insertbackground": "#D8DEE9", "font": ("Arial", 12)}
        button_style = {"bg": "#5E81AC", "fg": "#ECEFF4", "font": ("Arial", 12, "bold")}
        
        # Title Label
        tk.Label(self, text="Dynamic Dot Cloud Task", font=("Arial", 16, "bold"), bg="#2E3440", fg="#D8DEE9").pack(pady=1)
        
        # Create frames for left and right side
        main_frame = tk.Frame(self, bg="#2E3440")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=2)
        
        left_frame = tk.Frame(main_frame, bg="#2E3440")
        left_frame.grid(row=0, column=0, padx=40, pady=0, sticky="n")
        
        right_frame = tk.Frame(main_frame, bg="#2E3440")
        right_frame.grid(row=0, column=1, padx=40, pady=0, sticky="n")
        
        # Left side (Method, Subject ID, Block)
        tk.Label(left_frame, text="Method:", **label_style).pack(pady=2, anchor="w")
        method_menu = ttk.Combobox(left_frame, textvariable=self.method_var, values=["BEH", "fMRI"], state="readonly")
        method_menu.pack(pady=0, anchor="w")
        ToolTip(method_menu, "fMRI: 6 second initiation delay, 10 second delay after task completed")
        
        tk.Label(left_frame, text="Subject ID:", **label_style).pack(pady=2, anchor="w")
        subject_entry = tk.Entry(left_frame, textvariable=self.subject_var, **entry_style)
        subject_entry.pack(pady=0, anchor="w")
        
        tk.Label(left_frame, text="Block:", **label_style).pack(pady=2, anchor="w")
        block_menu = ttk.Combobox(left_frame, textvariable=self.block_var, values=[0, 1, 2, 3, 4, 5, 6, "practice"], state="readonly")
        block_menu.pack(pady=0, anchor="w")
        ToolTip(block_menu, "Practice: Reports participant score and whether 70% accuracy threshold has been met")
        
        
        tk.Label(left_frame, text="ISI LowerBound and UpperBound:", **label_style).pack(pady=2, anchor="w")

        isi_frame = tk.Frame(left_frame, bg="#2E3440")  # Create a frame to hold the entry widgets
        isi_frame.pack(anchor="w", pady=2)  # Pack the frame within left_frame
        
        isilow_entry = tk.Entry(isi_frame, textvariable=self.isilow_var, width=5, **entry_style)
        isihigh_entry = tk.Entry(isi_frame, textvariable=self.isihigh_var, width=5, **entry_style)
        
        isilow_entry.pack(side="left", pady=0, padx=(0, 5))  # Pack the low entry to the left with padding
        isihigh_entry.pack(side="left", pady=0)  # Pack the high entry to the left
        
        ToolTip(isihigh_entry, "Upperbound time in seconds between cue and target")
        ToolTip(isilow_entry, "Lowerbound time in seconds between cue and target")
        
        
        tk.Label(left_frame, text="ITI LowerBound and UpperBound:", **label_style).pack(pady=2, anchor="w")

        iti_frame = tk.Frame(left_frame, bg="#2E3440")  # Create a frame to hold the entry widgets
        iti_frame.pack(anchor="w", pady=2)  # Pack the frame within left_frame
        
        itilow_entry = tk.Entry(iti_frame, textvariable=self.itilow_var, width=5, **entry_style)
        itihigh_entry = tk.Entry(iti_frame, textvariable=self.itihigh_var, width=5, **entry_style)
        
        itilow_entry.pack(side="left", pady=0, padx=(0, 5))  # Pack the low entry to the left with padding
        itihigh_entry.pack(side="left", pady=0)  # Pack the high entry to the left
        
        
        ToolTip(itihigh_entry, "Upperbound time in seconds between trials")
        ToolTip(itilow_entry, "Lowerbound time in seconds between trials")
        
        guidecheckbox = tk.Checkbutton(left_frame, text="Self-guided", variable=self.self_guided_var, bg="#2E3440", fg="#D8DEE9", selectcolor="#4C566A", font=("Arial", 12))
        guidecheckbox.pack(pady=2, anchor="w")
        ToolTip(guidecheckbox, "Wait for user keypress to initiate next trial with a max limit of 30 seconds")
        
        # Right side (Proportion Differences)
        tk.Label(right_frame, text="Easiest Proportion Difference:", **label_style).pack(pady=2, anchor="w")
        easiest_diff_entry = tk.Entry(right_frame, textvariable=self.easiest_diff_var, **entry_style)
        easiest_diff_entry.pack(pady=0, anchor="w")
        ToolTip(easiest_diff_entry, "0 = 50-50 split of red/yellow\n1 = 100% of one color")
        
        tk.Label(right_frame, text="Easy Proportion Difference:", **label_style).pack(pady=2, anchor="w")
        easy_diff_entry = tk.Entry(right_frame, textvariable=self.easy_diff_var, **entry_style)
        easy_diff_entry.pack(pady=0, anchor="w")
        ToolTip(easy_diff_entry, "0 = 50-50 split of red/yellow\n1 = 100% of one color")
        
        tk.Label(right_frame, text="Medium Proportion Difference:", **label_style).pack(pady=2, anchor="w")
        medium_diff_entry = tk.Entry(right_frame, textvariable=self.medium_diff_var, **entry_style)
        medium_diff_entry.pack(pady=0, anchor="w")
        ToolTip(medium_diff_entry, "0 = 50-50 split of red/yellow\n1 = 100% of one color")
        
        tk.Label(right_frame, text="Hard Proportion Difference:", **label_style).pack(pady=2, anchor="w")
        hard_diff_entry = tk.Entry(right_frame, textvariable=self.hard_diff_var, **entry_style)
        hard_diff_entry.pack(pady=0, anchor="w")
        ToolTip(hard_diff_entry, "0 = 50-50 split of red/yellow\n1 = 100% of one color")
        
        tk.Label(right_frame, text="Stimuli Presentation Time", **label_style).pack(pady=2, anchor="w")
        stimulipres_entry = tk.Entry(right_frame, textvariable=self.stimulipres_var, **entry_style)
        stimulipres_entry.pack(pady=0, anchor="w")
        ToolTip(stimulipres_entry, "Dot Cloud Presentation Time")
        
        tk.Label(right_frame, text="Face/Scene Response Window", **label_style).pack(pady=2, anchor="w")
        responsewindow_entry = tk.Entry(right_frame, textvariable=self.responsewindow_var, **entry_style)
        responsewindow_entry.pack(pady=0, anchor="w")
        ToolTip(responsewindow_entry, "Response window time limit for face/scene decisions")
        
        tutorialcheckbox = tk.Checkbutton(right_frame, text="Tutorial", variable=self.tutorial_var, bg="#2E3440", fg="#D8DEE9", selectcolor="#4C566A", font=("Arial", 12))
        tutorialcheckbox.pack(pady=2, anchor="w")
        ToolTip(tutorialcheckbox, "Include tutorial instructions prior to beginning the task")
        
        # OK Button at the bottom center
        tk.Button(right_frame, text="OK", command=self.ok, **button_style).pack(pady=75, anchor='e')
        
        # Halassa Lab text at the bottom left
        tk.Label(left_frame, text="Halassa Lab, 2024", font=("Arial", 10), bg="#2E3440", fg="#D8DEE9").pack(side=tk.LEFT, padx=0, pady=20, anchor = 'w')
       
        
        self.result = None
    
    def ok(self):
        if (self.method_var.get() and self.subject_var.get() and self.block_var.get() and 
            self.easiest_diff_var.get() and self.easy_diff_var.get() and 
            self.medium_diff_var.get() and self.hard_diff_var.get() and self.isilow_var.get() and
            self.isihigh_var.get() and self.itilow_var.get() and self.itihigh_var.get()):
            easiest_diff = float(self.easiest_diff_var.get())
            easy_diff = float(self.easy_diff_var.get())
            medium_diff = float(self.medium_diff_var.get())
            hard_diff = float(self.hard_diff_var.get())
            itihigh = float(self.itihigh_var.get())
            isihigh = float(self.isihigh_var.get())
            itilow = float(self.itilow_var.get())
            isilow = float(self.isilow_var.get())
            stimulipres = float(self.stimulipres_var.get())
            responsewindow = float(self.responsewindow_var.get())
            self.result = {
                "Method": self.method_var.get(),
                "Subject": self.subject_var.get(),
                "Block": self.block_var.get(),
                "EasiestDiff": easiest_diff,
                "EasyDiff": easy_diff,
                "MediumDiff": medium_diff,
                "HardDiff": hard_diff,
                "SelfGuided": self.self_guided_var.get(),
                "Tutorial": self.tutorial_var.get(),
                "ITIHigh": itihigh,
                "ISIHigh": isihigh,
                "ITILow": itilow,
                "ISILow": isilow,
                "ResponseWindow": responsewindow,
                "StimuliPres": stimulipres
            }
            self.destroy()
        else:
            tk.messagebox.showwarning("Warning", "All fields must be filled out")


def draw_example_dot_cloud(win, win_size):
    """Draw an example dot cloud on the screen."""
    n_dots = 600
    dot_radius = 4
    view_radius = min(win_size) // 6
    win_center_x, win_center_y = win_size[0] // 2, win_size[1] // 2 + 100

    for _ in range(n_dots):
        x = random.uniform(-view_radius, view_radius)
        y_range = np.sqrt(view_radius**2 - x**2)
        y = random.uniform(-y_range, y_range)
        color = RED if random.random() < 0.6 else YELLOW
        pygame.draw.circle(win, color, (int(win_center_x + x), int(win_center_y + y)), dot_radius)

def draw_example_scene_with_face(win, win_size, rural_scenes, urban_scenes, male_faces, female_faces):
    """Draw an example scene with a face either overlayed or placed above/below the scene on the screen."""

    # Select random images
    scene_type = random.choice(['landscape', 'city'])
    face_type = random.choice(['male', 'female'])

    if scene_type == 'landscape':
        scene_image = random.choice(rural_scenes)
    else:
        scene_image = random.choice(urban_scenes)
    
    if face_type == 'male':
        face_image = random.choice(male_faces)
    else:
        face_image = random.choice(female_faces)
    
    # Scale both images to 50% of their original size
    scene_image = pygame.transform.scale(scene_image, (scene_image.get_width() // 2, scene_image.get_height() // 2))
    face_image = pygame.transform.scale(face_image, (face_image.get_width() // 2, face_image.get_height() // 2))
    
    # Apply transparency to the face image if it's going to overlay
    face_on_top = random.choice([True, False])
    
    # Calculate positions based on arrangement choice
    if face_on_top:  # Face above the scene
        face_rect = face_image.get_rect(midbottom=(win_size[0] // 2, win_size[1] // 2))
        scene_rect = scene_image.get_rect(midtop=face_rect.midbottom)
    else:  # Scene above the face
        scene_rect = scene_image.get_rect(midbottom=(win_size[0] // 2, win_size[1] // 2))
        face_rect = face_image.get_rect(midtop=scene_rect.midbottom)

    # Clear the window
    win.fill((128, 128, 128))  # Background color can be adjusted
    
    # Draw the images in the specified arrangement
    win.blit(scene_image, scene_rect)
    win.blit(face_image, face_rect)
    
    pygame.display.flip()

def draw_icons_with_arrows(win, icons, win_size, font):
    # Define positions for the icons on the left side
    icon_positions = {
        'male': (win_size[0] * 2 // 5, win_size[1] * 2 // 3 - 75),
        'female': (win_size[0] * 2 // 5, win_size[1] * 2 // 3 + 75),
        'city': (win_size[0] * 2 // 5 - 100, win_size[1] * 2 // 3),
        'landscape': (win_size[0] * 2 // 5 + 100, win_size[1] * 2 // 3)
    }

    # Define positions for the arrows on the right side, closer to the center and lower on the screen
    arrow_positions = {
        'up': (win_size[0] * 3 // 5, win_size[1] * 2 // 3 - 75),
        'down': (win_size[0] * 3 // 5, win_size[1] * 2 // 3 + 75),
        'left': (win_size[0] * 3 // 5 - 100, win_size[1] * 2 // 3),
        'right': (win_size[0] * 3 // 5 + 100, win_size[1] * 2 // 3)
    }

    # Draw the icons
    for icon_name, position in icon_positions.items():
        icon_surface = icons[icon_name]
        icon_rect = icon_surface.get_rect(center=position)
        win.blit(icon_surface, icon_rect)

    # Draw the triangles (arrows)
    arrow_size = 20  # Size of the triangle (arrow)
    for direction, pos in arrow_positions.items():
        if direction == 'up':
            points = [(pos[0], pos[1] - arrow_size), (pos[0] - arrow_size, pos[1] + arrow_size), (pos[0] + arrow_size, pos[1] + arrow_size)]
        elif direction == 'down':
            points = [(pos[0], pos[1] + arrow_size), (pos[0] - arrow_size, pos[1] - arrow_size), (pos[0] + arrow_size, pos[1] - arrow_size)]
        elif direction == 'left':
            points = [(pos[0] - arrow_size, pos[1]), (pos[0] + arrow_size, pos[1] - arrow_size), (pos[0] + arrow_size, pos[1] + arrow_size)]
        elif direction == 'right':
            points = [(pos[0] + arrow_size, pos[1]), (pos[0] - arrow_size, pos[1] - arrow_size), (pos[0] - arrow_size, pos[1] + arrow_size)]
        
        pygame.draw.polygon(win, BLACK, points)

    pygame.display.flip()


# Function to show tutorial screens
def show_tutorial_screens(win, font, win_size, rural_scenes, urban_scenes, male_faces, female_faces, icons):
    tutorial_screens = [
        {
            "title": "Welcome to the Dot Cloud Task",
            "text": "In this task, you will be presented a cue of colored dots, with the ratio of yellow vs. red varying. You will be tasked with making a judgment of the predominant color.  Press right key to move on.",
            "type": "dot_cloud",
        },
        {
            "title": "Instructions",
            "text": "The two colors are mapped to a specific feature, either scenery or face.  The face will be either male or female and the scene will either be city or landscape.  In this task you have to choose whether the scene is landscape/city or whether the face is female/male and the feature you have to attend to depends on the predominant color you determined earlier.",
            "type": "scene_with_face",
        },
        {
            "title": "Instructions",
            "text": "The cue-task mapping can be (1) yellow=face and red=scene.  If you think the predominant color in the cue is yellow, you make judgement on whether the face is male or female.  Conversely, if you think the cue is red, you make judgement on whether the scene is city or landscape.",
            "type": "text",
        },
        {
            "title": "Instructions",
            "text": "An alternative mapping would be:  (2) yellow=scene, red=face; In a given trial, the cue-task mapping is chosen from the two possible mappings, and it stays the same mapping for around 10-20 trials, then it changes to a different mapping covertly.",
            "type": "text",
        },
        {
            "title": "Instructions",
            "text": "Incorrect answers could be due to a wrong perception of the cue (it’s red dominant but you think it’s yellow dominant), or a wrong mapping between cue and task (it’s yellow = scene, but you think it’s yellow = face), or a wrong perception of the task (it’s a female face but you think it’s a male face).",
            "type": "text",
        },
        {
            "title": "Instructions",
            "text": "You will choose from the four icons below with arrow keys corresponding to the position of the options as shown below.  After that you will be presented with another response screen that asks you which color you thought was dominant and you will select your choice with either the left or right arrow key.",
            "type": "icons_with_arrows",
        },
        {
            "title": "Get Ready",
            "text": "After the feedback, a new trial will start following the same scheme.  Press the Right Key Button to start the task when you're ready.",
            "type": "text",
        },
    ]
    
    for screen in tutorial_screens:
            win.fill(GREY)
            
            # Render title
            title_surface = font.render(screen["title"], True, BLACK)
            win.blit(title_surface, (win_size[0]//2 - title_surface.get_width()//2, 50))
            
            # Wrap and render text
            wrapped_text = textwrap.wrap(screen["text"], width=40)  # Adjust width as needed
            y_offset = 150  # Start Y position for the wrapped text
            line_height = font.get_height() + 10  # Adjust line spacing as needed
            
            for line in wrapped_text:
                text_surface = font.render(line, True, BLACK)
                win.blit(text_surface, (win_size[0]//2 - text_surface.get_width()//2, y_offset))
                y_offset += line_height
            
            font = pygame.font.Font(None, 50)
            
            # Render specific content based on screen type
            if screen["type"] == "dot_cloud":
                draw_example_dot_cloud(win, win_size)
            elif screen["type"] == "scene_with_face":
                draw_example_scene_with_face(win, win_size, rural_scenes, urban_scenes, male_faces, female_faces)
            elif screen["type"] == "icons_with_arrows":
                draw_icons_with_arrows(win, icons, win_size, font)
            
            # Render "Next" label
            next_surface = font.render("Next", True, BLACK)
            win.blit(next_surface, (win_size[0] - next_surface.get_width() - 50, win_size[1] - next_surface.get_height() - 50))
            
            pygame.display.flip()
            
            # Wait for space bar press
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        break
                else:
                    continue
                break
        
root = ExperimentInfoDialog()
root.mainloop()

exp_info = root.result
if not exp_info:
    sys.exit()

subjectid = exp_info['Subject']
method = exp_info['Method']
block = exp_info['Block']
easiest_diff = exp_info['EasiestDiff']
easy_diff = exp_info['EasyDiff']
medium_diff = exp_info['MediumDiff']
hard_diff = exp_info['HardDiff']
self_guided = exp_info['SelfGuided']
tutorial = exp_info['Tutorial']
itihigh = exp_info["ITIHigh"]
isihigh = exp_info["ISIHigh"]
itilow = exp_info["ITILow"]
isilow = exp_info["ISILow"]
stimulipres = exp_info["StimuliPres"]
responsewindow = exp_info["ResponseWindow"]

# Initialize Pygame after tkinter window is closed
pygame.init()
pygame.font.init()

# Save the original screen resolution
screen_info = pygame.display.Info()
original_resolution = (screen_info.current_w, screen_info.current_h)

# Set up the Window in fullscreen mode
win = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN | pygame.NOFRAME)
win_size = win.get_size()
pygame.display.set_caption('Proportion Task')
clock = pygame.time.Clock()

# Initialize components for Routine
currenttime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 50)

if tutorial:
    show_tutorial_screens(win, font, win_size, rural_scenes, urban_scenes, male_faces, female_faces, icons)

    
# Dot Cloud
n_trials = 80
n_dots = 1000
dot_radius = 4  # Radius of each dot in pixels
view_radius = min(win_size) // 5  # Radius of the circle in pixels
dot_positions = []

def generate_position():
    """Generate a new dot position within the view radius."""
    x = random.uniform(-view_radius, view_radius)
    y_range = np.sqrt(view_radius**2 - x**2)
    y = random.uniform(-y_range, y_range)
    return x, y

def display_scene_with_face(win, scene_image, face_image, face_on_top):
    """Display a scene and face image with one on top of the other, touching each other."""
    
    # Scale both images to 50% of their original size
    scene_image = pygame.transform.scale(scene_image, (scene_image.get_width() // 2, scene_image.get_height() // 2))
    face_image = pygame.transform.scale(face_image, (face_image.get_width() // 2, face_image.get_height() // 2))
    
    # Define the positions for the images to ensure they are touching vertically
    if face_on_top:
        face_rect = face_image.get_rect(midbottom=(win_size[0] // 2, win_size[1] // 2))  # Center face at mid-bottom
        scene_rect = scene_image.get_rect(midtop=face_rect.midbottom)  # Place scene directly below face
    else:
        scene_rect = scene_image.get_rect(midbottom=(win_size[0] // 2, win_size[1] // 2))  # Center scene at mid-bottom
        face_rect = face_image.get_rect(midtop=scene_rect.midbottom)  # Place face directly below scene

    # Draw the images on the screen
    win.blit(face_image, face_rect) if face_on_top else win.blit(scene_image, scene_rect)
    win.blit(scene_image, scene_rect) if face_on_top else win.blit(face_image, face_rect)
    pygame.display.flip()

def shuffle_slice(a, start, stop):
    i = start
    while (i < stop-1):
        idx = random.randrange(i, stop)
        a[i], a[idx] = a[idx], a[i]
        i += 1

def display_choices(win, choices, win_size):
    """Display the choices at the four cardinal directions closer to the fixation square on the screen."""
    # Shuffle the choices so they appear in random directions
    random.shuffle(choices)
    
    # Define positions for the choices (closer to the center)
    positions = {
        'up': (win_size[0] // 2, win_size[1] // 2 - 100),
        'down': (win_size[0] // 2, win_size[1] // 2 + 100),
        'left': (win_size[0] // 2 - 150, win_size[1] // 2),
        'right': (win_size[0] // 2 + 150, win_size[1] // 2)
    }
    
    directions = ['up', 'down', 'left', 'right']
    
    # Randomize the positions of the icons
    choice_names = list(icons.keys())
    shuffle_slice(choice_names, 0, 2)
    shuffle_slice(choice_names, 2, 4)
    axischoice = random.choice([True,False])
    if axischoice == True:
        choice_names = choice_names[::-1]
    else:
        choice_names = choice_names
    # Display each icon at the corresponding position
    for choice_name, direction in zip(choice_names, directions):
        icon_surface = icons[choice_name]
        icon_rect = icon_surface.get_rect(center=positions[direction])
        win.blit(icon_surface, icon_rect)
    
    pygame.display.flip()

    return choice_names, directions

def get_choice_from_key(event_key, directions):
    """Map the arrow key press to the corresponding direction."""
    if event_key == pygame.K_UP:
        return directions[0]  # Up
    elif event_key == pygame.K_DOWN:
        return directions[1]  # Down
    elif event_key == pygame.K_LEFT:
        return directions[2]  # Left
    elif event_key == pygame.K_RIGHT:
        return directions[3]  # Right
    return None

def display_color_choices(win, win_size):
    """Display red and yellow circles on the left and right of the screen."""
    # Define the positions for the circles
    left_position = (win_size[0] // 2 - 150, win_size[1] // 2)
    right_position = (win_size[0] // 2 + 150, win_size[1] // 2)
    
    # Define the circle radius
    circle_radius = 50
    
    # Draw the circles
    win.fill(GREY)
    pygame.draw.rect(win, WHITE, (win_center_x - 5, win_center_y - 5, 10, 10))  # Draw fixation square
    pygame.draw.circle(win, RED, left_position, circle_radius)
    pygame.draw.circle(win, YELLOW, right_position, circle_radius)
    pygame.display.flip()
    
    # Wait for the participant to make a choice
    response_time = None
    chosen_color = None
    response_start_time = time.time()
    no_explain = 0
    
    while response_time is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    chosen_color = 'red'
                    response_time = time.time() - response_start_time
                elif event.key == pygame.K_RIGHT:
                    chosen_color = 'yellow'
                    response_time = time.time() - response_start_time
                break
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                df = pd.DataFrame(trial_data_list)
                df.to_csv(os.getcwd() + f"/HDMRalf_{subjectid}_{block}_{method}_{currenttime}_data.csv", index=False)
                pygame.quit()
                sys.exit()
        if time.time() - response_start_time > 3:  # Timeout after 3 seconds
            response_time = 3
            chosen_color = 'No Response'
            no_explain = 1
            break
    
    return chosen_color, response_time, no_response

# Generate dot positions within the circle without overlap
def generate_dot_positions_and_half_life(n_yellow, n_red):
    dot_positions = []
    half_lives = []
    colors = []

    for _ in range(n_red):
        x, y = generate_position()
        dot_positions.append((x, y))
        half_lives.append(random.uniform(0.1, 0.5))
        colors.append(RED)

    for _ in range(n_yellow):
        x, y = generate_position()
        dot_positions.append((x, y))
        half_lives.append(random.uniform(0.1, 0.5))
        colors.append(YELLOW)

    dot_data = list(zip(dot_positions, half_lives, colors))
    random.shuffle(dot_data)
    dot_positions, half_lives, colors = zip(*dot_data)

    return list(dot_positions), list(half_lives), list(colors)

# Helper function to generate dot proportions with randomized difficulty
def generate_dot_proportions(difficulty_level):
    difficulty_level = ''.join(difficulty_level)
    if difficulty_level == 'easiest':
        proportion_diff = easiest_diff
    elif difficulty_level == 'easy':
        proportion_diff = easy_diff
    elif difficulty_level == 'medium':
        proportion_diff = medium_diff
    else:
        proportion_diff = hard_diff
    majority_color = random.choice(['red', 'yellow'])
    
    if majority_color == 'red':
        red_proportion = 0.5 + proportion_diff / 2
        yellow_proportion = 1 - red_proportion
    else:
        yellow_proportion = 0.5 + proportion_diff / 2
        red_proportion = 1 - yellow_proportion
    
    return yellow_proportion, red_proportion

# ITI (Inter-Trial Interval)
ITI_file_dir = os.path.join(os.getcwd(), 'QuantumITI_afni')
chosen_ITI_file = random.choice(os.listdir(ITI_file_dir))
print(f"ITIs chosen from {chosen_ITI_file}")
with open(os.path.join(ITI_file_dir, chosen_ITI_file)) as file:
    itilist = []
    for iti in file:
        try:
            itilist.append(float(iti))
        except ValueError:
            print(f"Could not convert to float: {iti}")
isi_duration = itilist[0::2]
iti_duration = itilist[1::2]

switch_trials = []
while len(switch_trials) < 4:
    if not switch_trials:
        next_switch = random.randint(round((n_trials/4)-10), round(n_trials/4))
    else:
        next_switch = random.randint(round((n_trials/4)-10), round(n_trials/4)) + switch_trials[-1]

    if next_switch < n_trials - 5:
        switch_trials.append(next_switch)

if block == "practice":
    switch_difficulties = random.sample(['easy', 'easy', 'easy', 'hard'], 4)
else:
    switch_difficulties = random.sample(['easy', 'easy', 'hard', 'hard'], 4)


# Generate random difficulties for trials, ensuring no more than 4 consecutive same difficulty
difficulty_levels = []
if block == "practice":
    difficulty_pool = ['easiest', 'easiest', 'easiest', 'easiest', 'hard']
    for item in difficulty_pool:
        difficulty_levels += [item] * round((n_trials/4)+2)
else:
    difficulty_pool = ['easiest', 'easy', 'medium', 'hard']
    for item in difficulty_pool:
        difficulty_levels += [item] * round((n_trials/4)+2)
        
trial_difficulties = []
consecutive_count = 0
last_difficulty = random.sample(difficulty_levels, 1)
remove_level = (",".join(last_difficulty))
difficulty_levels.remove(remove_level)

for _ in range(n_trials):
    if _ in switch_trials:
        next_difficulty = switch_difficulties[switch_trials.index(_)]
        if next_difficulty == last_difficulty and consecutive_count >= 3:
            consecutive_count = 4
        else:
            consecutive_count = 3
    else:
        next_difficulty = random.sample(difficulty_levels, 1)
        if consecutive_count >= 4:
            while next_difficulty == last_difficulty:
                next_difficulty = random.sample(difficulty_levels, 1)
            consecutive_count = 1
        else:
            if next_difficulty == last_difficulty:
                consecutive_count += 1
            else:
                consecutive_count = 1

    trial_difficulties.append(next_difficulty)
    last_difficulty = next_difficulty
    remove_level = str(last_difficulty).strip("'[]'")
    difficulty_levels.remove(remove_level)

# Data collection list
current_context = random.randint(1, 2) 

trial_data_list = []
score = 0
iti_trial_number = 0

# Main trial loop
for trial_number in range(n_trials):
    responsewaitphase = 0
    trial_data = {}
    
    if method == "fMRI" and trial_number == 0:
        pygame.time.wait(6000)
    
    choices = ['male', 'female', 'city', 'landscape']
    
    # Check for escape key press
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            df = pd.DataFrame(trial_data_list)
            df.to_csv(os.getcwd() + f"/HDMRalf_{subjectid}_{block}_{method}_{currenttime}_data.csv", index=False)
            pygame.quit()
            sys.exit()
    
    # Determine dot colors based on trial difficulty
    if trial_number in switch_trials:
        difficulty = switch_difficulties[switch_trials.index(trial_number)]
    else:
        difficulty = trial_difficulties[trial_number]

    yellow_proportion, red_proportion = generate_dot_proportions(difficulty)
    n_yellow = int(yellow_proportion * n_dots)
    n_red = n_dots - n_yellow
    colors = [RED] * n_red + [YELLOW] * n_yellow
    random.shuffle(colors)
    
    win_center_x, win_center_y = win_size[0] // 2, win_size[1] // 2
    dot_positions, half_lives, dot_colors = generate_dot_positions_and_half_life(n_yellow, n_red)

    # Track the creation time of each dot
    creation_times = [time.time()] * n_dots

    start_time = time.time()
    

    while time.time() - start_time < stimulipres:  # Present dots for 1 second
        current_time = time.time()

        for i in range(n_dots):
            if current_time - creation_times[i] >= half_lives[i]:  # Check if the dot's half-life has passed
                # Replace the dot with a new one
                x, y = generate_position()
                dot_positions[i] = (x, y)
                half_lives[i] = random.uniform(0.1, 0.5)
                creation_times[i] = current_time

        # Draw the dot cloud
        win.fill(GREY)
        centered_dot_positions = [(x + win_center_x, y + win_center_y) for x, y in dot_positions]
        for pos, color in zip(centered_dot_positions, dot_colors):
            pygame.draw.circle(win, color, (int(pos[0]), int(pos[1])), dot_radius)
        pygame.draw.rect(win, WHITE, (win_center_x - 5, win_center_y - 5, 10, 10))  # Draw fixation square
        pygame.display.flip()

    # Inter-Trial Interval with fixation square
    if method == 'fMRI':
        trial_isi = isi_duration[trial_number]
        win.fill(GREY)
        pygame.draw.rect(win, WHITE, (win_size[0]//2 - 5, win_size[1]//2 - 5, 10, 10))  # Draw fixation square
        pygame.display.flip()
        pygame.time.wait(int(trial_isi * 1000))
    else:
        trial_isi = random.uniform(isilow,isihigh)
        win.fill(GREY)
        pygame.draw.rect(win, WHITE, (win_size[0]//2 - 5, win_size[1]//2 - 5, 10, 10))  # Draw fixation square
        pygame.display.flip()
        pygame.time.wait(int(trial_isi * 1000))

    scene_type = random.choice(['landscape', 'city'])
    face_type = random.choice(['male', 'female'])

    if scene_type == 'landscape':
        scene_image = random.choice(rural_scenes)
    else:
        scene_image = random.choice(urban_scenes)
    
    if face_type == 'male':
        face_image = random.choice(male_faces)
    else:
        face_image = random.choice(female_faces)
    
    face_on_top = random.choice([True, False])
    
    # Display the scene with the face on top
    display_scene_with_face(win, scene_image, face_image, face_on_top)
    pygame.display.flip()
    
    pygame.time.wait(1500)

    # Record time before showing response screen
    response_start_time = time.time()
    pygame.event.clear()
    
    win.fill(GREY)
    
    pygame.draw.rect(win, WHITE, (win_center_x - 5, win_center_y - 5, 10, 10))  # Draw fixation square
    
    # Display the choices
    shuffled_choices, directions = display_choices(win, choices, win_size)
    
    # Wait for the participant to make a choice
    response_time = None
    chosen_option = None
    response_start_time = time.time()
    no_response = 0
    
    while response_time is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction_chosen = get_choice_from_key(event.key, directions)
                if direction_chosen is not None:
                    response_time = time.time() - response_start_time
                    chosen_option = shuffled_choices[directions.index(direction_chosen)]
                    break
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                df = pd.DataFrame(trial_data_list)
                df.to_csv(os.getcwd() + f"/HDMRalf_{subjectid}_{block}_{method}_{currenttime}_data.csv", index=False)
                pygame.quit()
                sys.exit()
        if time.time() - response_start_time > responsewindow:  # Timeout after 3 seconds
            response_time = responsewindow
            chosen_option = 'No Response'
            no_response = 1
            break
        

    # chosen_color, color_response_time, color_no_response = display_color_choices(win, win_size)

    # Determine correct response
    correct = 0
    if current_context == 1:
        if n_red > n_yellow:  # User must discern square
            if (chosen_option == 'male' and face_type == 'male') or (chosen_option == 'female' and face_type == 'female'):
                correct = 1
            else:
                correct = 0
        else:
            if (chosen_option == 'city' and scene_type == 'city') or (chosen_option == 'landscape' and scene_type == 'landscape'):
                correct = 1
            else:
                correct = 0
    else:
        if n_red > n_yellow:  # User must discern shape
            if (chosen_option == 'city' and scene_type == 'city') or (chosen_option == 'landscape' and scene_type == 'landscape'):
                correct = 1
            else:
                correct = 0
        else:  # User must discern fill
            if (chosen_option == 'male' and face_type == 'male') or (chosen_option == 'female' and face_type == 'female'):
                correct = 1
            else:
                correct = 0

    # Feedback
    if correct:
        feedback = 'Correct'
        feedback_font = pygame.font.Font(None, 100) 
        feedback_surface = feedback_font.render(feedback, True, GREEN)
    elif no_response:
        feedback = 'Miss'
        feedback_font = pygame.font.Font(None, 100) 
        feedback_surface = feedback_font.render(feedback, True, ORANGE)
    else:
        feedback = 'Incorrect'
        feedback_font = pygame.font.Font(None, 100) 
        feedback_surface = feedback_font.render(feedback, True, RED)
    win.fill(GREY)
    win.blit(feedback_surface, (win_size[0]//2 - feedback_surface.get_width()//2, win_size[1]//2 - feedback_surface.get_height()//2))
    if correct:
        score += 1
    pygame.display.flip()
    pygame.time.wait(500)
    
    chosen_color, color_response_time, color_no_response = display_color_choices(win, win_size)
    
    if self_guided == False and method =="fMRI":
        trial_iti = iti_duration[trial_number]
        win.fill(GREY)
        pygame.draw.rect(win, WHITE, (win_size[0]//2 - 5, win_size[1]//2 - 5, 10, 10))  # Draw fixation square
        pygame.display.flip()
        pygame.time.wait(int(trial_iti * 1000))
    elif self_guided == False and method =="BEH":
        trial_iti = random.uniform(itilow,itihigh)
        win.fill(GREY)
        pygame.draw.rect(win, WHITE, (win_size[0]//2 - 5, win_size[1]//2 - 5, 10, 10))  # Draw fixation square
        pygame.display.flip()
        pygame.time.wait(int(trial_iti * 1000))
    elif self_guided == True:
        win.fill(GREY)
        pygame.draw.rect(win, WHITE, (win_size[0]//2 - 5, win_size[1]//2 - 5, 10, 10))  # Draw fixation square
        pygame.display.flip()
        next_trial_start_time = time.time()
        next_trial_key = None
    
        if method == "BEH":
            while next_trial_key is None:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        next_trial_key = event.key
                        break
                    elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        df = pd.DataFrame(trial_data_list)
                        df.to_csv(os.getcwd() + f"/HDMRalf_{subjectid}_{block}_{method}_{currenttime}_data.csv", index=False)
                        pygame.quit()
                        sys.exit()
                if time.time() - next_trial_start_time > 30:
                    break

    # Store trial data
    trial_data['proportion_diff'] = abs(yellow_proportion - red_proportion)
    trial_data['majority_color'] = 'red' if n_red > n_yellow else 'yellow'
    trial_data['isi_duration'] = trial_isi
    if self_guided == False:
        trial_data['iti_duration'] = trial_iti
    if correct:
        trial_data['correct'] = 'correct'
    elif no_response:
        trial_data['correct'] = 'no response'
    else:
        trial_data['correct'] = 'incorrect'
    trial_data['response_time'] = str(response_time)
    trial_data['chosen_color'] = chosen_color
    trial_data['current_context'] = current_context
    trial_data['running_score'] = score / (trial_number + 1)
    trial_data['correct_binary'] = correct
    trial_data['chosen_image'] = chosen_option

    trial_data_list.append(trial_data)
    
    if method == "fMRI" and trial_number == (n_trials - 1):
        pygame.time.wait(10000)
    if block == "practice" and trial_number == (n_trials - 1):
        accuracy = score / n_trials
        message = f'The overall accuracy is {accuracy*100:.2f}%\n'
        if accuracy < 0.7:
            message += 'You may want to practice again.'
        else:
            message += 'Press Escape to quit'
        font = pygame.font.Font(None, 36)
        win.fill(GREY)
        text_surface = font.render(message, True, BLACK)
        win.blit(text_surface, (win_size[0]//2 - text_surface.get_width()//2, win_size[1]//2 - text_surface.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(5000)
        
    if trial_number in switch_trials:
        current_context = 2 if current_context == 1 else 1

    iti_trial_number += 1

# Save trial data to CSV
df = pd.DataFrame(trial_data_list)
df.to_csv(os.getcwd() + f"/HDMRalf_{subjectid}_{block}_{method}_{currenttime}_data.csv", index=False)

pygame.quit()
print("Experiment finished.")

