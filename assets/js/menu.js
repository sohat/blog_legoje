// 모바일 메뉴 토글
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navigation = document.getElementById('site-navigation');

    if (!menuToggle || !navigation) return;

    // 메인 메뉴 토글
    menuToggle.addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true';

        this.setAttribute('aria-expanded', !expanded);
        navigation.classList.toggle('toggled');

        const menuList = navigation.querySelector('#menu-menu');
        if (menuList) {
            menuList.setAttribute('aria-hidden', expanded);
        }
    });

    // 서브메뉴 토글
    const dropdownToggles = navigation.querySelectorAll('.dropdown-menu-toggle');
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const parent = this.closest('.menu-item-has-children');
            const subMenu = parent.querySelector('.sub-menu');

            if (subMenu) {
                subMenu.classList.toggle('toggled-on');
                const isExpanded = subMenu.classList.contains('toggled-on');
                this.setAttribute('aria-expanded', isExpanded);
            }
        });
    });
});
