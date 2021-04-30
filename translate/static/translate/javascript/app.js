'use strict'

function getInputValue() 
{
    let inputVal = document.getElementById("inputId").value;
    return inputVal    
}

function setOutputValue(outputValue)
{
    var text = outputValue;
    var obj = JSON.parse(text, function (key, value)
    {
        if (key=="translatedText")
        {
            console.log(value);
            document.getElementById("outputId").value = value;
            return value.toUpperCase();
        }
        else
        {
            console.log(value)
            return value;
        }
    });    
}

async function sendText()
{  
    var text = getInputValue()
    var langin = selectin.value;
    var langout = selectout.value;
    console.log(langin);
    console.log(langout);
    const res = await fetch("http://localhost:5000/translate",
    {
        method:"POST",
        body:JSON.stringify
        ({
            q:text,
            source:langin,
            target:langout
        }),
        headers:{"Content-Type":"application/json"}
    });    
    var data = JSON.stringify(await res.json());
    console.log(data)
    setOutputValue(data)   
}

async function getLanguages()
{
    console.log("getlanguages")
    const res = await fetch("http://localhost:5000/languages",
    {
        method:"GET",        
        headers:{"Content-Type":"application/json"}
    });
    var data = JSON.stringify(await res.json());
    console.log(data)
}

function clearText()
{
    document.getElementById('inputId').value="";
    document.getElementById('outputId').value="";
}

const selectin = document.querySelector('#languagein');
selectin.addEventListener('change',(event =>{
    const{
        value,
        text
    }=event.target.options[event.target.selectedIndex]      
}))

const selectout = document.querySelector('#languageout');
selectout.addEventListener('change', (event=>{
    const{
        value,
        text
    }=event.target.options[event.target.selectedIndex]    
}))