let subtitlesData = [];
let subtitleContainer;
let displayedLines = 3;
let isDragging = false;
let dragStartX, dragStartY;
let origX, origY;
let localCache = {}; // videoID: subtitles
let lastVideoURL = "";
let subtitleUpdaterInterval = null;

function getVideoID(url) {
    const params = new URL(url).searchParams;
    return params.get("v");
}

function createSubtitleBox() {
    if (subtitleContainer && document.body.contains(subtitleContainer)) {
        console.log("[UI] Subtitle kutusu zaten DOM'da.");
        return;
    }
    console.log("[UI] Altyazı kutusu oluşturuluyor...");
    subtitleContainer = document.createElement("div");
    subtitleContainer.style.position = "fixed";
    subtitleContainer.style.bottom = "12%";
    subtitleContainer.style.left = "50%";
    subtitleContainer.style.transform = "translateX(-50%)";
    subtitleContainer.style.backgroundColor = "rgba(0, 0, 0, 0.75)";
    subtitleContainer.style.color = "#fff";
    subtitleContainer.style.padding = "15px 20px";
    subtitleContainer.style.borderRadius = "12px";
    subtitleContainer.style.zIndex = "999999";
    subtitleContainer.style.maxWidth = "80%";
    subtitleContainer.style.textAlign = "left";
    subtitleContainer.style.lineHeight = "1.5";
    subtitleContainer.style.fontFamily = "Arial, sans-serif";
    subtitleContainer.style.cursor = "grab";
    subtitleContainer.style.userSelect = "none";
    subtitleContainer.style.maxHeight = "300px";
    subtitleContainer.style.overflow = "hidden";
    subtitleContainer.style.display = "flex";
    subtitleContainer.style.flexDirection = "column";
    subtitleContainer.style.justifyContent = "center";
    document.body.appendChild(subtitleContainer);
    subtitleContainer.addEventListener("mousedown", dragStart);
    document.addEventListener("mousemove", dragMove);
    document.addEventListener("mouseup", dragEnd);
}

function dragStart(e) {
    isDragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    const rect = subtitleContainer.getBoundingClientRect();
    origX = rect.left;
    origY = rect.top;
    subtitleContainer.style.cursor = "grabbing";
}

function dragMove(e) {
    if (!isDragging) return;
    const dx = e.clientX - dragStartX;
    const dy = e.clientY - dragStartY;
    let newX = origX + dx;
    let newY = origY + dy;
    const maxX = window.innerWidth - subtitleContainer.offsetWidth;
    const maxY = window.innerHeight - subtitleContainer.offsetHeight;
    newX = Math.min(Math.max(0, newX), maxX);
    newY = Math.min(Math.max(0, newY), maxY);
    subtitleContainer.style.left = `${newX}px`;
    subtitleContainer.style.top = `${newY}px`;
    subtitleContainer.style.bottom = "auto";
    subtitleContainer.style.transform = "none";
}

function dragEnd() {
    if (isDragging) {
        isDragging = false;
        subtitleContainer.style.cursor = "grab";
    }
}

function renderScrollingSubtitles(currentIndex) {
    if (!subtitleContainer) return;
    subtitleContainer.innerHTML = "";
    for (let i = currentIndex; i < currentIndex + displayedLines; i++) {
        if (i >= subtitlesData.length) break;
        const engDiv = document.createElement("div");
        engDiv.textContent = subtitlesData[i].text;
        engDiv.style.color = "white";
        engDiv.style.fontWeight = (i === currentIndex) ? "bold" : "normal";
        engDiv.style.fontSize = "18px";
        engDiv.style.marginBottom = "2px";
        engDiv.style.whiteSpace = "pre-wrap";
        subtitleContainer.appendChild(engDiv);
        const trDiv = document.createElement("div");
        trDiv.textContent = subtitlesData[i].translation;
        trDiv.style.color = "lightgreen";
        trDiv.style.marginBottom = "12px";
        trDiv.style.fontSize = "16px";
        trDiv.style.whiteSpace = "pre-wrap";
        subtitleContainer.appendChild(trDiv);
    }
}

function updateSubtitles() {
    const video = document.querySelector("video");
    if (!video || subtitlesData.length === 0) {
        console.log("[Update] Video yok veya altyazı verisi boş.");
        return;
    }
    if (!subtitleContainer || !document.body.contains(subtitleContainer)) {
        console.log("[Update] Altyazı kutusu yok, yeniden oluşturuluyor.");
        createSubtitleBox();
    }
    const currentTime = video.currentTime;
    let currentIndex = subtitlesData.findIndex(
        sub => currentTime >= sub.start && currentTime <= sub.end
    );
    if (currentIndex === -1) {
        subtitleContainer.innerHTML = "";
        return;
    }
    renderScrollingSubtitles(currentIndex);
}

function fetchSubtitles(videoUrl) {
    const videoID = getVideoID(videoUrl);
    console.log(`[Fetch] Başlatıldı: ${videoID}`);
    if (localCache[videoID]) {
        subtitlesData = localCache[videoID];
        console.log("[Fetch] Cache'den veri bulundu.");
        createSubtitleBox();
        if (!subtitleUpdaterInterval) {
            subtitleUpdaterInterval = setInterval(updateSubtitles, 1000);
        }
        return;
    }
    fetch("http://localhost:8000/send_url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: videoUrl })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            subtitlesData = data.subtitles;
            localCache[videoID] = subtitlesData;
            console.log("[Fetch] Altyazı başarıyla alındı.");
            createSubtitleBox();
            if (!subtitleUpdaterInterval) {
                subtitleUpdaterInterval = setInterval(updateSubtitles, 1000);
            }
        } else {
            console.error("[Fetch] Sunucu hatası:", data.error);
        }
    })
    .catch(err => {
        console.error("[Fetch] Bağlantı hatası:", err);
    });
}

function init() {
    setInterval(() => {
        const url = window.location.href;
        if (!url.includes("youtube.com/watch")) {
            if (subtitleContainer) subtitleContainer.remove();
            subtitlesData = [];
            lastVideoURL = "";
            console.log("[Init] YouTube dışında, altyazılar kaldırıldı.");
            return;
        }
        if (url !== lastVideoURL) {
            console.log("[Init] Yeni video tespit edildi.");
            lastVideoURL = url;
            if (subtitleContainer) subtitleContainer.remove();
            subtitlesData = [];
            fetchSubtitles(url);
        }
        updateSubtitles();
    }, 1000);
}

window.addEventListener("load", () => {
    console.log("[Page] Yüklendi, sistem başlatılıyor...");
    init();
});
