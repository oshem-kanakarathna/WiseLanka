"use strict";
window.WiseAssistant = (() => {
    const base = window.WiseAPI.base;
    const form = document.getElementById('assistantForm');
    const status = document.getElementById('assistantStatus');
    const responseBox = document.getElementById('assistantResponse');
    let lastResponse = null;
    let optionsFailed = false;
    const t = (key, fallback) => window.WiseI18n.t(key, fallback);
    const node = (tag, text) => { const element = document.createElement(tag); element.textContent = text; return element; };
    function render(data) {
        responseBox.replaceChildren();
        const summaryKey = {GROUNDED:'guidance_note',UNSUPPORTED:'unsupported',NEEDS_PROFILE:'need_profile',NEEDS_PROGRAMME:'need_programme',NOT_ASSESSED:'no_evidence'}[data.status];
        if (summaryKey) status.dataset.i18n = summaryKey;
        status.textContent = summaryKey ? t(summaryKey,data.summary) : data.summary;
        if (data.status !== 'GROUNDED') status.focus();
        if (data.supported_topics) {
            const list = document.createElement('ul');
            Object.keys(data.supported_topics).forEach(key => list.appendChild(node('li', t(key, data.supported_topics[key]))));
            responseBox.appendChild(list);
        }
        (data.blocks || []).forEach(block => {
            responseBox.appendChild(node('h3', t(block.heading_key, block.heading_key)));
            const list = document.createElement('ul');
            list.lang = block.content_language || 'en';
            list.dataset.sourceContent = 'true';
            block.lines.forEach(line => list.appendChild(node('li', line)));
            responseBox.appendChild(list);
        });
        (data.sources || []).forEach(source => {
            let url;
            try { url = new URL(source.url); } catch { return; }
            if (!['https:','http:'].includes(url.protocol)) return;
            const link = node('a', `${t('official','Official resource')}: ${source.title}`);
            link.href = url.href; link.target = '_blank'; link.rel = 'noopener noreferrer';
            responseBox.appendChild(link);
        });
        responseBox.appendChild(node('p',t('source_content','Source content (original language)')));
        responseBox.appendChild(node('p',t('guidance_note','Guidance only. Admission is not guaranteed.')));
    }
    async function loadOptions() {
        try {
            const r = await window.WiseAPI.fetch(base+'/assistant/options');
            if (!r.ok) throw new Error('Options unavailable');
            const data = await r.json();
            if (!Array.isArray(data.programmes)) throw new Error('Invalid options');
            const select = document.getElementById('assistantProgramme');
            data.programmes.forEach(programme => {
                const option = node('option',programme.programme_name);
                option.value = programme.programme_id;
                select.appendChild(option);
            });
        } catch {
            optionsFailed = true;
            status.dataset.i18n = 'chat_error';
            status.textContent = t('chat_error','Guidance is unavailable. Try again or use the official source.');
        }
    }
    form.addEventListener('submit',async event => {
        event.preventDefault();
        lastResponse = null;
        responseBox.replaceChildren();
        let profile;
        if (document.getElementById('assistantUseProfile').checked) {
            try { profile = collectProfile().learner_profile; }
            catch (error) { delete status.dataset.i18n; status.textContent = error.message; status.focus(); return; }
        }
        const button = document.getElementById('assistantSend');
        button.disabled = true;
        status.dataset.i18n = 'chat_wait';
        status.textContent = t('chat_wait','Getting grounded guidance…');
        try {
            const r = await window.WiseAPI.fetch(base+'/assistant/guidance', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
                intent:document.getElementById('assistantTopic').value,
                programme_id:document.getElementById('assistantProgramme').value,
                question:document.getElementById('assistantQuestion').value.trim(),
                language:window.WiseI18n.language,
                ...(profile ? {learner_profile:profile} : {}),
            })});
            const data = await r.json();
            if (!r.ok || !Array.isArray(data.blocks)) throw new Error('Guidance failed');
            lastResponse = data;
            render(data);
        } catch {
            status.dataset.i18n = 'chat_error';
            status.textContent = t('chat_error','Guidance is unavailable. Try again or use the official source.');
            status.focus();
        } finally { button.disabled = false; }
    });
    document.addEventListener('wiselanka:language', () => {
        if (lastResponse) render(lastResponse);
        else if (optionsFailed) status.textContent = t('chat_error');
    });
    loadOptions();
    return {render};
})();

window.WiseVoice = (() => {
    const start = document.getElementById('voiceStart');
    const stop = document.getElementById('voiceStop');
    const status = document.getElementById('voiceStatus');
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let active = false;
    let state = Recognition ? 'voice_stopped' : 'voice_unsupported';
    let failed = false;
    function announce(key) { state = key; status.dataset.i18n = key; status.textContent = window.WiseI18n.t(key, 'Speech recognition is unavailable. Type your question instead.'); }
    function controls(listening) { active = listening; start.disabled = listening || !Recognition; stop.disabled = !listening; start.setAttribute('aria-pressed',String(listening)); }
    function end() { controls(false); if (!failed) announce('voice_stopped'); }
    function error(event) {
        failed = true;
        const key = {'not-allowed':'voice_denied','service-not-allowed':'voice_denied','language-not-supported':'voice_language','audio-capture':'voice_error','no-speech':'voice_error','network':'voice_error','aborted':'voice_stopped'}[event.error] || 'voice_error';
        announce(key);controls(false);
    }
    start.addEventListener('click',() => {
        if (!Recognition) { announce('voice_unsupported'); return; }
        if (!document.getElementById('voiceConsent').checked) { announce('voice_consent_needed'); return; }
        try {
            failed = false;
            recognition = new Recognition();
            recognition.lang = document.getElementById('voiceLanguage').value;
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            recognition.onstart = () => { controls(true);announce('voice_listening'); };
            recognition.onend = end;
            recognition.onerror = error;
            recognition.onresult = event => {
                if (!active || !document.getElementById('voiceConsent').checked) return;
                const text = event.results?.[0]?.[0]?.transcript;
                if (!text) { error({error:'no-speech'});return; }
                // Editable transcript only: never auto-submit a recognition result.
                const input = document.getElementById('assistantQuestion');
                input.value = text.slice(0,300);
                input.focus();
            };
            controls(true);
            announce('voice_listening');
            recognition.start();
        } catch { error({error:'unknown'}); }
    });
    stop.addEventListener('click',() => {
        try { recognition?.stop(); } catch { /* Text input remains available. */ }
        controls(false);announce('voice_stopped');
    });
    document.getElementById('voiceConsent').addEventListener('change',event => {
        if (!event.target.checked && active) { recognition?.abort();end(); }
    });
    function languageChanged() {
        if (active) { recognition?.abort(); controls(false);state='voice_stopped'; }
        announce(state);
    }
    document.addEventListener('wiselanka:language', languageChanged);
    document.addEventListener('wiselanka:translations', () => announce(state));
    controls(false);announce(state);
    return {get supported() {return !!Recognition;}};
})();
