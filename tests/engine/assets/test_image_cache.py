from unittest.mock import MagicMock, Mock

import pygame

from my_first_adventure_game.engine.assets import ImageCache


def test_load_reads_image_from_package_resources(monkeypatch) -> None:
    image_file = Mock()
    resource = MagicMock()
    resource.open.return_value.__enter__.return_value = image_file
    resource_root = Mock()
    resource_root.joinpath.return_value = resource

    files = Mock(return_value=resource_root)
    load_image = Mock(return_value=Mock(spec=pygame.Surface))

    monkeypatch.setattr(
        "my_first_adventure_game.engine.assets.image_cache.files",
        files,
    )
    monkeypatch.setattr(pygame.image, "load", load_image)

    cache = ImageCache("example.assets")

    image = cache.load("sprites/player.png")

    files.assert_called_once_with("example.assets")
    resource_root.joinpath.assert_called_once_with("sprites/player.png")
    resource.open.assert_called_once_with("rb")
    load_image.assert_called_once_with(image_file, "sprites/player.png")
    assert image is load_image.return_value


def test_load_returns_cached_image(monkeypatch) -> None:
    image_file = Mock()
    resource = MagicMock()
    resource.open.return_value.__enter__.return_value = image_file
    resource_root = Mock()
    resource_root.joinpath.return_value = resource

    monkeypatch.setattr(
        "my_first_adventure_game.engine.assets.image_cache.files",
        Mock(return_value=resource_root),
    )

    loaded_image = Mock(spec=pygame.Surface)
    load_image = Mock(return_value=loaded_image)
    monkeypatch.setattr(pygame.image, "load", load_image)

    cache = ImageCache("example.assets")

    first_image = cache.load("sprites/player.png")
    second_image = cache.load("sprites/player.png")

    assert first_image is loaded_image
    assert second_image is loaded_image
    load_image.assert_called_once_with(image_file, "sprites/player.png")
