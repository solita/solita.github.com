# Introduction to bidirectional languages in your website

## What are bidirectional languages?

Bidirectional languages or BiDi languages for short refers to Bidirectional languages which contains both left-to-right (LTR) and right-to-left (RTL) writing orders.

A website supporting BiDi text is just not all about translation or mirroring text depending on the language used. BiDi support is about expected behavior. On addition to displaying text there should be also ability to input text in either RTL or LTR depending on the language used and in some cases the ability to display different calendars, e.g. [Solar Hijri Calendar](https://en.wikipedia.org/wiki/Solar_Hijri_calendar)

## Examples on what to flip when displaying RTL writing systems

- Reading order
- Directional icons e.g. arrow icons
- Image locations
- Buttons
- Columns
- Page number

Some common mistakes are flipping elements that shouldn't be flipped such as images, original Arabic digits (1, 2, 3 etc.) and media player buttons.

Next I will demonstrate what to do and consider when creating a website for both LTR and RTL layouts.

## Tech stack

- React
- Typescript
- Vite
- TailwindCSS

Below is a simple site on my two lovely cats Ninni and Eino because who doesn't love cats?

![[simple website 1.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/1.png)

I have made two localization files `en.json` and `fa.json`. I will handle the localization with [react-i18next](https://www.react.i18next.com/).

Let's see what happens when I change the language without doing anything with RTL layout in mind.

![[simple website 2.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/2.png)

Not as bad as you would think but there are few things that are wrong here. The header should be flipped and the names `Ninni` and `Eino` beside the pictures should be aligned to the left side.

Fortunately there is a quick fix for this. We can set the directionality for the element's using the `dir` attribute. We can set it on specific elements but for this case we want it on the whole html.

```html
<html dir="rtl"></html>
```

Let's change the directionality every time the language changes.

```typescript
useEffect(() => {
  const dir = i18n.dir(i18n.language);
  document.documentElement.dir = dir;
}, [i18n, i18n.language]);
```

Let's see what's changed.

![[simple website 3.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/3.png)

Everything is now flipped correctly and we are finished here right? Well there seems to be few things still that are wrong here.

### Margin and padding

If we take a closer look we can see that the margins and paddings aren't flipped when the directionality changes. When creating a website with support for both directionalities you should avoid using `margin` and `padding`. Instead we should use `margin-inline-start`, `margin-inline-end, `
`padding-inline-start` and `padding-inline-start` which aligns items depending on the directionality.

[Tailwind](https://tailwindcss.com/blog/tailwindcss-v3) offers RTL and LTR modifiers which can be used.

```html
<header className="... ltr:pl-4 rtl:pr-4"></header>
```

![[simple website 4.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/4.png)

Now the margins are fixed on the header. There is still one small quirk when setting directionality for the page.

I didn't translate this text just to demonstrate this special case when having LTR text in a RTL directional page.

![[simple website 5.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/5.png)

### Neutral characters

Some Unicode characters are not associated with some directionality e.g. numbers and punctuation. These characters are considered to be weak or neutral. The [Unicode bidirectional algorithm](https://www.w3.org/International/articles/inline-bidi-markup/uba-basics) usually handles these situations but not always.

In this case the text is in English but the language is set to Farsi and the base direction is RTL. This is why the exclamation mark is on the left side.

We can fix this by using [bidirectional isolate element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi) `<bdi>` instead of e.g. `p` but as for now this isn't supported on Safari browser. The other way is to set the directionality on the element that contains LTR text.

```html
<p dir="ltr" className="self-center text-sm text-primary">{t("ltr_text")}</p>
```

![[simple website 6.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/6.png)

Now the exclamation mark is in the correct place and the website look already much better and supports RTL layouts correctly.

![[simple website 7.png]](/img/2025-05-16-introduction-to-bidirectional-languages-in-your-website/7.png)

## What else?

There is a lot more to be considered when supporting RTL layouts with localization such as inputs, dates, numerals. In the theme of introduction I wanted to keep it simple and focus on the layout itself and some edge cases like the LTR text in RTL directional page.

If there is a need for a deep dive on bidirectional text and localization I will make a another post with more info on how to tackle these cases.

## Final words

When deciding on supporting RTL layouts you should be considering the look of the website and the layout of the website right from start. It's much easier to work with bidirectionality from the start rather than implementing it on top of a LTR designed site.

I hope that this post will help you with your journey to RTL layouts.

!gnidoc yppaH
