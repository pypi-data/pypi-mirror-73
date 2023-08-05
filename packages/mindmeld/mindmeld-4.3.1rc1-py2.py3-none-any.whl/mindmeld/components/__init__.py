# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains the components of the MindMeld platform"""
from .dialogue import Conversation, DialogueManager, DialogueResponder
from .entity_resolver import EntityResolver
from .nlp import NaturalLanguageProcessor
from .preprocessor import Preprocessor
from .question_answerer import QuestionAnswerer
from .request import Request
from .custom_action import (
    CustomAction,
    CustomActionSequence,
    invoke_custom_action,
    invoke_custom_action_async,
)

__all__ = [
    "Conversation",
    "CustomAction",
    "CustomActionSequence",
    "DialogueResponder",
    "DialogueManager",
    "NaturalLanguageProcessor",
    "QuestionAnswerer",
    "EntityResolver",
    "Preprocessor",
    "Request",
    "invoke_custom_action",
    "invoke_custom_action_async",
]
