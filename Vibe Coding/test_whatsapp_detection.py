"""
WhatsApp Call Detection Diagnostic Tool
========================================
Run this script, then open your WhatsApp call screen (or show an incoming call).
It will continuously scan the screen and report what it sees.

Press Ctrl+C to stop.
"""
import pyautogui
import cv2
import numpy as np
import os
import time
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEPT_PATH = os.path.join(BASE_DIR, "accept.png")
DECLINE_PATH = os.path.join(BASE_DIR, "decline.png")

SCALES = [0.7, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.3, 1.4]


def load_gray(path):
    if not os.path.exists(path):
        print(f"  ❌ FILE MISSING: {path}")
        return None
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"  ❌ OPENCV CANNOT READ: {path}")
        return None
    print(f"  ✅ {os.path.basename(path)}: {img.shape[1]}x{img.shape[0]} px")
    return img


def match_all_scales(screen_gray, template_gray):
    """Returns list of (scale, confidence) tuples, sorted by confidence descending."""
    if template_gray is None:
        return []

    th, tw = template_gray.shape[:2]
    sh, sw = screen_gray.shape[:2]
    results = []

    for scale in SCALES:
        nw, nh = int(tw * scale), int(th * scale)
        if nw >= sw or nh >= sh or nw < 8 or nh < 8:
            continue
        resized = cv2.resize(template_gray, (nw, nh), interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(screen_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        results.append((scale, max_val, max_loc, nw, nh))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def save_debug_screenshot(screen_gray, accept_results, decline_results):
    """Save an annotated debug screenshot showing where matches were found."""
    debug = cv2.cvtColor(screen_gray, cv2.COLOR_GRAY2BGR)

    # Draw best accept match in green
    if accept_results and accept_results[0][1] >= 0.5:
        scale, conf, loc, nw, nh = accept_results[0]
        top_left = loc
        bottom_right = (loc[0] + nw, loc[1] + nh)
        cv2.rectangle(debug, top_left, bottom_right, (0, 255, 0), 3)
        cv2.putText(debug, f"Accept: {conf:.2f} @{scale}x",
                    (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Draw best decline match in red
    if decline_results and decline_results[0][1] >= 0.5:
        scale, conf, loc, nw, nh = decline_results[0]
        top_left = loc
        bottom_right = (loc[0] + nw, loc[1] + nh)
        cv2.rectangle(debug, top_left, bottom_right, (0, 0, 255), 3)
        cv2.putText(debug, f"Decline: {conf:.2f} @{scale}x",
                    (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    out_path = os.path.join(BASE_DIR, "debug_detection.png")
    cv2.imwrite(out_path, debug)
    return out_path


def main():
    print("=" * 60)
    print("  WHATSAPP CALL DETECTION DIAGNOSTIC")
    print("=" * 60)
    print()

    # 1. System info
    print("[1] SYSTEM INFO")
    screen_w, screen_h = pyautogui.size()
    print(f"  Screen: {screen_w}x{screen_h}")
    ss = pyautogui.screenshot()
    print(f"  Screenshot: {ss.size[0]}x{ss.size[1]}")
    print(f"  OpenCV: {cv2.__version__}")
    print()

    # 2. Load templates
    print("[2] LOADING TEMPLATES")
    accept_tmpl = load_gray(ACCEPT_PATH)
    decline_tmpl = load_gray(DECLINE_PATH)
    print()

    if accept_tmpl is None and decline_tmpl is None:
        print("  ⛔ No templates could be loaded! Cannot continue.")
        print("  → Make sure accept.png and/or decline.png are in the project root.")
        sys.exit(1)

    # 3. Live scan loop
    print("[3] LIVE SCANNING (press Ctrl+C to stop)")
    print("    Show a WhatsApp incoming call on screen now...")
    print("-" * 60)

    scan_count = 0
    try:
        while True:
            scan_count += 1
            t0 = time.time()

            screen = np.array(pyautogui.screenshot())
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

            accept_results = match_all_scales(screen_gray, accept_tmpl)
            decline_results = match_all_scales(screen_gray, decline_tmpl)

            elapsed = time.time() - t0

            # Show top result for each
            best_accept_conf = accept_results[0][1] if accept_results else 0.0
            best_accept_scale = accept_results[0][0] if accept_results else 0.0
            best_decline_conf = decline_results[0][1] if decline_results else 0.0
            best_decline_scale = decline_results[0][0] if decline_results else 0.0

            accept_status = "✅ DETECTED" if best_accept_conf >= 0.70 else "❌ not found"
            decline_status = "✅ DETECTED" if best_decline_conf >= 0.70 else "❌ not found"

            print(f"  Scan #{scan_count} ({elapsed:.2f}s) │ "
                  f"Accept: {best_accept_conf:.3f} @{best_accept_scale:.2f}x {accept_status} │ "
                  f"Decline: {best_decline_conf:.3f} @{best_decline_scale:.2f}x {decline_status}")

            # Save debug screenshot on first scan or when something is detected
            if scan_count == 1 or best_accept_conf >= 0.60 or best_decline_conf >= 0.60:
                debug_path = save_debug_screenshot(screen_gray, accept_results, decline_results)
                if scan_count == 1:
                    print(f"    → Debug screenshot saved: {debug_path}")

            time.sleep(2)

    except KeyboardInterrupt:
        print()
        print("-" * 60)
        print("  Stopped. Check 'debug_detection.png' for annotated screenshot.")
        print()
        print("  TROUBLESHOOTING TIPS:")
        print("  • If confidence is always below 0.40 → Your template images don't match")
        print("    the current WhatsApp UI. Retake fresh screenshots of the Accept/Decline")
        print("    buttons and save as accept.png / decline.png in the project root.")
        print("  • If confidence is 0.50-0.69 → Match is close but not reliable.")
        print("    Try cropping the template to just the ICON (not the full button).")
        print("  • If confidence is ≥ 0.70 → Detection should work! ✅")
        print()


if __name__ == "__main__":
    main()
