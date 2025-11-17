"""Main GUI application for batch image cropping."""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
from image_processor import batch_process_images


class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Image Cropper & Mirrorer")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.processing = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="Batch Image Cropper & Mirrorer", 
                         font=("Helvetica", 14, "bold"))
        title.pack(pady=(0, 10))
        
        # Input folder section
        ttk.Label(main_frame, text="Input Folder:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Entry(input_frame, textvariable=self.input_folder, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(input_frame, text="Browse", command=self._browse_input).pack(side=tk.LEFT)
        
        # Output folder section
        ttk.Label(main_frame, text="Output Folder:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Entry(output_frame, textvariable=self.output_folder, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self._browse_output).pack(side=tk.LEFT)
        
        # Crop values section
        ttk.Label(main_frame, text="Crop Pixel Values:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        values_frame = ttk.Frame(main_frame)
        values_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create spinboxes for each direction
        self.top_var = tk.IntVar(value=0)
        self.bottom_var = tk.IntVar(value=0)
        self.left_var = tk.IntVar(value=0)
        self.right_var = tk.IntVar(value=0)
        
        # Top
        ttk.Label(values_frame, text="Top:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(values_frame, from_=0, to=500, textvariable=self.top_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Bottom
        ttk.Label(values_frame, text="Bottom:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(values_frame, from_=0, to=500, textvariable=self.bottom_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Left
        ttk.Label(values_frame, text="Left:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(values_frame, from_=0, to=500, textvariable=self.left_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Right
        ttk.Label(values_frame, text="Right:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(values_frame, from_=0, to=500, textvariable=self.right_var, width=10).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Info text
        info_text = "Specify the number of pixels to crop from each side.\nThose pixels will be mirrored to the opposite side."
        ttk.Label(main_frame, text=info_text, foreground="gray", font=("Helvetica", 9)).pack(anchor=tk.W, pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="blue")
        self.status_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Log area
        ttk.Label(main_frame, text="Processing Log:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=70, yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Process Images", command=self._process_images)
        self.process_button.pack(fill=tk.X, pady=(0, 5))
        
        # Clear button
        ttk.Button(main_frame, text="Clear Log", command=self._clear_log).pack(fill=tk.X)
    
    def _browse_input(self):
        """Browse for input folder."""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
    
    def _browse_output(self):
        """Browse for output folder."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def _log(self, message):
        """Add message to log."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def _clear_log(self):
        """Clear log text."""
        self.log_text.delete("1.0", tk.END)
    
    def _progress_callback(self, current, total, filename):
        """Update progress during processing."""
        self.progress["value"] = (current / total) * 100
        self.status_label.config(text=f"Processing: {filename} ({current}/{total})")
        self.root.update_idletasks()
    
    def _process_images(self):
        """Process images in background thread."""
        if self.processing:
            messagebox.showwarning("Warning", "Processing already in progress!")
            return
        
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select an input folder")
            return
        
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        # Validate that input folder exists and has images
        input_path = Path(self.input_folder.get())
        if not input_path.exists():
            messagebox.showerror("Error", "Input folder does not exist")
            return
        
        # Disable button and start processing in thread
        self.process_button.config(state=tk.DISABLED)
        self.processing = True
        self.progress["value"] = 0
        self._clear_log()
        self._log("Starting batch processing...")
        
        thread = threading.Thread(target=self._process_thread)
        thread.start()
    
    def _process_thread(self):
        """Background thread for image processing."""
        try:
            top = self.top_var.get()
            bottom = self.bottom_var.get()
            left = self.left_var.get()
            right = self.right_var.get()
            
            if top == 0 and bottom == 0 and left == 0 and right == 0:
                self._log("Warning: All crop values are 0. No changes will be made.")
            
            self._log(f"Crop settings - Top: {top}, Bottom: {bottom}, Left: {left}, Right: {right}")
            self._log("")
            
            successful, failed, errors = batch_process_images(
                self.input_folder.get(),
                self.output_folder.get(),
                top_pixels=top,
                bottom_pixels=bottom,
                left_pixels=left,
                right_pixels=right,
                progress_callback=self._progress_callback,
            )
            
            self._log("")
            self._log(f"Processing complete!")
            self._log(f"Successful: {successful}")
            self._log(f"Failed: {failed}")
            
            if errors:
                self._log("")
                self._log("Errors:")
                for error in errors:
                    self._log(f"  - {error}")
            
            self.status_label.config(text=f"Complete - {successful} successful, {failed} failed", foreground="green")
            messagebox.showinfo("Complete", f"Batch processing complete!\n\nSuccessful: {successful}\nFailed: {failed}")
        
        except Exception as e:
            self._log(f"Error: {str(e)}")
            self.status_label.config(text="Error occurred", foreground="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.processing = False
            self.process_button.config(state=tk.NORMAL)
            self.progress["value"] = 0


def main():
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
