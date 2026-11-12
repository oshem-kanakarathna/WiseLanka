(() => {
    const picker = document.querySelector('.pathways-language');
    document.addEventListener('click', event => { if (!picker.contains(event.target)) picker.open = false; });
    picker.addEventListener('keydown', event => {
        if (event.key === 'Escape') { picker.open = false; picker.querySelector('summary').focus(); }
    });
})();
