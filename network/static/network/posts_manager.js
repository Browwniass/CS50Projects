document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    //document.querySelector('edit_but').addEventListener('click', () => editing_post());
});

function edit_view(post_id){
    
    var content = document.getElementById(`content-${post_id}`);
    var data =  document.getElementById(`data-${post_id}`);
    var edit_area = document.getElementById(`editarea-${post_id}`);
    var edit_form = document.getElementById(`form-${post_id}`);
    var edit_but = document.getElementById(`but-${post_id}`);
    if(edit_form.style.display == 'block'){
        edit_form.style.display = 'none';
        data.style.display = 'block';
        content.style.display = 'block';
        edit_but.className = "btn btn-success";
        edit_but.value  = "Edit";
    }
    else{
        edit_area.innerHTML = content.innerHTML;
        edit_form.style.display = 'block';
        data.style.display = 'none';
        content.style.display = 'none';
        edit_but.className = "btn btn-info";
        edit_but.value  = "Back";
        
    }
}

function saving_edit(post_id){
    var edit_area = document.getElementById(`editarea-${post_id}`).value;
    console.log(edit_area);
    fetch(`/editing/${post_id}?content=${edit_area}`)
    .then(response => response.json())
    .then(posts => {
        document.getElementById(`content-${post_id}`).innerHTML=posts['post'];
        edit_view(post_id)
    });

}