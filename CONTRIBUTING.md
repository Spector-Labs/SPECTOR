# Contributing to SPECTOR 

Thank you for your interest in contributing to SPECTOR!

## Code of Conduct

Be respectful, inclusive, and focused on building a great tool for people who rehearse on smart glasses.

## How to Contribute

1. **Fork the repo** at [github.com/hydrogenbondss/SPECTOR](https://github.com/hydrogenbondss/SPECTOR) to your own account.
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the existing code style (vanilla JS, minimal dependencies, clean HTML/CSS).
   - For UI changes, test on both desktop and mobile.
   - For player features (especially anything related to hardware controls like the right-temple button), test the simulation and document the expected real-hardware behavior.
4. **Test**:
   - Run `cd public; python -m http.server 8000` (or `--directory public 8080`)
   - In your browser, open http://localhost:8000 (or http://127.0.0.1:8000 if IPv6 localhost doesn't resolve). The terminal only shows the server banner — the site appears in the browser.
   - Test the landing, player launch (click samples then Launch), Comfort mode (tilt device or use DevTools > Sensors > Orientation on desktop), button simulator ('b' key or on-screen button), PWA install, and offline mode.
   - Run `?test` in the player to verify core logic still passes.
5. **Commit** with clear messages.
6. **Open a Pull Request** against the `main` branch of `hydrogenbondss/SPECTOR`.

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

## Open source approach

The full source is MIT-licensed and public. The "idea" (a better rehearsal tool for smart glasses) is visible to anyone. What creates lasting advantage is rapid iteration, real hardware validation with beta users, the brand + domain, the curated beta community, and shipping a polished experience that feels magical on actual devices. We welcome contributions and feedback while moving fast on the reference implementation. Focus on execution and community beats trying to hide code.

## License

MIT — see [LICENSE](LICENSE).

Thanks for helping make rehearsal better on smart glasses!
