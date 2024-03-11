import json
from typing import Dict, Any
from loguru import logger
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from asgiref.sync import sync_to_async
from pydantic import ValidationError

from inference.models import Request
from inference.apps import App as app


@csrf_exempt
@require_http_methods(["POST"])  # Ensuring only POST requests are handled
async def inference(request):
        
        if request.content_type != 'application/json':
            return JsonResponse({"error": "This endpoint requires a JSON payload."}, status=400)
        
        try:
    
            data = json.loads(request.body)
            req_obj = Request(**data)

            logger.info(f"Received request from {req_obj.email}")

            # Run the model
            response : Dict[str, Any] = app.llm(
                prompt = req_obj.prompt,
                **req_obj.params
            )

            return JsonResponse(
                {
                    **response,
                    **{
                        "timestamp": datetime.now().isoformat(),
                        "email": req_obj.email,
                    }
                }
            )
        except ValidationError as e:
            output = {name: (info.tinfo.description) for name, info in Request.model_fields.items()}
            return JsonResponse(
                {
                    "ERROR": (
                        "Could not validate the request. "
                        f"Expected {output}. "
                    )
                },
                status=400
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": (f"Invalid JSON format")}, status=400)
        
        except ValueError as e:
            return JsonResponse(
                {"error": (f"Invalid request: {e}")}, status=400)