
function postTemplate(post, pathname){
    let imageLink;
    let outerDiv = document.createElement('div')
    outerDiv.classList.add('col-sm-12', 'col-md-12', 'col-lg-6', 'grid-item');
    let innerDiv = document.createElement('div');
    innerDiv.classList.add('box-masonry');

    let date = post.dateEdited ? `${post.dateEdited}` : `${post._createdAt}`;
    let p_date = document.createElement('p')
    p_date.innerText = date;
    
    if('coverImage' in post){
        imageLink = document.createElement('a');
        if(pathname.includes('cms')){
            imageLink.href = `/cms/editPost/${post.slug}`;
        }
        else{
            imageLink.href = `/post/${post.slug}`;
        }
        imageLink.classList.add('box-masonry-image', 'with-hover-overlay', 'with-hover-icon');

        let image = document.createElement('img');
        image.src = `/static/images/covers/${post.coverImage[0]}`;
        image.classList.add('img-fluid');

        imageLink.appendChild(image);
    };
    if('coverImage' in post){
        innerDiv.appendChild(imageLink);
    };
    let innerDiv2 = document.createElement('div');
    innerDiv2.classList.add('box-masonry-text')
    let h4 = document.createElement('h4');
    let titleLink = document.createElement('a');
    if(pathname.includes('cms')){
        titleLink.href = `/cms/editPost/${post.slug}`;
    }
    else{
        titleLink.href = `/post/${post.slug}`;
    }
    titleLink.innerText = post.title.length > 100 ? `${post.title.slice(0, 100)}...`: `${post.title}`;
    h4.appendChild(titleLink);
    innerDiv2.appendChild(p_date);
    innerDiv2.appendChild(h4);
    let innerDiv3 = document.createElement('div');
    innerDiv3.classList.add('box-masonry-desription');
    let description = document.createElement('p');
    description.innerHTML = post.text.length > 300 ? `${post.text.slice(0,300)}...<br><br><a href="${titleLink.href}">Read more</a>`: `${post.text}`
    innerDiv3.appendChild(description)
    innerDiv2.appendChild(innerDiv3);
    innerDiv.appendChild(innerDiv2);
    outerDiv.appendChild(innerDiv);
    return(outerDiv);
}

function loadPosts(posts){
    for(let post of posts){
        //console.log('Loading post', post)
        document.getElementById('postsContainer').appendChild(postTemplate(post, window.location.pathname));
    }
}

function getPosts(){
    var selectionCount = document.querySelectorAll("#postsContainer > div").length;
    axios.get(`/api/v1/posts/getN?from=${selectionCount}&length=20`, {
        headers: {
        'content-type': 'application/json'
        }}).then(function (response) {
            if(response.data.status==='success'){
                loadPosts(response.data.data)
            }
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });
}

//detect when user scrolls to bottom
window.onscroll = function() {
    if ((window.innerHeight + Math.ceil(window.pageYOffset)) >= document.body.offsetHeight) {
        getPosts();
    }
}
