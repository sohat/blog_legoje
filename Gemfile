source "https://rubygems.org"

# Jekyll 4.3 및 Ruby 최신 버전 호환 설정
gem "jekyll", "~> 4.3.3"

# Ruby 3.x 이상에서 표준 라이브러리에서 제외된 항목들 (빌드 오류 방지)
gem "logger"
gem "csv"
gem "base64"
gem "webrick", "~> 1.8"

# GitHub Pages 및 SEO 최적화 필수 플러그인
group :jekyll_plugins do
  gem "jekyll-paginate"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-include-cache" # 빌드 속도 향상을 위한 캐시 플러그인 추가
  gem "jekyll-redirect-from" # URL 리다이렉트 처리
end

# Windows 환경 호환성 설정
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end