// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', all_posts);
    document.querySelector('#following').addEventListener('click', following);
    document.querySelector('#create_post_form').addEventListener('submit', new_post);

    // By default, load all posts
    all_posts();
    document.addEventListener('click', event => {
        // Find what was clicked on
        const element = event.target;

        // Check if the user clicked on a hide button
        if (element.id === 'username') {

            const username = element.textContent

            profile_page(username);
            console.log(username)
        }
    });




    // Select the submit button and post content to be used later
    const create_post_button = document.querySelector('#create_post_button');
    const post_content = document.querySelector('#post_content');


    // Disable submit button by default:
    create_post_button.disabled = true;

    // Listen for input to be typed into the input field
    post_content.onkeyup = () => {
        if (post_content.value.length > 0) { // Changed 'content' to 'value' to get the input value
            create_post_button.disabled = false;
        } else {
            create_post_button.disabled = true;
        }
    }


});


function load_post(id) {

    fetch(`/all_posts/${id}`)
        .then(response => response.json())
        .then(post => {

            console.log(post);
            document.querySelector('#all-posts-view').style.display = 'none';
            document.querySelector('#form').style.display = 'none';

            // Apply formatting logic to the timestamp once
            const formattedTimestamp = formatPostDate(post['timestamp']);


            document.querySelector('#post-view').innerHTML = `
     <div class="col-3"><strong>${post['created_by']}</strong></div></br>
                <div class="col-6"><div class="row">${post['content']}</div></div>
                <div class="col-3">${formattedTimestamp}</div>
            `;

        })
        .catch(error => {
            console.error('Error fetching post:', error);
        })
}

