document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#user-following').addEventListener('click', () => load_follows('following'));
    document.querySelector('#user-follower').addEventListener('click', () => load_follows('follower'));
    document.querySelector('#user-post').addEventListener('click', () => load_posts());
  
    // By default, load the inbox
    load_posts();
});

function load_posts() {
      // Show the mailbox and hide other views
  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#follow-view').style.display = 'none';
  
}

function load_follows(profilebox) {
    // Show compose view and hide other views
    document.querySelector('#follow-view').style.display = 'block';
    document.querySelector('#posts-view').style.display = 'none';

    document.querySelector('#follow-view').innerHTML = `<h3>${profilebox.charAt(0).toUpperCase() + profilebox.slice(1)}</h3>`;
    let user_id = document.querySelector('#user-name').innerHTML;
    
    fetch(`/profileShow/${profilebox}?id=${user_id}`)
    .then(response => response.json())
    .then(posts => {
        // Print emails
        //console.log(posts);
              // Show emails
        posts.forEach((post) => {
            const element = document.createElement('div');
            // Add a class to the element
            element.classList.add('post-item');
            // Mark read/unread 
            if(profilebox === 'follower'){
                element.innerHTML = `<h4><a class="link" color="black" href="${ post.id_er }"><strong>${ post.user_follower }</strong></a></h4>`;
            }
            else if(profilebox === 'following'){
                element.innerHTML = `<h4><a class="link" color="black" href="${ post.id_ing }"><strong>${ post.user_following }</strong></a></h4>`;
            }
            
            document.querySelector('#follow-view').append(element);  
        })    

    });
}

function follow(){
    let user_following = document.querySelector('#user-follow').innerHTML;
    let user_id = document.querySelector('#user-name').innerHTML;
    let user_follower = document.querySelector('#user-follower').innerHTML;
    count_folllowers = parseInt(user_follower.slice(-1));
    fetch(`/follow/${user_id}`)
    if(user_following==="Follow"){
        document.querySelector('#user-follow').innerHTML = `Unfollow`;
        document.querySelector('#user-follower').innerHTML = `Followers ${count_folllowers+1}`
    }
    else{
        document.querySelector('#user-follow').innerHTML = `Follow`;
        document.querySelector('#user-follower').innerHTML = `Followers ${count_folllowers-1}`
    }
}
