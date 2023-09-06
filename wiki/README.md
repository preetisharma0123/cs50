# Wikipedia like online encyclopedia
Design a Wikipedia-like online encyclopedia.

** Disclaimer: The project provided with utility functions for conversion of Markdown to HTML and 

## Features Developed

Description: Developed an encyclopedia web application using Django and Python, meeting the following key requirements:

- Entry Page: Implemented the functionality to display the contents of encyclopedia entries when users visit /wiki/TITLE, where TITLE is the entry title.
- Error Handling: Designed error pages to inform users if an entry doesn't exist or if an incorrect URL is provided.
- Index Page: Enhanced index.html to enable users to click on entry names for direct access to entry pages.
- Search: Enabled users to search for entries via a search box in the sidebar, redirecting to the relevant entry or displaying search results.
- New Page: Allowed users to create new encyclopedia entries with titles and Markdown content, ensuring no duplicates exist.
- Edit Page: Provided a user-friendly interface for editing entry content with pre-populated Markdown content.
- Random Page: Added a "Random Page" feature to navigate users to a random encyclopedia entry.
- Markdown to HTML Conversion: Integrated python-markdown2 package for converting Markdown content to HTML on entry pages.

## Technical Learnings:

- Django forms
- Django url to function mapping
- HTML Page Rendering
- Error handling
