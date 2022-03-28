---
layout: post
title: Embedding Google Fonts for better Privacy and GDPR conformance
author: esko.suomi
excerpt: >
  Regional court in Munich, Germany recently rules Google Fonts as non-GDPR compliant due to the serving mechanism. This does pose a minor challenge, how does one embed webfonts to stay GDPR compliant?

tags:
 - Google Fonts
 - GDPR
 - Privacy
---

Recently the regional court in Germany in Munich declared that embedding Google Fonts on a website violates GDPR ([news article](https://rewis.io/urteile/urteil/lhm-20-01-2022-3-o-1749320/), [judgement](https://rewis.io/s/u/zH2/)).

As a ripple effect, this judgement is now spreading through European Union member nations and especially public sector projects should take heed and replace the embedded fonts with self-hosted versions - after all, the issue isn't the fonts themselves, just the method of serving from an untrustworthy source.

This does pose a minor challenge though, what is the best way to embed Google fonts in 2022? Thankfully, turns out it's not that hard at all.

## Download the fonts

You'll be happy to know that the legwork is already done. I highly recommend the [Google Webfont Downloader](https://nextgenthemes.com/google-webfont-downloader/) which has up-to-date usage instructions right there on its homepage.

The summary of it is that you start by picking your desired fonts as one normally would, but instead of adding the `<link href="https://fonts.googleapis.com" ...>`to your website's `<head>` section you instead take that generated URL and paste it to the only input box on the Downloader page and hit Submit. The page reloads and gives you a download link - super easy!

Now, since this is not the only Google Fonts downloader out there, here's some reasons why you should prefer this one over others:

 - The resulting ZIP file contains a versioned structure of the fonts, eg. `fonts/piazzolla/v23/*.woff2` This is especially useful for serving multiple versions of the same font and just in general tracking which fonts and variants you have.
 - The font license file is included in the font directory. Even though most Google Fonts are [OFL](https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL) licensed, it's always a good bit of due diligence to have the license included and available in case questions arise.
 - There's two variants of the needed CSS included, one with file path references and another with data URLs. Depending on your use case you may prefer one over another, so it's good to have them both available.
 - The generated CSS includes both [`font-display: swap`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) and [`unicode-range`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range) CSS descriptors, which both improve the End User Experience as a whole.

## Add self-hosted fonts to your app

With the ZIP file, the process is really simple:

 1. Include the provided CSS to your project. I highly recommend the file path reference variant unless something blocks you from including static resources to your project.
 2. Include the font files as-is directly from the ZIP to your project's resources, including the license file, in the same structure as provided in the ZIP file.
 3. Do test that the fonts download and render properly after changes.

And that's it! The process really is that easy.