# Build prompt: scroll-driven three.js worlds

Two prompts for an AI coding agent: **A** adds a new world to
[Threejs scroll showcases](https://github.com/JayDev-27/Threejs-scroll-showcases) (MIT), and **B** builds an
engine like it from scratch. Background: [README.md](README.md).

> [!NOTE]
> The project is **MIT licensed**. Extending it or reusing its code is fine; keep its copyright notice and three.js's
> licence (`lib/THREE-LICENSE`).

---

## Prompt A: add a new world

**Copy from here to the next horizontal rule.**

You are a creative developer extending the open-source Threejs scroll showcases library. Clone
`https://github.com/JayDev-27/Threejs-scroll-showcases`, run `python3 serve.py`, and add a new world called
**`<theme>`** (for example `desert`: wind-carved dunes, a camel caravan at sunset, an oasis, a night sky full of stars).

Rules:
- One new file `scenes/<theme>.js` exporting `{ build(ctx) }`, plus one entry in `scenes/index.js` (name, subtitle,
  fonts, colours, chapter copy). Don't change `lib/` unless a shared feature is genuinely missing; if so, add it to
  `lib/kit.js` or `lib/flora.js` so every world can use it.
- **Fully procedural:** no model, image, font or audio files. Use the kit: sky dome, water, haze, caustics, particles,
  ground and rock materials, tiled instancing, grown trees and shrubs from `lib/flora.js`.
- `build({ scene, camera, look, env, mirror })` adds meshes, lights and particles and returns
  `{ rail, floor, update }`:
  - `rail`: 6–10 stops `{ p, pos: [x,y,z], look: [x,y,z], fov }` with `p` from 0 to 1. Make it a story in chapters
    (establishing wide shot → approach → hero detail → reveal → pull-back finale), matching the chapter copy.
  - `floor(x, z)`: the ground height, so the camera never sinks into terrain.
  - `update(time, progress)`: animate light, sky, water and life; let the time of day or mood shift with `progress`.
- Film finish: use the engine's HDR, bloom, light shafts, AO, ACES grade and grain; add aerial haze and a strong
  key/fill light story. Give the world one unforgettable hero object.
- Performance: instance repeated objects, use LOD for vegetation, stay smooth on a mid-range laptop (check
  `await __perf(0.5)` in the console). Build time on load under ~3 s.

Verify:
1. Open `showcase.html?s=<theme>` and `&autoplay=60`; scroll the whole journey; the camera never clips geometry.
2. Capture a still and a GIF with `tools/capture.js` and `tools/gif.sh` into `docs/media/<theme>.jpg|gif`.
3. Check the frame time, then add the world to the README table and open a pull request.

---

## Prompt B: build the engine from scratch

**Copy from here to the end of the file.**

You are a senior graphics engineer. Build a **scroll-driven three.js world engine** plus three example worlds, as
plain ES modules with no build step and three.js r180 as the only dependency (vendored in `lib/`).

**Public API**

```js
const world = await mount(canvas, 'space', { progress, autoplay, damping = 3.2, pointer = true, quality });
world.setScene(name); world.pause(); world.play(); world.dispose();
```

`progress()` returns 0–1 (native scroll, Lenis or GSAP ScrollTrigger). The camera eases toward it with the `damping`
rate, so raw scroll is fine. `autoplay` loops a pass in N seconds when there's no progress function.

**Engine (`lib/engine.js`)**
- Renderer with half-float HDR targets; post chain: SSAO → bloom → light shafts → ACES tonemap → grade → film grain.
- Camera rail: interpolate stops `{ p, pos, look, fov }` with a smooth spline (Catmull-Rom or monotone cubic), eased
  toward the target progress; pointer parallax; enforce `floor(x, z)` ground clearance.
- Planar mirror for water (reflected camera, clip plane, reduced resolution).
- Adaptive quality: watch frame time and step the resolution between `quality` 0.5 and 1; cached shadow maps.
- Scene loading: dynamic `import('../scenes/<name>.js')`, `build(ctx)`, dispose cleanly on `setScene`.

**Kit (`lib/kit.js`) and flora (`lib/flora.js`)**
- Noise (value, Perlin, fbm), a geometry builder (merge, bake transforms, vertex colours), a sky dome with sun, moon,
  stars, clouds, nebula and aurora options, particles, water, ground and rock materials, aerial haze, caustics,
  tiled instancing with culling.
- Grown trees with branching limbs and leaf, needle or blossom sprays; shrubs, grass clumps, kelp, boulders; distance
  LOD for grass and trees.

**Worlds (`scenes/`)**: each file exports `build(ctx) → { rail, floor, update(time, progress) }`; `scenes/index.js`
holds names, fonts, colours and chapter copy. Build Nature (dawn alpine valley, mirror lake), Cyberpunk (wet neon
street with reflections) and Space (planet, asteroid belt, ringed giant, black hole) to prove the kit's range.

**Showcase page (`showcase.html`)**: a long scrolling page over a fixed full-screen canvas, with per-chapter copy,
per-theme typography, a progress bar and chapter dots; `?s=<world>` picks the world.

**Constraints**: zero model or image assets; WebGL 2 with float targets; smooth on a mid-range laptop; respect
`prefers-reduced-motion` (autoplay off, damped camera).

**Done when** each world scrolls start to finish without clipping, holds its frame rate, and captures cleanly to a
still and a GIF.
