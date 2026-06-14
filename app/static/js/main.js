document.addEventListener('DOMContentLoaded', function () {

    function applyTheme(theme) {
        const html = document.documentElement;
        html.setAttribute('data-bs-theme', theme);
        document.body.className = theme + '-mode';
        document.querySelectorAll('#themeToggle, #themeToggleMobile').forEach(el => {
            if (el) el.innerHTML = theme === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-fill"></i>';
        });
        fetch('/api/settings/theme', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ theme: theme })
        }).catch(() => {});
    }

    function getTheme() { return document.documentElement.getAttribute('data-bs-theme') || 'light'; }

    document.querySelectorAll('#themeToggle, #themeToggleMobile').forEach(toggle => {
        if (toggle) {
            toggle.innerHTML = getTheme() === 'dark' ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-fill"></i>';
            toggle.addEventListener('click', function () {
                applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
            });
        }
    });

    document.querySelectorAll('.faq-question').forEach(btn => {
        btn.addEventListener('click', function () {
            const item = this.closest('.faq-item-modern, .faq-item');
            if (!item) return;
            const isActive = item.classList.contains('active');
            document.querySelectorAll('.faq-item-modern.active, .faq-item.active').forEach(el => el.classList.remove('active'));
            if (!isActive) item.classList.add('active');
        });
    });

    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        filterForm.querySelectorAll('select, input').forEach(el => {
            el.addEventListener('change', function () { filterForm.submit(); });
        });
    }

    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!confirm('هل أنت متأكد من الحذف؟')) e.preventDefault();
        });
    });

    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach(area => {
        const input = area.querySelector('input[type="file"]');
        if (input) {
            area.addEventListener('click', () => input.click());
            input.addEventListener('change', function () {
                if (this.files.length > 0) {
                    const label = area.querySelector('.upload-label');
                    if (label) label.textContent = this.files[0].name;
                    this.closest('form')?.submit();
                }
            });
        }
    });

    function previewImage(input, previewId) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const preview = document.getElementById(previewId);
                if (preview) preview.src = e.target.result;
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
    document.querySelectorAll('input[type="file"]').forEach(input => {
        const previewId = input.getAttribute('data-preview');
        if (previewId) {
            input.addEventListener('change', function () { previewImage(this, previewId); });
        }
    });

    /* ─── Mobile Sidebar Toggle ─── */
    const sidebar = document.getElementById('adminSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const closeBtn = document.getElementById('sidebarClose');
    let toggleBtn = document.getElementById('sidebarToggle');

    /* Inject toggle button if sidebar exists and toggle doesn't */
    if (sidebar && !toggleBtn) {
      toggleBtn = document.createElement('button');
      toggleBtn.id = 'sidebarToggle';
      toggleBtn.className = 'sidebar-toggle';
      toggleBtn.type = 'button';
      toggleBtn.setAttribute('aria-label', 'Toggle menu');
      toggleBtn.innerHTML = '<i class="bi bi-list"></i>';
      const content = document.querySelector('.admin-content');
      if (content) {
        const header = content.querySelector('.admin-content-header');
        if (header) {
          const titleDiv = header.querySelector('div');
          if (titleDiv) {
            titleDiv.insertBefore(toggleBtn, titleDiv.firstChild);
          } else {
            header.insertBefore(toggleBtn, header.firstChild);
          }
        } else {
          content.insertBefore(toggleBtn, content.firstChild);
        }
      }
    }

    if (sidebar && overlay) {
      function openSidebar() {
        sidebar.classList.add('open');
        overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
      }
      function closeSidebar() {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
        document.body.style.overflow = '';
      }
      if (toggleBtn) toggleBtn.addEventListener('click', openSidebar);
      if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
      overlay.addEventListener('click', closeSidebar);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) closeSidebar();
      });
    }

    const toastElList = document.querySelectorAll('.toast');
    toastElList.forEach(el => { new bootstrap.Toast(el).show(); });

    const notificationBell = document.getElementById('notificationBell');
    if (notificationBell) {
        function updateNotifCount() {
            fetch('/api/notifications/count')
                .then(r => r.json())
                .then(data => {
                    const badge = notificationBell.querySelector('.badge');
                    if (badge) {
                        badge.textContent = data.count;
                        badge.style.display = data.count > 0 ? '' : 'none';
                    }
                });
        }
        updateNotifCount();
        setInterval(updateNotifCount, 30000);
    }

});

function initSortable(containerId, url) {
    const container = document.getElementById(containerId);
    if (!container || typeof Sortable === 'undefined') return;

    new Sortable(container, {
        animation: 200,
        handle: '.drag-handle',
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        onEnd: function () {
            const order = [];
            container.querySelectorAll('[data-id]').forEach((el, index) => {
                order.push({ id: parseInt(el.dataset.id), order: index });
            });
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ order: order })
            }).then(r => r.json()).then(console.log).catch(console.error);
        }
    });
}

function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}
