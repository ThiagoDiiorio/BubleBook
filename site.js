(() => {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('#nav-links');

    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            const open = nav.classList.toggle('is-open');
            toggle.setAttribute('aria-expanded', String(open));
            toggle.textContent = open ? '✕' : '☰';
        });

        nav.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                nav.classList.remove('is-open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.textContent = '☰';
            });
        });
    }

    const sampleText = document.querySelector('#sample-text');
    if (sampleText) {
        let size = 18;
        document.querySelectorAll('[data-sample-font]').forEach((button) => {
            button.addEventListener('click', () => {
                size = Math.max(15, Math.min(25, size + Number(button.dataset.sampleFont) * 2));
                sampleText.style.fontSize = `${size}px`;
            });
        });
    }
})();
