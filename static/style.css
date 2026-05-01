document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scan-btn');
    const ipInput = document.getElementById('ip-input');
    const outputContainer = document.getElementById('output');
    const terminalBody = document.getElementById('terminal');
    const statusText = document.querySelector('.status-text');
    const statusDot = document.querySelector('.dot');

    let eventSource = null;

    function appendToTerminal(htmlContent) {
        const line = document.createElement('div');
        line.className = 'line';
        line.innerHTML = htmlContent;
        outputContainer.appendChild(line);
        
        // Auto-scroll to bottom
        terminalBody.scrollTop = terminalBody.scrollHeight;
    }

    function setScanningStatus(isScanning) {
        if (isScanning) {
            scanBtn.disabled = true;
            scanBtn.querySelector('.btn-text').textContent = 'SCANNING...';
            statusText.textContent = 'SCAN IN PROGRESS';
            statusText.style.color = 'var(--danger)';
            statusDot.style.backgroundColor = 'var(--danger)';
            statusDot.style.boxShadow = '0 0 10px rgba(255, 0, 85, 0.5)';
            ipInput.disabled = true;
        } else {
            scanBtn.disabled = false;
            scanBtn.querySelector('.btn-text').textContent = 'INITIATE SCAN';
            statusText.textContent = 'SYSTEM SECURE';
            statusText.style.color = 'var(--primary)';
            statusDot.style.backgroundColor = 'var(--primary)';
            statusDot.style.boxShadow = 'var(--glow)';
            ipInput.disabled = false;
        }
    }

    scanBtn.addEventListener('click', () => {
        const ip = ipInput.value.trim();
        if (!ip) {
            appendToTerminal(`<span class="prompt">root@system:~#</span> <span style="color: var(--danger)">Error: Please enter a target IP.</span>`);
            return;
        }

        // Reset terminal
        outputContainer.innerHTML = '';
        appendToTerminal(`<span class="prompt">root@system:~#</span> ./scan_network.sh ${ip}`);
        
        setScanningStatus(true);

        // Close any existing connection
        if (eventSource) {
            eventSource.close();
        }

        // Start SSE Connection
        eventSource = new EventSource(`/stream_scan?ip=${encodeURIComponent(ip)}`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.status === 'done') {
                eventSource.close();
                setScanningStatus(false);
                appendToTerminal(`<span class="prompt">root@system:~#</span> Scan sequence terminated.`);
                return;
            }

            if (data.message) {
                // Formatting message
                let msgHtml = data.message.replace(/\n/g, '<br>');
                appendToTerminal(`<span class="sys-msg">${msgHtml}</span>`);
            } else if (data.port) {
                // Formatting open port finding
                appendToTerminal(`[<span style="color: var(--secondary)">+</span>] Port <span class="port-open">${data.port}</span> is OPEN`);
            }
        };

        eventSource.onerror = (error) => {
            console.error("SSE Error:", error);
            eventSource.close();
            setScanningStatus(false);
            appendToTerminal(`<span class="prompt">root@system:~#</span> <span style="color: var(--danger)">Connection lost or scan interrupted.</span>`);
        };
    });

    // Allow pressing Enter in input field
    ipInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            scanBtn.click();
        }
    });
});
