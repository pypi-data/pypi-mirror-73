# -*- encoding: utf-8 -*-
# pylint: disable=E0203,E1101,C0111
"""
@file
@brief Runtime operator.
"""
from ._op import OpRun
from ..shape_object import ShapeObject


class Reshape(OpRun):

    def __init__(self, onnx_node, desc=None, **options):
        OpRun.__init__(self, onnx_node, desc=desc, **options)

    def _run(self, data, shape):  # pylint: disable=W0221
        return (data.reshape(shape), )

    def _infer_shapes(self, data, shape):  # pylint: disable=W0221
        return (ShapeObject(None, dtype=data.dtype), )
