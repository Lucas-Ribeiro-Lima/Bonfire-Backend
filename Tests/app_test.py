
class TestApp:
  def test_app_is_create(app):
    """Test if Flask main app is created"""
    assert app.name == 'main.app'