function all_posts(username) {

    document.querySelector('#all-posts-view').style.display = 'block';
    // document.querySelector('#post-view').style.display = 'none';


    // Load all posts
    const all_post_view = document.querySelector('#all-posts-view');

    // Construct the URL based on whether the username is provided or not
    let url = '/all_posts';
    if (username) {
        url = `/all_posts/${username}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(postsData => {
            all_post_view.innerHTML = ''; // Clear previous posts
            // loop through each post
            console.log(postsData)
            postsData.posts.forEach(post => {

                const newPostElement = document.createElement('div');

                // Apply formatting logic to the timestamp once
                const formattedTimestamp = formatPostDate(post['timestamp']);
                newPostElement.innerHTML = `
                <div class="card" >
                    <div class="px-3 pt-4 pb-2">
                        <div class="d-flex align-items-center justify-content-between">
                            <div class="d-flex align-items-center">
                                <img style="width:50px" class="me-2 avatar-sm rounded-circle"
                                    src="https://api.dicebear.com/6.x/fun-emoji/svg?seed=Mario" alt="Avatar">
                                <div>
                                    <h5 class="card-title mb-0"><a href="#"> ${post['created_by']} </a></h5>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-body ">
                        <div>
                            <p class="fs-6 fw-light text-muted">${post['content']}</p>
                            <div class="d-flex justify-content-between">
                                <div>
                                    <span id="like-image"></span>
                                    <span id = "likes">${post['total_likes'] ? post['total_likes'] : "0"}</span>
                                </div>
                                <div>
                                    <span class="fs-6 fw-light text-muted"> <span class="fas fa-clock"> </span> ${formattedTimestamp} </span>
                                </div>
                            </div>
                        </div>
                        <div id="comment_section">
                           

                        </div>
                    </div>
            `;

                // Like/Unlikelogic
                const buttonLike = document.createElement('button');

                buttonLike.className = post.likes ? " buttonLike fa-solid fa-heart " : "buttonLike fa-regular fa-heart ";

                // Update the button text based on the current post's like status
                buttonLike.innerHTML = post.likes ? "" : "";


                buttonLike.addEventListener('click', function() {


                    // Like button click logic

                    //buttonLike.innerHTML = "Like" ? "Unlike" : "Like"; // update button inner HTML
                    fetch(`/all_posts/${post.id}/like`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                likes: !post.likes
                            })
                        })
                        .then(response => response.json())
                        .then(updatedPost => {

                            // Toggle the like status
                            post.likes = updatedPost.likes;

                            // Update the like count in the HTML
                            const likeCountElement = newPostElement.querySelector('#likes');
                            likeCountElement.textContent = ` ${updatedPost.total_likes}`;

                            buttonLike.innerHTML = post.likes ? "" : "";
                            buttonLike.className = post.likes ? " buttonLike fa-solid fa-heart" : "buttonLike fa-regular fa-heart";
                        })
                        .catch(error => {
                            console.error('Error updating like status:', error);
                        });
                });
                newPostElement.querySelector('#like-image').appendChild(buttonLike);

                const comment_content = document.createElement('textarea');
                const create_comment_button = document.createElement('button')

                // Disable submit button by default:
                create_comment_button.disabled = true;
                // Listen for input to be typed into the input field
                comment_content.onkeyup = () => {
                    if (comment_content.value.length > 0) { // Changed 'content' to 'value' to get the input value
                        create_comment_button.disabled = false;
                    } else {
                        create_comment_button.disabled = true;
                    }
                }

                create_comment_button.addEventListener('click', function(){
                    fetch(`/all_posts/${post.id}/comments`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                comment: comment_content.value
                            })
                        })
                        .then(response => {
                            console.log(response);
                        })
                        .catch(error => {
                            console.error('Error updating like status:', error);
                        });
                });
                newPostElement.querySelector('#comment_section').appendChild(comment_content);
                newPostElement.querySelector('#comment_section').appendChild(create_comment_button);

                all_post_view.appendChild(newPostElement);
                // Create and append a horizontal line after the card
                all_post_view.appendChild(document.createElement('hr'));

            });
        })

    .catch(error => {
        console.error('Error fetching posts:', error);

    });


}

function new_post(event) {


    event.preventDefault(); // Prevent the form from submitting

    console.log("New post function called");

    const submit = document.querySelector('#submit');
    const newPost = document.querySelector('#post_content');

    document.querySelector('#all-posts-view').style.display = 'block';



    fetch('/new_post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: newPost.value,
                headers: {
                    'Content-Type': 'application/json' // Set the content type to JSON
                }
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log("Fetch request completed");
            document.querySelector('#alert').innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert" id="success">
                    Idea created Successfully
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `
            return response.json();

        })
        .then(result => {
            // Print result
            console.log(result);
            // Clear out input field:
            newPost.value = '';

            // Disable the submit button again:
            submit.disabled = true;
            console.log("all posts called");
            all_posts();

        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });

}

function formatPostDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };

    const postDate = new Date(dateString);
    const formattedDate = postDate.toLocaleDateString(undefined, options);
    return formattedDate;
}


function profile_page(username) {

    ////TODO

    all_posts(username);


    document.querySelector('#all-posts-view').style.display = 'block';
    document.querySelector('#form').style.display = 'none';

    fetch(`/profile_page/${username}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const user = data.user;

            const followersCountElement = document.createElement('div');
            followersCountElement.className = 'm-3';
            followersCountElement.innerHTML = `
            <div class="profile-container ">
                <h2 class="user col-8 col-sm-7">${user.username}</h2>
                <span class="follow col-8 col-sm-2">Following: ${user.following}</span>
                <span class="follow col-8 col-sm-2">Followers: ${user.followers}</span>
            </div>

            `;


            const followers = document.querySelector('#followers');

            followers.appendChild(followersCountElement);



        })

    .catch(error => {
        console.error('Error fetching user data:', error);
    });




    /*const buttonfollow = document.createElement('button');       
    buttonfollow.className = post.follow ? "d-grid gap-2 d-md-flex justify-content-md-end btn btn-outline-info my-2 " : "d-grid gap-2 d-md-flex justify-content-md-end btn btn-primary my-2";
    // Update the button text based on the current post's like status
    buttonLike.innerHTML = post.follow ? "Unfollow" : "follow";*/


}