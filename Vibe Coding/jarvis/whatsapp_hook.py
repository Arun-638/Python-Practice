import pyautogui
import cv2
import numpy as np
import os
import time


class WhatsAppHook:
    """
    Detects incoming WhatsApp calls by matching template images (accept.png, decline.png)
    against the live screen using OpenCV multi-scale template matching.

    This approach is far more robust than pyautogui.locateOnScreen because:
      - It uses grayscale matching (tolerates minor color shifts)
      - It tries multiple scales (handles slight size differences across sessions)
      - It captures the screen ONCE per detection cycle (faster + consistent)
      - It uses proper confidence thresholds (no false positives)
    """

    def __init__(self):
        self.is_ringing = False
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Template image paths
        self.accept_img_path = os.path.join(self.base_dir, "accept.png")
        self.decline_img_path = os.path.join(self.base_dir, "decline.png")

        # Pre-load templates in grayscale for fast matching
        self._accept_template = self._load_template(self.accept_img_path)
        self._decline_template = self._load_template(self.decline_img_path)

        # ── Tuning Knobs ──────────────────────────────────────────────────
        # Minimum confidence to consider a match valid
        self.detect_threshold = 0.70
        self.click_threshold = 0.65  # Slightly lower for clicking (user already confirmed call is ringing)

        # Scales to try. 1.0 = exact size of the template image.
        # We go 0.7x to 1.4x to cover minor rendering/resolution differences.
        self.scales = [0.7, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.3, 1.4]

    # ── Internal Helpers ──────────────────────────────────────────────────

    def _load_template(self, path):
        """Load template image as grayscale. Returns None if missing."""
        if not os.path.exists(path):
            print(f"[JARVIS] WARNING: Template not found → {path}")
            return None
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"[JARVIS] WARNING: cv2.imread failed → {path}")
            return None
        print(f"[JARVIS] Loaded template: {os.path.basename(path)} ({img.shape[1]}x{img.shape[0]} px)")
        return img

    def _grab_screen_gray(self):
        """Capture the full screen as a grayscale numpy array."""
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return gray

    def _match_template_multiscale(self, screen_gray, template_gray, threshold):
        """
        Try to find `template_gray` inside `screen_gray` at multiple scales.

        Returns:
            (confidence, center_xy, scale)  if found above threshold
            (best_confidence, None, None)    if not found
        """
        if template_gray is None:
            return 0.0, None, None

        th, tw = template_gray.shape[:2]
        sh, sw = screen_gray.shape[:2]

        best_val = 0.0
        best_loc = None
        best_scale = 1.0
        best_tw, best_th = tw, th

        for scale in self.scales:
            new_w = int(tw * scale)
            new_h = int(th * scale)

            # Skip if the resized template is larger than the screen or too tiny
            if new_w >= sw or new_h >= sh or new_w < 8 or new_h < 8:
                continue

            resized = cv2.resize(template_gray, (new_w, new_h), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > best_val:
                best_val = max_val
                best_loc = max_loc
                best_scale = scale
                best_tw, best_th = new_w, new_h

        if best_val >= threshold and best_loc is not None:
            cx = best_loc[0] + best_tw // 2
            cy = best_loc[1] + best_th // 2
            return best_val, (cx, cy), best_scale

        return best_val, None, None

    # ── Public API ────────────────────────────────────────────────────────

    def is_call_active(self):
        """Check if a WhatsApp call is currently incoming on screen."""
        try:
            screen = self._grab_screen_gray()

            # Try accept button first (it's the most distinctive)
            conf, loc, scale = self._match_template_multiscale(
                screen, self._accept_template, self.detect_threshold
            )
            if loc is not None:
                print(f"[JARVIS] ☎️  Call DETECTED via Accept button "
                      f"(confidence={conf:.2f}, scale={scale:.2f}x)")
                return True

            # Try decline button
            conf, loc, scale = self._match_template_multiscale(
                screen, self._decline_template, self.detect_threshold
            )
            if loc is not None:
                print(f"[JARVIS] ☎️  Call DETECTED via Decline button "
                      f"(confidence={conf:.2f}, scale={scale:.2f}x)")
                return True

        except Exception as e:
            print(f"[JARVIS] Call detection error: {e}")

        return False

    def accept_call(self):
        """Locate and click the green Accept button."""
        print("[JARVIS] Attempting to ACCEPT incoming call...")
        try:
            screen = self._grab_screen_gray()
            conf, loc, scale = self._match_template_multiscale(
                screen, self._accept_template, self.click_threshold
            )
            if loc is not None:
                x, y = loc
                pyautogui.click(x, y)
                print(f"[JARVIS] ✅ Clicked Accept at ({x}, {y}) "
                      f"[confidence={conf:.2f}, scale={scale:.2f}x]")
                return True
            else:
                print(f"[JARVIS] ❌ Accept button NOT found (best confidence={conf:.2f})")
        except Exception as e:
            print(f"[JARVIS] Accept click error: {e}")
        return False

    def decline_or_end_call(self):
        """Locate and click the Decline / End Call button."""
        print("[JARVIS] Attempting to DECLINE / END call...")
        success = False

        try:
            screen = self._grab_screen_gray()

            # 1. Try decline.png
            conf, loc, scale = self._match_template_multiscale(
                screen, self._decline_template, self.click_threshold
            )
            if loc is not None:
                x, y = loc
                pyautogui.click(x, y)
                print(f"[JARVIS] ✅ Clicked Decline at ({x}, {y}) "
                      f"[confidence={conf:.2f}, scale={scale:.2f}x]")
                return True

            # 2. Try end_call.png if it exists
            end_call_path = os.path.join(self.base_dir, "end_call.png")
            if os.path.exists(end_call_path):
                end_template = self._load_template(end_call_path)
                conf, loc, scale = self._match_template_multiscale(
                    screen, end_template, self.click_threshold
                )
                if loc is not None:
                    x, y = loc
                    pyautogui.click(x, y)
                    print(f"[JARVIS] ✅ Clicked End Call at ({x}, {y}) "
                          f"[confidence={conf:.2f}, scale={scale:.2f}x]")
                    return True

        except Exception as e:
            print(f"[JARVIS] Decline/End click error: {e}")

        # 3. Failsafe: Windows UI Automation (if image matching fails entirely)
        if not success:
            try:
                import uiautomation as auto
                auto.SetGlobalSearchTimeout(1.0)
                print("[JARVIS] Image match failed. Invoking Windows UI Automation failsafe...")
                for name in ['End call', 'End', 'Hang up', 'Decline']:
                    btn = auto.ButtonControl(Name=name)
                    if btn.Exists(0, 0):
                        btn.Click()
                        print(f"[JARVIS] ✅ UI Failsafe clicked '{name}'!")
                        success = True
                        break
            except Exception:
                pass
            finally:
                if 'auto' in locals():
                    auto.SetGlobalSearchTimeout(10)

        return success
