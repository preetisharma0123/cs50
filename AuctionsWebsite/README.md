# Auctions Website
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”


## Features Developed

- Create Listing: Create a new listing with a title for the listing, a text-based description, and what the starting bid should be,a URL for an image for the listing and a category (e.g. Fashion, Toys, Electronics, Home, etc.).
- Active Listings Page: The default route of the web application, lets users view all of the currently active auction listings. For each active listing, this page displays the title, description, current price, and photo (if one exists for the listing).
- Listing Page: Clicking on a specific listing will direct users to a dedicated page tailored to that listing. Here, users can access all pertinent details about the listing, including the current bidding price.
- If the user is signed in, they can add the item to their "Watchlist." If the item is already in their watchlist, they can remove it.
- Signed-in users also have the option to place bids on the item. The bid must meet or exceed the starting bid and surpass any existing bids (if applicable). If the bid doesn't meet these criteria, the user will receive an error message.
- Additionally, if the signed-in user is the creator of the listing, they can choose to "close" the auction from this page. This action will declare the highest bidder as the auction winner and deactivate the listing.
- On a closed listing page, if a signed-in user has won the auction, the page will confirm their victory.
- Users who are signed in have the ability to leave comments on the listing page. The listing page will display all comments posted by users.
- Watchlist: Signed-in users can navigate to their Watchlist page, which will present a collection of all listings they've added to their watchlist. Clicking on any of these listings will direct users to the respective listing's page.
- Categories: Users can access a dedicated page showcasing a list of all available listing categories. Clicking on the name of any category will take users to a page displaying all active listings within that specific category.
- Django Admin Interface: Through the Django admin interface, site administrators have the capability to view, add, edit, and delete listings, comments, and bids across the entire site.

## Concepts Learned

- SQL
- Django Models
- Django admin

## Demo
![](./demo.gif) 
