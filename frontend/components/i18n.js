"use strict";
window.WiseI18n = (() => {
    let catalogue = null;
    let language = "en";
    const originals = new WeakMap();
    const normalise = text => text.replace(/\s+/g, " ").trim();
    function t(key, fallback = key) { return catalogue?.[language]?.[key] || catalogue?.en?.[key] || fallback; }
    function textTranslation(original) {
        if (!catalogue || language === "en") return original;
        const normal = normalise(original);
        const key = Object.keys(catalogue.en).find(k => normalise(catalogue.en[k]) === normal);
        if (key) return t(key);
        const subject = normal.match(/^(A\/L|O\/L) [Ss]ubject (\d+)( grade)?$/);
        if (subject) return t(subject[1] === "A/L" ? "al_subject" : "ol_subject").replace("{number}", subject[2]) + (subject[3] ? " " + t("grade_word") : "");
        const remove = normal.match(/^Remove (subject|qualification) (\d+)$/);
        if (remove) return t(remove[1] === "subject" ? "remove_subject" : "remove_award").replace("{number}", remove[2]);
        const award = normal.match(/^(Award title|Framework \(optional\)|Level \(optional\)) — qualification (\d+)$/);
        if (award) return t({"Award title":"award_title","Framework (optional)":"framework","Level (optional)":"award_level"}[award[1]]) + " — " + t("qualification_word") + " " + award[2];
        for (const prefix of ["academic_label", "academic_requirements", "relevance_method", "grades_error"]) {
            const english = catalogue.en[prefix];
            if (normal.startsWith(english)) return t(prefix) + " " + textTranslation(normal.slice(english.length).trim());
        }
        if (normal.includes('more than once')) return t('duplicate_error');
        return original;
    }
    function apply(root = document.body) {
        if (!catalogue) return;
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(node => {
            if (node.parentElement?.closest('script, style, textarea, [data-source-content]')) return;
            if (!originals.has(node)) originals.set(node, node.nodeValue);
            const value = textTranslation(originals.get(node));
            if (node.nodeValue !== value) node.nodeValue = value;
        });
        root.querySelectorAll('[data-i18n]').forEach(node => {
            const key = node.dataset.i18n;
            if (catalogue.en[key] && node.textContent !== t(key)) {
                node.textContent = t(key);
                if (node.firstChild) originals.set(node.firstChild, catalogue.en[key]);
            }
        });
    }
    function setLanguage(value) {
        if (!['en','si','ta'].includes(value)) return;
        language = value;
        document.documentElement.lang = value;
        apply();
        document.dispatchEvent(new CustomEvent('wiselanka:language', {detail:value}));
    }
    async function load() {
        try {
            const response = await fetch(new URL('../../data/localisation/ui.json', document.baseURI));
            if (!response.ok) throw new Error('translations unavailable');
            catalogue = await response.json();
            for (const lang of ['en','si','ta']) {
                if (!catalogue[lang] || Object.keys(catalogue.en).some(key => !catalogue[lang][key])) throw new Error('missing translation keys');
            }
            window.WiseI18n.ready = true;
            apply();
            document.dispatchEvent(new CustomEvent('wiselanka:translations'));
        } catch {
            catalogue = null;
            document.getElementById('translationNotice').textContent = 'Translations could not be loaded. English remains available; reload to retry.';
            document.getElementById('interfaceLanguage').disabled = true;
        }
    }
    document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('interfaceLanguage').addEventListener('change', event => setLanguage(event.target.value));
        let scheduled = false;
        const observer = new MutationObserver(() => {
            if (scheduled) return;
            scheduled = true;
            queueMicrotask(() => { scheduled = false; observer.disconnect(); apply(); observer.observe(document.body,{childList:true,subtree:true,characterData:true}); });
        });
        observer.observe(document.body,{childList:true,subtree:true,characterData:true});
        load();
    });
    return {t, apply, setLanguage, ready:false, get language() {return language;}, get keys() {return catalogue ? Object.keys(catalogue.en) : [];}};
})();
