// 목차(TOC) 자동 생성
document.addEventListener('DOMContentLoaded', function() {

    // 목차 컨테이너 찾기
    const tocContainer = document.getElementById('toc');
    if (!tocContainer) {
        return;
    }

    // 본문에서 제목들 가져오기
    const headings = document.querySelectorAll('.entry-content h3, .entry-content h4');
    if (headings.length === 0) {
        return;
    }

    // 새 목차 리스트 생성
    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';

    headings.forEach(function(heading, index) {
        // 제목에 ID 부여
        const id = 'toc-heading-' + index;
        heading.id = id;

        // 목차 항목 생성
        const li = document.createElement('li');
        li.className = 'toc-item toc-' + heading.tagName.toLowerCase();

        const link = document.createElement('a');
        link.href = '#' + id;
        link.textContent = heading.textContent.trim();
        link.addEventListener('click', function(e) {
            e.preventDefault();
            heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
            history.pushState(null, null, '#' + id);
        });

        li.appendChild(link);
        tocList.appendChild(li);
    });

    // 기존 ez-toc 내용 교체
    const nav = tocContainer.querySelector('nav');
    if (nav) {
        nav.innerHTML = '';
        nav.appendChild(tocList);
    } else {
        // nav가 없으면 제목 다음에 추가
        const titleContainer = tocContainer.querySelector('.ez-toc-title-container');
        if (titleContainer) {
            const newNav = document.createElement('nav');
            newNav.appendChild(tocList);
            titleContainer.after(newNav);
        }
    }
});
