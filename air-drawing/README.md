# Air Drawing

Draw in the air with your webcam. Air Drawing is a browser-based computer vision app that tracks your hands in real time with MediaPipe Hands — your index fingertip is the pen, no mouse, no touch, no install. Everything runs 100% in the browser: your camera video is processed locally on your device and is never uploaded anywhere.

**Live demo:** https://muse.ai/s/air-drawing-xhj6xaelat0cxv/sQzKeQeh0SWuVs-TodjG0S1JKfDx5QAR_jQlOGekR5g

## Two modes

The app has two modes that stay strictly separate — only the active mode's features run. Hold a **fist for 3 seconds** to switch between them (a progress ring counts down with tick sounds, then a whoosh confirms the switch). In Drawing mode, holding a fist for about 1 second clears the canvas first — keep holding to reach 3 seconds and switch modes instead.

### Drawing mode
- **Air canvas** — draw smooth strokes by moving one index finger in front of the camera
- **Hands-free toolbar** — a slim dock on the left with 8 colours, three brush sizes, Rainbow Brush, Neon Glow, Sparkle Trail, Mirror/Kaleidoscope (4-way), Emoji Stamps (⭐ ❤️ 😊 🔥 🌸), Eraser, Undo, Clear and Save PNG
- **Colour cycling** — hold an open palm for about 0.6s to jump to the next colour
- **Pinch to stamp** — pinch your fingers to stamp the selected emoji onto the canvas
- **Two-hand heart** — bring both hands together with thumbs and index tips touching and a big glowing heart appears between them; pinch to change its colour
- **Undo** — button or Ctrl+Z, and even clearing the canvas is undoable
- **Save snapshot** — download a PNG of your drawing

### Object mode
- **Floating objects** — pick an Energy Ball, Glow Ring or Star (click or dwell-select); it floats between your two palms and grows or shrinks with the distance between your hands
- **Flick to throw** — flick your hands and the object flies in that direction with gravity, shrinking until it bursts at the edge of the screen
- **Pop** — open one hand fully to pop the object
- **Kamehameha** — cup your hands together facing each other and hold for about 1.2s to charge an energy orb, then thrust your hands forward to fire a beam; the more charge, the stronger the blast

## Sound

All sound effects are synthesized live with the Web Audio API — charge hums, beam blasts, pops, whooshes and UI clicks, no audio files. Use the 🔊/🔇 button in the top bar to mute.

## Gestures

### Any mode
| Gesture | Action |
| --- | --- |
| Fist (hold 3s) | Switch mode (Drawing ↔ Object) |
| Two fingers held over a UI item | Select it (dwell) |
| `H` key or the `?` button | Show / hide the gesture guide |

### Drawing mode
| Gesture | Action |
| --- | --- |
| One finger up | Draw |
| Two fingers up | Move with the pen lifted |
| Open palm (hold ~0.6s) | Cycle to the next colour |
| Pinch | Stamp (with the Stamp tool) |
| Both hands, thumbs + index tips touching | Glowing heart — pinch to recolour |
| Fist (hold ~1s) | Clear the canvas (undoable) |

### Object mode (two hands)
| Gesture | Action |
| --- | --- |
| Both palms up, object floating | Move / resize the object by spreading or closing your hands |
| Quick flick | Throw the object |
| One hand fully open | Pop the object |
| Cupped hands facing each other (hold) | Charge the Kamehameha orb |
| Push hands forward while charged | Fire the beam |

## Run it locally

You need internet access (the MediaPipe Hands library loads from a CDN) and a browser that can use your camera. Serve the folder over a local server — opening the file directly can block camera access:

```bash
cd air-drawing
python -m http.server 8000
```

Then open http://localhost:8000 in Chrome or Edge and allow camera access when asked.

## Tech

- **MediaPipe Hands** — real-time tracking of 21 hand landmarks per hand, up to two hands
- **HTML5 Canvas** — drawing surface, effects and particles
- **Web Audio API** — fully synthesized sound effects
- **Vanilla JavaScript** — no framework, no backend, no build step: a single `index.html`
- Fully responsive layout, from phones to large screens
