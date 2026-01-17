// 목차(TOC) 자동 생성 컴포넌트
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const tocContainer = document.getElementById('toc');
        if (!tocContainer) return;

        const contentArea = document.querySelector('.entry-content');
        if (!contentArea) return;

        // 1. h2와 h3를 모두 파악합니다.
        const h2Headings = contentArea.querySelectorAll('h2');
        const h3Headings = contentArea.querySelectorAll('h3');

        let selector = '';

        // 2. 조건별 추출 로직 결정
        if (h2Headings.length === 0) {
            // H2가 아예 없으면 H3를 메인으로 수집
            selector = 'h3';
        } else if (h2Headings.length === 1) {
            // H2가 1개면 보조를 위해 H3까지 수집
            selector = 'h2, h3';
        } else {
            // H2가 여러 개면 깔끔하게 H2만 수집
            selector = 'h2';
        }

        const headings = contentArea.querySelectorAll(selector);

        // 제목이 2개 미만이면 목차 표시 안함
        if (headings.length < 2) {
            tocContainer.style.display = 'none';
            return;
        }

        tocContainer.style.display = 'table';

        const tocList = document.createElement('ul');
        tocList.className = 'toc-list toc-list-level-1';

        let currentH2Item = null;
        let h2List = null;

        headings.forEach(function(heading, index) {
            const headingText = heading.textContent.trim();
            if (!headingText) return;

            const id = 'toc-' + index;
            heading.id = id;

            const li = document.createElement('li');
            // H2가 없을 때 H3가 최상위면 레벨을 2로 시각적 처리 (CSS 일관성)
            const displayLevel = (h2Headings.length === 0 && heading.tagName === 'H3') ? '2' : heading.tagName.charAt(1);
            li.className = 'toc-item toc-heading-level-' + displayLevel;

            const link = document.createElement('a');
            link.className = 'toc-link';
            link.href = '#' + id;
            link.textContent = headingText;

            link.addEventListener('click', function(e) {
                e.preventDefault();
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
                history.pushState(null, null, '#' + id);
            });

            li.appendChild(link);

            const level = parseInt(heading.tagName.charAt(1));

            // 계층 구조 처리
            if (level === 2 || (h2Headings.length === 0 && level === 3)) {
                // H2이거나, H2가 없는 상태에서 H3인 경우 (최상위)
                currentH2Item = li;
                h2List = null;
                tocList.appendChild(li);
            } else if (level === 3) {
                // H2 하위의 H3인 경우
                if (currentH2Item) {
                    if (!h2List) {
                        h2List = document.createElement('ul');
                        h2List.className = 'toc-list-level-3';
                        currentH2Item.appendChild(h2List);
                    }
                    h2List.appendChild(li);
                }
            }
        });

        const nav = tocContainer.querySelector('nav');
        if (nav) {
            nav.innerHTML = '';
            nav.appendChild(tocList);
        }

        const toggleBtn = tocContainer.querySelector('.toc-toggle');
        if (toggleBtn && nav) {
            let isOpen = true;
            toggleBtn.addEventListener('click', function(e) {
                e.preventDefault();
                isOpen = !isOpen;
                nav.style.display = isOpen ? 'block' : 'none';
            });
        }
    });
})();