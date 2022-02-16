#!/usr/bin/env python3

"""
Test suite for the API way to call align
"""

from pathlib import Path
from unittest import main

import click
from basic_test_case import BasicTestCase
from sound_swallower_stub import SoundSwallowerStub

import readalongs.api as api


class TestAlignApi(BasicTestCase):
    """Test suite for the API way to call align()"""

    def test_call_align(self):
        # We deliberately pass pathlib.Path objects as input, to make sure the
        # API accepts them too.
        data_dir = Path(self.data_dir)
        temp_dir = Path(self.tempdir)
        langs = ("fra",)  # make sure language can be an iterable, not just a list.
        with SoundSwallowerStub("t0b0d0p0s0w0:920:1520", "t0b0d0p0s1w0:1620:1690"):
            api.align(
                data_dir / "ej-fra.txt",
                data_dir / "ej-fra.m4a",
                temp_dir / "output",
                langs,
                output_formats=["html"],
            )
        expected_output_files = (
            "output.smil",
            "output.xml",
            "output.m4a",
            "index.html",
            "output.html",
        )
        for f in expected_output_files:
            self.assertTrue(
                (temp_dir / "output" / f).exists(),
                f"successful alignment should have created {f}",
            )
        self.assertEqual(
            list(langs),
            ["fra"],
            "Make sure the API call doesn't not modify my variables",
        )

    def test_call_prepare(self):
        data_dir = Path(self.data_dir)
        temp_dir = Path(self.tempdir)
        api.prepare(data_dir / "ej-fra.txt", temp_dir / "prepared.xml", ("fra", "eng"))
        with open(temp_dir / "prepared.xml") as f:
            xml_text = f.read()
            self.assertIn('xml:lang="fra" fallback-langs="eng,und"', xml_text)

        with self.assertRaises(click.BadParameter):
            api.prepare(
                data_dir / "ej-fra.txt", temp_dir / "bad.xml", ("fra", "not-a-lang")
            )
        with self.assertRaises(click.UsageError):
            api.prepare(
                data_dir / "file-not-found.txt", temp_dir / "none.xml", ("fra",)
            )


if __name__ == "__main__":
    main()
