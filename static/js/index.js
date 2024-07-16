document.addEventListener("DOMContentLoaded", () => {
  const startButton = document.getElementById("start-record");
  const stopButton = document.getElementById("stop-record");
  const audioResponse = document.getElementById("audio-response");

  let recognition;

  if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
  } else if ("SpeechRecognition" in window) {
    recognition = new SpeechRecognition();
  } else {
    console.log("Speech recognition not supported by this browser.");
    startButton.disabled = true;
  }

  if (recognition) {
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      startButton.disabled = true;
      stopButton.disabled = false;
      console.log("Recording started...");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("Transcript: ", transcript);

      // Send the transcript to the backend for further processing
      fetch("/api/transcribe/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ transcript: transcript }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.blob();
        })
        .then((blob) => {
          const audioUrl = URL.createObjectURL(blob);
          audioResponse.src = audioUrl;
          audioResponse.play();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    };

    recognition.onerror = (event) => {
      console.error("Error occurred in recognition: ", event.error);
    };

    recognition.onend = () => {
      startButton.disabled = false;
      stopButton.disabled = true;
      console.log("Recording stopped.");
    };

    startButton.addEventListener("click", () => {
      recognition.start();
    });

    stopButton.addEventListener("click", () => {
      recognition.stop();
    });
  }

  // Helper function to get CSRF token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; cookies.length > i; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
