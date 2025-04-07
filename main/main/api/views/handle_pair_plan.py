import json
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..database import SessionLocal
from ..models.caculators import Caculators
from ..models.pair_of_plans import Pair_Of_Plans
from ..models.pair_of_criterias import Pair_Of_Criterias


@api_view(["POST"])
def handel_point_plan(request):
    try:
        caculatorId = request.data.get("caculatorId")
        name_plan = request.data.get("namePlan")
        matrix_get = request.data.get("matrix")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            matrix = np.array(matrix_get, dtype=float)
            rows, cols = matrix.shape
            n = rows - 1
            sum_row = matrix[rows - 1]
            matrix = np.delete(matrix, rows - 1, axis=0)
            normalised_matrix = matrix / sum_row
            weighting_matrix = np.mean(normalised_matrix, axis=1)
            consistency_rate_matrix = matrix * weighting_matrix
            weighted_sum = np.sum(consistency_rate_matrix, axis=1)
            consistency_vector = weighted_sum / weighting_matrix
            lamda_max = np.mean(consistency_vector)
            CI = (lamda_max - n) / (n - 1)
            RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
            RI = RI_dict.get(n, 1.49)
            CR = CI / RI
            matrix1 = np.column_stack((weighting_matrix, weighted_sum))
            matrix2 = np.column_stack((matrix1, consistency_vector))
            matrix_to_json = json.dumps(matrix)
            new_matrix_plan = Pair_Of_Plans(caculatorId=caculatorId, matrix=matrix_to_json, name=name_plan, cr=CR)
            session.add(new_matrix_plan)
            session.commit()
            session.close()
            return Response(
                {"status": "Success", "matrix": matrix2.tolist(), "namePlan": name_plan, "lamdaMax": lamda_max, "CI": CI,
                 "CR": CR})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã bài tính không tồn tại!"})
    except Exception as ex:
        return Response({
            "status": "Server Error",
            "error": str(ex)
        })


def handle_matrix(matrix):
    rows, cols = matrix.shape
    sum_row = matrix[rows - 1]
    matrix = np.delete(matrix, rows - 1, axis=0)
    normalised_matrix = matrix / sum_row
    weighting_matrix = np.mean(normalised_matrix, axis=1)
    return weighting_matrix


@api_view(["GET"])
def get_rank_plan(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        pa_matrix = np.empty((0, 0))
        if caculator:
            matrix_plans = session.query(Pair_Of_Plans).filter(Pair_Of_Plans.caculatorId == caculatorId).all()
            criteria_record = session.query(Pair_Of_Criterias).filter(Pair_Of_Criterias.caculatorId == caculatorId).first()
            if matrix_plans and criteria_record:
                for plan in matrix_plans:
                    matrix = np.array(json.loads(plan.matrix))
                    if pa_matrix.size != 0:
                        result_matrix = handle_matrix(matrix)
                        pa_matrix = np.column_stack((pa_matrix, result_matrix))
                    else:
                        pa_matrix = handle_matrix(matrix)
                matrix_criteria = np.array(json.loads(criteria_record.matrix))
                pa_criteria = handle_matrix(matrix_criteria)
                result = np.dot(pa_matrix, pa_criteria)
                session.close()
                return Response({"status": "Success", "rank": result})
            else:
                session.close()
                return Response({"status": "Empty Value", "message": "Ma trận phương án hoặc tiêu chí trống!"})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã bài tính không tồn tại!"})
    except Exception as ex:
        return Response({
            "status": "Server Error",
            "error": str(ex)
        })


@api_view(["GET"])
def get_matrix_plan(request):
    try:
        caculatorId = request.GET.get("caculatorId")
        name_plan = request.GET.get("namePlan")
        session = SessionLocal()
        caculator = session.query(Caculators).filter(Caculators.id == caculatorId).first()
        if caculator:
            plan = (session.query(Pair_Of_Plans)
                           .filter((Pair_Of_Plans.caculatorId == caculatorId) & (Pair_Of_Plans.name == name_plan))).all()
            if plan:
                matrix = np.array(json.loads(plan.matrix))
                rows, cols = matrix.shape
                n = rows - 1
                sum_row = matrix[rows - 1]
                matrix = np.delete(matrix, rows - 1, axis=0)
                normalised_matrix = matrix / sum_row
                weighting_matrix = np.mean(normalised_matrix, axis=1)
                consistency_rate_matrix = matrix * weighting_matrix
                weighted_sum = np.sum(consistency_rate_matrix, axis=1)
                consistency_vector = weighted_sum / weighting_matrix
                lamda_max = np.mean(consistency_vector)
                CI = (lamda_max - n) / (n - 1)
                RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
                RI = RI_dict.get(n, 1.49)
                CR = CI / RI
                matrix1 = np.column_stack((weighting_matrix, weighted_sum))
                matrix2 = np.column_stack((matrix1, consistency_vector))
                session.close()
                return Response({"status": "Success", "matrix": matrix2.tolist(), "lamdaMax": lamda_max, "CI": CI, "CR": CR})
            else:
                session.close()
                return Response({"status": "Empty Value", "message": "Phương án không tồn tại!"})
        else:
            session.close()
            return Response({"status": "Not Found", "message": "Mã bài tính không tồn tại!"})
    except Exception as ex:
        return Response({
            "status": "Server Error",
            "error": str(ex)
        })
