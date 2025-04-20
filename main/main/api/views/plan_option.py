import json

import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..database import SessionLocal
from ..models.caculators import Caculators
from ..models.plans import Plans
from ..models.pair_of_plans import Pair_Of_Plans


@api_view(["GET"])
def get_plan_of_caculator(request):
    try:
        caculatorId = request.GET.get("caculatorId", "No Id")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            all_plans = session.query(Plans).filter(Plans.caculatorId == caculatorId).all()
            if all_plans:
                session.close()
                plan_list = [{"id": p.id, "name": p.name, "index": p.index} for p in all_plans]
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
        index = request.data.get("index")
        if not plan_name:
            return Response({"status": "Empty Value", "message": "Tên phương án trống!"})
        else:
            session = SessionLocal()
            caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
            if caculator:
                exists_plan = session.query(Plans).filter((Plans.caculatorId == caculatorId) & (Plans.name == plan_name)).first()
                if exists_plan:
                    session.close()
                    return Response({"status": "Fault", "message": "Tên phương án đã tồn tại!"})
                else:
                    matrix_plan_exists = session.query(Pair_Of_Plans).filter(
                        Pair_Of_Plans.caculatorId == caculatorId).all()
                    if matrix_plan_exists:
                        for matrix_plan in matrix_plan_exists:
                            session.delete(matrix_plan)
                    new_plan = Plans(caculatorId=caculator.id, name=plan_name, index=index)
                    session.add(new_plan)
                    session.commit()
                    all_plans = session.query(Plans).filter(Plans.caculatorId == caculator.id).all()
                    if all_plans:
                        session.close()
                        plan_list = [{"id": p.id, "name": p.name, "index": p.index} for p in all_plans]
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
                all_plans = session.query(Plans).filter(Plans.caculatorId == caculator.id).all()
                if all_plans:
                    session.close()
                    plan_list = [{"id": p.id, "name": p.name, "index": p.index} for p in all_plans]
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
