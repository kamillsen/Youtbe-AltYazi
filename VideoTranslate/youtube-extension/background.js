chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url && changeInfo.url.includes("youtube.com/watch")) {
    console.log("[Background] Yeni YouTube URL tespit edildi:", changeInfo.url);

    fetch("http://localhost:8000/send_url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: changeInfo.url })
    })
      .then(response => response.json())
      .then(data => {
        console.log("[Background] Sunucudan gelen yanıt:", data);
      })
      .catch(error => {
        console.error("[Background] Hata:", error);
      });
  }
});
