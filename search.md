---
layout: default
title: Search
---

<div class="search-container">
  <h1>Search the Archive</h1>
  <p class="search-subtitle">Search across all 143 preserved items: papers, videos, and blog posts.</p>

  <div class="search-box">
    <span class="search-icon">
      <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="9" r="6"/><path d="M14 14l4 4"/></svg>
    </span>
    <input type="text" id="search-input" placeholder="Search papers, videos, blog posts..." autocomplete="off">
  </div>

  <div class="search-filters">
    <label><input type="checkbox" id="filter-papers" checked> Papers</label>
    <label><input type="checkbox" id="filter-videos" checked> Videos</label>
    <label><input type="checkbox" id="filter-blog" checked> Blog Posts</label>
  </div>

  <div id="search-results" class="search-results">
    <p class="search-info">Type to search across all content types.</p>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const resultsContainer = document.getElementById('search-results');
  const filterPapers = document.getElementById('filter-papers');
  const filterVideos = document.getElementById('filter-videos');
  const filterBlog = document.getElementById('filter-blog');

  // Single source of truth: _data/*.json synced to data/*.json by
  // `npm run sync-data` (npm prebuild hook + CI step). Blog search defaults
  // to the works list (canonical_works); the 87 CDX captures stay
  // available via data/blog_posts.json. The /papers/, /videos/ and
  // /articles/ detail links below are built by scripts/build_collections.py,
  // and collection_drift() in test_canonical_57.py fails the suite if any
  // generated page is missing for a data row, so a detail link cannot 404
  // without the suite going red. Transcript text is NOT searchable here; it
  // is published under /transcripts/ and listed from the video pages.
  let allData = { papers: [], videos: [], blog_posts: [], captures: [] };
  let loaded = false;

  Promise.all([
    fetch('{{ "/data/papers.json" | relative_url }}').then(function(r) { return r.json(); }),
    fetch('{{ "/data/videos.json" | relative_url }}').then(function(r) { return r.json(); }),
    fetch('{{ "/data/canonical_works.json" | relative_url }}').then(function(r) { return r.json(); }),
    fetch('{{ "/data/blog_posts.json" | relative_url }}').then(function(r) { return r.json(); }).catch(function() { return []; })
  ]).then(function(results) {
    allData.papers = results[0];
    allData.videos = results[1];
    allData.blog_posts = results[2];
    allData.captures = results[3];
    loaded = true;
    updateResultCount();
  }).catch(function(err) {
    console.error('Failed to load search data:', err);
    resultsContainer.innerHTML = '<div class="search-error">Failed to load search data. Please refresh the page.</div>';
  });

  function updateResultCount() {
    if (!loaded) return;
    var total = allData.papers.length + allData.videos.length + allData.blog_posts.length;
    resultsContainer.innerHTML = '<p class="search-info">' + total + ' items ready for search.</p>';
  }

  function getSearchableText(item) {
    var parts = [];
    if (item.title) parts.push(item.title);
    if (item.excerpt) parts.push(item.excerpt);
    if (item.keywords) parts = parts.concat(item.keywords);
    if (item.slug) parts.push(item.slug);
    if (item.date) parts.push(item.date);
    if (item.publisher_journal) parts.push(item.publisher_journal);
    if (item.co_authors) parts = parts.concat(item.co_authors);
    if (item.type) parts.push(item.type);
    if (item.themes) parts = parts.concat(item.themes);
    if (item.topics) parts = parts.concat(item.topics);
    if (item.tone) parts.push(item.tone);
    if (item.url) parts.push(item.url);
    if (item.wayback_url) parts.push(item.wayback_url);
    if (item.filename) parts.push(item.filename);
    return parts.join(' ').toLowerCase();
  }

  // M-09: strip ?query/#fragment before slugify so slugs like
  // "post/?relatedposts=1" never leak into detail URLs.
  function cleanUrl(url) {
    return String(url || '').split('?')[0].split('#')[0];
  }

  // Allowlist: only http(s) URLs reach href attributes (blocks
  // javascript:/data:/vbscript:). Return '' for anything else.
  function safeUrl(url) {
    var u = String(url || '');
    if (!/^https?:\/\//i.test(u)) return '';
    return u.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function getBlogTitle(post) {
    if (post.title && post.title !== '' && !post.title.startsWith('?')) {
      return post.title;
    }
    if (post.slug) {
      return String(post.slug).replace(/[-_]/g, ' ').trim() || post.url || '';
    }
    var urlParts = cleanUrl(post.url).split('/');
    var slug = urlParts[urlParts.length - 1] || urlParts[urlParts.length - 2] || '';
    return slug.replace(/[-_]/g, ' ').replace(/\//g, '').trim() || post.url;
  }

  function renderResults(papers, videos, blogPosts) {
    var html = '';

    if (papers.length > 0) {
      html += '<div class="results-section"><h3>Papers (' + papers.length + ')</h3>';
      papers.forEach(function(paper) {
        html += '<div class="result-item">';
        html += '<h4><a href="{{ "/papers/" | relative_url }}' + encodeURIComponent(paper.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')) + '/">' + escapeHtml(paper.title) + '</a></h4>';
        html += '<div class="result-meta">' + escapeHtml(paper.publisher_journal || '') + '</div>';
        if (paper.co_authors && paper.co_authors.length > 0) {
          html += '<div class="result-meta">Co-authors: ' + escapeHtml(paper.co_authors.join(', ')) + '</div>';
        }
        html += '<div class="result-links">';
        var paperUrl = safeUrl(paper.url);
        if (paperUrl) html += '<a href="' + paperUrl + '" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary">View Original</a>';
        var paperPdf = safeUrl(paper.pdf_url);
        if (paperPdf) html += '<a href="' + paperPdf + '" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline">PDF</a>';
        html += '</div></div>';
      });
      html += '</div>';
    }

    if (videos.length > 0) {
      html += '<div class="results-section"><h3>Videos (' + videos.length + ')</h3>';
      videos.forEach(function(video) {
        html += '<div class="result-item">';
        html += '<h4><a href="{{ "/videos/" | relative_url }}' + encodeURIComponent(video.id) + '/">' + escapeHtml(video.title) + '</a></h4>';
        html += '<div class="result-meta">' + escapeHtml(video.format || '') + '</div>';
        if (video.themes && video.themes.length > 0) {
          html += '<div class="result-themes">';
          video.themes.forEach(function(theme) {
            html += '<span class="tag tag-theme">' + escapeHtml(theme) + '</span>';
          });
          html += '</div>';
        }
        html += '<div class="result-links">';
        var archiveUrl = safeUrl(video.archive_url);
        if (archiveUrl) html += '<a href="' + archiveUrl + '" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary">Download</a>';
        html += '</div></div>';
      });
      html += '</div>';
    }

    if (blogPosts.length > 0) {
      html += '<div class="results-section"><h3>Blog Posts (' + blogPosts.length + ')</h3>';
      blogPosts.forEach(function(post) {
        var title = getBlogTitle(post);
        if (!title) return;
        var rawSlug = post.slug || cleanUrl(post.url).split('/').filter(Boolean).pop() || '';
        html += '<div class="result-item">';
        html += '<h4><a href="{{ "/articles/" | relative_url }}' + encodeURIComponent(rawSlug) + '/">' + escapeHtml(title) + '</a></h4>';
        html += '<div class="result-meta">' + escapeHtml(post.url || post.wayback_url || '') + '</div>';
        if (post.excerpt) html += '<div class="result-excerpt">' + escapeHtml(post.excerpt) + '</div>';
        html += '<div class="result-links">';
        var waybackUrl = safeUrl(post.wayback_url);
        if (waybackUrl) html += '<a href="' + waybackUrl + '" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary">Wayback Machine</a>';
        html += '</div></div>';
      });
      html += '</div>';
    }

    if (!html) {
      html = '<div class="search-no-results">No results found.</div>';
    }

    resultsContainer.innerHTML = html;
  }

  function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  function performSearch() {
    if (!loaded) return;

    var query = searchInput.value.trim().toLowerCase();
    if (query.length < 2) {
      updateResultCount();
      return;
    }

    var matchedPapers = filterPapers.checked ? allData.papers.filter(function(paper) {
      return getSearchableText(paper).indexOf(query) !== -1;
    }) : [];

    var matchedVideos = filterVideos.checked ? allData.videos.filter(function(video) {
      return getSearchableText(video).indexOf(query) !== -1;
    }) : [];

    var matchedBlog = filterBlog.checked ? allData.blog_posts.filter(function(post) {
      if (!getBlogTitle(post)) return false;
      return getSearchableText(post).indexOf(query) !== -1;
    }) : [];

    var total = matchedPapers.length + matchedVideos.length + matchedBlog.length;
    resultsContainer.innerHTML = '<p class="search-info">' + total + ' result' + (total !== 1 ? 's' : '') + ' found.</p>';
    renderResults(matchedPapers, matchedVideos, matchedBlog);
  }

  var debounceTimer;
  searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(performSearch, 300);
  });

  filterPapers.addEventListener('change', performSearch);
  filterVideos.addEventListener('change', performSearch);
  filterBlog.addEventListener('change', performSearch);
});
</script>
