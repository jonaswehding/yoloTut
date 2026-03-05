import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
from pathlib import Path
import json

## Installer: - Pillow: `pip install Pillow`


class YOLOLabeller:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Image Labeller - ITEK2026")
        self.root.geometry("1200x800")
        
        # Variables
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.photo_image = None
        self.boxes = []  # List of (x1, y1, x2, y2, class_id)
        self.current_box = None  # (x1, y1, x2, y2) for box being drawn
        self.drawing = False
        self.scale_factor = 1.0
        self.class_id_input = tk.StringVar(value="0")
        
        # Create main layout
        self.create_widgets()
        
    def create_widgets(self):
        """Create UI widgets"""
        # Top menu bar
        menu_frame = tk.Frame(self.root, bg="lightgray", height=40)
        menu_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(menu_frame, text="Load Image", command=self.load_image, 
                 bg="green", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Save Annotations", command=self.save_annotations,
                 bg="blue", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Clear All", command=self.clear_all,
                 bg="red", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(menu_frame, text="Undo Last Box", command=self.undo_box,
                 bg="orange", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        
        # Class ID input
        tk.Label(menu_frame, text="Current Class ID:", bg="lightgray").pack(side=tk.LEFT, padx=(20, 5))
        tk.Spinbox(menu_frame, from_=0, to=99, textvariable=self.class_id_input, 
                  width=5).pack(side=tk.LEFT, padx=5)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left side: Canvas for image
        canvas_frame = tk.Frame(content_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = tk.Label(canvas_frame, text="Instructions: Click and drag to draw bounding boxes. Release to place box.",
                               bg="lightyellow", wraplength=400, justify=tk.LEFT)
        instructions.pack(fill=tk.X, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # Right side: Info panel
        info_frame = tk.Frame(content_frame, bg="lightgray", width=250)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        info_frame.pack_propagate(False)
        
        tk.Label(info_frame, text="Image Info", bg="lightgray", font=("Arial", 12, "bold")).pack(fill=tk.X, padx=5, pady=5)
        self.image_label = tk.Label(info_frame, text="No image loaded", bg="white", wraplength=200, justify=tk.LEFT)
        self.image_label.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(info_frame, text="Annotations", bg="lightgray", font=("Arial", 12, "bold")).pack(fill=tk.X, padx=5, pady=(10, 5))
        self.annotations_label = tk.Label(info_frame, text="0 boxes", bg="white", wraplength=200, justify=tk.LEFT)
        self.annotations_label.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(info_frame, text="Box List", bg="lightgray", font=("Arial", 12, "bold")).pack(fill=tk.X, padx=5, pady=(10, 5))
        
        # Scrollable frame for boxes
        boxes_container = tk.Frame(info_frame, bg="white")
        boxes_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas and scrollbar for scrolling
        self.boxes_canvas = tk.Canvas(boxes_container, bg="white", height=200)
        scrollbar = tk.Scrollbar(boxes_container, orient="vertical", command=self.boxes_canvas.yview)
        self.boxes_scrollable_frame = tk.Frame(self.boxes_canvas, bg="white")
        
        self.boxes_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.boxes_canvas.configure(scrollregion=self.boxes_canvas.bbox("all"))
        )
        
        self.boxes_canvas.create_window((0, 0), window=self.boxes_scrollable_frame, anchor="nw")
        self.boxes_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.boxes_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def load_image(self):
        """Load an image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.boxes = []  # Clear annotations for new image
            self.display_image = self.original_image.copy()
            self.update_canvas()
            self.update_image_info()
            
    def update_canvas(self):
        """Update canvas with current image and boxes"""
        if not self.original_image:
            return
            
        # Resize image to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet rendered
            return
            
        # Calculate scale factor
        img_width, img_height = self.original_image.size
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        self.scale_factor = min(scale_x, scale_y, 1.0)  # Don't scale up
        
        # Resize original image
        new_width = int(img_width * self.scale_factor)
        new_height = int(img_height * self.scale_factor)
        self.display_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Draw boxes on display image
        draw = ImageDraw.Draw(self.display_image)
        for box in self.boxes:
            x1, y1, x2, y2, class_id = box
            # Convert normalized coords to pixel coords
            px1 = x1 * new_width
            py1 = y1 * new_height
            px2 = x2 * new_width
            py2 = y2 * new_height
            
            draw.rectangle([px1, py1, px2, py2], outline="red", width=2)
            draw.text((px1 + 2, py1 - 15), f"Class {class_id}", fill="red")
        
        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")
        self.canvas.config(width=self.display_image.width, height=self.display_image.height)
        
    def on_canvas_press(self, event):
        """Handle mouse press on canvas"""
        if not self.original_image:
            messagebox.showwarning("No Image", "Please load an image first")
            return
        self.drawing = True
        self.current_box = (event.x, event.y, event.x, event.y)
        
    def on_canvas_drag(self, event):
        """Handle mouse drag on canvas"""
        if self.drawing and self.current_box:
            x1, y1, _, _ = self.current_box
            self.current_box = (x1, y1, event.x, event.y)
            self.draw_preview()
            
    def on_canvas_release(self, event):
        """Handle mouse release on canvas"""
        if not self.drawing or not self.current_box:
            return
            
        self.drawing = False
        x1, y1, x2, y2 = self.current_box
        
        # Ensure x1 < x2 and y1 < y2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
            
        # Check minimum box size
        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            self.current_box = None
            self.update_canvas()
            return
            
        # Convert pixel coords to normalized coords (based on display image)
        if self.display_image:
            display_width = self.display_image.width
            display_height = self.display_image.height
            
            norm_x1 = x1 / display_width
            norm_y1 = y1 / display_height
            norm_x2 = x2 / display_width
            norm_y2 = y2 / display_height
            
            # Clamp to [0, 1]
            norm_x1 = max(0, min(norm_x1, 1))
            norm_y1 = max(0, min(norm_y1, 1))
            norm_x2 = max(0, min(norm_x2, 1))
            norm_y2 = max(0, min(norm_y2, 1))
            
            class_id = int(self.class_id_input.get())
            self.boxes.append((norm_x1, norm_y1, norm_x2, norm_y2, class_id))
            
        self.current_box = None
        self.update_canvas()
        self.update_annotations_list()
        
    def draw_preview(self):
        """Draw preview of current box being drawn"""
        self.update_canvas()
        if self.current_box and self.photo_image:
            x1, y1, x2, y2 = self.current_box
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2)
            
    def update_image_info(self):
        """Update image information display"""
        if self.original_image:
            width, height = self.original_image.size
            file_name = os.path.basename(self.image_path)
            info_text = f"File: {file_name}\nSize: {width}x{height}px"
            self.image_label.config(text=info_text)
        else:
            self.image_label.config(text="No image loaded")
            
    def update_annotations_list(self):
        """Update the list of annotations"""
        count = len(self.boxes)
        self.annotations_label.config(text=f"{count} box{'es' if count != 1 else ''}")
        
        # Clear existing box frames
        for widget in self.boxes_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Create individual box entries
        for i, (x1, y1, x2, y2, class_id) in enumerate(self.boxes):
            # Create frame for this box
            box_frame = tk.Frame(self.boxes_scrollable_frame, bg="white", relief="ridge", bd=1)
            box_frame.pack(fill=tk.X, padx=2, pady=2)
            
            # Box info label
            width = x2 - x1
            height = y2 - y1
            text = f"Box {i+1}: Class {class_id}, {width:.3f}x{height:.3f}"
            label = tk.Label(box_frame, text=text, bg="white", anchor="w")
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
            
            # Delete button for this box
            delete_btn = tk.Button(box_frame, text="×", command=lambda idx=i: self.delete_box(idx),
                                  bg="red", fg="white", width=3, font=("Arial", 10, "bold"))
            delete_btn.pack(side=tk.RIGHT, padx=5, pady=2)
            
    def on_box_select(self, event):
        """Handle box selection in listbox"""
        pass  # Can highlight selected box in future enhancement
        
    def delete_box(self, index):
        """Delete a specific box by index"""
        if 0 <= index < len(self.boxes):
            del self.boxes[index]
            self.update_canvas()
            self.update_annotations_list()
            
    def undo_box(self):
        """Undo the last box"""
        if self.boxes:
            self.boxes.pop()
            self.update_canvas()
            self.update_annotations_list()
            
    def clear_all(self):
        """Clear all annotations"""
        if messagebox.askyesno("Clear All", "Clear all annotations for this image?"):
            self.boxes = []
            self.update_canvas()
            self.update_annotations_list()
            
    def save_annotations(self):
        """Save annotations in YOLO format"""
        if not self.image_path:
            messagebox.showwarning("No Image", "Please load an image first")
            return
            
        # Generate output file path
        image_path = Path(self.image_path)
        output_path = image_path.with_suffix('.txt')
        
        # Write YOLO format
        with open(output_path, 'w') as f:
            for x1, y1, x2, y2, class_id in self.boxes:
                # Convert to YOLO format: class_id center_x center_y width height
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                width = x2 - x1
                height = y2 - y1
                
                f.write(f"{int(class_id)} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")
                
        messagebox.showinfo("Success", f"Annotations saved to:\n{output_path}")
        

def main():
    root = tk.Tk()
    app = YOLOLabeller(root)
    root.mainloop()


if __name__ == "__main__":
    main()
