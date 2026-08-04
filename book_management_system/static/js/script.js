/* =============================================================
   College Library - Book Management System
   Main JavaScript (Vanilla JS only - no jQuery, no frameworks)
   Written in plain ES5-style syntax for compatibility with
   older browsers that may still be in use on Windows 7 labs.
   ============================================================= */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------------- Sidebar toggle ---------------- */
    var toggleBtn = document.getElementById('sidebarToggle');
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.getElementById('mainContent');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            var isMobile = window.innerWidth <= 900;
            if (isMobile) {
                sidebar.className = sidebar.className.indexOf('show') === -1
                    ? sidebar.className + ' show'
                    : sidebar.className.replace(' show', '');
            } else {
                if (sidebar.className.indexOf('collapsed') === -1) {
                    sidebar.className += ' collapsed';
                    if (mainContent) { mainContent.className += ' expanded'; }
                } else {
                    sidebar.className = sidebar.className.replace(' collapsed', '');
                    if (mainContent) { mainContent.className = mainContent.className.replace(' expanded', ''); }
                }
            }
        });
    }

    /* ---------------- Auto-dismiss alert messages ---------------- */
    var alerts = document.querySelectorAll('.alert');
    for (var i = 0; i < alerts.length; i++) {
        (function (alertEl) {
            setTimeout(function () {
                alertEl.style.display = 'none';
            }, 5000);
        })(alerts[i]);
    }

    /* ---------------- Basic client-side form validation ---------------- */
    var forms = document.querySelectorAll('form[novalidate]');
    for (var j = 0; j < forms.length; j++) {
        forms[j].addEventListener('submit', function (event) {
            if (!this.checkValidity || typeof this.checkValidity !== 'function') {
                return; // very old browsers without HTML5 validation API - skip silently
            }
            if (!this.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    }

    /* ---------------- Close modal when clicking outside modal-box ---------------- */
    var overlays = document.querySelectorAll('.modal-overlay');
    for (var k = 0; k < overlays.length; k++) {
        overlays[k].addEventListener('click', function (event) {
            if (event.target === this) {
                this.className = this.className.replace(' open', '');
            }
        });
    }

    /* ---------------- Close any open modal on Escape key ---------------- */
    document.addEventListener('keyup', function (event) {
        if (event.keyCode === 27) {
            var openModals = document.querySelectorAll('.modal-overlay.open');
            for (var m = 0; m < openModals.length; m++) {
                openModals[m].className = openModals[m].className.replace(' open', '');
            }
        }
    });
});

/* ---------------- Modal open/close helpers (used inline via onclick) ---------------- */

function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.className += ' open';
    }
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.className = modal.className.replace(' open', '');
    }
}
