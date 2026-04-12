from jarvis.learning.recorder import ActionRecorder

def test_action_recording():
    rec = ActionRecorder()
    rec.start()
    rec.record_action("click", {"x": 100, "y": 200})
    rec.stop()

    assert len(rec.history) == 1
    assert rec.history[0]["type"] == "click"
    assert rec.history[0]["data"] == {"x": 100, "y": 200}
    assert "timestamp" in rec.history[0]
