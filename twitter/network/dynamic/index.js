// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // Select the submit button and post content to be used later
    const submit = document.querySelector('#submit');
    const newPost = document.querySelector('#post_content');

    // Disable submit button by default:
    submit.disabled = true;

    // Listen for input to be typed into the input field
    newPost.onkeyup = () => {
        if (newPost.content.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    // Listen for submission of form
    document.querySelector('form').onsubmit = () => {

        // Find the post the user just submitted
        const post = newPost.content;

        // Create a list item for the new post and add the post to it
        const li = document.createElement('li');
        li.innerHTML = post;

        // Add new element to our unordered list:
        document.querySelector('#tasks').append(li);

        // Clear out input field:
        newPost.value = '';

        // Disable the submit button again:
        submit.disabled = true;

        // Stop form from submitting
        return false;
    }
});