
document.getElementById('searchBar').addEventListener('keypress', function(e){
    if(e.key === 'Enter'){
        location.href=`/search?query=${document.getElementById('searchBar').value}`
    }
})