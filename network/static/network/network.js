document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    if (document.querySelector('#follow')) {
        document.querySelector('#follow').addEventListener('click', event => follow_user(event));
    }
    if (document.querySelector('.like')){
        document.querySelectorAll('.like').forEach(button => {
            button.addEventListener('click', event => like(event))
        });
    }
    if (document.querySelector('.edit')) {
        document.querySelectorAll('.edit').forEach(button => {
            button.addEventListener('click', event => edit(event))
        });
    }
  
  });


function follow_user(event) {

    const element = event.target;
    const id_num = element.parentElement.id;
    const parent = element.parentElement;
    console.log(parent);
    fetch(`/follow_update/${id_num}`)
    .then(response => response.json())
    .then(message => {
        console.log(message);
        if (element.innerHTML === 'Follow') {
            element.innerHTML = 'Unfollow';
            element.setAttribute("class", "");
            element.classList.add("btn", "btn-danger");
        }
        else {
            element.innerHTML = 'Follow';
            element.setAttribute("class", "");
            element.classList.add("btn", "btn-primary");
        }
        follower_count = parent.querySelector('#followers');
        follower_count.innerHTML = `Followers: ${message.count}`;
    });
   
}

function like(event) {
    const element = event.target;
    const post_id = element.parentElement.parentElement.id;
    console.log(`post : ${post_id}`);

    fetch(`/like_update/${post_id}`)
    .then(response => response.json())
    .then(message => {
        console.log(message);
        element.innerHTML = ` ♥️  ${message.count}`;
        element.setAttribute("class","");
        if (message.new_action === 'like') {
            element.classList.add("like", "btn", "btn-light");

        }
        else {
            element.classList.add("like", "btn", "btn-danger");
        }
    });

}


function edit(event) {
    const element = event.target;
    const parent = element.parentElement.parentElement;
    const post_id = parent.id;
    const edit_box = parent.nextElementSibling;
    console.log(edit_box);
    edit_box.setAttribute("class", "post");
    edit_box.style.display = 'block';
    parent.style.display = 'none';

    edit_box.querySelector(".submit_edit").addEventListener('click', event => {

        const new_text = edit_box.querySelector('textarea').value.trim();
        if (new_text === '') {
            edit_box.style.display='none';
            parent.style.display ='block';
            return;
        }
        console.log(new_text);
        edit_box.style.display='none';
        parent.style.display ='block';
        const content = parent.querySelector('.content');
        console.log(content);
        content.innerHTML = new_text;
        fetch(`/edit_post/${post_id}/${new_text}`)
        .then(response => response.json())
        .then(message => {
            console.log(message);
        });
    });
    
}