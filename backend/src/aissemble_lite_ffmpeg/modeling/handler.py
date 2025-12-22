# Copyright 2025 Booz Allen Hamilton.
#
# Booz Allen Hamilton Confidential Information.
#
# The contents of this file are the intellectual property of
# Booz Allen Hamilton, Inc. ("BAH") and are subject to copyright protection
# under the laws of the United States and other countries.
#
# You acknowledge that misappropriation, misuse, or redistribution of content
# on the file could cause irreparable harm to BAH and/or to third parties.
#
# You may not copy, reproduce, distribute, publish, display, execute, modify,
# create derivative works of, transmit, sell or offer for resale, or in any way
# exploit any part of this code or program without BAH's express written permission.
#
# The contents of this code or program contains code
# that is itself or was created using artificial intelligence.
#
# To the best of our knowledge, this code does not infringe third-party intellectual
# property rights, contain errors, inaccuracies, bias, or security concerns.
#
# However, Booz Allen does not warrant, claim, or provide any implied
# or express warranty for the aforementioned, nor of merchantability
# or fitness for purpose.
#
# Booz Allen expressly limits liability, whether by contract, tort or in equity
# for any damage or harm caused by use of this artificial intelligence code or program.
#
# Booz Allen is providing this code or program "as is" with the understanding
# that any separately negotiated standards of performance for said code
# or program will be met for the duration of any applicable contract under which
# the code or program is provided.

"""aissemble_lite_ffmpeg custom handler."""

from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.types.dataplane import (
    Datatype,
    InferenceRequest,
    InferenceResponse,
    MetadataTensor,
    ModelMetadataResponse,
    ModelReadyResponse,
    ResponseOutput,
    TensorData,
)


class InferenceHandler(DataplaneHandler):
    """Example of custom handler.

    This is an example of a simple custom handler that can be
     used with the aiSSEMBLE Open Inference Protocol FastAPI implementation.
    For more information, reference the aiSSEMBLE Open Inference Protocol FastAPI README
     (https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-fastapi/README.md).
    """

    def __init__(self):
        """Init function."""
        super().__init__()

    def infer(
            self,
            payload: InferenceRequest,
            model_name: str,
            model_version: str | None = None,
    ) -> InferenceResponse:
        """Example infer function."""
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[
                ResponseOutput(
                    name=model_name,
                    shape=[1, 2],
                    datatype=Datatype.BYTES,
                    data=TensorData(root=["Hello", "World"]),
                )
            ],
        )

    def model_metadata(
            self,
            model_name: str,
            model_version: str | None = None,
    ) -> ModelMetadataResponse:
        """Example model metadata function."""
        input_tensors = [
            MetadataTensor(name="input", datatype=Datatype.BYTES, shape=[1, 2])
        ]
        output_tensors = [
            MetadataTensor(name="output", datatype=Datatype.BYTES, shape=[1, 2])
        ]
        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="placeholder_platform",
            inputs=input_tensors,
            outputs=output_tensors,
        )

    def model_ready(
            self,
            model_name: str,
            model_version: str | None = None,  # noqa: ARG002
    ) -> ModelReadyResponse:
        """Example model ready function."""
        return ModelReadyResponse(name=model_name, ready=True)
