document.getElementById("checkEmail").addEventListener("click", async function () {
    const emailText = document.getElementById("emailInput").value;
    const resultDiv = document.getElementById("result");

    if (!emailText) {
        resultDiv.innerText = "⚠️ Please enter email text.";
        resultDiv.className = "loading";
        resultDiv.style.display = "block";
        return;
    }

    checkPhishing(emailText);
});

// ✅ Fix "Check Page" button function
document.getElementById("checkPageBtn").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript(
            {
                target: { tabId: tabs[0].id },
                function: extractEmailContent
            },
            (results) => {
                if (results && results[0] && results[0].result) {
                    checkPhishing(results[0].result);
                } else {
                    const resultDiv = document.getElementById("result");
                    resultDiv.innerText = "⚠️ No email detected!";
                    resultDiv.className = "loading";
                    resultDiv.style.display = "block";
                }
            }
        );
    });
});

// ✅ Function to send email text to Flask API
function checkPhishing(emailText) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerText = "⏳ Checking for phishing...";
    resultDiv.className = "loading";
    resultDiv.style.display = "block";

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: emailText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_phishing) {
            resultDiv.innerHTML = "🚨 <strong>Phishing Detected!</strong>";
            resultDiv.className = "phishing";
        } else {
            resultDiv.innerHTML = "✅ <strong>Safe Email</strong>";
            resultDiv.className = "safe";
        }
    })
    .catch(error => {
        resultDiv.innerText = "❌ Error checking email.";
        resultDiv.className = "loading";
        console.error(error);
    });
}

// ✅ Function to extract email content
function extractEmailContent() {
    let emailBody = document.querySelector(".a3s.aiL");
    return emailBody ? emailBody.innerText.trim() : "";
}
