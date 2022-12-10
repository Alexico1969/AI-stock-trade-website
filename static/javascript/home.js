$(document).ready(function(){
    console.log('--- js file loaded ---');

    var content =  $.ajax({
        url: "https://api.nasa.gov/planetary/apod?api_key=VM2f40EQQ0tk58nvmPhpVa6gthc5ma6Chgll56N7",
        contentType: "application/json",
        dataType: 'json',
        success: function(result){
            console.log(result);
        }



})