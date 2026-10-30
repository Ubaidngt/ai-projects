# Air Drawing

Draw in the air with your webcam. Air Drawing is a browser-based computer vision app that tracks your hand in real time with MediaPipe Hands — your index fingertip is the pen, no mouse, no touch, no install.

**Live demo:** https://muse.ai/s/air-drawing-xhj6xaelat0cxv/sQzKeQeh0SWuVs-TodjG0S1JKfDx5QAR_jQlOGekR5g

## Features

- **Air canvas** — draw smooth strokes by moving your index finger in front of the camera
- **Gesture controls** — everything is hands-free, including picking tools from the toolbar
- **Rainbow brush** — stroke colour cycles through the rainbow as you draw
- **Neon glow & sparkle trail** — electric glowing strokes with star particles bursting from your fingertip
- **Mirror mode** — every stroke is mirrored into four symmetric copies
- **Emoji stamps** — stamp stars, hearts, smileys, fire and flowers onto the canvas
- **Gesture magic** — form a heart with both hands and an animated heart appears between them (pinch to change its colour); hold up an open palm and a flower blooms in your hand
- **Undo** — button or Ctrl+Z, and even clearing the canvas is undoable
- **Save snapshot** — download a PNG of you plus your drawing

## Gestures

| Gesture | Action |
| --- | --- |
| One finger up | Draw |
| Two fingers up | Move with the pen lifted |
| Two fingers held over a toolbar item | Select that tool |
| Fist (hold) | Clear the canvas |
| Pinch on canvas | Stamp (in stamp mode) |
| Both hands in a heart shape | Animated heart appears — pinch to recolour it |
| Open palm (hold) | A flower blooms in your palm |

## Run it locally

The camera needs a secure context, so serve the file instead of opening it directly:

```bash
cd air-drawing
python -m http.server 8000
```

Then open http://localhost:8000 in Chrome and allow camera access.

## Tech

- MediaPipe Hands (real-time hand landmark tracking, up to two hands)
- Vanilla JavaScript + HTML5 Canvas
- No backend, no build step — a single `index.html`
