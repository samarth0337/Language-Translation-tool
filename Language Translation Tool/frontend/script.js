async function translateText() {
  const text = document.getElementById("inputText").value;
  const source = document.getElementById("sourceLang").value;
  const target = document.getElementById("targetLang").value;

  try {
    const response = await fetch("http://localhost:5000/api/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text, source, target })
    });

    const data = await response.json();

    if (!response.ok) {
      document.getElementById("outputText").value = "Error: " + (data.error || "Translation failed");
    } else {
      document.getElementById("outputText").value = data.translatedText;
    }
  } catch (error) {
    document.getElementById("outputText").value = "Error: Could not connect to the server.";
  }
}

function copyText() {
  const output = document.getElementById("outputText");
  output.select();
  document.execCommand("copy");
  alert("Copied!");
}

function speakText() {
  const text = document.getElementById("outputText").value;

  const speech = new SpeechSynthesisUtterance(text);
  speech.lang = "en-US";

  window.speechSynthesis.speak(speech);
}