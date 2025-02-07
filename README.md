# Facebook Comments Scraper

## Overview
This script is a GUI-based Facebook Comments Scraper using Python, built with the `facebook_scraper` library and `tkinter` for the user interface. The script allows users to input a Facebook post ID, specify the number of comments to scrape, and save the extracted comments and replies to a CSV file.

## Features
- **Post ID Validation**: Ensures the entered post ID follows the expected format using regular expressions.
- **GUI Interface**: Built using `tkinter` for ease of use.
- **Comment Scraping**: Uses `facebook_scraper` to retrieve comments from a Facebook post.
- **CSV Export**: Saves comments and replies in a structured CSV file.
- **Error Handling**: Displays appropriate error messages for incorrect inputs or failures in data retrieval.

## Requirements
Ensure you have the following dependencies installed before running the script:

```bash
pip install facebook_scraper
```

## Usage
1. Run the script to open the GUI.
2. Enter the Facebook post ID in the specified format (e.g., `%2FgroupName%2Fposts%2Fpfbid...&`).
3. Specify the maximum number of comments to scrape.
4. Provide a filename for the CSV output.
5. Click the **Scrape Comments** button to begin the scraping process.
6. The extracted comments and replies will be saved to the specified CSV file.

## Code Breakdown
### **1. Validate Post ID**
The function `validate_post_id(post_id)` ensures the user inputs a correctly formatted post ID.

```python
def validate_post_id(post_id):
    pattern = r'^%2F[^\s]+%2Fposts%2F[pP][fF][bB][iI][dD][0-9a-zA-Z]+&$'
    return re.match(pattern, post_id)
```

### **2. Scrape Facebook Comments**
The function `scrape_comments()` retrieves comments and replies using `facebook_scraper`, processes the data, and saves it to a CSV file.

```python
def scrape_comments():
    post_id = post_id_entry.get()
    max_comments = int(max_comments_entry.get())
    csv_filename = filename_entry.get()

    if not validate_post_id(post_id):
        messagebox.showerror("Error", "Invalid Post ID format. Please enter a valid Post ID.")
        return

    if not csv_filename.endswith('.csv'):
        csv_filename += '.csv'

    try:
        gen = fs.get_posts(post_urls=[post_id], options={"comments": max_comments, "progress": True})
        post = next(gen)

        if 'comments_full' not in post:
            messagebox.showerror("Error", "The structure of the provided Post ID is incomplete. Comments data could not be retrieved.")
            return

        comments = post['comments_full']

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Comment', 'Reply']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for comment in comments:
                writer.writerow({'Comment': comment['comment_text'], 'Reply': ''})
                for reply in comment['replies']:
                    writer.writerow({'Comment': '', 'Reply': reply['comment_text']})

        messagebox.showinfo("Success", "Comments scraped successfully and saved to '{}'".format(csv_filename))
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: {}".format(str(e)))
```

### **3. User Interface**
A `tkinter` GUI is implemented to allow users to input necessary parameters easily.

```python
root = tk.Tk()
root.title("Facebook Comments Scraper")
root.geometry("600x250")
```

#### **Input Fields**
- Post ID
- Max Comments
- CSV Filename

#### **Button to Start Scraping**
```python
scrape_button = tk.Button(root, text="Scrape Comments", command=scrape_comments, font=font_style)
scrape_button.grid(row=4, column=0, columnspan=2, pady=10)
```

## Expected Output
The extracted comments will be saved in a CSV file with the following structure:

| Comment | Reply |
|---------|-------|
| Main Comment 1 |   |
|   | Reply 1 to Comment 1 |
|   | Reply 2 to Comment 1 |
| Main Comment 2 |   |
|   | Reply 1 to Comment 2 |

## Notes
- Ensure that the Facebook post is **public** to scrape comments successfully.
- Scraping Facebook data should be done in compliance with Facebook's terms of service.

## Future Improvements
- Add support for logging scraped data.
- Improve error handling and debugging tools.
- Implement pagination handling for large comment sections.
