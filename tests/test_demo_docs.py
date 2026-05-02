from pathlib import Path


def test_demo_walkthrough_exists():
    path = Path("docs/DEMO_WALKTHROUGH.md")

    assert path.exists()
    text = path.read_text()
    assert "Demo Walkthrough" in text
    assert "Build Proposal" in text
    assert "Quality Gate" in text
    assert "Benchmark Tab" in text


def test_interview_talk_track_exists():
    path = Path("docs/INTERVIEW_TALK_TRACK.md")

    assert path.exists()
    text = path.read_text()
    assert "Thirty-Second Version" in text
    assert "Two-Minute Version" in text
    assert "Technical Talking Points" in text
    assert "OpenAI Agents" in text


def test_readme_links_demo_materials():
    text = Path("README.md").read_text()

    assert "docs/DEMO_WALKTHROUGH.md" in text
    assert "docs/INTERVIEW_TALK_TRACK.md" in text
