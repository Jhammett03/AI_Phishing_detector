chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.emailContent) {
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email_text: message.emailContent }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.is_phishing) {
          alert("🚨 Warning: Phishing email detected!");
        }
      })
      .catch((error) => console.error("Error:", error));
  }
});
