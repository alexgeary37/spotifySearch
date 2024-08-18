import tkinter as tk
from tkinter import messagebox
from search_logic import search_for_artists_by_popularity
import threading

def on_search_click(keyword_entry, min_popularity_entry, max_popularity_entry, results_text, loading_label):
    def perform_search():
        try:
            keyword = keyword_entry.get()
            min_popularity = int(min_popularity_entry.get())
            max_popularity = int(max_popularity_entry.get())

            # Clear the text area as soon as the search button is pressed
            results_text.delete(1.0, tk.END)

            if keyword == "":
                messagebox.showerror("Input Error", "Please enter a keyword.")
                loading_label.grid_remove()  # Hide loading indicator
                return

            # Show the loading indicator
            loading_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            results = search_for_artists_by_popularity(keyword, min_popularity, max_popularity)

            if not results:
                results_text.insert(tk.END, "No artists found within the specified popularity range.\n")
            else:
                for result in results:
                    results_text.insert(tk.END, f"Artist: {result['name']}, Popularity: {result['popularity']}, URL: {result['url']}\n")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for popularity.")
        finally:
            loading_label.grid_remove()  # Hide loading indicator after search is done

    # Run the search in a separate thread to keep the UI responsive
    search_thread = threading.Thread(target=perform_search)
    search_thread.start()


def create_ui():
    root = tk.Tk()
    root.title("Spotify Artist Search by Popularity")

    # Apply dark theme colors
    root.configure(bg='#2E2E2E')  # Background color

    # Configure grid to make widgets grow with the window
    root.grid_rowconfigure(5, weight=1)  # Row for the results_text
    root.grid_columnconfigure(1, weight=1)  # Column for the entry fields and text area

    # Style settings for the dark theme
    label_bg_color = '#2E2E2E'  # Background color for labels
    label_fg_color = '#FFFFFF'  # Text color for labels
    entry_bg_color = '#3C3C3C'  # Background color for entry fields
    entry_fg_color = '#FFFFFF'  # Text color for entry fields
    button_bg_color = '#4C4C4C'  # Background color for the button
    button_fg_color = '#FFFFFF'  # Text color for the button
    text_bg_color = '#1E1E1E'  # Background color for the text area
    text_fg_color = '#FFFFFF'  # Text color for the text area

    # Keyword input
    tk.Label(root, text="Keyword:", bg=label_bg_color, fg=label_fg_color).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    keyword_entry = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
    keyword_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Minimum popularity input
    tk.Label(root, text="Min Popularity:", bg=label_bg_color, fg=label_fg_color).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    min_popularity_entry = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
    min_popularity_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Maximum popularity input
    tk.Label(root, text="Max Popularity:", bg=label_bg_color, fg=label_fg_color).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    max_popularity_entry = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
    max_popularity_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Search button
    search_button = tk.Button(root, text="Search", bg=button_bg_color, fg=button_fg_color,
                              command=lambda: on_search_click(keyword_entry, min_popularity_entry, max_popularity_entry, results_text, loading_label))
    search_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Text area to display results
    results_text = tk.Text(root, height=15, width=80, bg=text_bg_color, fg=text_fg_color, insertbackground=text_fg_color)
    results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Loading indicator
    loading_label = tk.Label(root, text="Loading...", bg=label_bg_color, fg=label_fg_color)
    loading_label.grid_remove()  # Hide initially

    # Run the application
    root.mainloop()
