from infrastructure.cli import BonfireArgumentParser, CLIArgs


def test_cli_args_default():
    args = CLIArgs.parse([])
    assert args.port == 5000
    assert args.debug is False


def test_cli_args_custom_port():
    args = CLIArgs.parse(["--port", "8080"])
    assert args.port == 8080
    assert args.debug is False


def test_cli_args_debug_flag():
    args = CLIArgs.parse(["--debug"])
    assert args.port == 5000
    assert args.debug is True


def test_cli_args_combined():
    args = CLIArgs.parse(["--port", "9000", "--debug"])
    assert args.port == 9000
    assert args.debug is True


def test_cli_backward_compatibility_alias():
    args = BonfireArgumentParser(["--port", "3000"])
    assert args.port == 3000
