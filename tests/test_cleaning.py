from src.data_preprocessing import clean_text

def test_clean_text():
    text = "Hello @user! Check this: https://url.com 😊"
    cleaned = clean_text(text)
    assert "http" not in cleaned
    assert "@" not in cleaned
    assert "😊" not in cleaned
