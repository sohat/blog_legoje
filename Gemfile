source "https://rubygems.org"

# Ruby 4.0 호환 Jekyll 설정
gem "jekyll", "~> 4.3"

# Ruby 4.0에서 기본 gem에서 제외된 라이브러리들
gem "logger"
gem "csv"
gem "base64"

group :jekyll_plugins do
  gem "jekyll-paginate"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
end

# Windows and JRuby does not include zoneinfo files
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "webrick", "~> 1.8"
