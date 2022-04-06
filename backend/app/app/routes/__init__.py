from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


from .models import router_models
from .models.types import router_model_types
from .actions import router as router_actions
from .webhooks import router_webhooks

routers = [
    router_actions,
    router_models,
    router_model_types,
    router_webhooks,
]