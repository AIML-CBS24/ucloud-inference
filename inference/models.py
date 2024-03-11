from typing import Annotated, Dict, Any
from pydantic import BaseModel, StringConstraints, Field


class Request(BaseModel):

    email: Annotated[str, StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            pattern=r"^[a-z0-9\.]+@(student\.)?cbs\.dk$", # Only CBS emails
            strict=True,
        ),
        Field(default=..., description="The user's email address, which must end with '@cbs.dk' or '@student.cbs.dk'.")
    ]
    prompt: Annotated[str, StringConstraints(
            min_length=10,
            max_length=5_000,
        ),
        Field(default=..., description="The prompt text, with a minimum length of 10 and a maximum length of 5000 characters.")
    ]
    params: Dict[str, Any] = Field(
        default={}, 
        description=(
            "A dictionary of model parameters for further customization. "
            "See https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama.__call__ "
            "for more information on the expected model parameters."
        )
    )
