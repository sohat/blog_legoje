// 목차(TOC) 자동 생성 컴포넌트 (최종 수정본)
(function() {
    'use strict';

    function initTOC() {
        const tocContainer = document.getElementById('toc');
        if (!tocContainer) {
            console.log('TOC: #toc 컨테이너를 찾을 수 없습니다.');
            return;
        }

        const contentArea = document.querySelector('.entry-content');
        if (!contentArea) {
            console.log('TOC: .entry-content 영역을 찾을 수 없습니다.');
            return;
        }

        // 1. h2와 h3 파악
        const h2Headings = contentArea.querySelectorAll('h2');
        let selector = '';

        // 2. 조건별 추출 로직 결정
        if (h2Headings.length === 0) {
            selector = 'h3'; // H2 없으면 H3만
        } else if (h2Headings.length === 1) {
            selector = 'h2, h3'; // H2 1개면 H3까지
        } else {
            selector = 'h2'; // H2 여러 개면 H2만
        }

        const headings = contentArea.querySelectorAll(selector);
        console.log('TOC: 선택된 제목 개수 =', headings.length);

        // 제목이 2개 미만이면 숨김
        if (headings.length < 2) {
            tocContainer.style.setProperty('display', 'none', 'important');
            return;
        }

        // 목차 강제 표시 (CSS 우선순위 무시를 위해 !important 스타일 적용)
        tocContainer.style.setProperty('display', 'table', 'important');

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
                currentH2Item = li;
                h2List = null;
                tocList.appendChild(li);
            } else if (level === 3) {
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
            nav.style.display = 'block'; // nav 영역도 확실히 표시
        }

        // 토글 기능
        const toggleBtn = tocContainer.querySelector('.toc-toggle');
        if (toggleBtn && nav) {
            let isOpen = true;
            toggleBtn.addEventListener('click', function(e) {
                e.preventDefault();
                isOpen = !isOpen;
                nav.style.display = isOpen ? 'block' : 'none';
            });
        }
    }

    // DOM이 이미 로드되었는지 확인 후 실행
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTOC);
    } else {
        initTOC();
    }
})();