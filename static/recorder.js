const start_btn = document.getElementById("record-start-btn");
const start_img = document.getElementById("record-start-img");
const stop_btn = document.getElementById("record-stop-btn");
const stop_img = document.getElementById("record-stop-img");
const text = document.getElementById("text");
const stop_load = document.getElementById("record-stop-loading");
const canvas = document.getElementById('waveform');
const canvasCtx = canvas.getContext('2d');

let audioContext;
let analyser;
let bufferLength;
let dataArray;
let animationId;

let blobs = [];
let stream;
let rec;
let recordUrl;
let audioResponseHandler;

async function initAudio() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        source.connect(analyser);
        analyser.fftSize = 2048;
        bufferLength = analyser.fftSize;
        dataArray = new Uint8Array(bufferLength);
    } catch (e) {
        alert("No fue posible obtener el permiso para el micrófono. Por favor, verifica los permisos y asegúrate de estar en HTTPS.");
        console.error(e);
    }
}

function recorder(url, handler) {
    recordUrl = url;
    if (typeof handler !== "undefined") {
        audioResponseHandler = handler;
    }
}

async function record() {
    try {
        console.log("Iniciando grabación...");
        text.innerHTML = "<i>Grabando...</i>";
        start_btn.style.display = "none";
        start_btn.style.disabled = true;
        start_img.style.display = "none";
        stop_btn.style.display = "";
        stop_btn.style.disabled = false;
        stop_img.style.display = "";
        stop_load.style.display = "none";
        canvas.style.display = "";
        drawWaveform();

        blobs = [];
        rec = new MediaRecorder(stream);
        rec.ondataavailable = (e) => {
            blobs.push(e.data);
        };
        rec.onstop = async () => {
            const blob = new Blob(blobs, { type: 'audio/mp3' });
            const formData = new FormData();
            formData.append('audio', blob, 'recording.mp3');
            try {
                const response = await fetch(recordUrl, {
                    method: 'POST',
                    body: formData,
                });
                const result = await response.json();
                if (audioResponseHandler) {
                    audioResponseHandler(result);
                }
            } catch (e) {
                console.error("Error al enviar el audio:", e);
            }
        };
        rec.start();
    } catch (e) {
        alert("No fue posible iniciar el grabador de audio! Favor de verificar que se tenga el permiso adecuado, estar en HTTPS, etc...");
        console.error(e);
    }
}

function stop() {
    console.log("Deteniendo grabación...");
    text.innerHTML = "<i>Procesando audio...</i>";

    stop_btn.style.disabled = true;
    stop_img.style.display = "none";
    stop_load.style.display = "";
    canvas.style.display = "none";
    cancelAnimationFrame(animationId);
    rec.stop();
}

function drawWaveform() {
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
    canvasCtx.beginPath();

    const sliceWidth = canvas.width * 1.0 / bufferLength;
    let x = 0;

    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * canvas.height / 2;

        if (i === 0) {
            canvasCtx.moveTo(x, y);
        } else {
            canvasCtx.lineTo(x, y);
        }
        x += sliceWidth;
    }
    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();
    animationId = requestAnimationFrame(drawWaveform);
}

window.onload = initAudio;
