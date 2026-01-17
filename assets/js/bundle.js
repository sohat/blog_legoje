---
---
{% capture jscode %}
{% include_relative menu.js %}
{% include_relative toc.js %}
{% endcapture %}
{{ jscode | strip_newlines | replace: '  ', '' | replace: '	', '' }}
;