# Lumax Wind Actions — SANS 10160-3

Wind actions calculator to SANS 10160-3.

**Live site:** https://lumax-energy.github.io/lumax-wind-actions/

Single-page app — open `index.html` or use GitHub Pages above.

## Files

| File | What it is |
|---|---|
| `index.html` | The app: markup, styles and script |
| `fig1-map.js` | SANS 10160-3 Figure 1 (3 s gust map, 958 × 768 px) as a data URI. Loaded by `index.html` to show the site on the map and read the wind zone under it. Without it the municipality table still works |

The site and v<sub>b,0</sub> are set with **Set the site on the map**: choose a municipality (table value, site at its centroid), enter GPS coordinates, or click the map (zone colour under the site; the higher value on a zone boundary). This is the former [sans10160-wind-map](https://github.com/Lumax-Energy/sans10160-wind-map) tool built in.
