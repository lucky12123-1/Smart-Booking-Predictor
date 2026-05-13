const routes = [
    {
        source: "BOM",
        destination: "DEL",
        type: "Business",
        bestDay: "Thursday",
        weeks: 12,
        ranking: [
            ["Thursday", 5],
            ["Monday", 4],
            ["Wednesday", 3],
            ["Tuesday", 1],
            ["Friday", 0],
            ["Saturday", 0],
            ["Sunday", 0],
        ],
    },
    {
        source: "BOM",
        destination: "GOA",
        type: "Leisure",
        bestDay: "Tuesday",
        weeks: 12,
        ranking: [
            ["Tuesday", 4],
            ["Wednesday", 3],
            ["Monday", 2],
            ["Thursday", 2],
            ["Friday", 1],
            ["Saturday", 0],
            ["Sunday", 0],
        ],
    },
    {
        source: "BOM",
        destination: "BLR",
        type: "Business",
        bestDay: "Monday",
        weeks: 12,
        ranking: [
            ["Monday", 5],
            ["Thursday", 3],
            ["Tuesday", 2],
            ["Wednesday", 2],
            ["Friday", 0],
            ["Saturday", 0],
            ["Sunday", 0],
        ],
    },
    {
        source: "DEL",
        destination: "HYD",
        type: "Business",
        bestDay: "Wednesday",
        weeks: 12,
        ranking: [
            ["Wednesday", 4],
            ["Monday", 3],
            ["Thursday", 3],
            ["Tuesday", 2],
            ["Friday", 0],
            ["Saturday", 0],
            ["Sunday", 0],
        ],
    },
];

const airports = {
    BOM: { name: "Mumbai", x: 0.22, y: 0.68 },
    DEL: { name: "Delhi", x: 0.47, y: 0.28 },
    GOA: { name: "Goa", x: 0.26, y: 0.78 },
    BLR: { name: "Bengaluru", x: 0.42, y: 0.82 },
    HYD: { name: "Hyderabad", x: 0.45, y: 0.64 },
};

const sourceInput = document.querySelector("#source");
const destinationInput = document.querySelector("#destination");
const form = document.querySelector("#route-form");
const quickRoutes = document.querySelector("#quick-routes");
const resultPanel = document.querySelector("#result-panel");
const swapButton = document.querySelector("#swap-button");
const canvas = document.querySelector("#route-canvas");
const context = canvas.getContext("2d");

function normalize(value) {
    return value.trim().toUpperCase();
}

function findRoute(source, destination) {
    return routes.find((route) => route.source === source && route.destination === destination);
}

function percentage(times, weeks) {
    return Math.round((times / weeks) * 100);
}

function renderQuickRoutes(activeRoute) {
    quickRoutes.innerHTML = routes.map((route) => {
        const active = activeRoute && route.source === activeRoute.source && route.destination === activeRoute.destination;
        return `
            <button class="quick-route${active ? " is-active" : ""}" type="button" data-source="${route.source}" data-destination="${route.destination}">
                ${route.source} -> ${route.destination}
            </button>
        `;
    }).join("");
}

function renderResult(route, source, destination) {
    if (!route) {
        resultPanel.innerHTML = `
            <div class="empty-state">
                <p class="route-kicker">${source} -> ${destination}</p>
                <h2>No flight found for that sector</h2>
                <p>This route is not available in the current sample data.</p>
            </div>
        `;
        renderCanvas(null, source, destination);
        renderQuickRoutes(null);
        return;
    }

    const rows = route.ranking.map(([day, times], index) => {
        const percent = percentage(times, route.weeks);
        return `
            <div class="rank-row">
                <div class="rank-number">${index + 1}</div>
                <div class="rank-label">
                    <strong>${day}</strong>
                    <div class="rank-bar" aria-hidden="true">
                        <div class="rank-fill" style="--fill: ${Math.max(percent, 4)}%"></div>
                    </div>
                </div>
                <div>
                    <div class="rank-percent">${percent}%</div>
                    <div class="rank-meta">${times}/${route.weeks}</div>
                </div>
            </div>
        `;
    }).join("");

    resultPanel.innerHTML = `
        <p class="route-kicker">${route.type} sector</p>
        <h2 class="route-title">${route.source} -> ${route.destination}</h2>
        <div class="best-day">
            <span>Best day to book</span>
            <strong>${route.bestDay}</strong>
        </div>
        <div class="rank-list">${rows}</div>
    `;

    renderCanvas(route, source, destination);
    renderQuickRoutes(route);
}

