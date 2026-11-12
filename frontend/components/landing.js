(() => {
    const picker = document.querySelector('.landing-language');
    document.addEventListener('click', event => { if (!picker.contains(event.target)) picker.open = false; });
    picker.addEventListener('keydown', event => { if (event.key === 'Escape') { picker.open = false; picker.querySelector('summary').focus(); } });
})();
