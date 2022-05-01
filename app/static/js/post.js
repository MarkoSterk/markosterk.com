import { showMessage }  from './statusMessage.js';

const formData = new FormData();

function getCategoryArray(){
    const chosenCategories = [];
    const categories = document.getElementById('category');
    const options = categories.getElementsByTagName('input');
    for(let option of options){
        if(option.checked){
            chosenCategories.push(option.value)
        }
    }
    return chosenCategories;

}

const submitBtn = document.getElementById('submitBtn');
const fileUpload = document.getElementById('coverImage');
const removePreviewImage = document.getElementById('removePreviewImage');
const delBtn = document.getElementById('delBtn');


fileUpload.addEventListener('change', function(e){
    const files = e.target.files // getting our files after upload
    console.log('Here')
    formData.delete('coverImage');
    for (const file of files) {
        formData.append('coverImage', file) // appending every file to formdata
        document.getElementById('coverImagePreview').src = URL.createObjectURL(file);
        document.getElementById('removePreviewImage').style.display = 'inline';
        document.getElementById('coverImage').style.display = 'none';
    }

});

submitBtn.addEventListener('click', function() {
    
    formData.append('title', document.getElementById('title').value);
    formData.append('text', document.getElementById('text').value);
    const categories = getCategoryArray();
    if(categories.length>0){
        formData.append('category', categories);
    }

    axios({
        method: `${document.getElementById('requestMethod').value}`,
        url: `${document.getElementById('targetUrl').value}`,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" }
      })
        .then(function (response) {
            window.scrollTo(0,0);
            showMessage(response.data.message, response.data.status);
            if(response.data.status === 'success'){
                window.setTimeout(function() {
                    location.href = '/cms/dashboard'
                }, 3000);
            }
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });;
});

delBtn.addEventListener('click', function(){
    axios({
        method: 'DELETE',
        url: `${document.getElementById('targetUrl').value}`
    })
    .then(function(response){
        window.scrollTo(0,0);
        showMessage('Post deleted successfully', 'success');
        window.setTimeout(function() {
            location.href = '/cms/dashboard'
        }, 1000);
    })
    .catch(function (error) {
        //PRINT ERROR
        console.log(error);
    });;
})

removePreviewImage.addEventListener('click', function(){
    document.getElementById('coverImagePreview').src = '';
    formData.delete('coverImage');
    fileUpload.value='';
    document.getElementById('removePreviewImage').style.display = 'none';
    formData.append('coverImage', '_DELETE')
    document.getElementById('coverImage').style.display='inline';
})
