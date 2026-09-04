from dependency_injector import containers, providers
from app.core.config import configs
from app.core.database import Database
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository



from app.services.domain_service import DomainService
from app.repository.domain_repository import DomainRepository

from app.services.roles_service import RolesService
from app.repository.roles_repository import RolesRepository

from app.repository.company_repository import CompanyRepository

from app.services.user_profile_service import UserProfileService
from app.repository.user_profile_repository import UserProfileRepository

from app.services.measures_service import MeasuresService
from app.repository.measures_repository import MeasuresRepository

from app.repository import TopOfMindTypesRolesRepository

from app.services.user_measures_service import UserMeasuresService
from app.repository.user_measures_repository import UserMeasuresRepository

from app.services.user_personas_service import UserPersonasService
from app.repository.user_personas_repository import UserPersonasRepository

from app.services.insight_service import InsightService

from app.services.question_answer_service import QuestionAnswerService
from app.repository.question_answer_repository import QuestionAnswerRepository

from app.repository.framework_types_repository import FrameworkTypesRepository
from app.repository.framework_subtypes_repository import FrameworkSubtypesRepository
from app.repository.questions_repository import QuestionsRepository
from app.repository.answers_repository import AnswersRepository

from app.services.user_selected_answers_service import UserSelectedAnswersService
from app.repository.user_selected_answers_repository import UserSelectedAnswersRepository

from app.services.comment_service import CommentService
from app.repository.comment_repository import CommentRepository

from app.services.chart_service import ChartService

from app.repository.other_measures_repository import OtherMeasuresRepository

from app.services.feedback_service import FeedbackService
from app.repository.strengths_repository import StrengthsRepository
from app.repository.improvements_repository import ImprovementsRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            #"app.api.v1.endpoints.auth",
            #"app.api.v1.endpoints.post",
            #"app.api.v1.endpoints.tag",
            "app.api.v2.endpoints.auth",
            "app.api.v2.endpoints.setup",
            "app.api.v2.endpoints.domain",
            "app.api.v2.endpoints.role",
            "app.api.v2.endpoints.user_profile",
            "app.api.v2.endpoints.measure",
            "app.api.v2.endpoints.user_measure",
            "app.api.v2.endpoints.user_persona",
            "app.api.v2.endpoints.insight",
            "app.api.v2.endpoints.question_answer",
            "app.api.v2.endpoints.user_answer",
            "app.api.v2.endpoints.comment",
            "app.api.v2.endpoints.chart",
            "app.api.v2.endpoints.feedback",
            

            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    #post_repository = providers.Factory(PostRepository, session_factory=db.provided.session)
    #tag_repository = providers.Factory(TagRepository, session_factory=db.provided.session)
    
    # Repositories
    
    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    
    # setup_organization_repository = providers.Factory(SetupOrganizationRepository, session_factory=db.provided.session)
    domain_repository = providers.Factory(DomainRepository, session_factory=db.provided.session)
    roles_repository = providers.Factory(RolesRepository, session_factory=db.provided.session)
    # domain_repository = providers.Factory(DomainRepository, session_factory=db.provided.session)
    # role_table_repository = providers.Factory(RoleTableRepository, session_factory=db.provided.session)
    company_repository = providers.Factory(CompanyRepository, session_factory=db.provided.session)
    user_profile_repository = providers.Factory(UserProfileRepository, session_factory=db.provided.session)
    measures_repository = providers.Factory(MeasuresRepository, session_factory=db.provided.session)
    top_of_mind_types_roles_repository = providers.Factory(TopOfMindTypesRolesRepository, session_factory=db.provided.session)
    user_measures_repository = providers.Factory(UserMeasuresRepository, session_factory=db.provided.session)
    user_personas_repository = providers.Factory(UserPersonasRepository, session_factory=db.provided.session)
    question_answer_repository = providers.Factory(QuestionAnswerRepository, session_factory=db.provided.session)
    framework_types_repository = providers.Factory(FrameworkTypesRepository, session_factory=db.provided.session)
    framework_subtypes_repository = providers.Factory(FrameworkSubtypesRepository, session_factory=db.provided.session)
    questions_repository = providers.Factory(QuestionsRepository, session_factory=db.provided.session)
    answers_repository = providers.Factory(AnswersRepository, session_factory=db.provided.session)
    user_selected_answers_repository = providers.Factory(UserSelectedAnswersRepository, session_factory=db.provided.session)
    comment_repository = providers.Factory(CommentRepository, session_factory=db.provided.session)
    other_measures_repository = providers.Factory(OtherMeasuresRepository, session_factory=db.provided.session)
    strengths_repository = providers.Factory(StrengthsRepository, session_factory=db.provided.session)
    improvements_repository = providers.Factory(ImprovementsRepository, session_factory=db.provided.session)
    
    
    # Services

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    # setup_organization_service = providers.Factory(SetupService, setup_organization=setup_organization_repository)
    domain_service = providers.Factory( DomainService, domain_repository=domain_repository)
    roles_service = providers.Factory(RolesService, roles_repository=roles_repository)
    # domain_service = providers.Factory(DomainService, domain_repository=domain_repository)
    # role_table_service = providers.Factory(RoleTableService, role_table_repository=role_table_repository)
    
    user_profile_service = providers.Factory(
        UserProfileService, 
        user_profile_repository=user_profile_repository,
        company_repository=company_repository,
        user_measures_repository=user_measures_repository)
    
    measures_service = providers.Factory(
        MeasuresService,
        measures_repository=measures_repository,
        top_of_mind_types_roles_repository= top_of_mind_types_roles_repository)
    user_measures_service = providers.Factory(
        UserMeasuresService, 
        user_measures_repository=user_measures_repository,
        other_measures_repository=other_measures_repository)
    user_personas_service = providers.Factory(
        UserPersonasService, 
        user_personas_repository=user_personas_repository,
        user_profile_repository=user_profile_repository,
        other_measures_repository=other_measures_repository)
    
    insight_service = providers.Factory(
        InsightService,
        measures_repository=measures_repository,
        top_of_mind_types_roles_repository=top_of_mind_types_roles_repository,
        user_profile_repository=user_profile_repository,
        user_measures_repository=user_measures_repository
    )
    
    question_answer_service = providers.Factory(
        QuestionAnswerService, 
        question_answer_repository=question_answer_repository,
        framework_types_repository=framework_types_repository,
        framework_subtypes_repository=framework_subtypes_repository,
        questions_repository=questions_repository,
        answers_repository=answers_repository,
        user_selected_answers_repository=user_selected_answers_repository,
        comment_repository=comment_repository)
    
    user_selected_answers_service = providers.Factory(
        UserSelectedAnswersService, 
        user_selected_answers_repository=user_selected_answers_repository,
        framework_types_repository=framework_types_repository,
        framework_subtypes_repository=framework_subtypes_repository,
        questions_repository=questions_repository,
        answers_repository=answers_repository)
    
    comment_service = providers.Factory(CommentService, comment_repository=comment_repository)
    chart_service = providers.Factory(
        ChartService,
        framework_types_repository=framework_types_repository,
        questions_repository=questions_repository,
        answers_repository=answers_repository,
        user_selected_answers_repository=user_selected_answers_repository)
    
    feedback_service = providers.Factory(
        FeedbackService,
        strengths_repository=strengths_repository,
        improvements_repository=improvements_repository)