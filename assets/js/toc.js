// 목차(TOC) 자동 생성 컴포넌트
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const tocContainer = document.getElementById('toc');
        if (!tocContainer) return;

        // 본문에서 제목들 가져오기 (h2, h3, h4)
        const contentArea = document.querySelector('.entry-content');
        if (!contentArea) return;

        const headings = contentArea.querySelectorAll('h2, h3, h4');

        // 제목이 2개 미만이면 목차 표시 안함
        if (headings.length < 2) {
            tocContainer.style.display = 'none';
            return;
        }

        // 목차 컨테이너 표시
        tocContainer.style.display = 'table';

        // 목차 리스트 생성
        const tocList = document.createElement('ul');
        tocList.className = 'toc-list toc-list-level-1';

        let currentH2Item = null;
        let currentH3Item = null;
        let h2List = null;
        let h3List = null;

        headings.forEach(function(heading, index) {
            // 빈 제목 무시
            const headingText = heading.textContent.trim();
            if (!headingText) return;

            // 제목에 고유 ID 부여
            const id = 'toc-' + index;
            heading.id = id;

            // 목차 항목 생성
            const li = document.createElement('li');
            li.className = 'toc-item toc-heading-level-' + heading.tagName.charAt(1);

            const link = document.createElement('a');
            link.className = 'toc-link';
            link.href = '#' + id;
            link.textContent = headingText;

            // 부드러운 스크롤
            link.addEventListener('click', function(e) {
                e.preventDefault();
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
                history.pushState(null, null, '#' + id);
            });

            li.appendChild(link);

            // 계층 구조 처리
            const level = parseInt(heading.tagName.charAt(1));

            if (level === 2) {
                // H2: 최상위 레벨
                currentH2Item = li;
                currentH3Item = null;
                h2List = null;
                h3List = null;
                tocList.appendChild(li);
            } else if (level === 3) {
                // H3: H2 하위
                if (currentH2Item) {
                    if (!h2List) {
                        h2List = document.createElement('ul');
                        h2List.className = 'toc-list-level-3';
                        currentH2Item.appendChild(h2List);
                    }
                    h2List.appendChild(li);
                    currentH3Item = li;
                    h3List = null;
                } else {
                    // H2가 없으면 최상위에 추가
                    tocList.appendChild(li);
                    currentH3Item = li;
                }
            } else if (level === 4) {
                // H4: H3 하위
                if (currentH3Item) {
                    if (!h3List) {
                        h3List = document.createElement('ul');
                        h3List.className = 'toc-list-level-4';
                        currentH3Item.appendChild(h3List);
                    }
                    h3List.appendChild(li);
                } else if (h2List) {
                    // H3가 없지만 H2가 있으면 H2 하위에 추가
                    h2List.appendChild(li);
                } else {
                    // 그 외에는 최상위에 추가
                    tocList.appendChild(li);
                }
            }
        });

        // 목차가 비어있으면 숨김
        if (tocList.children.length === 0) {
            tocContainer.style.display = 'none';
            return;
        }

        // 기존 nav에 목차 추가
        const nav = tocContainer.querySelector('nav');
        if (nav) {
            nav.innerHTML = '';
            nav.appendChild(tocList);
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
    });
})();
