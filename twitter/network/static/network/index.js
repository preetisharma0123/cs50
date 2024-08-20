// Wait for page to load
document.addEventListener('DOMContentLoaded', function () {
    // Use buttons to toggle between views
    document.querySelector('#all_posts').addEventListener('click', all_posts);
    document.querySelector('#view-profile').addEventListener('click', profile_page);
    document.querySelector('#my-feed').addEventListener('click', following);

    // By default, load all posts
    // all_posts('following');
    const profile = document.querySelector("#view-profile")
    username = profile.attributes['username'].nodeValue
    all_posts('following')
    // Select the submit button and post content to be used later
    const create_post_button = document.querySelector('#create_post_button');
    const post_content = document.querySelector('#post_content');

    // Disable submit button by default:
    create_post_button.disabled = true;

    // Listen for input to be typed into the input field
    post_content.onkeyup = () => {
        create_post_button.disabled = post_content.value.length === 0;
    }
    loadTrendingHashtags();
    load_profile();
});

function load_profile(username) {
    logged_in_user = document.querySelector("#view-profile").attributes['username'].nodeValue;
    if (!username) {
        username = logged_in_user;
    }
    fetch(`/profile_page/${username}`)
        .then(response => response.json())
        .then(profile => {
            console.log(profile);
            const element = document.querySelector('#profile-container');
            const isFollowing = profile.is_following ? 'Unfollow' : 'Follow';
            const followButtonHtml = `
                <button class="btn btn-primary" id="follow-btn" data-username="${username}">
                    <i class="fa ${profile.is_following ? 'fa-solid fa-user-minus' : 'fa-solid fa-user-plus'}"></i> ${isFollowing}
                </button>
            `;
            element.innerHTML = `
                <div class="card-body py-5">
                    <div class="d-flex justify-content-center mb-3">
                        <img src="https://api.dicebear.com/6.x/fun-emoji/svg" alt="Profile Image" class="rounded-circle" style="width: 120px; height: 120px; object-fit: cover;">
                    </div>
                    <h5 class="card-title mb-2">@${profile.username}</h5>
                    <div class="d-flex justify-content-around">
                        <div>
                            <h6 class="card-subtitle mb-2 text-muted">Followers</h6>
                            <p class="card-text">${profile.followers}</p>
                        </div>
                        <div>
                            <h6 class="card-subtitle mb-2 text-muted">Following</h6>
                            <p class="card-text">${profile.following}</p>
                        </div>
                    </div>
                    ${logged_in_user !== profile.username ? followButtonHtml : ''}
                </div>
            `;

            // Add event listener to follow/unfollow button
            const followButton = document.querySelector('#follow-btn');
            if (followButton) {
                followButton.addEventListener('click', () => {
                    const action = profile.is_following ? 'unfollow' : 'follow';
                    fetch(`/follow/${action}/${username}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') // Assuming you have a function to get the CSRF token
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            load_profile(username); // Reload profile to update button state
                        } else {
                            console.error('Error:', data.error);
                        }
                    });
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie's name matches the one we're looking for
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// function load_profile(username) {
//     const loggedInUser = document.querySelector("#view-profile").attributes['username'].nodeValue;
//     if (!username) {
//         username = loggedInUser;
//     }
    
//     fetch(`/profile_page/${username}`)
//         .then(response => response.json())
//         .then(profile => {
//             console.log(profile);
//             const element = document.querySelector('#profile-container');
            
//             // Determine the follow button's icon based on the `is_following` value
//             let followButtonIcon = profile.is_following ? 
//                 '<i class="fas fa-user-check"></i>' : 
//                 '<i class="far fa-user-plus"></i>';
            
//             // Only show the follow button if the profile is not the logged-in user
//             const followButton = (username !== loggedInUser) ? 
//                 `<button class="btn btn-outline-primary mt-3" id="follow-button" data-username="${username}">
//                     ${followButtonIcon} Follow
//                 </button>` 
//                 : '';

//             element.innerHTML = `
//                 <div class="card-body py-5">
//                     <div class="d-flex justify-content-center mb-3">
//                         <img src="https://api.dicebear.com/6.x/fun-emoji/svg" alt="Profile Image" class="rounded-circle" style="width: 120px; height: 120px; object-fit: cover;">
//                     </div>
//                     <h5 class="card-title mb-2">@${profile.username}</h5>
//                     <div class="d-flex justify-content-around">
//                         <div>
//                             <h6 class="card-subtitle mb-2 text-muted">Followers</h6>
//                             <p class="card-text">${profile.followers}</p>
//                         </div>
//                         <div>
//                             <h6 class="card-subtitle mb-2 text-muted">Following</h6>
//                             <p class="card-text">${profile.following}</p>
//                         </div>
//                     </div>
//                     ${followButton}
//                 </div>
//             `;

//             // Add event listener to the follow button
//             const followButtonElement = document.querySelector('#follow-button');
//             if (followButtonElement) {
//                 followButtonElement.addEventListener('click', () => {
//                     // Perform follow/unfollow action
//                     followUser(username);
//                 });
//             }
//         });
// }

function followUser(username) {
    fetch(`/follow/${username}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()  // Add CSRF token if needed
        },
        body: JSON.stringify({})  // You may send additional data if needed
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Reload the profile to update the follow status
            load_profile(username);
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCsrfToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)')?.pop() || '';
    return cookieValue;
}

function loadTrendingHashtags() {
    fetch('/trending_hashtags')
        .then(response => response.json())
        .then(data => {
            const trendingHashtagsContainer = document.querySelector('#trending-hashtags');
            trendingHashtagsContainer.innerHTML = ''; // Clear previous hashtags

            data.trending_hashtags.forEach(hashtag => {
                const hashtagElement = document.createElement('span');
                hashtagElement.id = "hashtag"
                hashtagElement.className = 'badge bg-secondary buttonLike';
                hashtagElement.textContent = `${hashtag.hashtag} (${hashtag.num_posts})`;
                hashtagElement.setAttribute('tag', hashtag.hashtag.replace("#", ''));
                hashtagElement.addEventListener('click', hashtag_posts)
                trendingHashtagsContainer.appendChild(hashtagElement);
            });
        })
        .catch(error => {
            console.error('Error fetching trending hashtags:', error);
        });
}

function load_post(id) {
    fetch(`/all_posts/${id}`)
        .then(response => response.json())
        .then(post => {
            console.log(post);
            document.querySelector('#all-posts-view').style.display = 'none';
            document.querySelector('#form').style.display = 'none';

            const formattedTimestamp = formatPostDate(post.timestamp);

            document.querySelector('#post-view').innerHTML = `
                <div class="col-3"><strong>${post.created_by}</strong></div></br>
                <div class="col-6"><div class="row">${post.content}</div></div>
                <div class="col-3">${formattedTimestamp}</div>
            `;
        })
        .catch(error => {
            console.error('Error fetching post:', error);
        });
}

function all_posts(username) {
    document.querySelector('#all-posts-view').style.display = 'block';
    document.querySelector('#create_post_form').addEventListener('submit', new_post);
    loadingMessage = document.querySelector('#loading_message');


    const all_post_view = document.querySelector('#all-posts-view');
    let url = '/all_posts';
    if (username) {
        console.log(username)
        url = `/all_posts/${username}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(postsData => {
            all_post_view.innerHTML = ''; // Clear previous posts
            if (postsData.posts.length === 0) {
                if (username === 'following') {
                    loadingMessage.innerHTML = '<span class="text-muted">Follow users to load content!</span>';
                } else {
                    loadingMessage.innerHTML = '<span class="text-muted">Share your first idea in the box above!</span>';
                }
                loadingMessage.classList.add('fade-in');
            } else {
                postsData.posts.forEach(post => {
                    const newPostElement = createPostElement(post);
                    all_post_view.appendChild(newPostElement);
                    all_post_view.appendChild(document.createElement('hr'));
                });
                loadingMessage.display = "None"
            }
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });
}

function all_posts_hashtag(hashtag) {
    document.querySelector('#all-posts-view').style.display = 'block';
    document.querySelector('#create_post_form').addEventListener('submit', new_post);

    const all_post_view = document.querySelector('#all-posts-view');
    let url = `/all_posts_hashtag/${hashtag}`;

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(postsData => {
            all_post_view.innerHTML = ''; // Clear previous posts
            console.log(postsData);
            postsData.posts.forEach(post => {
                const newPostElement = createPostElement(post);
                all_post_view.appendChild(newPostElement);
                all_post_view.appendChild(document.createElement('hr'));
            });
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });
}

function createPostElement(post) {
    const newPostElement = document.createElement('div');
    const formattedTimestamp = formatPostDate(post.timestamp);
    
    newPostElement.innerHTML = `
        <div class="card">
            <div class="px-3 pt-4 pb-2">
                <div class="d-flex align-items-center justify-content-between">
                    <div class="d-flex align-items-center">
                        <img style="width:50px" class="me-2 avatar-sm rounded-circle"
                            src="https://api.dicebear.com/6.x/fun-emoji/svg?seed=Mario" alt="Avatar">
                        <div>
                            <h5 class="card-title mb-0">
                                <a href="#" class="post-creator" data-username="${post.created_by}">${post.created_by}</a>
                            </h5>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <div>
                    <p class="fs-6 fw-light text-muted">${post.content}</p>
                    <div id="hashtags" class="mb-2"></div> <!-- Hashtags will be added here -->
                    <div class="d-flex justify-content-between">
                        <div>
                            <span id="like-image"></span>
                            <span id="likes">${post.total_likes || "0"}</span>
                            <span id="comments-image" class="fa-solid fa-message"></span>
                            <span id="comments">${post.total_comments || "0"}</span>
                        </div>
                        <div>
                            <span class="fs-6 fw-light text-muted">
                                <span class="fas fa-clock"></span> ${formattedTimestamp}
                            </span>
                        </div>
                    </div>
                </div>
                <div id="comment_section"></div>
                <div id="comment_list"></div>
            </div>
        </div>
    `;

    const buttonLike = createLikeButton(post, newPostElement);
    newPostElement.querySelector('#like-image').appendChild(buttonLike);

    const commentSection = createCommentSection(post, newPostElement);
    newPostElement.querySelector('#comment_section').appendChild(commentSection.comment_content);
    newPostElement.querySelector('#comment_section').appendChild(commentSection.create_comment_button);

    loadComments(post.id, newPostElement.querySelector('#comment_list'), 1, 3);

    const expandButton = document.createElement('button');
    expandButton.innerHTML = "Expand";
    expandButton.className = "btn btn-secondary btn-sm my-2";
    expandButton.addEventListener('click', () => {
        openPostModal(post);
    });

    newPostElement.querySelector('.card-body').appendChild(expandButton);

    // Add hashtags to the post
    const hashtagsContainer = newPostElement.querySelector('#hashtags');
    post.hashtags.forEach(hashtag => {
        const hashtagElement = document.createElement('span');
        hashtagElement.className = 'badge bg-primary me-1';
        hashtagElement.innerText = `${hashtag}`;
        hashtagsContainer.appendChild(hashtagElement);
    });

    // Add click event to the post creator's name
    const postCreatorElement = newPostElement.querySelector('.post-creator');
    postCreatorElement.addEventListener('click', (event) => {
        event.preventDefault();
        const username = postCreatorElement.getAttribute('data-username');
        load_profile(username);
        // Optionally, if you want to show the posts of the clicked user
        all_posts(username);
    });

    return newPostElement;
}


// function createPostElement(post) {
//     const newPostElement = document.createElement('div');
//     const formattedTimestamp = formatPostDate(post.timestamp);
//     newPostElement.innerHTML = `
//         <div class="card">
//             <div class="px-3 pt-4 pb-2">
//                 <div class="d-flex align-items-center justify-content-between">
//                     <div class="d-flex align-items-center">
//                         <img style="width:50px" class="me-2 avatar-sm rounded-circle"
//                             src="https://api.dicebear.com/6.x/fun-emoji/svg?seed=Mario" alt="Avatar">
//                         <div>
//                             <h5 class="card-title mb-0"><a href="#">${post.created_by}</a></h5>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//             <div class="card-body">
//                 <div>
//                     <p class="fs-6 fw-light text-muted">${post.content}</p>
//                     <div class="d-flex justify-content-between">
//                         <div>
//                             <span id="like-image"></span>
//                             <span id="likes">${post.total_likes || "0"}</span>
//                             <span id="comments-image" class="fa-solid fa-message"></span>
//                             <span id="comments">${post.total_comments || "0"}</span>
//                         </div>
//                         <div>
//                             <span class="fs-6 fw-light text-muted">
//                                 <span class="fas fa-clock"></span> ${formattedTimestamp}
//                             </span>
//                         </div>
//                     </div>
//                 </div>
//                 <div id="comment_section"></div>
//                 <div id="comment_list"></div>
//             </div>
//         </div>
//     `;

//     const buttonLike = createLikeButton(post, newPostElement);
//     newPostElement.querySelector('#like-image').appendChild(buttonLike);

//     const commentSection = createCommentSection(post, newPostElement);
//     newPostElement.querySelector('#comment_section').appendChild(commentSection.comment_content);
//     newPostElement.querySelector('#comment_section').appendChild(commentSection.create_comment_button);

//     loadComments(post.id, newPostElement.querySelector('#comment_list'), 1, 3);

//     const expandButton = document.createElement('button');
//     expandButton.innerHTML = "Expand";
//     expandButton.className = "btn btn-secondary btn-sm my-2";
//     expandButton.addEventListener('click', () => {
//         openPostModal(post);
//     });

//     newPostElement.querySelector('.card-body').appendChild(expandButton);


//     return newPostElement;
// }

function createLikeButton(post, newPostElement) {
    const buttonLike = document.createElement('button');
    buttonLike.className = post.likes ? "buttonLike fa-solid fa-heart" : "buttonLike fa-regular fa-heart";

    buttonLike.addEventListener('click', function () {
        fetch(`/all_posts/${post.id}/like`, {
            method: 'PUT',
            body: JSON.stringify({ likes: !post.likes })
        })
            .then(response => response.json())
            .then(updatedPost => {
                post.likes = updatedPost.likes;
                const likeCountElement = newPostElement.querySelector('#likes');
                likeCountElement.textContent = updatedPost.total_likes;
                buttonLike.className = post.likes ? "buttonLike fa-solid fa-heart" : "buttonLike fa-regular fa-heart";
            })
            .catch(error => {
                console.error('Error updating like status:', error);
            });
    });

    return buttonLike;
}

function loadComments(postId, commentSection, page, perPage) {
    fetch(`/all_posts/${postId}/comments?page=${page}&per_page=${perPage}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing comments before appending new ones
            const existingComments = commentSection.querySelectorAll('.comment');
            existingComments.forEach(comment => comment.remove());
            
            // Append new comments from the server
            data.comments.forEach(comment => {
                const commentElement = document.createElement('div');
                commentElement.className = "comment card p-2 mb-2 ms-3"; // Added classes for styling
                commentElement.innerHTML = `
                    <div class="d-flex">
                        <div class="avatar-sm me-2">
                            <img style="width:30px" class="rounded-circle"
                                src="https://api.dicebear.com/6.x/fun-emoji/svg?seed=${comment.created_by}" alt="Avatar">
                        </div>
                        <div>
                            <h6 class="mb-0">${comment.created_by}</h6>
                            <p class="fs-6 fw-light text-muted mb-0">${comment.text}</p>
                            <span class="fs-6 fw-light text-muted"><span class="fas fa-clock"></span> ${formatPostDate(comment.timestamp)}</span>
                        </div>
                    </div>
                `;
                commentSection.appendChild(commentElement);
            });
        })
        .catch(error => {
            console.error('Error loading comments:', error);
        });
}



function createCommentSection(post, newPostElement) {
    const comment_content = document.createElement('textarea');
    comment_content.className = "fs-6 form-control";
    comment_content.setAttribute("rows", 1);

    const create_comment_button = document.createElement('button');
    create_comment_button.innerHTML = "Post Comment";
    create_comment_button.className = "btn btn-primary btn-sm my-2";
    create_comment_button.disabled = true;

    comment_content.onkeyup = () => {
        create_comment_button.disabled = comment_content.value.length === 0;
    }
    const commentsList = newPostElement.querySelector('#comment_list');
    create_comment_button.addEventListener('click', function () {
        fetch(`/all_posts/${post.id}/comments`, {
            method: 'PUT',
            body: JSON.stringify({ comment: comment_content.value })
        })
            .then(response => response.json())
            .then(comment => {
                appendNewComment(commentsList, comment, true);
                comment_content.value = '';
                create_comment_button.disabled = true;
            })
            .catch(error => {
                console.error('Error posting comment:', error);
            });
    });

    return { comment_content, create_comment_button };
}

function appendNewComment(commentsList, comment, only_three) {
    

    // Create new comment element
    const newCommentElement = document.createElement('div');
    newCommentElement.className = "comment card p-2 mb-2 ms-3";
    newCommentElement.innerHTML = `
        <div class="d-flex">
            <div class="avatar-sm me-2">
                <img style="width:30px" class="rounded-circle"
                    src="https://api.dicebear.com/6.x/fun-emoji/svg?seed=${comment.created_by}" alt="Avatar">
            </div>
            <div>
                <h6 class="mb-0">${comment.created_by}</h6>
                <p class="fs-6 fw-light text-muted mb-0">${comment.text}</p>
                <span class="fs-6 fw-light text-muted"><span class="fas fa-clock"></span> ${formatPostDate(comment.timestamp)}</span>
            </div>
        </div>
    `;
    
    // Remove the oldest comment if there are already 3 comments
    const existingComments = commentsList.querySelectorAll('.comment');
    if (existingComments.length >= 3 && only_three) {
        commentsList.removeChild(existingComments[existingComments.length - 1]);
    }

    // Add the new comment to the top
    commentsList.insertBefore(newCommentElement, commentsList.firstChild);
}


function openPostModal(post) {
    const modal = document.createElement('div');
    modal.className = "modal fade";
    modal.id = "postModal";
    modal.tabIndex = "-1";
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${post.created_by}'s Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div id="modal-post-content">${post.content}</div>
                    <div id="modal-comment-list" class="comment-list"></div>
                    <div id="loading-message" class="text-center mt-2"></div>
                </div>
                <div class="modal-footer">
                    <textarea id="modal-comment-content" class="form-control" rows="2" placeholder="Add a comment..."></textarea>
                    <button id="modal-create-comment-button" class="btn btn-primary">Post Comment</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    const commentContent = modal.querySelector('#modal-comment-content');
    const createCommentButton = modal.querySelector('#modal-create-comment-button');
    const commentList = modal.querySelector('#modal-comment-list');
    const loadingMessage = modal.querySelector('#loading-message');
    
    createCommentButton.disabled = commentContent.value.length === 0;

    commentContent.onkeyup = () => {
        createCommentButton.disabled = commentContent.value.length === 0;
    };

    createCommentButton.addEventListener('click', () => {
        fetch(`/all_posts/${post.id}/comments`, {
            method: 'PUT',
            body: JSON.stringify({ comment: commentContent.value })
        })
            .then(response => response.json())
            .then(comment => {
                appendNewComment(commentList, comment);
                commentContent.value = '';
                createCommentButton.disabled = true;
            })
            .catch(error => console.error('Error posting comment:', error));
    });

    // Infinite scroll setup
    let page = 1;
    const perPage = 10;
    let loading = false;

    function modalLoadComments(commentList) {
        if (loading) return;
        loading = true;
        fetch(`/all_posts/${post.id}/comments?page=${page}&per_page=${perPage}`)
            .then(response => response.json())
            .then(data => {
                if (data.comments.length === 0) {
                    loadingMessage.innerHTML = '<span class="text-muted">You are up to date!</span>';
                    loadingMessage.classList.add('fade-in');
                    loading = false;
                } else {
                    data.comments.forEach(comment => {
                        appendNewComment(commentList, comment);
                    });
                    page++;
                }
            })
            .catch(error => console.error('Error loading comments:', error));
    }

    commentList.addEventListener('scroll', () => {
        if (commentList.scrollTop + commentList.clientHeight >= commentList.scrollHeight) {
            modalLoadComments(commentList);
        }
    });

    // Initialize loading of comments
    modalLoadComments(commentList);

    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}


function new_post(event) {
    event.preventDefault(); // Prevent the form from submitting

    console.log("New post function called");

    const submit = document.querySelector('#submit');
    const newPost = document.querySelector('#post_content');

    document.querySelector('#all-posts-view').style.display = 'block';

    fetch('/new_post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            content: newPost.value,
            headers: { 'Content-Type': 'application/json' }
        })
    }).then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        console.log("Fetch request completed");
        document.querySelector('#alert').innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert" id="success">
                Idea created Successfully
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        return response.json();
    })
    .then(result => {
        console.log(result);
        newPost.value = '';
        console.log("all posts called");
        all_posts();
        loadTrendingHashtags();
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}

function formatPostDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function following() {
    const profile = document.querySelector("#view-profile")
    username = profile.attributes['username'].nodeValue
    load_profile(username)
    all_posts('following')
}

function profile_page() {
    const profile = document.querySelector("#view-profile")
    username = profile.attributes['username'].nodeValue
    load_profile(username)
    all_posts(username)
}

function hashtag_posts(element) {
    all_posts_hashtag(element.originalTarget.attributes['tag'].nodeValue)
}

function user_profile(username) {
    load_profile(username)
    all_posts(username)
}
