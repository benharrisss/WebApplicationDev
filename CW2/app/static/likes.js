// Wait for the DOM content to load before executing the script
document.addEventListener('DOMContentLoaded', function() {
   // Get the CSRF token for secure AJAX requests
   const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
   
   // Event listener for each like button
   document.querySelectorAll('.like-btn').forEach(button => {
      button.addEventListener('click', function() {
      	 
      	 // Get postID associated with like button
         const postId = this.getAttribute('data-post-id');
         // set action to either like or unlike on the post
         const action = this.classList.contains('liked') ? 'unlike' : 'like';
      
         // Send AJAX POST request to update status of the post
         fetch(`/likes/${postId}`, {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json', // Sending JSON data
               'X-CSRFToken': csrfToken // CSRF token for security
            },
            body: JSON.stringify({ action }) // Pass the action into the request 
         })
         .then(response => response.json()) // Parse reponse as JSON
         .then(data => {
            // If request is successful...
            if (data.success) {
               const likeCountSpan = document.querySelector(`#like-count-${postId}`);
               likeCountSpan.textContent = data.like_count; // Update like count
            
	       // If action...
               if (action === "like") {
                  this.classList.add('liked'); // Add 'liked' class
                  this.textContent = 'Unlike'; // Change like button to 'Unlike'
               } else {
                  this.classList.remove('liked'); // Remove 'liked' class
                  this.textContent = 'Like'; // Change like button to 'Like'
               }
            } else {
               console.error('Error updating likes:', data.error); // Catch any errors
            }
         })
         .catch(error => console.error('Error with request:', error)); // Catch any network errors
      });
   });
});
