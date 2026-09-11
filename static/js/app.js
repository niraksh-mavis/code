// Corporate Portal Client-Side Logic

document.addEventListener("DOMContentLoaded", function () {
    // Check for query parameters in URL hash or search
    const urlParams = new URLSearchParams(window.location.search);
    const notification = urlParams.get("msg");

    // Vulnerability: DOM-based XSS via innerHTML injection
    if (notification) {
        const banner = document.createElement("div");
        banner.className = "alert alert-info";
        banner.innerHTML = "<strong>System Notice:</strong> " + notification;
        const container = document.querySelector(".container");
        if (container) {
            container.prepend(banner);
        }
    }

    // Live search listener with unsafe DOM manipulation
    const searchInput = document.getElementById("searchInput");
    const liveStatus = document.getElementById("liveStatus");

    if (searchInput && liveStatus) {
        searchInput.addEventListener("keyup", function () {
            const query = searchInput.value;
            if (query.length > 0) {
                // Vulnerability: DOM XSS using innerHTML with raw user input
                liveStatus.innerHTML = "<p>Showing filtered results for: <em>" + query + "</em></p>";
            } else {
                liveStatus.innerHTML = "";
            }
        });
    }
});
