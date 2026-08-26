// ============================================================
// PHISHGUARD FRONTEND
// ============================================================

// IMPORTANT:
// FastAPI backend must be running on:
// http://127.0.0.1:8000

const API_BASE = "http://127.0.0.1:8000/api";

const ENDPOINTS = {
    link: `${API_BASE}/scan/link`,
    email: `${API_BASE}/scan/email`
};


// ============================================================
// DOM ELEMENTS
// ============================================================

const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".tab-panel");

const resultEl = document.getElementById("result");
const resultIcon = document.getElementById("resultIcon");
const resultVerdict = document.getElementById("resultVerdict");
const resultConfidence = document.getElementById("resultConfidence");
const resultModel = document.getElementById("resultModel");

const recentList = document.getElementById("recentList");

const linkInput = document.getElementById("linkInput");
const emailInput = document.getElementById("emailInput");

const scanLinkBtn = document.getElementById("scanLinkBtn");
const scanEmailBtn = document.getElementById("scanEmailBtn");


// ============================================================
// ICONS
// ============================================================

const ICONS = {

    danger:
        `<svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path
                d="M12 9v4M12 17h.01M10.3 3.9L2.7 17a2 2 0 001.7 3h15.2a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
        </svg>`,

    safe:
        `<svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path
                d="M12 2L4 5v6c0 5.2 3.4 9.9 8 11 4.6-1.1 8-5.8 8-11V5l-8-3z"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linejoin="round"
            />
            <path
                d="M9 12l2 2 4-4"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
            />
        </svg>`
};


// ============================================================
// TABS
// ============================================================

tabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        const mode = tab.dataset.mode;

        tabs.forEach((t) => {

            t.classList.remove("is-active");

            t.setAttribute(
                "aria-selected",
                "false"
            );

        });

        tab.classList.add("is-active");

        tab.setAttribute(
            "aria-selected",
            "true"
        );


        panels.forEach((panel) => {

            panel.classList.remove("is-active");

        });


        const activePanel =
            document.querySelector(
                `.tab-panel[data-panel="${mode}"]`
            );

        if (activePanel) {

            activePanel.classList.add(
                "is-active"
            );

        }

    });

});


// ============================================================
// RENDER RESULT
// ============================================================

function renderResult(data) {

    console.log("Rendering backend result:", data);

    resultEl.hidden = false;


    // --------------------------------------------------------
    // Threat status
    // --------------------------------------------------------

    const isThreat =
        Boolean(data.isThreat);


    // --------------------------------------------------------
    // Icon
    // --------------------------------------------------------

    resultIcon.className =
        "result-icon " +
        (isThreat ? "danger" : "safe");

    resultIcon.innerHTML =
        isThreat
            ? ICONS.danger
            : ICONS.safe;


    // --------------------------------------------------------
    // Verdict
    // --------------------------------------------------------

    resultVerdict.textContent =
        data.label || "Unknown";


    resultVerdict.style.color =
        isThreat
            ? "var(--danger)"
            : "var(--safe)";


    // --------------------------------------------------------
    // Confidence
    // --------------------------------------------------------

    resultConfidence.textContent =
        `${Number(data.confidence).toFixed(2)}%`;


    // --------------------------------------------------------
    // Model
    // --------------------------------------------------------

    resultModel.textContent =
        data.model || "AI Model";


    // --------------------------------------------------------
    // Scroll
    // --------------------------------------------------------

    resultEl.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });

}


// ============================================================
// RECENT SCANS
// ============================================================

function addRecentRow(
    targetLabel,
    iconSvg,
    isThreat,
    tagLabel
) {

    const row =
        document.createElement("div");

    row.className =
        "recent-row";


    row.innerHTML = `
        <span class="recent-target">
            ${iconSvg}
            ${escapeHtml(targetLabel)}
        </span>

        <span class="tag ${
            isThreat
                ? "tag-danger"
                : "tag-safe"
        }">
            ${escapeHtml(tagLabel)}
        </span>
    `;


    recentList.prepend(row);


    while (
        recentList.children.length > 5
    ) {

        recentList.removeChild(
            recentList.lastChild
        );

    }

}


// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


// ============================================================
// API CALL
// ============================================================

async function callScanApi(
    endpoint,
    body
) {

    console.log("--------------------------------");
    console.log("Sending request to:");
    console.log(endpoint);

    console.log("Request body:");
    console.log(body);


    const response =
        await fetch(
            endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(body)
            }
        );


    console.log(
        "HTTP status:",
        response.status
    );


    const data =
        await response.json();


    console.log(
        "Backend response:",
        data
    );


    if (!response.ok) {

        throw new Error(
            data.detail ||
            `Request failed: ${response.status}`
        );

    }


    return data;

}


// ============================================================
// LINK SCAN
// ============================================================

if (scanLinkBtn) {

    scanLinkBtn.addEventListener(
        "click",
        async () => {

            const url =
                linkInput.value.trim();


            // ------------------------------------------------
            // Validation
            // ------------------------------------------------

            if (!url) {

                return flagInvalid(
                    linkInput,
                    "Enter a URL first"
                );

            }


            // ------------------------------------------------
            // Disable button
            // ------------------------------------------------

            scanLinkBtn.disabled = true;


            const originalText =
                scanLinkBtn.textContent;

            scanLinkBtn.textContent =
                "Scanning...";


            try {

                // ------------------------------------------------
                // SEND TO FASTAPI
                // ------------------------------------------------

                const data =
                    await callScanApi(
                        ENDPOINTS.link,
                        {
                            url: url
                        }
                    );


                // ------------------------------------------------
                // DEBUG
                // ------------------------------------------------

                console.log(
                    "PHISHING LINK RESULT:",
                    data
                );


                // ------------------------------------------------
                // RENDER
                // ------------------------------------------------

                renderResult(data);


                // ------------------------------------------------
                // RECENT SCAN
                // ------------------------------------------------

                addRecentRow(

                    url.length > 34
                        ? url.slice(0, 34) + "…"
                        : url,

                    iconFor("link"),

                    Boolean(data.isThreat),

                    data.label || "Unknown"

                );


            } catch (error) {

                console.error(
                    "Link scan error:",
                    error
                );


                alert(
                    "Link scan failed:\n" +
                    error.message
                );


            } finally {

                scanLinkBtn.disabled =
                    false;

                scanLinkBtn.textContent =
                    originalText;

            }

        }
    );

}


// ============================================================
// EMAIL SCAN
// ============================================================

if (scanEmailBtn) {

    scanEmailBtn.addEventListener(
        "click",
        async () => {

            const text =
                emailInput.value.trim();


            // ------------------------------------------------
            // Validation
            // ------------------------------------------------

            if (!text) {

                return flagInvalid(
                    emailInput,
                    "Paste email content first"
                );

            }


            scanEmailBtn.disabled = true;


            const originalText =
                scanEmailBtn.textContent;

            scanEmailBtn.textContent =
                "Scanning...";


            try {

                // ------------------------------------------------
                // SEND TO FASTAPI
                // ------------------------------------------------

                const data =
                    await callScanApi(
                        ENDPOINTS.email,
                        {
                            text: text
                        }
                    );


                // ------------------------------------------------
                // DEBUG
                // ------------------------------------------------

                console.log(
                    "SPAM EMAIL RESULT:",
                    data
                );


                // ------------------------------------------------
                // RENDER
                // ------------------------------------------------

                renderResult(data);


                // ------------------------------------------------
                // RECENT SCAN
                // ------------------------------------------------

                const preview =
                    text
                        .split("\n")[0]
                        .slice(0, 34);


                addRecentRow(

                    `"${preview}${
                        preview.length === 34
                            ? "…"
                            : ""
                    }"`,

                    iconFor("email"),

                    Boolean(data.isThreat),

                    data.label || "Unknown"

                );


            } catch (error) {

                console.error(
                    "Email scan error:",
                    error
                );


                alert(
                    "Email scan failed:\n" +
                    error.message
                );


            } finally {

                scanEmailBtn.disabled =
                    false;

                scanEmailBtn.textContent =
                    originalText;

            }

        }
    );

}


