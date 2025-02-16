console.log("✅ Phishing Detector Extension Loaded");


function scanEmail() {
    let emailBody = document.querySelector(".a3s.aiL");  // Gmail's email body class

    if (emailBody) {
        let emailText = emailBody.innerText.trim();
        
        console.log("📩 Scanning Email Content...");

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_text: emailText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_phishing) {
                console.warn("🚨 Phishing Detected!");

                let emailContainer = document.querySelector(".nH .h7"); // Adjust selector if needed
                
                if (emailContainer && !document.getElementById("phishing-warning-banner")) {
                    let iconUrl = chrome.runtime.getURL("icon.png");
                    
                    let warningBanner = document.createElement("div");
                    warningBanner.id = "phishing-warning-banner";
                    warningBanner.innerHTML = `
                        <div style="display: flex; align-items: center; justify-content: space-between;
                                    background: #ffebeb; color: #b30000; font-size: 16px; 
                                    padding: 12px; border: 2px solid #b30000; border-radius: 5px;
                                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); position: relative;">
                            <div style="display: flex; align-items: center;">
                            <img src="${iconUrl}" width="40" height="40" 
                            style="margin-right: 10px; display: block !important; visibility: visible !important; background: white;">
                       
                                <div>
                                    <strong>🚨 WARNING: This email may be phishing!</strong><br>
                                    <span style="font-size: 14px;">Avoid clicking suspicious links.</span>
                                </div>
                            </div>
                            <div>
                                <button id="moreInfoBtn" style="margin-right: 10px; padding: 6px 10px; 
                                        background: #ffc107; color: #5a3c00; border: none; 
                                        cursor: pointer; font-size: 14px; border-radius: 4px;">
                                    ℹ More Info
                                </button>
                                <button id="ignoreWarningBtn" style="padding: 6px 10px; background: #007bff; 
                                        color: white; border: none; cursor: pointer; 
                                        font-size: 14px; border-radius: 4px;">
                                    Ignore
                                </button>
                            </div>
                        </div>
                    `;

                    emailContainer.prepend(warningBanner);  // ✅ Add banner first

                    // ✅ Attach event listeners dynamically AFTER the banner is added
                    setTimeout(() => {
                        let moreInfoBtn = document.getElementById("moreInfoBtn");
                        let ignoreWarningBtn = document.getElementById("ignoreWarningBtn");

                        if (moreInfoBtn) {
                            moreInfoBtn.addEventListener("click", () => {
                                window.open("https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams", "_blank");
                            });
                        } else {
                            console.warn("⚠️ More Info button not found!");
                        }

                        if (ignoreWarningBtn) {
                            ignoreWarningBtn.addEventListener("click", () => {
                                document.getElementById("phishing-warning-banner").remove();
                                console.log("❌ Warning ignored.");
                            });
                        } else {
                            console.warn("⚠️ Ignore Warning button not found!");
                        }
                    }, 500); // ✅ Ensure DOM updates before attaching listeners

                    console.log("✅ Warning banner added.");
                } else {
                    console.warn("⚠️ Email container not found! Check selector.");
                }

                highlightPhishingWords(emailBody);
            }
        })
        .catch(error => console.error("❌ API Error:", error));
    }
}

// Function to highlight suspicious words in emails
function highlightPhishingWords(emailBody) {
    let suspiciousWords = ["verify", "account suspended", "bank details", "click here", "reset password"];
    let emailHtml = emailBody.innerHTML;

    suspiciousWords.forEach(word => {
        let regex = new RegExp(`\\b${word}\\b`, "gi");
        emailHtml = emailHtml.replace(regex, `<span style="background: yellow; color: red; font-weight: bold;">${word}</span>`);
    });

    emailBody.innerHTML = emailHtml;
}

// Detect when a new email is opened in Gmail
let lastUrl = location.href;
setInterval(() => {
    if (lastUrl !== location.href) {
        lastUrl = location.href;
        setTimeout(scanEmail, 3000);
    }
}, 1000);
