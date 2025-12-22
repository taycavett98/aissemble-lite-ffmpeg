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

"""FastAPI Web App.

This module configures the FastAPI Web Server that provides HTTP/API access
to the rest of the "backend".

You will need to import your project-specific library in this module and
configure the relevant routes to call your project-specific code.
"""

import asyncio
import os


from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)

from .modeling.handler import InferenceHandler
from .routers.audio import router as audio_router

from pydantic import BaseModel

if not os.environ.get('KRAUSENING_BASE'):
    os.environ["KRAUSENING_BASE"] = "src/resources/krausening/base"

"""
Creates AissembleOIPFastAPI object with custom handler and default adapter.
Users should update this to use their custom handler/adapter as needed.
For more information, reference the aiSSEMBLE Open Inference Protocol FastAPI README
(https://github.com/boozallen/aissemble-open-inference-protocol/blob/dev/aissemble-open-inference-protocol-fastapi/README.md).
"""
service = AissembleOIPFastAPI(InferenceHandler)
app = service.server
app.include_router(audio_router)

class MyResponseModel(BaseModel):
    """Response model for greeting."""

    content: str = "Hello World"


@app.get("/", response_model=MyResponseModel)
async def root() -> MyResponseModel:
    """Example "Root" route.

    This is an example configuration of the "Root" route.
    You will almost definitely want to update or remove this route.

    It's here mostly to serve as an example/reference.
    """
    return MyResponseModel(content="Hello World")

def start_app() -> None:
    """Start the AissembleOIPFastAPI webapp."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
