'use strict';

function TagCloud(tagElements, maxFontSize, minFontSize, fontSizeUnit, colorHue, colorSaturation, colorLightness) {
    var tags = [],
        tagCounts = [];

    for (var i = 0; i < tagElements.length; ++i) {
        var el = tagElements[i];
        var tag = {
            element: el,
            count: parseInt(el.getAttribute('data-count'))
        };
        tags.push(tag);
        tagCounts.push(tag.count);
    }

    var min = Math.min.apply(null, tagCounts),
        max = Math.max.apply(null, tagCounts);

    tags.forEach(function (tag) {
        // Calculate weights
        var weight = (Math.log(tag.count) - Math.log(min)) / (Math.log(max) - Math.log(min));

        // Calculate styles based on weight
        var fontSize = minFontSize + ((maxFontSize - minFontSize) * weight);
        var lightness = colorLightness - (((fontSize - minFontSize) / 4));

        // Set styles
        tag.element.style.fontSize = fontSize + fontSizeUnit;
        tag.element.style.color = 'hsl(' + colorHue + ',' + colorSaturation + '%,' + lightness + '%)';
    });
}
