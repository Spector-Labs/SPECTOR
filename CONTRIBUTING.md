# Contributing to SPECTOR

Thank you for your interest in contributing to SPECTOR!

## Code of Conduct

Be respectful, inclusive, and focused on building a great tool for people who rehearse on smart glasses.

## How to Contribute

1. **Fork the repo** under the spectorlabs organization (or your own fork if you don't have access).
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the existing code style (vanilla JS, minimal dependencies, clean HTML/CSS).
   - For UI changes, test on both desktop and mobile.
   - For player features (especially anything related to hardware controls like the right-temple button), test the simulation and document the expected real-hardware behavior.
4. **Test**:
   - Run `python -m http.server --directory public 8080`
   - Test the landing, player launch, samples, cues, Comfort mode, button simulator ('b' key), PWA install, and offline mode.
   - Run `?test` in the player to verify core logic still passes.
5. **Commit** with clear messages.
6. **Open a Pull Request** against the main branch in the spectorlabs org.

## Reporting Issues

- Use the GitHub Issues tab.
- For hardware-specific issues (right-temple button on Ray-Ban Meta, HUD readability, etc.), please include:
  - Your exact glasses model
  - What you were testing (e.g., "button advance during Comfort mode")
  - Steps to reproduce
  - Screenshots or screen recordings if possible

## Development Notes

- The site is a static PWA (served from `public/`).
- All logic is in `public/index.html` and `public/app.html`.
- Core engine (`SpectorCore`) is exposed on `window` for portability.
- We prioritize a premium feel (glassmorphism, haptics, sounds) while keeping the code simple.
- New features should consider both phone rehearsal and future glasses HUD use.

## License

MIT — see [LICENSE](LICENSE).

Thanks for helping make rehearsal better on smart glasses!