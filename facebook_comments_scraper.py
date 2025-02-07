# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:32:50 2024

@author: haifa
"""

import re
import csv
import tkinter as tk
from tkinter import messagebox, ttk
import facebook_scraper as fs

def validate_post_id(post_id):
    # Regular expression to match the expected Post ID format
    pattern = r'^%2F[^\s]+%2Fposts%2F[pP][fF][bB][iI][dD][0-9a-zA-Z]+&$'
    return re.match(pattern, post_id)

def scrape_comments():
    # Get input values from the entry fields
    post_id = post_id_entry.get()
    max_comments = int(max_comments_entry.get())
    csv_filename = filename_entry.get()

    # Validate Post ID format
    if not validate_post_id(post_id):
        messagebox.showerror("Error", "Invalid Post ID format. Please enter a valid Post ID.")
        return

    # Add .csv extension if not provided by the user
    if not csv_filename.endswith('.csv'):
        csv_filename += '.csv'

    try:
        # Get the post (this gives a generator)
        gen = fs.get_posts(post_urls=[post_id], options={"comments": max_comments, "progress": True})

        # Take the first element of the generator which is the post we requested
        post = next(gen)

        # Check if the 'comments_full' key exists in the post object
        if 'comments_full' not in post:
            messagebox.showerror("Error", "The structure of the provided Post ID is incomplete. Comments data could not be retrieved.")
            return

        # Extract the comments part
        comments = post['comments_full']

        # Open the CSV file in write mode
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define fieldnames for the CSV file
            fieldnames = ['Comment', 'Reply']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Process comments and replies
            for comment in comments:
                # Write comment to CSV
                writer.writerow({'Comment': comment['comment_text'], 'Reply': ''})

                # Process replies
                for reply in comment['replies']:
                    # Write reply to CSV
                    writer.writerow({'Comment': '', 'Reply': reply['comment_text']})

        messagebox.showinfo("Success", "Comments scraped successfully and saved to '{}'.".format(csv_filename))
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: {}".format(str(e)))

# Create the main window
root = tk.Tk()
root.title("Facebook Comments Scraper")

# Set window size
root.geometry("600x250")

# Increase font size for text and tabs
font_style = ("Arial", 12)

# Create and pack widgets
tk.Label(root, text="Enter the POST_ID from the URL of the post (e.g., '%2FgroupName%2Fposts%2Fpfbid...&').", font=font_style).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
tk.Label(root, text="Post ID:", font=font_style).grid(row=1, column=0, sticky="w", padx=5, pady=5)
post_id_entry = tk.Entry(root, width=50, font=font_style)
post_id_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Max Comments:", font=font_style).grid(row=2, column=0, sticky="w", padx=5, pady=5)
max_comments_entry = tk.Entry(root, font=font_style)
max_comments_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="CSV Filename:", font=font_style).grid(row=3, column=0, sticky="w", padx=5, pady=5)
filename_entry = tk.Entry(root, font=font_style)
filename_entry.grid(row=3, column=1, padx=5, pady=5)

scrape_button = tk.Button(root, text="Scrape Comments", command=scrape_comments, font=font_style)
scrape_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
