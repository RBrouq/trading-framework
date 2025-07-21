def test_import():
    import trading_framework

    assert hasattr(trading_framework, "__version__")
