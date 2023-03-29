# Generated by luzgen at 2023-03-19 10:33:30.358603
from pathlib import Path
from luz import Control, Module, Meta
import shutil

meta = Meta(
    release=True,
    sdk="iPhoneOS14.5.sdk",
    rootless=True,
    archs=[
        "armv7",
        # "armv7s",
        "arm64",
        "arm64e",
    ],
    min_vers="10.0",
)

# Define control metadata here
control = Control(
    name="PreferenceLoader",
    id="preferenceloader",
    version="2.2.6",
    author="Dustin Howett <cydia.pl@relay.howett.net>",
    maintainer="Dhinak G <dhinak@dhinak.net>",
    description="load preferences in style",
    depends=["mobilesubstrate"],
    section="System",
    architecture="iphoneos-arm64",
)

install_dir = meta.root_dir.relative_to(meta.staging_dir)
if install_dir == Path("."):
    install_dir = ""
else:
    install_dir = str(install_dir)


def copy_libprefs_headers():
    libprefs_path = meta.root_dir / "usr/include/libprefs"
    libprefs_path.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path("prefs.h"), libprefs_path / "prefs.h")


def create_preference_folders():
    (meta.root_dir / "Library/PreferenceLoader/Preferences").mkdir(parents=True, exist_ok=True)
    (meta.root_dir / "Library/PreferenceBundles").mkdir(parents=True, exist_ok=True)


libprefs_compatibility_version = "2.2.0"
libprefs_current_version = control.version.partition("-")[0]


# Module info
modules = [
    Module(
        ["prefs.xm"],
        "libprefs",
        "library",
        linker_flags=[
            "-compatibility_version",
            libprefs_compatibility_version,
            "-current_version",
            libprefs_current_version,
        ],
        use_arc=False,
        frameworks=["UIKit"],
        private_frameworks=["Preferences"],
        libraries=["substrate"],
        after_stage=copy_libprefs_headers,
    ),
    Module(
        ["Tweak.xm"],
        "PreferenceLoader",
        "tweak",
        filter={"bundles": ["com.apple.Preferences"]},
        use_arc=False,
        frameworks=["UIKit"],
        private_frameworks=["Preferences"],
        libraries=["prefs"],
        after_stage=create_preference_folders,
    ),
]