// ============================================================
// VALIDATION
// ============================================================

function flagInvalid(
    element,
    message
) {

    element.style.borderColor =
        "var(--danger)";


    let hint =
        element.parentElement.querySelector(
            ".field-error"
        );


    if (!hint) {

        hint =
            document.createElement("p");

        hint.className =
            "field-error";

        hint.style.cssText =
            `
            color: var(--danger);
            font-size: 12px;
            margin-top: 6px;
            `;

        element.insertAdjacentElement(
            "afterend",
            hint
        );

    }


    hint.textContent =
        message;


    element.addEventListener(
        "input",
        () => {

            element.style.borderColor =
                "";

            if (hint) {
                hint.remove();
            }

        },
        {
            once: true
        }
    );

}


// ============================================================
// RECENT SCAN ICONS
// ============================================================

function iconFor(mode) {

    const map = {

        link:
            `<svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none">

                <path
                    d="M9 15l6-6M10 7l1-1a4 4 0 015.7 5.7l-1 1M14 17l-1 1A4 4 0 017.3 12.3l1-1"
                    stroke="currentColor"
                    stroke-width="1.7"
                    stroke-linecap="round"
                />

            </svg>`,

        email:
            `<svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none">

                <rect
                    x="3"
                    y="5"
                    width="18"
                    height="14"
                    rx="2"
                    stroke="currentColor"
                    stroke-width="1.7"
                />

                <path
                    d="M3 7l9 6 9-6"
                    stroke="currentColor"
                    stroke-width="1.7"
                    stroke-linecap="round"
                />

            </svg>`

    };


    return map[mode] || "";

}


// ============================================================
// HERO TERMINAL
// ============================================================

const heroLog =
    document.getElementById(
        "heroLog"
    );


const LOG_LINES = [

    {
        time: "12:04:01",
        text:
            "scanning secure-paypal-login.net",
        type: "neutral"
    },

    {
        time: "12:04:02",
        text:
            "→ verdict: phishing (94%)",
        type: "danger"
    },

    {
        time: "12:04:20",
        text:
            "classifying inbound email",
        type: "neutral"
    },

    {
        time: "12:04:21",
        text:
            "→ verdict: spam (91%)",
        type: "danger"
    }

];


let logIndex = 0;


function pushLogLine() {

    if (!heroLog) {
        return;
    }


    const entry =
        LOG_LINES[
            logIndex %
            LOG_LINES.length
        ];


    const line =
        document.createElement("div");


    line.className =
        "log-line";


    line.innerHTML = `

        <span class="log-time">
            ${entry.time}
        </span>

        <span class="log-${entry.type}">
            ${entry.text}
        </span>

    `;


    heroLog.appendChild(line);


    if (
        heroLog.children.length > 6
    ) {

        heroLog.removeChild(
            heroLog.firstChild
        );

    }


    logIndex++;

}


// Initial logs

for (
    let i = 0;
    i < 4;
    i++
) {

    pushLogLine();

}


// Continue animation

setInterval(
    pushLogLine,
    2600
);


// ============================================================
// STARTUP DEBUG
// ============================================================

console.log(
    "========================================"
);

console.log(
    "PhishGuard Frontend Started"
);

console.log(
    "API Base:",
    API_BASE
);

console.log(
    "Link endpoint:",
    ENDPOINTS.link
);

console.log(
    "Email endpoint:",
    ENDPOINTS.email
);

console.log(
    "========================================"
);