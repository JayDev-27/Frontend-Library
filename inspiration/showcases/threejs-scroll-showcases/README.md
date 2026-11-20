<div align="center">

# Threejs scroll showcases

**Ten cinematic, scroll-driven three.js worlds you can drop into any website. Fully procedural, no build step.**

<a href="https://threejs-scroll-showcases.vercel.app"><img src="https://raw.githubusercontent.com/JayDev-27/Threejs-scroll-showcases/cfcfa2d76880cf3ee392a2b8b413be06c2b231b0/docs/media/sheet.jpg" width="100%" alt="The ten worlds: Nature, Japanese, Cyberpunk, Gaming, Health, Space, Underwater, Mythology, Fantasy and Jaipur"></a>

<sub><a href="https://threejs-scroll-showcases.vercel.app">Open the gallery</a> · <a href="https://github.com/JayDev-27/Threejs-scroll-showcases">Repository</a> (MIT) · <a href="BUILD-PROMPT.md"><b>Build prompt for AI agents →</b></a></sub>

</div>

## At a glance

| | |
|:--|:--|
| **What it is** | A library of ten finished 3D worlds, each with an art-directed camera journey. Feed it scroll progress from 0 to 1; the camera flies, the light changes and the story unfolds. |
| **Author** | [satiricalguru](https://github.com/JayDev-27) |
| **Stack** | three.js r180, WebGL 2, plain ES modules (no bundler), GLSL. Page typography from Google Fonts; everything inside the scenes is local. |
| **Assets** | None. Geometry, textures, foliage, skies and particles are procedural; about 1 MB of source. |
| **Rendering** | HDR pipeline with bloom, light shafts, ambient occlusion, ACES grading, film grain, planar water reflections, aerial haze, drifting cloud shadows. |
| **Performance** | Tiled culling, distance LOD for grass and trees, cached shadow maps, adaptive resolution. |
| **Licence** | **MIT** (three.js MIT in `lib/THREE-LICENSE`). Reuse with attribution. |

## The worlds

| # | World | The journey | Open |
|--:|:--|:--|:--|
| 01 | Nature, *Verdant* | Dawn to full day over an alpine valley: spruce and birch, grass, wildflowers, a mirror lake | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=nature) |
| 02 | Japanese, *Yoizakura* | Vermilion torii, stone lanterns, night sakura, a five-storey pagoda in a moonlit pond | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=japanese) |
| 03 | Cyberpunk, *Neon Rain* | A wet megacity street with reflections, neon signage, hover traffic, holographic koi | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=cyberpunk) |
| 04 | Gaming, *Level Up* | Voxel islands over a synthwave grid, a coin trail, pixel sprites, a portal | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=gaming) |
| 05 | Health, *Vital* | DNA, a living cell, the bloodstream, firing neurons, a beating heart with ECG | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=health) |
| 06 | Space, *Event Horizon* | A living planet, an asteroid belt, a ringed giant, a nebula, a black hole | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=space) |
| 07 | Underwater, *Abyss* | A reef under caustics, fish schools, kelp, a whale, bioluminescent jellyfish | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=underwater) |
| 08 | Mythology, *Olympus* | A marble temple above a sea of cloud, a thunderstorm, an eternal flame, constellations | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=mythology) |
| 09 | Fantasy, *Arcanum* | Floating isles under an aurora, an elder tree of light, a crystal spire, a rune circle | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=fantasy) |
| 10 | Jaipur, *Gulabi Nagar* | Hawa Mahal over a bazaar, decorated elephants, cusped arches, rangoli, a stepwell of diyas | [▶](https://threejs-scroll-showcases.vercel.app/showcase.html?s=jaipur) |

## How it's built

| File | Role |
|:--|:--|
| `lib/engine.js` | Renderer, scroll-to-camera rail, HDR post chain, planar mirror, adaptive quality, ground clearance |
| `lib/kit.js` | Noise, geometry builder, sky dome (sun, moon, stars, clouds, nebula, aurora), particles, water, ground and rock materials, aerial haze, caustics, tiled instancing |
| `lib/flora.js` | Grown trees with branching limbs and leaf, needle or blossom sprays; shrubs, grass clumps, kelp, boulders |
| `scenes/*.js` | One world per file: `build(ctx)` returns a camera rail and `update(time, progress)` |
| `scenes/index.js` | Registry: names, fonts, colours, chapter copy |
| `showcase.html` | A complete scrolling page on `mount()`: chapter copy, per-theme type, progress bar, chapter dots |

```js
import { mount } from './lib/engine.js';
const world = await mount(canvas, 'underwater', {
  progress: () => scrollY / (document.documentElement.scrollHeight - innerHeight),
});
// world.setScene('space') · world.pause() · world.play() · world.dispose()
```

Options: `progress` (0–1 function; the camera eases toward it), `autoplay` (seconds per pass), `damping` (default 3.2), `pointer` (parallax), `quality` (0.5–1 start scale).

### Ideas worth learning

1. **A camera rail keyed by progress**, not time: `{ p, pos, look, fov }` stops eased toward the scroll target, so any scroll library just supplies a number.
2. **One world, one file, one contract:** `build(ctx)` returns `{ rail, floor, update }`; adding a world never touches the engine.
3. **A shared kit** (sky dome, water, haze, caustics, flora) gives ten very different worlds one film-like finish.
4. **Ground clearance** (`floor(x, z)`) keeps the camera out of the terrain on any rail.
5. **Performance as a feature:** tiled culling, LOD, cached shadows and adaptive resolution.

## Use with an agent

The [build prompt](BUILD-PROMPT.md) covers adding a new world in the same style, or building the engine from scratch.

```bash
python3 scripts/query-library.py "scroll" --type showcases --json
```

## Source and rights

Discovered at <https://github.com/JayDev-27/Threejs-scroll-showcases> (commit `cfcfa2d`, 2026-11-16). Facts come from its README and file tree. **MIT licence.** Media on this page is linked from the repository, not copied.
