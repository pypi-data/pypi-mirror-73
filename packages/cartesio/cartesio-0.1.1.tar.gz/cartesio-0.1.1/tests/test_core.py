#!/usr/bin/env python

"""Tests for `cartesio.core` subpackage and modules."""


import unittest
import numpy as np
import cartesio as cs


class TestCartesioCore(unittest.TestCase):
    """Tests for `cartesio.core` subpackage and modules."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_length(self):
        d = np.array([0, 0, 1, 1])
        self.assertAlmostEqual(cs.core.segment_length(d), np.sqrt(2))
