/**
 * 목차(TOC) 자동 생성 컴포넌트 - 최종 배포 버전
 * 실행 시점 지연 및 CSS 강제 주입 로직 포함
 */
(function() {
    'use strict';

    function buildTOC() {
        // 1. 필수 요소 정의
        const tocContainer = document.getElementById('toc');
        const contentArea = document.querySelector('.entry-content');
        const navElement = document.querySelector('#toc nav');

        // 요소가 하나라도 없으면 중단
        if (!tocContainer || !contentArea || !navElement) return;

        // 2. 제목 수집 로직
        const h2Headings = contentArea.querySelectorAll('h2');
        let selector = (h2Headings.length <= 1) ? 'h2, h3' : 'h2';
        const headings = contentArea.querySelectorAll(selector);

        // 3. 조건부 노출 (제목이 2개 미만일 때)
        if (headings.length < 2) {
            tocContainer.style.setProperty('display', 'none', 'important');
            return;
        }

        // 4. 리스트 생성
        const tocList = document.createElement('ul');
        tocList.className = 'toc-list toc-list-level-1';

        let currentH2Item = null;
        let h2List = null;

        headings.forEach(function(heading, index) {
            const headingText = heading.textContent.trim();
            if (!headingText) return;

            // ID 부여 및 스크롤 위치 보정용 스타일
            const id = 'toc-item-' + index;
            heading.id = id;

            const li = document.createElement('li');
            const level = parseInt(heading.tagName.charAt(1));
            li.className = 'toc-item toc-heading-level-' + level;

            const link = document.createElement('a');
            link.className = 'toc-link';
            link.href = '#' + id;
            link.textContent = headingText;

            // 부드러운 스크롤 이벤트
            link.addEventListener('click', function(e) {
                e.preventDefault();
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
                history.pushState(null, null, '#' + id);
            });

            li.appendChild(link);

            // 계층 구조 (H2-H3) 처리
            if (level === 2 || (h2Headings.length === 0 && level === 3)) {
                currentH2Item = li;
                h2List = null;
                tocList.appendChild(li);
            } else if (level === 3 && currentH2Item) {
                if (!h2List) {
                    h2List = document.createElement('ul');
                    h2List.className = 'toc-list-level-3';
                    currentH2Item.appendChild(h2List);
                }
                h2List.appendChild(li);
            }
        });

        // 5. 화면에 주입 및 강제 노출
        navElement.innerHTML = '';
        navElement.appendChild(tocList);

        // CSS 우선순위 문제를 해결하기 위해 !important 스타일 강제 부여
        tocContainer.style.setProperty('display', 'table', 'important');
        navElement.style.setProperty('display', 'block', 'important');
    }

    // [핵심] DOM 파싱 완료 즉시 실행 (이미지 로드 기다리지 않음)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildTOC);
    } else {
        buildTOC();
    }
})();