from jarvis.learning.observer import SystemObserver

def test_pattern_detection():
    obs = SystemObserver()
    # Simulate opening VS Code then Spotify 3 times to meet the threshold
    for _ in range(3):
        obs.record_event("vscode")
        obs.record_event("spotify")

    patterns = obs.get_detected_patterns()
    assert any("vscode" in p and "spotify" in p for p in patterns)
