import json

import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..database import SessionLocal
from ..models.caculators import Caculators
from ..models.plans import Plans
from ..models.pair_of_plans import Pair_Of_Plans
from ..models.plan_default import PlanDefault
from ..models.criterias import Criterias


@api_view(["GET"])
def get_plan_of_caculator(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            all_plans = session.query(Plans, PlanDefault).join(PlanDefault,
                                                                Plans.catalystId == PlanDefault.id).filter(
                Plans.caculatorId == caculatorId).all()
            if all_plans:
                session.close()
                plan_list = [{
                    "id": plan.id,
                    "catalystId": plan.catalystId,
                    "name": plan.name,
                    "index": plan.index,
                    "category": default.category,
                    "imdb": default.imdb,
                    "duration": default.duration,
                    "director": default.director,
                    "awards": default.awards,
                    "nation": default.nation,
                } for plan, default in all_plans]
                return Response({"status": "Success", "plans": plan_list})
            else:
                session.close()
                return Response({"status": "Success", "plans": []})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã Bài Tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["POST"])
def add_plan(request):
    try:
        caculatorId = request.data.get("caculatorId")
        plan_name = request.data.get("plan")
        catalyst_id = request.data.get("catalystId")
        index = request.data.get("index")
        if not plan_name:
            return Response({"status": "Empty Value", "message": "Tên phương án trống!"})
        else:
            session = SessionLocal()
            caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
            if caculator:
                exists_plan = session.query(Plans).filter(
                    (Plans.caculatorId == caculatorId) & (Plans.catalystId == catalyst_id)).first()
                if exists_plan:
                    session.close()
                    return Response({"status": "Fault", "message": f"Phương án {plan_name} đã tồn tại!"})
                else:
                    matrix_plan_exists = session.query(Pair_Of_Plans).filter(
                        Pair_Of_Plans.caculatorId == caculatorId).all()
                    if matrix_plan_exists:
                        for matrix_plan in matrix_plan_exists:
                            session.delete(matrix_plan)
                    new_plan = Plans(caculatorId=caculator.id, catalystId=catalyst_id, name=plan_name, index=index)
                    session.add(new_plan)
                    session.commit()
                    all_plans = session.query(Plans, PlanDefault).join(PlanDefault,
                                                                        Plans.catalystId == PlanDefault.id).filter(
                        Plans.caculatorId == caculatorId).all()
                    if all_plans:
                        session.close()
                        plan_list = [{
                            "id": plan.id,
                            "catalystId": plan.catalystId,
                            "name": plan.name,
                            "index": plan.index,
                            "category": default.category,
                            "imdb": default.imdb,
                            "duration": default.duration,
                            "director": default.director,
                            "awards": default.awards,
                            "nation": default.nation,
                        } for plan, default in all_plans]
                        return Response({"plans": plan_list, "status": "Success"})
                    else:
                        session.close()
                        return Response({"plans": [], "status": "Success"})
            else:
                session.close()
                return Response({"status": "Not Found", "message": "Mã Bài tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["DELETE"])
def delete_plan(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        planId = request.GET.get("planId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            plan = session.query(Plans).filter(Plans.id == planId).first()
            if plan:
                matrix_plan_exists = session.query(Pair_Of_Plans).filter(Pair_Of_Plans.caculatorId == caculatorId).all()
                if matrix_plan_exists:
                    for matrix_plan in matrix_plan_exists:
                        session.delete(matrix_plan)
                session.delete(plan)
                session.query(Plans).filter(Plans.index > plan.index).update(
                    {Plans.index: Plans.index - 1}, synchronize_session=False
                )
                session.commit()
                all_plans = session.query(Plans, PlanDefault).join(PlanDefault,
                                                                    Plans.catalystId == PlanDefault.id).filter(
                    Plans.caculatorId == caculatorId).all()
                if all_plans:
                    session.close()
                    plan_list = [{
                        "id": plan.id,
                        "catalystId": plan.catalystId,
                        "name": plan.name,
                        "index": plan.index,
                        "category": default.category,
                        "imdb": default.imdb,
                        "duration": default.duration,
                        "director": default.director,
                        "awards": default.awards,
                        "nation": default.nation,
                    } for plan, default in all_plans]
                    return Response({"status": "Success", "plans": plan_list})
                else:
                    session.close()
                    return Response({"status": "Success", "plans": []})
            else:
                session.close()
                return Response({"status": "Empty Value", "message": "Phương án không được trống!"})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã Bài tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["POST"])
def add_plan_catalyst(request):
    try:
        id = request.data.get("id")
        name = request.data.get("name")
        category = request.data.get("category")
        imdb = request.data.get("imdb")
        duration = request.data.get("duration")
        director = request.data.get("director")
        awards = request.data.get("awards", "Không có")
        nation = request.data.get("nation")
        if name and category and imdb and duration and director and awards and nation:
            session = SessionLocal()
            if id:
                update_plan = session.query(PlanDefault).filter(PlanDefault.id == id).first()
                if update_plan:
                    update_plan.name = name
                    update_plan.category = category
                    update_plan.imdb = imdb
                    update_plan.duration = duration
                    update_plan.director = director
                    update_plan.awards = awards
                    update_plan.nation = nation
                    session.commit()
                    all_plans = session.query(PlanDefault).all()
                    if all_plans:
                        session.close()
                        plan_data = [{"id": p.id,
                                      "name": p.name,
                                      "category": p.category,
                                      "imdb": p.imdb,
                                      "duration": p.duration,
                                      "director": p.director,
                                      "awards": p.awards,
                                      "nation": p.nation,
                                      } for p in all_plans]
                        return Response({"status": "Success", "plans": plan_data})
                    else:
                        session.close()
                        return Response({"status": "Success", "plans": []})
                else:
                    session.close()
                    return Response({"status": "Not Found", "message": "Cập nhật thất bại!"})
            else:
                exists_plan = session.query(PlanDefault).filter(PlanDefault.name == name).first()
                if exists_plan:
                    session.close()
                    return Response({"status": "Exists Value", "message": "Phương án đã tồn tại!"})
                else:
                    new_plan = PlanDefault(name=name, category=category, imdb=imdb, duration=duration,
                                            director=director,
                                            awards=awards, nation=nation)
                    session.add(new_plan)
                    session.commit()
                    all_plans = session.query(PlanDefault).all()
                    if all_plans:
                        session.close()
                        plan_data = [{"id": p.id,
                                      "name": p.name,
                                      "category": p.category,
                                      "imdb": p.imdb,
                                      "duration": p.duration,
                                      "director": p.director,
                                      "awards": p.awards,
                                      "nation": p.nation,
                                      } for p in all_plans]
                        return Response({"status": "Success", "plans": plan_data})
                    else:
                        session.close()
                        return Response({"status": "Success", "plans": []})
        else:
            return Response({"status": "Empty Value", "message": "Một số trường dữ liệu trống!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["GET"])
def get_all_plan_catalyst(request):
    try:
        session = SessionLocal()
        all_plans = session.query(PlanDefault).all()
        if all_plans:
            session.close()
            plan_data = [{"id": p.id,
                          "name": p.name,
                          "category": p.category,
                          "imdb": p.imdb,
                          "duration": p.duration,
                          "director": p.director,
                          "awards": p.awards,
                          "nation": p.nation,
                          } for p in all_plans]
            return Response({"status": "Success", "plans": plan_data})
        else:
            session.close()
            return Response({"status": "Success", "plans": []})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["DELETE"])
def delete_plan_catalyst(request):
    try:
        id = request.GET.get("planId")
        if id:
            session = SessionLocal()
            plan = session.query(PlanDefault).filter(PlanDefault.id == id).first()
            if plan:
                session.delete(plan)
                session.commit()
                all_plans = session.query(PlanDefault).all()
                if all_plans:
                    session.close()
                    plan_data = [{"id": p.id,
                                  "name": p.name,
                                  "category": p.category,
                                  "imdb": p.imdb,
                                  "duration": p.duration,
                                  "director": p.director,
                                  "awards": p.awards,
                                  "nation": p.nation,
                                  } for p in all_plans]
                    return Response({"status": "Success", "plan": plan_data})
                else:
                    session.close()
                    return Response({"status": "Success", "plan": []})
            else:
                session.close()
                return Response({"status": "Not Found", "message": "Mã phương án không tồn tại!"})
        else:
            return Response({"status": "Empty Value", "message": "Id trường dữ liệu trống!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


def split_each_string(string):
    return [s.strip() for s in string.split(",") if s.strip()]


column_map = {
    "Thể Loại": "category",
    "Đánh Giá IMDb": "imdb",
    "Thời Lượng": "duration",
    "Đạo Diễn": "director",
    "Đề Cử & Giải Thưởng": "awards",
    "Quốc Gia": "nation"
}


@api_view(["GET"])
def get_catalyst_menu(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        if caculatorId:
            session = SessionLocal()
            get_plans = session.query(Plans, PlanDefault).join(PlanDefault, Plans.catalystId == PlanDefault.id).filter(Plans.caculatorId == caculatorId).all()
            get_criteria = session.query(Criterias).filter(Criterias.caculatorId == caculatorId).all()
            if get_plans and get_criteria:
                catalyst = []
                for item in get_criteria:
                    list_string = []
                    print(item.name)
                    column_name = column_map.get(item.name)
                    print(column_name)
                    if column_name:
                        for plan, default in get_plans:
                            value = getattr(default, column_name)
                            if isinstance(value, str):
                                list_string.extend(split_each_string(value))
                            else:
                                list_string.append(value)

                        catalyst.append({
                            "name": item.name,
                            "listCatalyst": list(set(list_string))
                        })
                session.close()
                return Response({"status": "Success", "catalyst": catalyst})
            else:
                session.close()
                return Response({"status": "Success", "catalyst": []})
        else:
            return Response({"status": "Empty Value", "message": "Id trường dữ liệu trống!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["POST"])
def filter_plan(request):
    try:
        caculatorId = request.data.get("caculatorId")
        list_plan = request.data.get("listPlan", [])
        if caculatorId:
            session = SessionLocal()
            all_plans = session.query(Plans).filter(Plans.caculatorId == caculatorId).all()
            if list_plan and all_plans:
                valid_ids = [item["Mã"] for item in list_plan]
                for plan in all_plans:
                    if plan.id not in valid_ids:
                        session.delete(plan)
                session.commit()
                session.close()
                return Response({"status": "Success", "message": "Đã lọc và xóa các plan không còn trong danh sách."})
            else:
                session.close()
                return Response({"status": "Empty Value", "message": "Không phát hiện danh sách phương án."})
        else:
            return Response({"status": "Empty Value", "message": "Id trường dữ liệu trống!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})
