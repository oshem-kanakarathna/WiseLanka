/* Local default. The deployment build replaces this file with the Render URL. */
window.WISELANKA_API_BASE = window.WISELANKA_API_BASE ||
    (['localhost', '127.0.0.1', ''].includes(location.hostname) ? 'http://127.0.0.1:8000' : '');
