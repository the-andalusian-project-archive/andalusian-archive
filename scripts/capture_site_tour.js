// Capture the site-tour source frames. Light theme. 2026-09-28.
//
// Kept in the repository because the previous tour was cut by a script that
// lived outside it: the 19 source frames went into a gitignored directory and
// the pipeline that produced them was lost, so re-recording meant rebuilding it
// from scratch. build_site_tour.py records the other half - the segments, the
// captions and the ffmpeg invocation - and this records the first half.
//
// HOW TO RUN. The repository has no Playwright dependency and this is not a
// standalone runner; it is a function to paste into the browser tool, which
// supplies `page`. `node scripts/capture_site_tour.js` will not work, and adding
// Playwright means a devDependency and a ~150 MB Chromium download, which is
// not worth it to re-record thirteen frames.
//
//   await page -> paste, then:
//
//   (await import('D:/The Andalusian Project/scripts/capture_site_tour.js'))
//
// The tour is captured from a LOCAL build served on 127.0.0.1, not from the
// deployed github.io site. The docs previously said otherwise; that was wrong.
//
// WHY BOTH theme calls. emulateMedia sets the OS preference; the localStorage
// write is what the site actually reads. _layouts/default.html applies
// data-theme from localStorage['tap-theme'] before first paint, and the light
// tokens live under :root[data-theme="light"] in assets/css/style.css, so
// without the storage write the capture would only be a media-query
// approximation of light rather than the genuine light theme a reader gets by
// choosing it.
//
// WHY await document.fonts.ready. The webfonts load after `load`, and a frame
// captured mid-swap reflows the whole page while zoompan is moving it, which
// reads as a jump. The old capture used a fixed 450ms wait, which is a race
// with the font that happens to win on a warm cache.
async (page) => {
  const BASE = 'http://127.0.0.1:8899/andalusian-archive';
  const DIR = 'D:/The Andalusian Project/andalusian-archive/_staging/demo-tour/';
  const THEME = 'light';

  // The 13 SEGMENTS in scripts/build_site_tour.py, in order. The two `-b`
  // frames are the same URL scrolled one viewport down.
  const FRAMES = [
    ['01-home', '/', false],
    ['01-home-b', '/', true],
    ['02-topics', '/topics/', false],
    ['03-subject', '/topics/atheism-doubt/', false],
    ['03-subject-b', '/topics/atheism-doubt/', true],
    ['04-articles', '/articles/', false],
    ['05-work', '/articles/atheism-doubting-your-doubts/', false],
    ['06-papers', '/papers/', false],
    ['07-paper', '/papers/the-qur-an-and-science-a-forced-marriage/', false],
    ['08-transcripts', '/transcripts/', false],
    ['09-transcript', '/transcripts/1962338957360877/', false],
    ['10-channel', '/channel/', false],
    ['11-search', '/search/', false],
  ];

  await page.emulateMedia({ colorScheme: THEME });
  await page.setViewportSize({ width: 1440, height: 900 });

  // Set the preference AFTER landing on the site origin, not before. The first
  // version of this script wrote localStorage before its first goto, where the
  // page was still whatever the previous tool call left behind; if that was not
  // this origin the write threw, the surrounding `catch` swallowed it, and the
  // capture carried on - producing frames that were light only because the
  // emulated OS was light. It looked correct and was not the theme a reader
  // gets by choosing Light, which is the thing being recorded.
  await page.goto(BASE + '/', { waitUntil: 'load' });
  await page.evaluate((t) => {
    localStorage.setItem('tap-theme', t);
  }, THEME);

  const done = [];
  const problems = [];
  for (const [name, path, scroll] of FRAMES) {
    await page.goto(BASE + path, { waitUntil: 'load' });
    // Fonts first, then the scroll, then a beat for the sticky nav to settle.
    await page.evaluate(() => document.fonts.ready);
    if (scroll) {
      await page.evaluate(() => window.scrollTo(0, Math.round(window.innerHeight * 0.9)));
      await page.evaluate(() => document.fonts.ready);
    }
    await page.waitForTimeout(250);
    // Record what the frame actually is, so the caption cannot drift from it.
    const seen = await page.evaluate(() => ({
      stored: localStorage.getItem('tap-theme'),
      theme: document.documentElement.getAttribute('data-theme'),
      bg: getComputedStyle(document.body).backgroundColor,
      h1: (document.querySelector('h1') || {}).textContent || '',
    }));
    // A wrong theme here is a failed capture, not a warning: a light frame
    // reached by the media query instead of by the reader's own choice is not
    // the light theme, and would make the docs claim true only by luck.
    if (seen.theme !== THEME || seen.stored !== THEME) {
      problems.push(`${name}: stored=${seen.stored} data-theme=${seen.theme}, `
        + `expected ${THEME}`);
      continue;
    }
    await page.screenshot({ path: DIR + name + '.png' });
    done.push({ name, bg: seen.bg, h1: seen.h1.trim().slice(0, 40) });
  }
  // Leave the reader's stored preference alone for whatever runs next.
  await page.evaluate(() => { try { localStorage.removeItem('tap-theme'); } catch (e) {} });
  return { captured: done.length, expected: FRAMES.length, theme: THEME, problems, frames: done };
}
