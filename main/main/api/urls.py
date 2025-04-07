from django.urls import path
from .views.plan_option import get_plan_of_caculator, add_plan, delete_plan
from .views.criteria_option import get_criteria_of_caculator, get_default_criteria, add_criteria, delete_criteria
from .views.caculator_option import get_caculator
from .views.handle_pair_criteria import handle_point_criteria, get_criterias
from .views.handle_pair_plan import get_matrix_plan, handel_point_plan, get_rank_plan

urlpatterns = [
    path("get_plan/", get_plan_of_caculator, name="Get Plan"),
    path("add_plan/", add_plan, name="Add Plan"),
    path("delete_plan/", delete_plan, name="Delete Plan"),
    path("get_criterias/", get_criteria_of_caculator, name="Get Criterias"),
    path("get_default_criterias/", get_default_criteria, name="Get Default Criterias"),
    path("add_criteria/", add_criteria, name="Add Criteria"),
    path("delete_criteria/", delete_criteria, name="Delete Criteria"),
    path("get_caculator/", get_caculator, name="Create Id Caculator"),
    path("handle_point_criteria/", handle_point_criteria, name="Handle Point Criteria"),
    path("get_matrix_criteria/", get_criterias, name="Get Matrix Criteria"),
    path("get_matrix_plan/", get_matrix_plan, name="Get Matrix Plan"),
    path("handle_point_plan/", handel_point_plan, name="Handle Point Plan"),
    path("get_rank_plan/", get_rank_plan, name="Get Rank Plan"),
]
