let mediaRecorder = null;
let audioChunks = [];
let audioBlob = null;
let language = "fon"; // default language

getImage("Bienvenu")

document.getElementById("language-select").addEventListener("change", () => {
    language = document.getElementById("language-select").value;
    const recordButton = document.getElementById("recordButton");
    if (language === "dendi") {
        recordButton.style.display = "none";
    } else {
        recordButton.style.display = "block";
    }
});

document.getElementById("sendButton").addEventListener('click', () => {
    const language = document.getElementById("language-select").value;
    const text = document.getElementById("translate").value;

    if (language === "dendi") {
        sendDendi(text)
    } else {
        sendFon(text)
    }
})



async function sendFon(text) {
    console.log('send translate')
    var formData = new FormData();
    formData.append('source_language',"Fon")
    formData.append('target_language',"French")
    formData.append('source_sentence',"Acɛ, susu kpo sisi ɖokpo ɔ kpo wɛ gbɛtɔ bi ɖo ɖò gbɛwiwa tɔn hwenu; ye ɖo linkpɔn bɔ ayi yetɔn mɛ kpe lo bɔ ye ɖo na do alɔ yeɖee ɖi nɔvinɔvi ɖɔhun.")

    data = {
        source_language: "Fon",
        target_language: "French",
        source_sentence: text,
    }
    axios.post('http://localhost:8000/translate/dendi', data)
    .then(response => {
        const data = response.data
        console.log(data)
        getImage(data.result)
    })
   
}
async function sendDendi(text) {
    console.log('send translate')
    

    data = {
        source_sentence: text,
    }
    axios.post('http://localhost:8000/translate/dendi', data)
.then(response => {
    const data = response.data
    console.log(data)
    getImage(data.result)
})
    
}

async function getImage(text) {
    console.log('send')
    // const text = document.getElementById("translate").value;
    const response = await fetch("https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0", {
        method: "POST",
        headers: {
            "Authorization": "Bearer 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"
        },
        body: text,
    });
    const data = await response.blob();
    const imageUrl = URL.createObjectURL(data);
    const image = document.getElementById("printImage");
    image.src = imageUrl;
    console.log(data);
}

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.addEventListener("dataavailable", event => {
        audioChunks.push(event.data);
    });
    mediaRecorder.addEventListener("stop", () => {
        audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            const base64data = reader.result;
            const audioData = base64data.split(",")[1];
            fetch("https://api-inference.huggingface.co/models/speechbrain/asr-wav2vec2-dvoice-fongbe", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer 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"
                },
                body: audioBlob,
            })
           .then(response => response.json())
           .then(data => {
            console.info(data);
            console.info(data['text']);
            const inputField = document.getElementById("translate");
                inputField.value = data['text'];
                sendFon(data['text'])
            })
           .catch(error => {
                console.error("Error:", error);
            });
        };
    });
    mediaRecorder.start();
    document.getElementById("recordButton").classList.add("record-button-recording"); // add the recording class
}

document.getElementById("recordButton").addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        document.getElementById("recordButton").classList.remove("record-button-recording"); // remove the recording class
    } else {
        startRecording();
    }
});