
function postTemplate(post){
    let imageLink;
    let outerDiv = document.createElement('div')
    outerDiv.classList.add('col-sm-12', 'col-md-12', 'col-lg-6', 'grid-item');
    let innerDiv = document.createElement('div');
    innerDiv.classList.add('box-masonry');
    if('coverImage' in post){
        imageLink = document.createElement('a');
        imageLink.href = `/post/${post.slug}`;
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
    titleLink.href = `/post/${post.slug}`;

    titleLink.innerText = `${post.title}`;
    h4.appendChild(titleLink);
    innerDiv2.appendChild(h4);
    let innerDiv3 = document.createElement('div');
    innerDiv3.classList.add('box-masonry-desription');
    let description = document.createElement('p');
    description.innerHTML = `${post.text.slice(0,300)}`
    innerDiv3.appendChild(description)
    innerDiv2.appendChild(innerDiv3);
    innerDiv.appendChild(innerDiv2);
    outerDiv.appendChild(innerDiv);
    return(outerDiv);
}

function loadPosts(posts){
    for(let post of posts){
        //console.log('Loading post', post)
        document.getElementById('postsContainer').appendChild(postTemplate(post));
    }
}

function loadPageVar (sVar) {
    return unescape(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + escape(sVar).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}

function getSearchQuery(){
    const query= loadPageVar("query")
    axios.get(`/api/v1/posts/search?title=${query}&authorName=${query}&text=${query}`, {
        headers: {
        'content-type': 'application/json'
        }}).then(function (response) {
            //console.log(data);
            if(response.data.status==='success'){
                if(response.data.data.length > 0){
                    loadPosts(response.data.data)
                }
                else{
                    document.getElementById('postsContainer').innerHTML = '<h6>No results match you search</h6>';
                }
            }
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });
}