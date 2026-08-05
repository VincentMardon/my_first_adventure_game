from unittest.mock import MagicMock, Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache


def test_load_reads_font_from_package_resources(monkeypatch) -> None:
    font_file = Mock()
    resource = MagicMock()
    resource.open.return_value.__enter__.return_value = font_file
    resource_root = Mock()
    resource_root.joinpath.return_value = resource

    files = Mock(return_value=resource_root)
    load_font = Mock(return_value=Mock(spec=pygame.font.Font))

    monkeypatch.setattr(
        "my_first_adventure_game.engine.assets.font_cache.files",
        files,
    )
    monkeypatch.setattr(pygame.font, "Font", load_font)

    cache = FontCache("example.assets")

    font = cache.load("fonts/main.ttf", 24)

    files.assert_called_once_with("example.assets")
    resource_root.joinpath.assert_called_once_with("fonts/main.ttf")
    resource.open.assert_called_once_with("rb")
    load_font.assert_called_once_with(font_file, 24)
    assert font is load_font.return_value


def test_load_returns_cached_font_for_same_path_and_size(monkeypatch) -> None:
    font_file = Mock()
    resource = MagicMock()
    resource.open.return_value.__enter__.return_value = font_file
    resource_root = Mock()
    resource_root.joinpath.return_value = resource

    monkeypatch.setattr(
        "my_first_adventure_game.engine.assets.font_cache.files",
        Mock(return_value=resource_root),
    )

    loaded_font = Mock(spec=pygame.font.Font)
    load_font = Mock(return_value=loaded_font)
    monkeypatch.setattr(pygame.font, "Font", load_font)

    cache = FontCache("example.assets")

    first_font = cache.load("fonts/main.ttf", 24)
    second_font = cache.load("fonts/main.ttf", 24)

    assert first_font is loaded_font
    assert second_font is loaded_font
    load_font.assert_called_once_with(font_file, 24)


def test_load_caches_each_font_size_separately(monkeypatch) -> None:
    font_file = Mock()
    resource = MagicMock()
    resource.open.return_value.__enter__.return_value = font_file
    resource_root = Mock()
    resource_root.joinpath.return_value = resource

    monkeypatch.setattr(
        "my_first_adventure_game.engine.assets.font_cache.files",
        Mock(return_value=resource_root),
    )

    small_font = Mock(spec=pygame.font.Font)
    large_font = Mock(spec=pygame.font.Font)
    load_font = Mock(side_effect=[small_font, large_font])
    monkeypatch.setattr(pygame.font, "Font", load_font)

    cache = FontCache("example.assets")

    assert cache.load("fonts/main.ttf", 16) is small_font
    assert cache.load("fonts/main.ttf", 32) is large_font
    assert load_font.call_args_list == [
        call(font_file, 16),
        call(font_file, 32),
    ]
