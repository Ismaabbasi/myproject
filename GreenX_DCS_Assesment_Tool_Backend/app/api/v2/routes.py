from fastapi import APIRouter

from app.api.v2.endpoints.auth import router as auth_router
from app.api.v2.endpoints.setup import router as setup_router
from app.api.v2.endpoints.comment import router as comment_router
from app.api.v2.endpoints.domain import router as domain_router
from app.api.v2.endpoints.role import router as role_router
from app.api.v2.endpoints.user_profile import router as user_profile_router
from app.api.v2.endpoints.measure import router as measure_router
from app.api.v2.endpoints.user_measure import router as user_measure_router
from app.api.v2.endpoints.user_persona import router as user_persona_router
from app.api.v2.endpoints.insight import router as insight_router
from app.api.v2.endpoints.question_answer import router as question_answer_router
from app.api.v2.endpoints.user_answer import router as user_answer_router
from app.api.v2.endpoints.chart import router as chart_router
from app.api.v2.endpoints.feedback import router as feedback_router


routers = APIRouter()
router_list = [auth_router, setup_router, domain_router, role_router, user_profile_router, measure_router, user_measure_router, user_persona_router, insight_router, question_answer_router, user_answer_router, comment_router, chart_router, feedback_router]

for router in router_list:
    router.tags = routers.tags.append("v2")
    routers.include_router(router)