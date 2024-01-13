function orderReturn(){
    document.getElementById("form").addEventListener("click", function(event){
        event.preventDefault()
      });
        console.log("rftg");
        
        const txt = document.getElementById("back").value
        if(txt.length!==0){
            console.log('entered');
            $('#form').submit()
        }
}