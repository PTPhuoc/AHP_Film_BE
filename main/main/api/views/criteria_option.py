from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..database import SessionLocal
from ..models.caculators import Caculators
from ..models.criterias import Criterias


@api_view(["GET"])
def get_criteria_of_caculator(request):
    try:
        caculatorId = request.GET.get("caculatorId", "No Id")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId)
        if caculator:
            all_criteria = session.query(Criterias.id, Criterias.index, Criterias.name).filter(
                Criterias.caculatorId == caculatorId).all()
            session.close()
            criteria_list = [
                {"id": p.id, "index": p.index, "name": p.name} for p in all_criteria
            ]
            return Response({"status": "Success", "criterias": criteria_list})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã Bài Tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["POST"])
def add_criteria(request):
    try:
        caculatorId = request.data.get("caculatorId")
        criteria_name = request.data.get("criteria")
        index = request.data.get("index")
        if not criteria_name:
            return Response({"status": "Empty Value", "message": "Tên tiêu chí trống!"})
        else:
            session = SessionLocal()
            caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
            if caculator:
                new_criteria = Criterias(caculatorId=caculator.id, name=criteria_name, index=index)
                session.add(new_criteria)
                session.commit()
                all_criteria = session.query(Criterias.name, Criterias.index, Criterias.id).filter(
                    Criterias.caculatorId == caculator.id).all()
                session.close()
                criteria_list = [{"id": p.id, "index": p.index, "name": p.name} for p in all_criteria]
                return Response({"criterias": criteria_list, "status": "Success"})
            else:
                session.close()
                return Response({"status": "Not Found", "message": "Mã Bài tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["DELETE"])
def delete_criteria(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        criteriaId = request.GET.get("criteriaId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            plan = session.query(Criterias).filter(Criterias.id == criteriaId).first()
            if plan:
                session.delete(plan)
                session.commit()
                all_criteria = session.query(Criterias.name, Criterias.index, Criterias.id).filter(
                    Criterias.caculatorId == caculator.id).all()
                session.close()
                criteria_list = [{"id": p.id, "index": p.index, "name": p.name} for p in all_criteria]
                return Response({"status": "Success", "plans": criteria_list})
            else:
                session.close()
                return Response({"status": "Empty Value", "message": "Tiêu chí không được để trống!"})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã Bài tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})


@api_view(["GET"])
def get_default_criteria(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            default_value = [
                {"name": "Thể Loại", "index": 1, "caculatorId": caculatorId},
                {"name": "Đánh Giá IMDb", "index": 2, "caculatorId": caculatorId},
                {"name": "Thời Lượng", "index": 3, "caculatorId": caculatorId},
                {"name": "Đạo Diễm", "index": 4, "caculatorId": caculatorId},
                {"name": "Đề Cử & Giải Thưởng", "index": 5, "caculatorId": caculatorId},
                {"name": "Quốc Gia", "index": 6, "caculatorId": caculatorId}
            ]
            all_criteria = session.query(Criterias).filter(Criterias.caculatorId == caculatorId).all()
            if all_criteria:
                for criteria in all_criteria:
                    session.delete(criteria)
            for criteria in default_value:
                new_criteria = Criterias(name=criteria["name"], index=criteria["index"], caculatorId=caculatorId)
                session.add(new_criteria)
            session.commit()
            session.close()
            return Response({"status": "Success", "criterias": default_value})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã bảng tính không tồn tại!"})
    except Exception as ex:
        return Response({"status": "Server Error", "error": str(ex)})
