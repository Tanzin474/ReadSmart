
var pdf_url=""
// "https://probe-test-alpha.s3.ap-south-1.amazonaws.com/Intrigual_props.pdf"
var query= "Why do we sneeze?"
var system_prompt="Answer the query given in the input"

text_form=document.getElementById('text_form')
answer_field=document.getElementById('answer')
get_history=document.getElementById('get_history')


document.getElementById('pdf_form').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if(!file)
    {
        alert("Please upload a file");
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);

    console.log("Uploading file...");

    fetch('http://127.0.0.1:5000/upload',{
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        pdf_url=data.pdf_url;})
});


get_history.addEventListener('click', function(event) {
    event.preventDefault();

    console.log("Fetching history...");

    fetch(`http://127.0.0.1:5000/history`,{
        method: 'GET',
    }).then(response => response.json())
    .then(data => {
        console.log(data.message);
        console.log(data.history);
    })
    

});

text_form.addEventListener('submit', function(event) {
    event.preventDefault();

    const queryInput = document.getElementById('text_query');
    const query =queryInput.value;

    if(!query)
    {
        alert("Please enter some text");
        return;
    }

    body = JSON.stringify({
        "query": query,
        "pdf_url": pdf_url,
        "system_prompt": system_prompt,
    })

    console.log("querying...");

    fetch(`https://ilcgnodtyc.execute-api.ap-south-1.amazonaws.com/default/testt`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
          },
        // body: body,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        answer_field.textContent = data.answer;
    })

});