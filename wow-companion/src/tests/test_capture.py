from src.core.capture import capture

def test_capture_frame_shape():
    frame = capture.grab_frame()
    assert frame is not None
    assert len(frame.shape) == 3
