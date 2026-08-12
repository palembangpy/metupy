/* ==========================================================================
   Metupy Custom JavaScript (Fixed Version)
   ========================================================================== */

// Simpan instance observer secara global agar bisa dicleanup
let tocObserver = null;

function initToC() {
    const content = document.getElementById('main-content');
    if (!content) return;

    // Ambil semua tag heading yang di-render oleh Markdown Python
    const headings = content.querySelectorAll('h1, h2, h3');
    const tocDesktop = document.getElementById('toc-desktop');
    const tocMobile = document.getElementById('toc-mobile');
    const fabBtn = document.getElementById('fab-toc-btn');
    const desktopContainer = document.getElementById('toc-desktop-container');

    // Jika halaman tidak memiliki heading sama sekali
    if (!headings || headings.length === 0) {
        if (desktopContainer) desktopContainer.style.display = 'none';
        if (fabBtn) fabBtn.classList.add('hidden');
        if (tocDesktop) tocDesktop.innerHTML = '<span class="toc-empty">Tidak ada daftar isi</span>';
        if (tocMobile) tocMobile.innerHTML = '<span class="toc-empty">Tidak ada daftar isi</span>';
        return;
    }

    // Tampilkan kembali jika ada heading
    if (desktopContainer) desktopContainer.style.display = 'block';
    if (fabBtn) fabBtn.classList.remove('hidden');

    let tocHtml = '';
    headings.forEach((heading, index) => {
        // Buat ID unik jika heading belum punya ID
        if (!heading.id) {
            const cleanText = heading.textContent.trim().toLowerCase().replace(/[^\w]+/g, '-');
            heading.id = `heading-${index}-${cleanText}`;
        }

        const tag = heading.tagName.toLowerCase();
        const text = heading.textContent.trim();

        tocHtml += `<a href="#${heading.id}" class="toc-link toc-${tag}" data-toc-id="${heading.id}">${text}</a>`;
    });

    // Suntikkan HTML ToC ke Desktop & Mobile
    if (tocDesktop) tocDesktop.innerHTML = tocHtml;
    if (tocMobile) tocMobile.innerHTML = tocHtml;

    // --- SCROLLSPY (INDIKATOR LINK AKTIFA) ---
    // Cleanup observer lama jika ada
    if (tocObserver) {
        tocObserver.disconnect();
    }

    tocObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                document.querySelectorAll('.toc-link').forEach(link => {
                    if (link.getAttribute('data-toc-id') === id) {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });
            }
        });
    }, {
        root: null,
        rootMargin: '-80px 0px -60% 0px',
        threshold: 0
    });

    headings.forEach(heading => tocObserver.observe(heading));
}

// Jalankan saat load awal & setiap kali HTMX swap halaman
document.addEventListener('DOMContentLoaded', initToC);
document.addEventListener('htmx:afterSettle', initToC);

// Keyboard Shortcut (Ctrl + K) untuk Search Modal
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        const searchTrigger = document.querySelector('.search-trigger');
        if (searchTrigger) searchTrigger.click();
    }
});

// Copy Code Terminal
function copyMetupyCode(btn) {
    const codeBlock = btn.closest('.metupy-terminal')?.querySelector('code');
    if (!codeBlock) return;

    navigator.clipboard.writeText(codeBlock.textContent).then(() => {
        const span = btn.querySelector('span');
        const originalText = span ? span.textContent : 'Copy';
        
        if (span) span.textContent = 'Copied!';
        btn.style.color = '#27c93f';
        btn.style.borderColor = '#27c93f';

        setTimeout(() => {
            if (span) span.textContent = originalText;
            btn.style.color = '';
            btn.style.borderColor = '';
        }, 2000);
    });
}
