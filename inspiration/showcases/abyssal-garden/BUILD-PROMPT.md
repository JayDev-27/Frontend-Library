# Build prompt: Abyssal Garden–class WebGPU world

Background: [README.md](README.md). Abyssal Garden is **MIT licensed**, so its author's original prompt is
reproduced below with credit, followed by an expanded specification drawn from the finished project.

---

## 1. The author's original prompt

Reproduced from [`prompt.txt`](https://github.com/Noniv/abyssal-garden/blob/a596354eff400d458bc2aeb9bdf5e0a9734b2bcf/prompt.txt)
by Noniv (MIT). This is the prompt the world was built from.

```text
Build a real-time fantasy underwater scene that runs in the browser. It only needs to look beautiful and let me fly a free camera through it.

PRIORITIES (in this order when they conflict)
1. Visual quality
2. Stable frame pacing at the target spec
3. Small bundle size

CONSTRAINTS
- No Three.js/Babylon.js or other engines.
- WebGPU rendered.
- Everything procedural: no texture/model files. Deliverable is a single self-contained index.html. Report minified size.
- Zero per-frame JS allocations (no GC stutter). Preallocate all buffers.

TARGET
- Windows 11 25H2, Chrome 157, RTX 5070 Ti, Ryzen 7800X3D, 180 Hz monitor
- 2560×1440 at full resolution. GPU frame time ≤ 11 ms average, no frame > 16.7 ms during a scripted 60 s fly-through.

SCENE
- Dense, towering kelp columns with sparkling green/gold specks, swaying
- Strong depth fog/absorption: cyan near the surface → deep blue in the distance
- God rays, animated caustics, wavy surface visible from below
- Rock canyons, arches and overhangs; floating boulders
- Iridescent purple/pink foliage, magenta ground cover, barrel sponges, coral
- Animated life: manta rays, fish schools, rising bubbles, drifting particles
- Set pieces: a sunken ship hull, a stone whale-fluke sculpture
- World: bounded, but the boundaries can't be visible from the starting area

CONTROLS
WASD move, mouse look (pointer lock), Q/E up/down, Shift to accelerate

VERIFICATION
- Visual critic: a separate subagent that sees ONLY the your renders, never your code or reasoning. Give it 6 fixed camera poses, rendered at 2560×1440 in GPU-accelerated Chrome, plus a short recording of the fly-through to catch shimmer, aliasing, popping and banding. It returns prioritized, concrete defects. Iterate until it reports nothing above "minor".
- Performance: GPU timestamp queries plus a frame-time log from the scripted fly-through. Report average, 99th percentile and max.

DONE WHEN: both verification gates pass. Deliver index.html, the bundle size, the perf report and the critic's final review.
```

---

## 2. Expanded specification (add to the prompt above)

Features the finished project has beyond the original prompt. Paste after it for a closer match.

**Structure**
- Readable source in `source/src/` (`main.js`, `world.js`, `shaders.js`, `math.js`, `audio.js`, `quality.js`,
  `dev.js`) bundled and minified by `source/build.mjs` into one `index.html` from `template.html`.

**World building**
- Sculpt the seabed (canyons, arches, overhangs, floating boulders) on the GPU at load with a compute pass, then
  scatter ~2 million kelp leaves and plants, tens of thousands of rocks, and thousands of sponges, corals and fish as
  instances. Build the ship hull, whale fluke, mantas, fish and corals from simple mathematical shapes.
- Collision: the seabed, cliffs and arches are solid (the camera glides along rock and still fits every tunnel and
  arch); plants, corals, loose rocks, boulders, the ship and the fluke can be swum through.

**Experience**
- A start screen with **Dive in**; the scene already renders, blurred, behind it so quality tuning finishes first.
- Six viewpoints on keys `1`–`6` (use them as the critic's fixed poses); `Esc` menu with controls and Resume; `M`
  sound; `H` stats; touch controls (hold to swim, slide to steer, two fingers to go faster); phones forced to landscape.
- A soundscape synthesised live with Web Audio: deep rumble, distant whale calls, soft chimes, bubbles; starts on dive.
- A clear message if WebGPU is missing: "This scene needs WebGPU".

**Quality**
- Low / Medium / High presets (High full; Medium halves leaves, sparkles and pebbles and removes small shadow casters;
  Low quarters leaves, drops anti-aliasing, coarsens geometry, simplifies lighting, starts at 480p). Pick by device
  memory on first visit; remember the level, resolution and draw distance; step down one level after a crash or
  device loss.
- Aim for 60 fps on slower hardware by lowering resolution first, then draw distance, in small steps.

**Done when**: both of the original verification gates pass, plus the six viewpoints match the reference stills in
mood (shipwreck, kelp looking up, barrel sponges, light rays over the basin, the purple grotto, the whale fluke).
