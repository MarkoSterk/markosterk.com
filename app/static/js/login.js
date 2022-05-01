import { showMessage }  from './statusMessage.js';

try{
    const btn = document.getElementById('loginBtn')
    btn.addEventListener('click', function(e){
    e.preventDefault();

    const contactData = new FormData()
    contactData.set('email', document.getElementById('email').value)
    contactData.set('password', document.getElementById('password').value)

    axios.post('/api/v1/users/login', contactData, {
        headers: {
        'content-type': 'multipart/form-data'
        }}).then(function (response) {
            //console.log(data);
            window.scrollTo(0,0);
            if(response.data.status==='success'){
                document.getElementById('login-form').reset()
                window.setTimeout(function() {
                    location.href = '/cms/dashboard'
                }, 3000);
            }
            showMessage(response.data.message, response.data.status)
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error.message);
        });
    })
}
catch(e){
    //pass
}

try{
    const logoutBtn = document.getElementById('logoutBtn')
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
    
        axios.get('/api/v1/users/logout')
                .then(function (response) {
                //console.log(data);
                window.scrollTo(0,0);
                if(response.data.status==='success'){
                    window.setTimeout(function() {
                        location.href = '/'
                    }, 3000);
                }
                showMessage(response.data.message, response.data.status)
            })
            .catch(function (error) {
                //PRINT ERROR
                console.log(error);
            });
    })
}
catch(e){
    //pass
}