function drawAirport(code, point, isActive) {
    const x = point.x;
    const y = point.y;
    context.beginPath();
    context.arc(x, y, isActive ? 13 : 8, 0, Math.PI * 2);
    context.fillStyle = isActive ? "#df5b42" : "#9fb0c4";
    context.fill();
    context.lineWidth = isActive ? 5 : 0;
    context.strokeStyle = "rgba(223, 91, 66, 0.18)";
    context.stroke();

    context.fillStyle = "#18212f";
    context.font = "800 16px system-ui, sans-serif";
    context.textAlign = "center";
    context.fillText(code, x, y - 18);
}

function drawRouteArc(from, to, color) {
    const controlX = (from.x + to.x) / 2;
    const controlY = Math.min(from.y, to.y) - 82;
    context.beginPath();
    context.moveTo(from.x, from.y);
    context.quadraticCurveTo(controlX, controlY, to.x, to.y);
    context.lineWidth = 5;
    context.strokeStyle = color;
    context.lineCap = "round";
    context.stroke();

    const planeX = (from.x + to.x + controlX) / 3;
    const planeY = (from.y + to.y + controlY) / 3;
    context.save();
    context.translate(planeX, planeY);
    context.rotate(Math.atan2(to.y - from.y, to.x - from.x));
    context.fillStyle = color;
    context.beginPath();
    context.moveTo(13, 0);
    context.lineTo(-11, -7);
    context.lineTo(-6, 0);
    context.lineTo(-11, 7);
    context.closePath();
    context.fill();
    context.restore();
}

function drawRanking(route) {
    const startX = 52;
    const baseY = canvas.height - 98;
    const barWidth = (canvas.width - 104) / route.ranking.length;

    context.fillStyle = "#647084";
    context.font = "800 12px system-ui, sans-serif";
    context.textAlign = "left";
    context.fillText("Weekly cheapest frequency", startX, baseY - 48);

    route.ranking.forEach(([day, times], index) => {
        const percent = times / route.weeks;
        const x = startX + index * barWidth;
        const h = 22 + percent * 76;
        const y = baseY - h;

        context.fillStyle = index === 0 ? "#047b72" : "#bfd0df";
        context.fillRect(x + 7, y, Math.max(16, barWidth - 16), h);

        context.fillStyle = "#18212f";
        context.font = "800 11px system-ui, sans-serif";
        context.textAlign = "center";
        context.fillText(day.slice(0, 3), x + barWidth / 2, baseY + 22);
    });
}

function renderCanvas(route, source, destination) {
    const ratio = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(320, Math.floor(rect.width * ratio));
    canvas.height = Math.max(360, Math.floor(rect.height * ratio));
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    const width = canvas.width / ratio;
    const height = canvas.height / ratio;
    context.clearRect(0, 0, width, height);

    context.fillStyle = "#f8fbfd";
    context.fillRect(0, 0, width, height);

    context.strokeStyle = "rgba(30, 53, 87, 0.08)";
    context.lineWidth = 1;
    for (let y = 38; y < height; y += 48) {
        context.beginPath();
        context.moveTo(0, y);
        context.lineTo(width, y);
        context.stroke();
    }

    const scaledAirports = Object.fromEntries(Object.entries(airports).map(([code, point]) => [
        code,
        {
            name: point.name,
            x: 54 + point.x * (width - 108),
            y: 54 + point.y * (height - 190),
        },
    ]));

    Object.entries(scaledAirports).forEach(([code, point]) => {
        drawAirport(code, point, code === source || code === destination);
    });

    if (route && scaledAirports[source] && scaledAirports[destination]) {
        drawRouteArc(scaledAirports[source], scaledAirports[destination], "#047b72");
        drawRanking(route);
        return;
    }

    context.fillStyle = "#647084";
    context.font = "800 18px system-ui, sans-serif";
    context.textAlign = "center";
    context.fillText("No route data available", width / 2, height / 2);
}

function search() {
    const source = normalize(sourceInput.value);
    const destination = normalize(destinationInput.value);
    sourceInput.value = source;
    destinationInput.value = destination;
    renderResult(findRoute(source, destination), source || "FROM", destination || "TO");
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    search();
});

swapButton.addEventListener("click", () => {
    const source = sourceInput.value;
    sourceInput.value = destinationInput.value;
    destinationInput.value = source;
    search();
});

quickRoutes.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) {
        return;
    }

    sourceInput.value = button.dataset.source;
    destinationInput.value = button.dataset.destination;
    search();
});

[sourceInput, destinationInput].forEach((input) => {
    input.addEventListener("input", () => {
        input.value = input.value.replace(/[^a-zA-Z]/g, "").toUpperCase();
    });
});

window.addEventListener("resize", search);

renderQuickRoutes(routes[0]);
search();
