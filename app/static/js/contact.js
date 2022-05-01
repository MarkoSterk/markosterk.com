import { showMessage }  from './statusMessage.js';
const btn = document.getElementById('submitContact')

btn.addEventListener('click', function(e){
    e.preventDefault();
    const contactData = {
        name: document.getElementById('name').value,
        surname: document.getElementById('surname').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    }
    axios.post('/cms/sendContactForm', contactData, {
        headers: {
        'content-type': 'application/json'
        }}).then(function (response) {
            //console.log(data);
            window.scrollTo(0,0);
            if(response.data.status==='success'){
                document.getElementById('contact-form').reset()
                window.setTimeout(function(){
                    location.reload()
                }, 3000);
            }
            showMessage(response.data.message, response.data.status)
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });
})
