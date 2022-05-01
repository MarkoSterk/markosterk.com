export const hideMessage = () => {
    const el = document.querySelector('.alert');
    if (el) el.parentElement.removeChild(el);
}

//type is 'success' or 'error
export const showMessage = (msg, status, time = 7) => {
    hideMessage();
    //success
    let msgClass = 'bg-primary text-white'
    if(status != 'success'){
        msgClass = 'bg-danger text-white'
    }

    const markup = `<div class="alert text-center p-3 mb-2 ${msgClass}">${msg}</div>`
    document.querySelector('body').insertAdjacentHTML('afterbegin', markup);

    window.setTimeout(hideMessage, time * 1000);
};


export const showErrorFields = (msg, status) => {

}