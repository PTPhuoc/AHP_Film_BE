from django.urls import path
from .views.plan_option import get_plan_of_caculator, add_plan, delete_plan, add_plan_catalyst, delete_plan_catalyst, get_all_plan_catalyst, get_catalyst_menu, filter_plan
from .views.criteria_option import get_criteria_of_caculator, get_default_criteria, add_criteria, delete_criteria, delete_criteria_catalyst, get_all_criteria_catalyst, add_criteria_catalyst
from .views.caculator_option import get_caculator, get_history
from .views.handle_pair_criteria import handle_point_criteria, get_criterias
from .views.handle_pair_plan import get_matrix_plan, handel_point_plan, get_rank_plan

urlpatterns = [
    path("get_plan/", get_plan_of_caculator, name="Get Plan"),
    path("add_plan/", add_plan, name="Add Plan"),
    path("delete_plan/", delete_plan, name="Delete Plan"),
    path("get_criterias/", get_criteria_of_caculator, name="Get Criterias"),
    path("add_plan_catalyst/", add_plan_catalyst, name="add_plan_catalyst"),
    path("delete_plan_catalyst/", delete_plan_catalyst, name="delete_plan_catalyst"),
    path("get_all_plan_catalyst/", get_all_plan_catalyst, name="get_all_plan_catalyst"),
    path("delete_criteria_catalyst/", delete_criteria_catalyst, name="delete_criteria_catalyst"),
    path("get_all_criteria_catalyst/", get_all_criteria_catalyst, name="get_all_criteria_catalyst"),
    path("add_criteria_catalyst/", add_criteria_catalyst, name="add_criteria_catalyst"),
    path("get_default_criterias/", get_default_criteria, name="Get Default Criterias"),
    path("add_criteria/", add_criteria, name="Add Criteria"),
    path("delete_criteria/", delete_criteria, name="Delete Criteria"),
    path("get_caculator/", get_caculator, name="Create Id Caculator"),
    path("get_history/", get_history, name="Get History"),
    path("handle_point_criteria/", handle_point_criteria, name="Handle Point Criteria"),
    path("get_matrix_criteria/", get_criterias, name="Get Matrix Criteria"),
    path("get_matrix_plan/", get_matrix_plan, name="Get Matrix Plan"),
    path("handle_point_plan/", handel_point_plan, name="Handle Point Plan"),
    path("get_rank_plan/", get_rank_plan, name="Get Rank Plan"),
    path("get_catalyst_menu/", get_catalyst_menu, name="get_catalyst_menu"),
    path("filter_plan/", filter_plan, name="filter_plan"),
]
