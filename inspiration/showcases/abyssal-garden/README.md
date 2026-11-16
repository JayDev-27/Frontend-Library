<div align="center">

# Abyssal Garden

**A dreamy underwater world you swim through in the browser. Raw WebGPU, no engine, everything procedural, one ~97 KB HTML file.**

<a href="https://noniv.github.io/abyssal-garden/"><img src="https://raw.githubusercontent.com/Noniv/abyssal-garden/a596354eff400d458bc2aeb9bdf5e0a9734b2bcf/.github/screenshots/whale-fluke.jpg" width="100%" alt="A kelp forest with a giant stone whale tail and a manta ray gliding overhead"></a>

<sub><a href="https://noniv.github.io/abyssal-garden/">Dive in live</a> (Chrome or Edge with WebGPU) · <a href="https://github.com/Noniv/abyssal-garden">Repository</a> (MIT) · <a href="BUILD-PROMPT.md"><b>Build prompt for AI agents →</b></a></sub>

</div>

## At a glance

| | |
|:--|:--|
| **What it is** | A free-camera underwater world: kelp forests, sunbeams through a rippling surface, caustics, rock canyons and arches, a sunken ship, a stone whale fluke, manta rays, fish schools, a purple grotto and a live-synthesised soundscape. |
| **Author** | [Noniv](https://github.com/Noniv) |
| **Stack** | **WebGPU directly** (WGSL), no engine or 3D library; Web Audio API; a small Node build in `source/`. |
| **Assets** | None. The seabed is sculpted on the GPU at load, then decorated with ~2 million kelp leaves and plants, tens of thousands of rocks, and thousands of sponges, corals and fish. |
| **Size** | `index.html` ≈ 97 KB. |
| **Performance** | ~180 fps at 2560×1440 on an RTX 5070 Ti; aims for 60 fps on slower hardware by lowering resolution, then draw distance. |
| **Licence** | **MIT.** Reuse with attribution. |

## Controls

`WASD` swim · mouse look (pointer lock) · `E`/`Q` up/down · `Shift` faster · `1`–`6` viewpoints · `Esc` menu · `M` sound · `H` stats. Touch: hold to swim, slide to steer, two fingers to go faster. Seabed, cliffs and arches are solid; plants, corals, the ship and the fluke you swim through.

## Stills

| | |
|:--|:--|
| ![Shipwreck](https://raw.githubusercontent.com/Noniv/abyssal-garden/a596354eff400d458bc2aeb9bdf5e0a9734b2bcf/.github/screenshots/shipwreck.jpg) | ![Looking up through the kelp](https://raw.githubusercontent.com/Noniv/abyssal-garden/a596354eff400d458bc2aeb9bdf5e0a9734b2bcf/.github/screenshots/kelp-forest.jpg) |
| ![Barrel sponges](https://raw.githubusercontent.com/Noniv/abyssal-garden/a596354eff400d458bc2aeb9bdf5e0a9734b2bcf/.github/screenshots/sponge-garden.jpg) | ![Light rays over the kelp basin](https://raw.githubusercontent.com/Noniv/abyssal-garden/a596354eff400d458bc2aeb9bdf5e0a9734b2bcf/.github/screenshots/light-rays.jpg) |

## How it's built

| File (`source/`) | Role |
|:--|:--|
| `src/main.js` | Boot, WebGPU device and pipelines, render loop, camera and collision, input, menu, adaptive quality |
| `src/world.js` | Seabed sculpting; scattering kelp, plants, rocks, sponges, corals, fish; set pieces |
| `src/shaders.js` | WGSL: terrain, kelp and foliage, surface from below, god rays, caustics, depth absorption, post |
| `src/math.js` | Vector/matrix maths, noise, preallocated buffers |
| `src/audio.js` | Live soundscape: rumble, distant whale calls, chimes, bubbles |
| `src/quality.js` | Low / Medium / High presets, remembered per visitor, stepped down after a crash |
| `build.mjs`, `template.html` | Bundle and minify into one `index.html` |

### Ideas worth learning

1. **No engine at all:** raw WebGPU and WGSL keep the world to ~97 KB.
2. **Zero per-frame JS allocation:** every buffer preallocated, so no GC stutter.
3. **GPU-side world building:** the seabed is sculpted on the GPU at load, then millions of instances are scattered.
4. **Warm start:** the scene runs, blurred, behind the start menu, so quality tuning finishes before you dive.
5. **Crash-aware quality:** a crashed load restarts one level lower and remembers it.
6. **Built with an agent and a visual critic:** the author's `prompt.txt` asked for a subagent that only sees renders and reports defects until nothing above "minor" remains, plus a GPU-timestamp perf gate. It's reproduced in the [build prompt](BUILD-PROMPT.md).

## Source and rights

Discovered at <https://github.com/Noniv/abyssal-garden> (commit `a596354`, 2026-11-16). Facts come from its README, file tree and `prompt.txt`. **MIT licence.** Screenshots are linked from the repository, not copied.
