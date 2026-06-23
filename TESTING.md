# Spector Testing Guide

This guide explains how to test Spector on real Meta Ray-Ban smart glasses using Developer Mode.

---

## 1. Enable Developer Mode on Your Glasses

1. Open the **Meta AI app** on your phone.
2. Go to your profile → tap the **Meta AI app version number** at the bottom **5 times**.
3. A hidden toggle called **Developer Mode** will appear. Turn it **on**.

---

## 2. Open Spector on Your Glasses

1. Make sure your Ray-Ban Meta glasses are connected and awake.
2. On your phone, open the **Meta AI app**.
3. Go to **Settings → App connections → Add a Web App**.
4. Paste this URL:

   **https://spector-plum.vercel.app**

5. Spector should open directly on your glasses.

---

## 3. How to Use Spector

- Paste or upload your script on the landing page.
- Tap **"Launch Teleprompter"**.
- **Comfort mode**: Subtle breathing + gentle spatial movement when you move your head. Feels more natural and calm. On Display glasses, the right-temple button/touch controls (and future Neural Band gestures) can advance or pause the script where supported by the platform.
- **Focus mode**: Completely static. No breathing, no movement. Best for when you want maximum stability.
- **Non-Display models (Gen 1/2)**: Use as phone companion rehearsal tool with haptics and audio. Glasses provide camera/AI.
- **Display / HUD models**: Run directly on the glasses lens for heads-up teleprompting.
- **Other smart glasses** (XREAL, Viture, Brilliant Labs, etc.): Works via PWA on phone companion or browser-supported devices. Controls depend on the hardware (touch, voice, external controller).
- Tap the screen or press play to start/stop.
- Use the speed presets (Slow / Normal / Fast) to match your speaking pace.
- Tap anywhere to show/hide controls.
- When finished, you’ll see a clean end screen with stats (chunks read + total time).

---

## 4. Known Limitations (Early Version)

- Spatial movement works best with moderate head movement.
- Very long scripts may feel slower.
- Haptics only work if your device supports vibration.
- This is still a web-based experience.

---

## 5. Feedback

If you're testing Spector, feedback on these areas would be very helpful:
- How natural does Comfort mode feel compared to Focus mode?
- Is the drag / head movement sensitivity comfortable?
- Does the breathing feel calming or distracting?
- Would you use this for real speeches or presentations?

---

**Current Live Version**: https://spector-plum.vercel.app

Thank you for testing Spector!
