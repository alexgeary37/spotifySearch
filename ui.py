import tkinter as tk
from tkinter import messagebox
from search_logic import search_for_artists_by_popularity
import threading

def on_search_click(keyword_entry, popularity_entry, start_offset_entry, results_text, loading_label):
    def perform_search():
        try:
            keyword = keyword_entry.get()
            popularity_setting = int(popularity_entry.get())
            start_offset = int(start_offset_entry.get())

            # Clear the text area as soon as the search button is pressed
            results_text.delete(1.0, tk.END)

            if keyword == "":
                messagebox.showerror("Input Error", "Please enter a keyword.")
                loading_label.grid_remove()  # Hide loading indicator
                return
            
            if start_offset > 9999:
                messagebox.showerror("Input Error", "Please enter an offset < 9999.")
                loading_label.grid_remove()  # Hide loading indicator
                return

            # Show the loading indicator
            loading_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            results = search_for_artists_by_popularity(keyword, popularity_setting, start_offset)

            # If no results are found, give this message
            if not results:
                results_text.insert(tk.END, "No artists found with the specified popularity.\n")
            else:
                filename = f"{results[0]['keyword']}_pop_{results[0]['popularity']}_offset_{results[0]['start_offset']}.tsv"
                with open(filename, mode='w', newline='', encoding='utf-8') as file:
                    # Write header for the TSV file
                    file.write(f"Keyword-{results[0]['keyword']}\tPopularity-{results[0]['popularity']}\tStart Offset-{results[0]['start_offset']}\n")
                    # file.write(f"{results[0]['keyword']}\t{results[0]['popularity']}\t{results[0]['start_offset']}\t\t\t\n")
                    
                    file.write("Artist\tArtist Popularity\tURL\n")
                    # Start writing artist results from the second entry onwards
                    index = 1
                    for result in results[1:]:
                        # Write each artist's information into the TSV file
                        file.write(f"{result['name']}\t{result['popularity']}\t{result['url']}\n")
                        index += 1

                    # Optional: Provide user feedback or display in UI (e.g., Tkinter text box)
                    results_text.insert(tk.END, f"Data written to {filename}\n")


        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for popularity.")
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
    keyword_entry.focus_set()

    # Popularity input
    tk.Label(root, text="Popularity:", bg=label_bg_color, fg=label_fg_color).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    popularity_entry = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
    popularity_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Start offset input
    tk.Label(root, text="Start Offset:", bg=label_bg_color, fg=label_fg_color).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    start_offset_entry = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
    start_offset_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Search button
    search_button = tk.Button(root, text="Search", bg=button_bg_color, fg=button_fg_color,
                              command=lambda: on_search_click(keyword_entry, popularity_entry, start_offset_entry, results_text, loading_label))
    search_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Text area to display results
    results_text = tk.Text(root, height=15, width=80, bg=text_bg_color, fg=text_fg_color, insertbackground=text_fg_color)
    results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Loading indicator
    loading_label = tk.Label(root, text="Loading...", bg=label_bg_color, fg=label_fg_color)
    loading_label.grid_remove()  # Hide initially

    # Run the application
    root.mainloop()
